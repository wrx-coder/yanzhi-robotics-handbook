"""学习路线数据契约；构建与内容验证共用。"""
import re

def validate_learning(paths, entries):
    by_id = {e['id']: e for e in entries}
    assert [p['id'] for p in paths] == ['research-foundations','arm-control','ros-mobile','embodied-learning']
    stages = {(p['id'], s['id']) for p in paths for s in p['stages']}
    assert len(stages) == 16
    for p in paths:
        assert all(p.get(k) for k in ['title','audience','description'])
        assert len(p['stages']) == 4
        for s in p['stages']:
            assert re.fullmatch('[a-z][a-z0-9-]*',s['id'])
            assert all(s.get(k) for k in ['title','level','goal','prerequisites','environment'])
            assert 3 <= len(s['readings']) <= 5 and len(set(s['readings'])) == len(s['readings'])
            assert all(r in by_id for r in s['readings'])
            for r in s['suggested']:
                assert (r['path'],r['stage']) in stages
                assert (r['path'],r['stage']) != (p['id'],s['id'])
            ex = s['exercise']
            assert ex['task'] and ex['expected'] and ex['solution']
            for k in ['steps','checklist','hints']:
                assert len(ex[k]) >= 2 and all(isinstance(x,str) and x.strip() for x in ex[k])
            assert all(r in by_id and 'project' in by_id[r] for r in ex['projects'])
            assert ex['troubleshooting'] and all(r in by_id and by_id[r]['kind']=='报错' for r in ex['troubleshooting'])
            assert len(s['quiz']) == 3
            assert [q['id'] for q in s['quiz']] == ['q1','q2','q3']
            assert [q['kind'] for q in s['quiz']] == ['概念','操作判断','常见错误']
            for q in s['quiz']:
                assert q['question'] and q['explanation'] and q['reading'] in by_id
                assert len(q['options']) >= 3 and len(set(q['options'])) == len(q['options'])
                assert type(q['answer']) is int and 0 <= q['answer'] < len(q['options'])
