#!/usr/bin/env python3
"""检查官方入口状态；报告访问受限，不绕过网站访问保护。"""
import concurrent.futures
import json
import urllib.request
import urllib.error
from pathlib import Path
from build import SOURCES, ROOT

def check(item):
    key, (title, url) = item
    try:
        request = urllib.request.Request(url, headers={'User-Agent': 'ResearchHandbook-LinkCheck/1.0'})
        with urllib.request.urlopen(request, timeout=12) as response:
            head = response.read(4096).decode('utf-8', errors='replace')
            guarded = any(s in head for s in ['Oh noes!', 'Making sure you', 'Access Denied'])
            return dict(key=key, title=title, url=url, status=response.status, final_url=response.url, access='需访问验证' if guarded else '可访问')
    except Exception as error:
        return dict(key=key, title=title, url=url, status=getattr(error, 'code', None), access=str(error))

if __name__ == '__main__':
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        results = list(pool.map(check, SOURCES.items()))
    (ROOT/'data'/'source-audit.json').write_text(json.dumps(dict(date='2026-09-20', sources=results), ensure_ascii=False, indent=2))
    for row in results:
        if row['access'] != '可访问':
            print(row['key'], row['status'], row['access'], row['url'])
    print('Checked:', len(results), 'Accessible:', sum(x['access']=='可访问' for x in results))
