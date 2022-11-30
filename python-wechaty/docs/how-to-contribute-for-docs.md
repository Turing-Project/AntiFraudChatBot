# 如何贡献文档

非常感谢各位开发者能够查看此章节，python-wechaty团队正在努力编写开发者友好的文档系统，从而减少学习成本。

## 一、找到问题

在贡献之前，开发者需要明确这是否是有待完善之处，推荐从如下三点查找：

* 文档系统会在此[issue](https://github.com/wechaty/python-wechaty/issues/201)下不停更新TODO LIST，以提供各位开发者查看未完成的模块
* 开发者在浏览文档的过程中如果发现有任何觉得不合理需要调整地方，请提交PR来优化，同时编写详细的说明来描述。
* 在Issue列表中查看相关Bug或者Feature，确定能否解决

## 二、如何贡献

### fork & install

* fork[python-wechaty](https://github.com/wechaty/python-wechaty)项目

* 安装依赖包

```shell
make install
```

or

```shell
pip install -r requirements.txt
pip install -r requirements-dev.txt

# cleanup existing pre-commit configuration (if any)
pre-commit clean
pre-commit gc
# setup pre-commit
# Ensures pre-commit hooks point to latest versions
pre-commit autoupdate
pre-commit install
pre-commit install --hook-type pre-push
```

* 提交文档更新PR

有如下要求：

- [ ] 标题为：Improve Docs: [title-of-your-pr]
- [ ] PR 内容的详细描述

# 成为 Contributor

如果优化了部分文档，即可成为Wechaty的Contribtuor，享受社区提供的长期免费token服务，具体可查看：[contributor-program](https://wechaty.js.org/docs/contributor-program/)。
