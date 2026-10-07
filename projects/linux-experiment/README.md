# 远程实验流程 · 独立环境、日志与归档

运行随附的线性回归程序，隔离 Python 环境，用 tmux 管理会话并归档真实结果。

## 环境前提

Ubuntu 22.04 / 24.04，Python 3.10+、python3-venv、tmux、tar。训练本身只用 Python 标准库，无 GPU 要求。

## 实验原理

梯度下降在合成数据上拟合 y=2x+1。固定种子控制采样；虚拟环境隔离依赖；Bash pipefail 将训练失败传递到流水线；tee 同时写入日志并显示输出；tar 将配置与结果打包。

## 使用步骤

### 1. 准备独立环境

apt 安装虚拟环境支持与会话工具；venv 创建本目录环境；source 让当前 shell 的 python3 指向该环境。

```bash
sudo apt install python3-venv tmux
python3 -m venv .venv
source .venv/bin/activate
python3 --version
```

### 2. 启动并保留会话

tmux new 创建 research 会话；在新会话中 run.sh 调用真实 train.py，按时间与进程号建立输出目录，并在成功后归档。Ctrl+B 后按 D 可离开会话；完成后输入 exit 关闭空闲会话。

```bash
tmux new -s research
source .venv/bin/activate
bash run.sh
```

### 3. 重新连接与检查

attach 连接仍在运行的会话；训练很快，若会话已退出则无需重连。find 列出结果；检查 JSON 中 loss 与两个拟合参数，并保留 tar.gz。

```bash
tmux attach -t research
find runs -maxdepth 2 -type f
cat runs/*/result.json
```

## 验收

每次运行生成 metrics.csv（200 行数据）、result.json、日志及 tar.gz。默认种子下 loss 应低于 0.01，weight 接近 2、bias 接近 1。归档解压后应含同一结果目录和日志。

## 验证记录

状态：目标环境运行通过。日期：2026-09-21。环境：Linux x86_64 · Python 3.10.12。

Bash 流水线与真实训练运行成功，loss=0.003008，CSV/JSON/日志/tar.gz 均生成。未运行 tmux 交互会话；其命令已静态核对。

## 关联排障

在研知网站搜索以下条目 ID：

- linux-error-command
- linux-error-permission
- linux-error-module

## 官方参考

[Python venv 官方文档](https://docs.python.org/3/library/venv.html)

## 文件与复现

本目录中的代码为完整示例；README 与网页由同一说明源生成。外部依赖按上述固定版本准备。输出数据不随网站分发，需实际运行生成。修改参数后使用新输出目录，保留命令、版本、种子、日志与配置。
