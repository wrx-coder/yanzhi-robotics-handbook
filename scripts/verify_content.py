"""校验知识库引用、可解析代码、工程 ZIP 与页面源码一致性。"""
import ast
import hashlib
import json
from pathlib import Path
import subprocess
import zipfile
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parent.parent
data=json.loads((ROOT/'dist/knowledge.json').read_text())
script=(ROOT/'dist/knowledge.js').read_text()
assert script.startswith('window.KNOWLEDGE = ') and script.endswith(';\n')
assert json.loads(script[len('window.KNOWLEDGE = '):-2]) == data, '离线 JS 与 JSON 索引不一致'
from learning import validate_learning
validate_learning(data['learningPaths'], data['entries'])
from embodied import validate_skills
validate_skills([e for e in data['entries'] if e['kind']=='技能'], data['sources'])
assert len(data['modules']) == 7
counts={'bash':0,'python':0,'xml':0,'zip_files':0}
ids={e['id'] for e in data['entries']}
assert len(ids)==len(data['entries'])==503
for entry in data['entries']:
    assert entry['source'] in data['sources']
    assert all(ref in ids for ref in entry.get('related',[]))
    language,code=entry.get('language'),entry.get('code')
    if language=='bash':
        result=subprocess.run(['bash','-n'],input=code,text=True,capture_output=True)
        assert result.returncode==0,(entry['id'],result.stderr)
        counts['bash']+=1
    elif language=='python':
        ast.parse(code,filename=entry['id']);counts['python']+=1
    elif language=='xml':
        ET.fromstring('<fragment>'+code+'</fragment>');counts['xml']+=1
    for section in entry.get('sections',[]):
        if section.get('code') and entry.get('project'):
            result=subprocess.run(['bash','-n'],input=section['code'],text=True,capture_output=True)
            assert result.returncode==0,(entry['id'],section['title'],result.stderr)
    if 'project' in entry:
        project=entry['project'];archive=ROOT/'dist'/project['download']
        assert hashlib.sha256(archive.read_bytes()).hexdigest()==project['sha256']
        with zipfile.ZipFile(archive) as package:
            assert len(package.namelist())==len(project['files'])
            for file in project['files']:
                contents=(ROOT/'projects'/project['directory']/file['path']).read_text()
                assert contents==file['content']
                assert package.read(project['directory']+'/'+file['path']).decode()==contents
                counts['zip_files']+=1
        assert project['verification']['status'] in ['未运行','静态检查通过','目标环境运行通过']
for chapter in data['coverage']['chapters']:
    assert all(ref in ids for ref in chapter['entries'])
    assert chapter['status']!='detailed' or chapter['verification']=='checked'
assert len([e for e in data['entries'] if e['kind']=='报错'])==72
assert len([e for e in data['entries'] if 'project' in e])==12
print(json.dumps(counts,ensure_ascii=False,indent=2))
print('503 篇词条 / 96 项技能、72 篇报错、12 套实战、章节引用及 ZIP 同源性检查通过')
