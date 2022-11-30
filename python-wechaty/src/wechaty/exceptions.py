"""
Python Wechaty - https://github.com/wechaty/python-wechaty

Authors:    Alfred Huang (黃文超) <https://github.com/fish-ball>

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


from typing import Any


class WechatyError(Exception):
    """ Wechaty error """

    def __init__(self, message: str, code: Any = None, params: Any = None):
        super().__init__(message, code, params)

        self.message = message
        self.code = code
        self.params = params

    def __str__(self) -> str:
        return repr(self)


class WechatyAccessoryBindingError(WechatyError):
    """ Raises when using Accessory classes in the wrong way """


class WechatyStatusError(WechatyError, AttributeError):
    """ Wechaty method calling o non-proper status (e.g. lack of await ready) """


class WechatyConfigurationError(WechatyError, AttributeError):
    """ Raises when configuration out of expected case """


class WechatyOperationError(WechatyError):
    """ Logical out of business error occurs when using wechaty """


class WechatyPluginError(WechatyError):
    """ Error occurs when using plugin """


class WechatyPayloadError(WechatyError, ValueError):
    """ Error occurs when the GRPC service return data out of expected """
