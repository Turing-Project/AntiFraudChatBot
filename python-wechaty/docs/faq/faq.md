# python-wechaty 能登录多个微信吗？

可以。必须保证一个进程内只启动一个wechaty实例，可通过多行命令来启动多个wechaty实例，或在程序当中使用多进程启动多个wechaty实例（不推荐）。


# the network is not good, the bot will try to restart  after 60 seconds

此类问题的出现主要是由于Service(Token Provider Service, Gateway Service)连接不上。

你可以从如下方式进行排查：
* 使用latest和0.62.3版本的wechaty docker镜像来都给启动service。
* 查看服务的endpoint（ip、port）是否可连通？
* 查看docker镜像当中是否有connection的记录？

# 什么是Puppet

The term `Puppet`in Wechaty is an Abstract Class for implementing protocol plugins. The plugins are the component that helps Wechaty to control the Wechat(that's the reason we call it puppet).

The plugins are named XXXPuppet, like PuppetPuppeteer is using the chrome puppeteer to control the WeChat Web API via a chrome browser, PuppetPadchat is using the WebSocket protocol to connect with a Protocol Server for controlling the iPad Wechat program.