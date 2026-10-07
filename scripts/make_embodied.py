#!/usr/bin/env python3
"""编译人工编写的技能速查卡。构建离线完成，不生成实验验证声明。"""
import json
from pathlib import Path
from embodied import CATEGORIES, REFERENCE_DATA, SOURCES, validate_skills
ROOT = Path(__file__).resolve().parent.parent
entries = []
category = None
for n, line in enumerate((ROOT/'data/skills/embodied.txt').read_text().splitlines(), 1):
    if not line.strip():
        continue
    if line.startswith('# '):
        category = line[2:]
        assert category in CATEGORIES, category
        continue
    fields = line.split('¦')
    assert len(fields) == 12, (n, len(fields))
    slug,title,english,level,summary,principle,prerequisites,steps,tool,pitfall,refs,related = fields
    source_keys = refs.split(',')
    keywords = ['embodied','具身智能', english, *english.split(' / ')]
    if category == '模仿学习': keywords += ['IL','Imitation Learning']
    if category == '强化学习': keywords += ['RL','Reinforcement Learning']
    if category == 'VLA 与多模态策略': keywords += ['VLA','Vision Language Action']
    entries.append(dict(id='embodied-'+slug,module='embodied',title=title,englishTitle=english,category=category,
        kind='技能',level=level,summary=summary,principle=principle,prerequisites=prerequisites,
        explain=steps.split(';;'),tools=tool,pitfall=pitfall,keywords=keywords,source=source_keys[0],
        sources=[dict(key=k,version=REFERENCE_DATA[k][2],checked='2026-09-21') for k in source_keys],
        version=REFERENCE_DATA[source_keys[0]][2],related=related.split(',')))
validate_skills(entries,SOURCES)
(ROOT/'data/embodied.json').write_text(json.dumps(entries,ensure_ascii=False,indent=2)+'\n')
print('已生成 96 项具身智能技能 / 12 类，每类 8 项')
