"""
Python Wechaty - https://github.com/wechaty/python-wechaty

Authors:    Huan LI (李卓桓) <https://github.com/huan>
            Jingjing WU (吴京京) <https://github.com/wj-Mcat>

2020-now @ Copyright Wechaty

Licensed under the Apache License, Version 2.0 (the 'License');
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an 'AS IS' BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
from __future__ import annotations

import asyncio
from logging import Logger
import os
import sys
import re
from abc import ABC
from collections import OrderedDict
from copy import deepcopy
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from telnetlib import Telnet
import socket
from typing import (
    TYPE_CHECKING,
    List,
    Optional,
    Dict,
    Union,
    Any,
    cast, Tuple,
    Callable,
    Coroutine
)
import signal

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from quart import Quart
from quart_cors import cors

from wechaty_puppet import (
    WechatyPuppetError,
    get_logger,
    EventErrorPayload,
    EventHeartbeatPayload,
    EventReadyPayload,
    ScanStatus
)

from .config import config

from .exceptions import (
    WechatyPluginError,
)

if TYPE_CHECKING:
    from .wechaty import (
        Wechaty
    )
    from .user import (
        Room,
        RoomInvitation,
        Friendship,
        Contact,
        Message,
    )
log: Logger = get_logger(__name__)


def _check_local_port(port: int) -> bool:
    """
    check if the local port is in use
    Args:
        port (int): port

    Return:
        return True if the local port is valid, otherwise False

    Examples:
        >>> assert _check_local_port(5000)

    """
    # 1. extract host & port
    tn = Telnet()

    # 2. test host:port with socket
    res = True
    try:
        tn.open('127.0.0.1', port=port, timeout=3)
    except socket.error:
        res = False

    return res


def _list_routes_txt(app: Quart) -> List[str]:
    """
    refer to: https://gitlab.com/pgjones/quart/-/blob/main/src/quart/cli.py#L283
    Args:
        app: the instance of Quart

    Returns: routes info

    """
    rules = list(app.url_map.iter_rules())
    if len(rules) == 0:
        return []

    rules = list(sorted(rules, key=lambda rule: rule.endpoint))

    headers = ("Endpoint", "Methods", "Websocket", "Rule")
    rule_methods = [", ".join(sorted(rule.methods)) for rule in rules if rule.methods]

    widths = [
        max(len(rule.endpoint) for rule in rules),
        max(len(methods) for methods in rule_methods),
        len("Websocket"),
        max(len(rule.rule) for rule in rules),
    ]
    widths = [max(len(header), width) for header, width in zip(headers, widths)]

    # pylint: disable=C0209
    row = "{{0:<{0}}} | {{1:<{1}}} | {{2:<{2}}} | {{3:<{3}}}".format(*widths)

    routes_txt: List[str] = []
    routes_txt.append(row.format(*headers).strip())
    routes_txt.append(row.format(*("-" * width for width in widths)))

    for rule, methods in zip(rules, rule_methods):
        routes_txt.append(
            row.format(rule.endpoint, methods, str(rule.websocket), rule.rule).rstrip()
        )
    return routes_txt


async def get_shutdown_trigger() -> Callable[[], Coroutine[Any, Any, Any]]:
    """register the system shutdown trigger event"""
    signal_event = asyncio.Event()
    loop = asyncio.get_event_loop()

    def _signal_handler(*_: Any) -> None:  # noqa: N803
        print('receive signal event ...')
        signal_event.set()

    for signal_name in ["SIGINT", "SIGTERM", "SIGBREAK"]:
        if hasattr(signal, signal_name):
            try:
                loop.add_signal_handler(getattr(signal, signal_name), _signal_handler)
            except NotImplementedError:
                # Add signal handler may not be implemented on Windows
                signal.signal(getattr(signal, signal_name), _signal_handler)

    return signal_event.wait


async def shutdown(trigger: Callable[[], Coroutine[Any, Any, Any]]) -> None:
    """when trigger the shutdown, it will call sys.exit"""
    await trigger()
    sys.exit(0)


@dataclass
class WechatyPluginOptions:
    """options for wechaty plugin"""
    name: Optional[str] = None
    metadata: Optional[dict] = None


@dataclass
class WechatySchedulerOptions:
    """options for wechaty scheduler"""
    job_store: Union[str, SQLAlchemyJobStore] = f'sqlite:///{config.cache_dir}/job.db'
    job_store_alias: str = 'wechaty-scheduler'


class PluginStatus(Enum):
    """plugin running status"""
    Running = 0
    Stopped = 1


class WechatySchedulerMixin:
    """scheduler mixin for wechaty
    """
    _scheduler_field: str = "_scheduler"

    scheduler_job_alias: str = 'wechaty_scheduler'
    scheduler_db_file: str = f'{config.cache_dir}/job.db'

    @property
    def scheduler(self) -> AsyncIOScheduler:
        """get the scheduler"""
        scheduler_instance = getattr(self, self._scheduler_field, None)
        if scheduler_instance is None:
            raise WechatyPluginError('there is an error')

        assert isinstance(scheduler_instance, AsyncIOScheduler)
        return scheduler_instance

    @scheduler.setter
    def scheduler(self, scheduler_instance: AsyncIOScheduler) -> None:
        """set the scheduler

        Args:
            scheduler_instance (AsyncIOScheduler): the instance of the scheduler
        """
        if getattr(self, self._scheduler_field, None) is not None:
            raise WechatyPuppetError(
                "can't set scheduler twice"
            )
        setattr(self, self._scheduler_field, scheduler_instance)

    def add_daily_job(
        self,
        hour: int,
        handler: Any,
        job_id: Optional[Union[str, int]] = None,
        args: Optional[set] = None,
        kwargs: Optional[dict] = None
    ) -> None:
        """add daily scheduler job
        Args:
            hour (int): the target hour of daily time
            handler (callable): the target callable function
            job_id (Optional[Union[str, int]], optional):
                the job id stored in the stored. Defaults to None.
            args (Optional[set]): default args of handler
            kwargs (Optional[dict]): default kwargs of handler
        """
        if not job_id:
            job_id = f'daily-job-{hour}'

        job_id = str(job_id)

        trigger = CronTrigger(
            hour=hour
        )

        self.scheduler.add_job(
            func=handler,
            trigger=trigger,
            args=args,
            kwargs=kwargs
        )

    def add_interval_job(
        self, minutes: int,
        handler: Any,
        job_id: Optional[Union[str, int]] = None,
        args: Optional[set] = None,
        kwargs: Optional[dict] = None
    ) -> None:
        """add interval jobs which will trigger the job every minutes

        Args:
            minutes (int): the await time which will trigger the event
        """
        if not job_id:
            job_id = f'interval-job-{minutes}'

        job_id = str(job_id)

        trigger = IntervalTrigger(
            minutes=minutes
        )

        self.scheduler.add_job(
            func=handler,
            trigger=trigger,
            args=args,
            kwargs=kwargs
        )


class WechatyEventMixin:
    """wechaty event relative functions mixin"""
    async def on_error(self, payload: EventErrorPayload) -> None:
        """
        listen error event for puppet

        this is friendly for code typing
        """

    async def on_heartbeat(self, payload: EventHeartbeatPayload) -> None:
        """
        listen heartbeat event for puppet

        this is friendly for code typing
        """

    async def on_friendship(self, friendship: Friendship) -> None:
        """
        listen friendship event for puppet

        this is friendly for code typing
        """

    async def on_login(self, contact: Contact) -> None:
        """
        listen login event for puppet

        this is friendly for code typing
        """

    async def on_logout(self, contact: Contact) -> None:
        """
        listen logout event for puppet

        this is friendly for code typing
        """

    async def on_message(self, msg: Message) -> None:
        """
        listen message event for puppet

        this is friendly for code typing
        """

    async def on_ready(self, payload: EventReadyPayload) -> None:
        """
        listen ready event for puppet

        this is friendly for code typing
        """

    async def on_room_invite(self, room_invitation: RoomInvitation) -> None:
        """
        listen room_invitation event for puppet

        this is friendly for code typing
        """

    async def on_room_join(self, room: Room, invitees: List[Contact],
                           inviter: Contact, date: datetime) -> None:
        """
        listen room_join event for puppet

        this is friendly for code typing
        """

    async def on_room_leave(self, room: Room, leavers: List[Contact],
                            remover: Contact, date: datetime) -> None:
        """
        listen room_leave event for puppet

        room, leavers, remover, date

        this is friendly for code typing
        """

    # pylint: disable=R0913
    async def on_room_topic(self, room: Room, new_topic: str, old_topic: str,
                            changer: Contact, date: datetime) -> None:
        """
        listen room_topic event for puppet

        this is friendly for code typing
        """

    async def on_scan(self, qr_code: str, status: ScanStatus,
                      data: Optional[str] = None) -> None:
        """
        listen scan event for puppet

        this is friendly for code typing
        """


class WechatyPlugin(ABC, WechatySchedulerMixin, WechatyEventMixin):
    """
    abstract wechaty plugin base class

    listen events from
    """

    def __init__(self, options: Optional[WechatyPluginOptions] = None):
        self.output: Dict[str, Any] = {}
        self.bot: Optional[Wechaty] = None
        if options is None:
            options = WechatyPluginOptions()
        self.options = options
        self._default_logger: Optional[Logger] = None
        self._cache_dir: Optional[str] = None

    def set_bot(self, bot: Wechaty) -> None:
        """set bot instance to WechatyPlugin

        Args:
            bot (Wechaty): the instance of Wechaty
        """
        self.bot = bot

    async def init_plugin(self, wechaty: Wechaty) -> None:
        """set wechaty to the plugin"""

    async def blueprint(self, app: Quart) -> None:
        """register blueprint into default web server"""

    @property
    def name(self) -> str:
        """you must give a name for wechaty plugin

        the name of the plugin should not be a required field,
        and the name of plugin class can be the default name field.
        """
        if not self.options.name:
            # set the class name as the name of the plugin
            self.options.name = self.__class__.__name__

        return self.options.name

    @property
    def cache_dir(self) -> str:
        """
        cache dir for plugin

        this is friendly for code typing
        """
        _cache_dir = os.path.join(config.cache_dir, self.name)
        os.makedirs(_cache_dir, exist_ok=True)
        return _cache_dir

    @cache_dir.setter
    def cache_dir(self, value: str) -> None:
        """set the cache dir although there is already set

        Args:
            value (str): the new cache dir
        """
        if not self._cache_dir:
            self.logger.warning(
                'there is already cache_dir<%s>', self._cache_dir
            )

        os.makedirs(value, exist_ok=True)
        self._cache_dir = value

    @property
    def logger(self) -> Logger:
        """get the default logger of plugin which will automaticly
        log info into the plugin cache dir

        Returns:
            Logger: Instance of Logger

        Examples:
            ding_dong_plugin = DingDongPlugin()
            ding_dong_plugin.logger.info('log info ...')
        """
        if self._default_logger:
            return self._default_logger

        self._default_logger = get_logger(
            self.name,
            file=os.path.join(self.cache_dir, 'log.log')
        )
        assert self._default_logger is not None, 'can not set default logger'

        return self._default_logger

    def set_logger(self, logger: Logger) -> None:
        """if you want to change the behavior of logger, all of you need is to set a new logger

        Args:
            logger (Logger): the new instance of logger
        """
        if self._default_logger:
            self._default_logger.warning(
                'there is already a logger in the plugin, but you set a new logger.'
                'Anyway, do all things  you like.'
            )
        self._default_logger = logger

    def get_output(self) -> dict:
        """if necessary , get the output of the plugin"""
        final_output = deepcopy(self.output)
        self.output = {}
        return final_output

    async def on_loaded(self) -> None:
        """hook the plugin when loaded"""

    async def on_stoped(self) -> None:
        """hook the plugin when stoped"""

    async def on_running(self) -> None:
        """hook the plugin event when active"""


PluginTree = Dict[str, Union[str, List[str]]]
EndPoint = Tuple[str, int]


def _load_default_plugins() -> List[WechatyPlugin]:
    """
    load the system default plugins to enable more default features
    Returns:
    """
    # TODO: to be implemented


class WechatyPluginManager(WechatyEventMixin, WechatySchedulerMixin):     # pylint: disable=too-many-instance-attributes
    """manage the wechaty plugin, It will support some features."""

    def __init__(
        self, wechaty: Wechaty,
        endpoint: EndPoint,
        scheduler_options: Optional[Union[AsyncIOScheduler, WechatySchedulerOptions]] = None
    ):
        self._plugins: Dict[str, WechatyPlugin] = OrderedDict()
        self._wechaty: Wechaty = wechaty
        self._plugin_status: Dict[str, PluginStatus] = {}

        self.app: Quart = cors(Quart('Wechaty Server', static_folder=None))

        self.endpoint: Tuple[str, int] = endpoint

        if scheduler_options is None:
            scheduler_options = WechatySchedulerOptions()

        if isinstance(scheduler_options, WechatySchedulerOptions):
            scheduler = AsyncIOScheduler()

            if isinstance(scheduler_options.job_store, str):
                scheduler_options.job_store = SQLAlchemyJobStore(scheduler_options.job_store)

            scheduler.add_jobstore(scheduler_options.job_store, scheduler_options.job_store_alias)
        self.scheduler: AsyncIOScheduler = scheduler

    # pylint: disable=R1711
    @staticmethod
    def _load_plugin_from_local_file(plugin_path: str) -> Optional[WechatyPlugin]:
        """load plugin from local file"""
        log.info('load plugin from local file <%s>', plugin_path)
        return None

    # pylint: disable=R1711
    @staticmethod
    def _load_plugin_from_github_url(github_url: str
                                     ) -> Optional[WechatyPlugin]:
        """load plugin from github url, but, this is dangerous

        TODO(wj-Mcat): this feature is the final way for project.
        """
        log.info('load plugin from github url <%s>', github_url)
        return None

    def add_plugin(self, plugin: Union[str, WechatyPlugin]) -> None:
        """add plugin to the manager, if the plugin name exist, it will not to
        be installed

        TODO(wj-Mcat): should support:
            - [ ] load plugin from local dir
            - [ ] load plugin from plugin contrib store
            - [ ] load plugin from github url

        """
        if isinstance(plugin, str):
            regex = re.compile(
                r'^(?:http|ftp)s?://'  # http:// or https://
                r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}'
                r'\.?|[A-Z0-9-]{2,}\.?)|'
                r'localhost|'  # localhost...
                r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
                r'(?::\d+)?'  # optional port
                r'(?:/?|[/?]\S+)$', re.IGNORECASE)
            if regex.match(plugin) is None:
                # load plugin from local file
                plugin_instance = self._load_plugin_from_local_file(plugin)
            else:
                plugin_instance = self._load_plugin_from_github_url(plugin)
            if plugin_instance is None:
                raise WechatyPluginError(f'can"t load plugin {plugin}')
        else:
            if plugin.name in self._plugins:
                log.warning('plugin : %s has exist', plugin.name)
                return
            plugin_instance = plugin

        self._plugins[plugin_instance.name] = plugin_instance
        # default wechaty plugin status is Running
        self._plugin_status[plugin_instance.name] = PluginStatus.Running

        # TODO(wj-Mcat): disable this event hook
        # await plugin_instance.on_loaded()

    def remove_plugin(self, name: str) -> None:
        """remove plugin"""
        if name not in self._plugins:
            raise WechatyPluginError(f'plugin {name} not exist')
        self._plugins.pop(name)
        self._plugin_status.pop(name)

    def _check_plugins(self, name: str) -> None:
        """
        check the plugins whether
        """
        if name not in self._plugins and name not in self._plugin_status:
            raise WechatyPluginError(f'plugins <{name}> not exist')

    async def stop_plugin(self, name: str) -> None:
        """stop the plugin"""
        log.info('stopping the plugin <%s>', name)
        self._check_plugins(name)

        if self._plugin_status[name] == PluginStatus.Stopped:
            log.warning('plugins <%s> has stopped', name)
        self._plugin_status[name] = PluginStatus.Stopped
        await self._plugins[name].on_stoped()

    async def start_plugin(self, name: str) -> None:
        """starting the plugin"""
        log.info('starting the plugin <%s>', name)
        self._check_plugins(name)
        self._plugin_status[name] = PluginStatus.Running
        await self._plugins[name].on_running()

    def plugin_status(self, name: str) -> PluginStatus:
        """get the plugin status"""
        self._check_plugins(name)
        return self._plugin_status[name]

    @property
    def server_endpoint(self) -> str:
        """
        send the endpoint of wechaty bot service
        Returns: <host>:<port>, eg: http://0.0.0.0:5000
        """
        prefix = ''
        host, port = self.endpoint[0], self.endpoint[1]
        if not host.startswith('http'):
            prefix = 'http://'

        url = f'{prefix}{host}:{port}'
        return url

    async def start(self) -> None:
        """
        set wechaty to plugins
        """
        log.info('start the plugins ...')

        # 1. init the plugins
        for name, plugin in self._plugins.items():
            log.info('init %s-plugin ...', name)
            assert isinstance(plugin, WechatyPlugin)
            # set wechaty instance to all of the plugin bot attribute

            plugin.set_bot(self._wechaty)
            await plugin.init_plugin(self._wechaty)
            await plugin.blueprint(self.app)
        # check the host & port configuration

        # pylint: disable=W0212
        host, port = self.endpoint[0], self.endpoint[1]
        if _check_local_port(port):
            raise WechatyPluginError(
                f'local port<{port}> is in use, can"t start plugin server. '
                'So please use the another valid port'
            )
        # 3. list all valid endpoints in web service
        # checking the number of registered blueprints
        routes_txt = _list_routes_txt(self.app)
        # if len(routes_txt) == 0:
        #     log.warning(
        #         'there is not registed blueprint in the plugins, '
    #         'so bot will not start the web service'
        #     )
        #     return

        log.info('============================starting web service========================')
        log.info('starting web service at endpoint: <{%s}:{%d}>', host, port)

        shutdown_trigger = await get_shutdown_trigger()
        task = self.app.run_task(
            host=host,
            port=port,
            use_reloader=False,
            shutdown_trigger=shutdown_trigger
        )
        loop = asyncio.get_event_loop()
        loop.create_task(task)

        loop.create_task(
            shutdown(shutdown_trigger)
        )

        for route_txt in routes_txt:
            log.info(route_txt)

        log.info('============================web service has started========================')

    # pylint: disable=too-many-locals,too-many-statements,too-many-branches
    async def emit_events(self, event_name: str, *args: Any, **kwargs: Any) -> None:
        """
        during the try-stage, only support message_events

        event_name: get event
        event_payload:
        """

        # import the User types locally
        # pylint: disable=import-outside-toplevel
        from .user import (
            Room,
            RoomInvitation,
            Friendship,
            Contact,
            Message,
        )

        if event_name == 'message':
            # https://stackoverflow.com/a/154156/2544762
            # The most Pythonic way to check the type of an object is... not to check it.
            if not args and 'msg' not in kwargs:
                raise WechatyPluginError(
                    f'the plugin args of message is invalid, the source args:'
                    f'<{args}>, but expected args is message ')

            message = args[0]
            assert isinstance(message, Message)

            # this will make the plugins running sequential, _plugins
            # is a sort dict
            for name, plugin in self._plugins.items():
                log.info('emit %s-plugin ...', name)
                if self.plugin_status(name) == PluginStatus.Running:
                    await plugin.on_message(message)

        elif event_name == 'friendship':
            if not args or len(args) != 1:
                raise WechatyPluginError(
                    f'the plugin args of friendship event is invalid,'
                    f'the source args is <{args}>,'
                    f'but expected args is : Friendship')

            friendship = args[0]
            assert isinstance(friendship, Friendship)

            for name, plugin in self._plugins.items():
                log.info('emit %s-plugin ...', name)
                if self.plugin_status(name) == PluginStatus.Running:
                    await plugin.on_friendship(friendship)

        elif event_name == 'login':
            if not args or len(args) != 1:
                raise WechatyPluginError(
                    f'the plugin args of login event is invalid,'
                    f'the source args is : <{args}>,'
                    f'but expected args is : Contact ')

            contact = args[0]
            assert isinstance(contact, Contact)

            for name, plugin in self._plugins.items():
                log.info('emit %s-plugin ...', name)
                if self.plugin_status(name) == PluginStatus.Running:
                    await plugin.on_login(contact)

        elif event_name == 'room-invite':
            if not args or len(args) != 1:
                raise WechatyPluginError(
                    f'the plugin args of room-invite event is invalid,'
                    f'the source args is : <{args}>,'
                    f'but expected args is : RoomInvitation ')

            room_invitation = args[0]
            assert isinstance(room_invitation, RoomInvitation)

            for name, plugin in self._plugins.items():
                log.info('emit %s-plugin ...', name)
                if self.plugin_status(name) == PluginStatus.Running:
                    await plugin.on_room_invite(room_invitation)

        elif event_name == 'room-join':
            # there must be four arguments: room, invitees, inviter, date
            if not args or len(args) != 4:
                raise WechatyPluginError(
                    f'the plugin args of room-join is invalid, the source args:'
                    f'<{args}>, but expected args is room, invitees, inviter, '
                    f'date')

            # get the parameters of room-join event
            room = args[0]
            assert isinstance(room, Room)

            invitees = args[1]
            assert isinstance(invitees, list)
            # must convert the type of invitees to List[Contact]
            invitees = cast(List[Contact], invitees)

            inviter = args[2]
            assert isinstance(inviter, Contact)

            date = args[3]
            assert isinstance(date, datetime)

            for name, plugin in self._plugins.items():
                log.info('emit %s-plugin ...', name)
                if self.plugin_status(name) == PluginStatus.Running:
                    await plugin.on_room_join(room, invitees, inviter, date)

        elif event_name == 'room-leave':
            # there must be four arguments: room, leavers, remover, date
            if not args or len(args) != 4:
                raise WechatyPluginError(
                    f'the plugin args of room-leave is invalid, the source args:'
                    f'<{args}>, but expected args is room, invitees, inviter, '
                    f'date')

            # get the parameters of room-join event
            room = args[0]
            assert isinstance(room, Room)

            leavers = args[1]
            assert isinstance(leavers, list)
            # must convert the type of leavers to List[Contact]
            leavers = cast(List[Contact], leavers)

            remover = args[2]
            assert isinstance(remover, Contact)

            date = args[3]
            assert isinstance(date, datetime)

            for name, plugin in self._plugins.items():
                log.info('emit %s-plugin ...', name)
                if self.plugin_status(name) == PluginStatus.Running:
                    await plugin.on_room_leave(room, leavers, remover, date)

        elif event_name == 'room-topic':
            if not args or len(args) != 5:
                raise WechatyPluginError(
                    f'the plugin args of room-topic is invalid, the source args:'
                    f'<{args}>, but expected args is room, payload.new_topic,'
                    f'payload.old_topic, changer, date'
                )
            room = args[0]
            assert isinstance(room, Room)

            new_topic = args[1]
            assert isinstance(new_topic, str)

            old_topic = args[2]
            assert isinstance(old_topic, str)

            changer = args[3]
            assert isinstance(changer, Contact)

            date = args[4]
            assert isinstance(date, datetime)

            for name, plugin in self._plugins.items():
                log.info('emit %s-plugin ...', name)
                if self.plugin_status(name) == PluginStatus.Running:
                    await plugin.on_room_topic(
                        room, new_topic, old_topic,
                        changer, date
                    )

        elif event_name == 'scan':
            if not args or len(args) < 0 or len(args) > 3:
                raise WechatyPluginError(
                    f'the plugin args of scan is invalid, the source args: '
                    f'{args}, but expected args is payload_status, '
                    f'qr_code, payload.data'
                )

            qr_code = args[0]
            assert isinstance(qr_code, str)

            scan_status = args[1]
            assert isinstance(scan_status, str)

            # pylint: disable=isinstance-second-argument-not-valid-type
            # assert isinstance(qr_code, Tuple[None, Type[str]])

            data = args[2]
            data = cast(Optional[str], data)

            # # pylint: disable=isinstance-second-argument-not-valid-type
            # assert isinstance(data, (None, str))

            for name, plugin in self._plugins.items():
                log.info('emit %s-plugin ...', name)
                if self.plugin_status(name) == PluginStatus.Running:
                    await plugin.on_scan(
                        qr_code,
                        scan_status, data
                    )
