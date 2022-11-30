# AntiFraudChatBot
A simple prompt-chatting AI based on wechaty and fintuned NLP model
<br>
一个简单的基于prompt的预训练大模型中文聊天人工智能框架，仅限交流与科普。


![image](https://img.shields.io/badge/License-Apache--2.0-green) ![image](https://img.shields.io/badge/License-MIT-orange)  ![image](https://img.shields.io/badge/License-Anti--996-red)  ![image](https://img.shields.io/badge/pypi-v0.0.1a4-yellowgreen) ![image](https://img.shields.io/badge/stars-%3C%201k-blue) ![image](https://img.shields.io/badge/issues-1%20open-brightgreen)  



## 项目简介
AntiFraudChatBot是基于大规模预训练中文模型、语义识别与检测、对话意图等技术所构建的生成式对话QA框架，目前第一版模型针对反诈骗的场景化任务，对比传统的BertQA模型或non-prompt模型，在真实测试中AI对话的流畅度有明显提高。
| 项目作者        | 主页1           | 主页2  | 
| ------------- |:------:|:----:|
| Y1ran       | [CSDN](https://y1ran.blog.csdn.net/) |[Github](https://github.com/Y1ran) |

<br>

## 框架说明
- [x] 基于wechaty框架，AI可以7x24的实时、无缝进行微信对话
- [x] 对话核心是YUAN1.0——2457亿参数的开源中文预训练大模型
- [x] 整体框架模块化设计，对话核心可被替换为其他模型（文心、盘古等）
- [x] 端到端生成，服务启动后可以持续对话（除非云服务器宕机）


## 本地环境
* Ubuntu 18.04.2/ Windows10 x86
* Python >= 3.7
* Tensorflow-gpu 1.15.2
* paddlenlp 2.4.2
* paddlepaddle 2.0.0
* CUDA >= 10.0
* CuDNN >= 7.6.0
* Wechat 3.3.0.115


## 系统结构
整个框架分为服务器端、本地端和模型端3个模块，每个模块之间解耦，可单独迭代或替换。


整体框架：
![405](https://user-images.githubusercontent.com/24304668/204587515-2a3a9c7b-8ae5-4055-9446-a62531dddd80.png)

### 对话核心
YUAN-1.0是国内最新的预训练大模型，整体参数量2457亿，预训练语料5000G，超过GPT-3。在中文语言理解评测基准CLUE榜单的零样本学习（zero-shot）和小样本学习（few-shot）都拿过总榜第一。用这个的原因也很简单——API接口使用方便、最主要是免费调用：[YUAN-1.0](https://github.com/Shawn-Inspur/Yuan-1.0)。如果想替换成其他模型，请直接修改代码中API对应的传参。

YUAN-1.0开源预训练中文模型
<div align=center><img width="750" height="350" src="https://user-images.githubusercontent.com/24304668/204587578-89cf5783-7a5b-40d5-8026-4f75bc8d3a99.png"/></div>

<br>

#### 对话设计
*	设定每条信息的回复间隔，模拟真实打字速度（total_len / 10 * 2s)
*	加入通用emoji替换关键词，但目前还不支持表情包
*	连续语句拼接，当对面在限定时间内说了多段话时，wechaty会hold本轮对话，直到对方结束
* 这种情况下，对方的输入会被拼接成一句话之后输入AI，只回复一次

<br>

## 对话demo
### 安装依赖

源1.0采用了目前python API调用所需的主流依赖库，用如下命令安装或确认相关依赖：
```bash
pip install requests hashlib json
```

完成安装后在硬盘上任意位置，用如下命令将GitHub上的代码fork下来即可。
```
git clone https://github.com/Shawn-Inspur/Yuan-1.0.git
```
需要注意的是，`GitHub`上下载的代码包含了三个部分，`src`中是模型训练的代码，`sandbox`中是web示例开发使用的沙箱代码，需要额外安装`yarn`，`yuan_api`中是采用API进行推理的示例代码和工具。

### 快速开始

这里给大家演示不基于wechaty框架，如何用YUAN-1.0来构建一个对话机器人的过程。
首先确认项目工作目录为`yuan_api`，然后在`examples`目录下新建一个`python`文件：`dialog.py`。
```python
from inspurai import Yuan, set_yuan_account,Example
```
代码中首先从`inspurai`导入`Yuan`和`Example`这两个类，以及`set_yuan_account`函数。其中`Yuan`类中包含了用于提交`API`请求以及获取推理结果的各种函数，具体将在后文中进行解释。`Example`类用于构建输入输出示例，通过对`yuan`实例中添加`example`，即可实现one-shot或few-shot。
<br>

在YUAN的官网注册后，请用申请API时使用的账号和手机号来获得授权。

```python
# 1. set account
set_yuan_account("用户名", "手机号")
```
<br>

初始化`Yuan`实例`yuan`，并对其加入一个样例：
```python
yuan = Yuan(input_prefix="对话：“",
            input_suffix="”",
            output_prefix="答：“",
            output_suffix="”",)
# 3. add examples if in need.
yuan.add_example(Example(inp="对百雅轩798艺术中心有了解吗？",
                        out="有些了解，它位于北京798艺术区，创办于2003年。"))
```
<br>
其中`input_prefix`和`input_suffix`分别为输入的前缀和后缀。`output_prefix`和`output_suffix`为输出的前缀和后缀。
如果对实例`yuan`添加了`example`，则会在提交query前在`example`的输入和输出部分分别添加前缀和后缀。如果有需要，实例`yuan`中还可以继续添加更多`example`，实现few-shot。其他参数将在后面详细介绍。

至此一个问答机器人就已经完成了，接下来就可以提问了。把问题放在`prompt`变量里，然后提交给`yuan`的API。
<br>
### 返回结果
```python
prompt = "故宫的珍宝馆里有什么好玩的？"
response = yuan.submit_API(prompt=prompt,trun="”")
```
其中`trun`为截断符，yuan API推理服务返回的生成结果有可能包含重复的答案，通过设置`trun`可以在第一次出现该字符时截断返回结果。因为我们在之前设置的输出后缀为‘”’,对于推理返回的结果，我们可以将trun设为‘”’,在返回完第一个完整输出时将其截断。因为截断时最后这个字符并不会被保留，为了保持我们对话机器人输出符号的对称性，我们人为在打印时加上后引号。
> 注：这种设计是必要的，因为对于更普遍的任务而言，加入的后缀是无意义的，仅作为语句分割用。我们并不希望这种字符被返回。

<br>

为了能够连续进行对话，我们将上面提交prompt和返回结果的过程重构如下：
```python
print("====问答机器人====")

while(1):
    print("输入Q退出")
    prompt = input("问：")
    if prompt.lower() == "q":
        break
    response = yuan.submit_API(prompt=prompt,trun="”")
    print(response+"”")
```
这样一个简单的问答机器人就开发完毕，此时就可以在命令行和他互动了。


### Prompt优化
“杀猪盘”是一种规则化、模式化的对话博弈，传统的无目标导向的“开放域对话”或“词槽式目的域对话”方案都表现不佳。而源1.0作为一种生成式预训练模型，擅长零样本（Zero-Shot）和小样本（Few-Shot）学习，而非目前更多模型所擅长的微调学习（finetune）。
因此，少量（1~ 3个）规则化的example示范下，模型可以很好的理解我们希望实现的“对话策略”，比如反套路、用语料抛梗等等，让AI看起来能够对骗子具备识别能力，本质上这也是一种query->value的查询匹配，在搜索引擎和注意力机制中很常见。

在一开始的测试中我们发现，如果没有example，模型的生成非常不靠谱，甚至会出现答非所问的情况。因此，关键就在于如何针对“反诈骗”这一场景选择适当的example供给模型。

我们最终参考[AI剧本杀](https://github.com/bigbrother666sh/shezhangbujianle)的方案：基于模型的few-shot能力建立example语料库，针对每次提问从语料库中选择最贴近的top-k个example作为模型生成的prompt输入。这里我们选择了百度飞桨@PaddlePaddle发布的预训练模型——simnet_bow ，它能够自动计算短语相似度，基于百度海量搜索数据预训练，实际效果不错，主要是运算速度快，不影响对话的实时性能。


example语料主要抽取自B站和贴吧的热门评论，一来因为评论是天然的对话形式，有显式的回复与被回复关系。二来自古评论出人才，一些金句和梗可以把人机对话变得不那么生硬。具体语料经过人工筛选，过滤不当言论，再处理成prompt格式。
下述文本展示了`Prompt Example`的生成样例。

| 说明 | 样例 |
| :------- | :--------- |
| 原始Json | {"comment":"你这算什么？知乎都人均百万了，我自己年薪200个也没说啥","reply1":"富哥V50",..}|
| 抽取文本 | [你/这/算什么/？/知乎/都/人均/百万/了,富哥/V/50]|
| Prompt检索 | 查询抽取文本List[0]与当前对话的Query相似度，加入对话Example |
| 生成Example |{"对话":"你这算什么？知乎都人均百万了，我自己年薪200个也没说啥","小源":"富哥V50"}  |

<br>


### 记忆机制
最后，由于微信聊天是多轮对话，AI有时并不记得自己或对方上一句说过什么。比如输入我想去杭州，再问她刚才我想去哪，AI多数时候都是答非所问。
为了解决这个问题，我参考LSTM的思想，为系统增加了记忆机制，具体机制如下：

![404](https://user-images.githubusercontent.com/24304668/204588953-6b1b21d5-1f0a-44f0-bea5-f237a9351068.png)


* 聊天记录放入记忆区，在每次回复时计算相似度
* 超过相似度阈值的历史对话将被AI读取使用
* 设定遗忘窗口M，超过M/2轮次的对话将被pop()
这样，AI就能够实现简单的长短期对话记忆，比如昨天聊过的内容或上一轮对话内容。

注意，对于example语料匹配度比较低的提问，过长的记忆机制反而可能让生成效果下降，最典型的情况是造成"重复回答"，即AI会在后续轮次的对话中一直重复之前已经说过的话，比如：
<div align=center><img width="550" height="275" src="https://user-images.githubusercontent.com/24304668/204710776-004a9150-24b1-408d-8869-1fe0f1b25ac7.png"/></div>

至此对话核心部分已经基本优化完毕，接下来是如何基于wechaty来构建一个无缝对话的AI聊天机器人。

## 对话框架
Wechaty 是一个开源聊天机器人框架SDK，具有高度封装、高可用的特性，支持NodeJs, Python, Go 和Java 等多语言版本。在过去的4年中，服务了数万名开发者，收获了 Github 的 1w+ Star。同时配置了完整的 DevOps 体系并持续按照 Apache 的方式管理技术社区。
开发前需要准备：
* Linux服务器（CentOS 8.0+，Python环境，Docker）
* 本地Python开发环境（我个人使用Anaconda+Intelij）
* 申请一个Wechaty秘钥Token（有免费的也有收费的）
* 一个AI专用的微信号（不建议用个人号）

### 1. Npm

[![NPM Version](https://img.shields.io/npm/v/wechaty?color=brightgreen&label=wechaty%40latest)](https://www.npmjs.com/package/wechaty)
[![npm (tag)](https://img.shields.io/npm/v/wechaty/next?color=yellow&label=wechaty%40next)](https://www.npmjs.com/package/wechaty?activeTab=versions)

[![Downloads](https://img.shields.io/npm/dm/wechaty.svg?style=flat-square)](https://www.npmjs.com/package/wechaty)
[![install size](https://packagephobia.now.sh/badge?p=wechaty)](https://packagephobia.now.sh/result?p=wechaty)

```shell
npm init
npm install wechaty

# create your first bot.js file, you can copy/paste from the above "The World's Shortest ChatBot Code: 6 lines of JavaScript"
# then:
node bot.js
```


### 2. Docker
Linux服务器下载Wechaty的docker镜像：
```
docker pull wechaty/wechaty:0.65
```

安装完成后输入
```
export WECHATY_PUPPET=wechaty-puppet-padlocal
export WECHATY_PUPPET_PADLOCAL_TOKEN=puppet_padlocal_xxxxxxxxx
export WECHATY_TOKEN=your_uuid4_token
export WECHATY_PUPPET_SERVER_PORT=8788
export WECHATY_LOG=verbose


docker run -ti \
--name wechaty_gateway \
--rm \
-e WECHATY_LOG \
-e WECHATY_PUPPET \
-e WECHATY_PUPPET_PADLOCAL_TOKEN \
-e WECHATY_PUPPET_SERVER_PORT \
-e WECHATY_TOKEN \
-p "$WECHATY_PUPPET_SERVER_PORT:$WECHATY_PUPPET_SERVER_PORT" \
wechaty/wechaty:0.65
```
> 注：0.65版本比较稳定，也可以用最新的

如果docker是部署在虚拟服务器上，还需要在Python代码入口文件中额外加一个参数

```
os.environ['WECHATY_PUPPET_SERVICE_ENDPOINT']='127.198.0.0:0000(你的虚拟服务器IP+端口号)'
```
至此，机器人的本地Grpc依赖服务已启动。

<br>

使用git clone https://github.com/wechaty/python-wechaty

选择一个puppet服务实例（除了第一个限制调用次数的service是免费的，其他应该都要付费）
### Wechaty Puppets

| Protocol | NPM |
| :--- | :--- |
| Puppet Service | `wechaty-puppet-service` |
| Whatsapp Web | `wechaty-puppet-whatsapp` |
| WeChat Web | `wechaty-puppet-wechat` |
| WeChat Pad | `wechaty-puppet-padlocal` |

> Visit our website to learn more about [Wechaty Puppet Service Providers](https://wechaty.js.org/docs/puppet-services/)

<br>
打开\app\dialog.py，在图示位置添加秘钥和配置环境变量：

![403](https://user-images.githubusercontent.com/24304668/204588909-f89d6ce2-7d75-4b6e-8c4c-195afc24e37e.png)


运行dialog.py，坐等QR code出现扫码就好
<div align=center><img width="725" height="450" src="https://user-images.githubusercontent.com/24304668/204590938-9ccb73f9-13f6-4dbe-89b7-fa14f81f55e5.png"/></div>

<br>


## 开发日志

* 2022.09.23 本地项目建立
* 2022.09.30 整体模型架构搭建，demo测试
* 2022.10.08 Prompt语料收集、处理
* 2022.10.11 接入API后wecahty对话测试
* 2022.10.15 各平台注册寻找测试对象
* 2022.10.23 开始真实场景聊天
* 2022.11.07 数据收集反馈
* 2022.11.18 优化Prompt设计与参数
* 2022.12.29 代码Review与开源发布


## Citation
```
@misc{EssayKillerBrain,
  author = {Turing's Cat},
  title = {AntiFraud AI Framework},
  year = {2022},
  publisher = {GitHub},
  journal = {GitHub repository},
  howpublished = {\url{https://github.com/Turing-Project/AntiFraudChatBot}},
}
```

<br>


## 参考资料  
[1] Long Time No See! Open-Domain Conversation with Long-Term Persona Memory  
[2] Yuan 1.0: Large-Scale Pre-trained Language Model in Zero-Shot and Few-Shot Learning 
[3] ERNIE: Enhanced Representation through Knowledge Integration   
[4] Language Models are Unsupervised Multitask Learners  
[5] Pre-train, Prompt, and Predict: A Systematic Survey of Prompting Methods in Natural Language Processing
[6] The Power of Scale for Parameter-Efficient Prompt Tuning  
[7] PPT: Pre-trained Prompt Tuning for Few-shot Learning  
[8] AI剧本杀：https://github.com/bigbrother666sh/shezhangbujianle  
[9] Wechay：https://github.com/wechaty/wechaty  
[10] PaddlePaddle：https://github.com/PaddlePaddle/PaddleNLP   
[11] PadLocal：https://wechaty.js.org/2021/03/08/python-wechaty-and-wechaty-puppet-padlocal/  
[12] [知乎：杀猪盘的套路明明很简单，为什么还是会有大量的女性相信，并且愿意掏钱上当受骗](https://www.zhihu.com/question/445232064/answer/2275257277)  


## 免责声明
该项目中的内容仅供技术研究与科普，不作为任何结论性依据，不提供任何商业化应用授权
