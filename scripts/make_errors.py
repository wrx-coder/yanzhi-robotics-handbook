"""把人工编写的故障案例编译成结构化条目。日志检索完全离线。"""
import json
from build import ROOT, MODULES, CORE_MODULE_IDS

def make_errors():
    errors = []
    for module in MODULES:
        if module['id'] not in CORE_MODULE_IDS:
            continue
        path = ROOT/'data/errors'/f"{module['id']}.txt"
        for number, line in enumerate(path.read_text().splitlines(), 1):
            if not line or line.startswith('#'):
                continue
            fields = line.split('¦')
            if len(fields) != 14:
                raise ValueError((path.name, number, len(fields)))
            slug,title,category,patterns,cause,command,why,normal,abnormal,fix,verify,expected,related,source = fields
            assert all(fields)
            command,verify = command.replace('\\n','\n'),verify.replace('\\n','\n')
            version = module['version']
            if module['id']=='ros':
                version = 'ROS 1 Noetic' if slug.startswith('ros1-') else 'ROS 2 Humble / Jazzy'
            patterns = patterns.split(';;')
            errors.append(dict(id=f"{module['id']}-error-{slug}",module=module['id'],title=title,
                category=category,summary=f"遇到“{patterns[0]}”或同类症状时，按环境、输入和运行状态逐步确认原因。",
                principle=cause,code=command,language='bash',explain=[why,normal,abnormal],
                pitfall='下列原因是排查候选，不代表仅凭错误文本即可确定根因。先保存配置与必要日志，再按检查结果选择修复。',
                source=source,version=version,level='进阶',kind='报错',related=related.split(','),
                prerequisites=module['prerequisites']+' 排障中的文件路径、节点名和进程编号须替换为自己的对象。rg 来自 ripgrep；若本机缺少它，可先安装 ripgrep，或将简单文本过滤改为 grep -E。检查命令若持续监听，用 Ctrl+C 结束后再继续下一步。',
                troubleshooting=dict(patterns=patterns,diagnosis=[dict(title='执行诊断检查',code=command,reason=why,normal=normal,abnormal=abnormal)],
                    fixes=fix.split(';;'),verification=dict(code=verify,expected=expected),checked='2026-09-21')))
    assert len(errors)==72
    (ROOT/'data/errors.json').write_text(json.dumps(errors,ensure_ascii=False,indent=2))
    print('已生成 72 篇结构化排障条目')

if __name__=='__main__':make_errors()
