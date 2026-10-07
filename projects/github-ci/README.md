# 科研代码自动化 · Python 测试矩阵与标签发布

完整指标代码、三个单元测试、双 Python 版本 CI 和仅标签触发的 Release 工作流。

## 环境前提

本地 Python 3.10+、Git；远端需你有权限的 GitHub 仓库且 Actions 已启用。工作流 actions/checkout@v4、setup-python@v5 是固定主版本入口，严格供应链复现时可自行审计并锁定提交 SHA。

## 实验原理

CI 在干净 Runner 上重建环境并测试数学结果与异常边界；矩阵检验 Python 兼容性。发布 job 先运行测试，再归档 HEAD，并用受限于标签事件的写权限创建 Release。PR 验证仅有只读权限。

## 使用步骤

### 1. 本地完整测试

unittest discover 从 tests 发现测试，覆盖已知数值、相同输入和非法输入；不需要下载第三方 Python 包。

```bash
python3 -m unittest discover -s tests -v
```

### 2. 加入已有仓库

把本项目文件放到目标仓库根目录；确认 .github 隐藏目录也被复制。git add 只暂存相关文件，远程 push 会触发 main 或 PR 检查。

```bash
git add research_math.py tests .github README.md RELEASE.md .gitignore
git commit -m "添加科研指标测试和发布流程"
git push
```

### 3. 检查矩阵执行

gh run list 显示运行，view --log-failed 定位失败步骤。只有远端两个 Python job 均通过才能声称云端矩阵验证通过。

```bash
gh run list --limit 5
gh run view --log-failed
```

### 4. 标签触发发布

确认在已通过审查和测试的提交上；创建此前未使用的版本标签，推送触发 release.yml。工作流使用 RELEASE.md 并附上当前提交的 ZIP。

```bash
git tag -a v0.1.0 -m "指标与测试首版"
git push origin v0.1.0
gh release view v0.1.0
```

## 验收

本地输出 Ran 3 tests / OK。云端矩阵覆盖 Python 3.10 与 3.12；标签发布应出现 research-code.zip。远端工作流未由网站构建代为执行，首次使用需在自己的仓库核实权限与分支策略。

## 验证记录

状态：静态检查通过。日期：2026-09-21。环境：Linux x86_64 · Python 3.10.12。

本机三个单元测试通过，两个 Actions YAML 已解析。未在 GitHub Runner 运行 Python 矩阵或发布工作流。

## 关联排障

在研知网站搜索以下条目 ID：

- github-error-actions
- github-error-ci
- github-error-actions-permission

## 官方参考

[GitHub Actions：自动化工作流](https://docs.github.com/en/actions)

## 文件与复现

本目录中的代码为完整示例；README 与网页由同一说明源生成。外部依赖按上述固定版本准备。输出数据不随网站分发，需实际运行生成。修改参数后使用新输出目录，保留命令、版本、种子、日志与配置。
