# 科研发布流程 · 从实验分支到论文版本

使用真实可运行 train.py 演练本地提交、实验分支、PR 说明与带标签的发布。

## 环境前提

Git、Python 3.10+；远程步骤另需 GitHub 账号、已安装并登录 gh、有权限的仓库。先修改示例维护者信息。脚本不会自动创建仓库或推送。

## 实验原理

提交固定源码快照，分支指向一条实验历史，PR 记录变更和验证，标签将论文引用绑定到明确提交。数据产物与代码版本分别归档，避免把不断变动的默认分支当成论文版本。

## 使用步骤

### 1. 本地实验与提交

执行完整训练生成结果；git init 创建本地仓库，git add 只暂存指定源码与说明，避免误提交实验产物。首次 commit 前需已配置自己的 Git 身份。

```bash
python3 train.py --output runs/baseline
git init -b main
git add train.py README.md PR.md RELEASE.md .gitignore
git commit -m "建立可复现实验基线"
```

### 2. 实验分支

switch 创建独立分支；执行不同种子并记录结果到 PR.md。修改说明后提交，使后续 PR 有明确可审查内容。

```bash
git switch -c experiment/seed-check
python3 train.py --seed 7 --output runs/seed7
cat runs/seed7/result.json
# 编辑 PR.md，填写真实对比结果
git add PR.md
git commit -m "记录种子对照实验"
```

### 3. 远程 PR · 由你在目标仓库执行

OWNER/REPO 替换为自己的空仓库。添加 origin 后分别推送 main 和当前分支；gh pr create 会真的向 GitHub 创建 PR，因此先核对仓库和 PR.md。

```bash
git remote add origin https://github.com/OWNER/REPO.git
git push -u origin main
git push -u origin experiment/seed-check
gh pr create --base main --title "记录种子对照实验" --body-file PR.md
```

### 4. 合并后发布

PR 按仓库规则完成审查合并后，切回 main 并只接受快进更新。检查提交，再建立注解标签；push 标签和 gh release create 都作用于真实远程。

```bash
git switch main
git pull --ff-only
git log -1 --oneline
git tag -a v0.1.0 -m "科研实验基线 v0.1.0"
git push origin v0.1.0
gh release create v0.1.0 --verify-tag --notes-file RELEASE.md
```

## 验收

本地 train.py 生成有限结果且 loss < 0.01；分支提交可追溯。远程验收需真实 PR 已合并、标签对应预期提交、Release 说明记录环境与结果。本网站构建过程没有创建远程 PR 或 Release。

## 验证记录

状态：静态检查通过。日期：2026-09-21。环境：Linux x86_64 · Python 3.10.12。

Python 实验和临时仓库的初始化、提交、分支操作运行通过。未连接 GitHub；PR、推送、标签与 Release 的远端流程未运行。

## 关联排障

在研知网站搜索以下条目 ID：

- github-error-ssh
- github-error-nonfast
- github-error-protected

## 官方参考

[GitHub：分支协作流程](https://docs.github.com/en/get-started/using-github/github-flow)

## 文件与复现

本目录中的代码为完整示例；README 与网页由同一说明源生成。外部依赖按上述固定版本准备。输出数据不随网站分发，需实际运行生成。修改参数后使用新输出目录，保留命令、版本、种子、日志与配置。
