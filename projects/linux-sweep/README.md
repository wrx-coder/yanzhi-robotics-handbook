# 多种子实验 · 参数扫描、失败记录与指标汇总

对两档学习率和三个种子执行六次真实实验，保留失败退出码、日志及统计摘要。

## 环境前提

Python 3.10+，仅标准库。目录中已包含 train.py；在可写的新输出目录运行。

## 实验原理

每组参数由独立子进程执行，避免随机状态串扰。汇总表保留成功与失败两类记录；均值和样本标准差仅使用成功数据，同时报告失败数量，避免把失败实验悄悄丢弃。

## 使用步骤

### 1. 完整参数扫描

sweep.py 按固定参数表顺序启动六个子进程。--output 必须是不存在的目录，防止覆盖旧实验。

```bash
python3 sweep.py --output sweep-results
cat sweep-results/summary.csv
cat sweep-results/aggregate.json
```

### 2. 验证失败记录

--fail-seed 1 为两个 seed=1 实验注入非法学习率。其余实验继续完成，进程最后返回 1，代表该扫描存在失败。紧接着 echo $? 读取退出码；不要在其间执行其他命令。

```bash
python3 sweep.py --output sweep-with-failure --fail-seed 1
echo $?
cat sweep-with-failure/summary.csv
```

### 3. 保存可复现结果

tar 归档全部分组日志与配置结果。查看失败日志应能追溯明确异常，而不是只看到汇总里的 failed。

```bash
cat sweep-with-failure/lr0.03-seed1.log
tar -czf sweep-results.tar.gz sweep-results
```

## 验收

正常扫描：summary.csv 有 6 条 ok，aggregate.json 有 2 组统计。注入失败：4 条 ok、2 条 failed，两个失败日志明确指出学习率非法，程序退出码为 1。统计可复现意味着保留种子、配置、失败比例与环境，而不是只复制一个均值。

## 验证记录

状态：目标环境运行通过。日期：2026-09-21。环境：Linux x86_64 · Python 3.10.12。

六组扫描全部成功；注入故障后四组成功、两组失败，程序退出码 1；CSV 与分组统计保留失败记录。

## 关联排障

在研知网站搜索以下条目 ID：

- linux-error-space
- linux-error-oom
- linux-error-permission

## 官方参考

[GNU Bash 官方手册](https://www.gnu.org/software/bash/manual/bash.html)

## 文件与复现

本目录中的代码为完整示例；README 与网页由同一说明源生成。外部依赖按上述固定版本准备。输出数据不随网站分发，需实际运行生成。修改参数后使用新输出目录，保留命令、版本、种子、日志与配置。
