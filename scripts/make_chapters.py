"""使用已保存的官方目录快照构建章节表；不在构建阶段联网。"""
import hashlib
import json
import re
from urllib.parse import urljoin
from build import ROOT

BOOKS=[]
CHAPTERS=[]
labels_path=ROOT/'data/chapter-labels.json'
LABELS=json.loads(labels_path.read_text()) if labels_path.exists() else {}
ROS_HEADINGS=json.loads((ROOT/'data/official-snapshots/ros-headings.json').read_text())
BASH_HEADINGS=json.loads((ROOT/'data/official-snapshots/bash-source-toc.json').read_text())['rows']
UNMAPPED={}


def snapshot(key):return json.loads((ROOT/'data/official-snapshots'/f'{key}.json').read_text())


def book(id,module,title,version,url,scope,verification='checked'):
    b=dict(id=id,module=module,title=title,version=version,url=url,scope=scope,snapshotDate='2026-09-21',verification=verification)
    BOOKS.append(b)
    return b


def add(b, original, url, parent=None, label_key=None, verification=None):
    key=label_key or b['id']+'|'+original
    label=LABELS.get(key) or LABELS.get(original)
    if not label:
        UNMAPPED[key]=original
        label={'title':'待翻译章节','entries':[]}
    refs=label.get('entries',[])
    status=label.get('status','overview' if refs else 'missing')
    display_original=ROS_HEADINGS.get(url,{}).get('title') or original
    if b['id']=='bash':
        for row in BASH_HEADINGS:
            if row['node'].rstrip('?')==original:
                display_original=row['title']
                break
        display_original={'Introduction and Notation':'Introduction to Line Editing','History Interaction':'History Expansion','Implementation Differences From The SVR4_002e2 Shell':'Implementation Differences From The SVR4.2 Shell','Builtin Index':'Index of Shell Builtin Commands','Reserved Word Index':'Index of Shell Reserved Words','Variable Index':'Parameter and Variable Index'}.get(display_original,display_original)
    c=dict(id=b['id']+'-'+hashlib.sha1((original+'|'+url).encode()).hexdigest()[:10],
           module=b['module'],book=b['id'],parent=parent,title=label['title'],originalTitle=display_original,
           url=url,version=b['version'],status=status,verification=verification or b['verification'],
           checked='2026-09-21',entries=refs,
           reason=label.get('reason','本地内容涵盖主要操作、原理与验收步骤。' if status=='detailed' else
                            '仅收录该章部分常用主题，完整范围仍需查阅原文。' if refs else '尚无对应本地讲解；保留官方入口便于补充。'))
    CHAPTERS.append(c)
    return c['id']


def from_nav(key,module,title,version):
    snap=snapshot(key)
    b=book(key,module,title,version,snap['url'],'纳入该版本全站导航的一、二级目录；外部项目链接排除。API 只计参考章节，不逐函数计数。')
    parents={}
    for row in snap['rows']:
        parents[row['url']]=add(b,row['title'],row['url'],parents.get(row.get('parent')))


from_nav('mujoco-nav','mujoco','MuJoCo 官方文档','3.3.7')
from_nav('gazebo-nav','gazebo','Gazebo 官方用户与库指南','Harmonic · 目录快照')
snap=snapshot('isaac-nav')
b=book('isaac-nav','isaac','Isaac Lab 官方文档','v2.3.0',snap['url'],'纳入全站导航一、二级目录；同 URL 只计一次。教程总页当前跳转，教程目录另与官方 v2.3.0 标签源码核对；API 不展开类和函数。')
seen=set();parent=None
for line in snap['links'].splitlines():
    match=re.match(r"(\[.*?\]) (.*?) \| (.*)",line)
    if not match:continue
    classes,title,href=match.groups()
    url=urljoin(snap['url'],href).rstrip('#')
    if url in seen or not url.startswith('https://isaac-sim.github.io/IsaacLab/v2.3.0/'):continue
    seen.add(url)
    current=add(b,title,url,parent if 'toctree-l2' in classes else None)
    if 'toctree-l1' in classes:parent=current

for key,version,base in [('coreutils','9.5','https://www.gnu.org/software/coreutils/manual/html_node/'),('findutils','4.9.0','https://www.gnu.org/software/findutils/manual/html_node/find_html/')]:
    snap=snapshot(key+'-texi')
    b=book(key,'linux','GNU '+key+' 手册',version,snap['url'],'按官方版本源码中的 chapter / section 收录一、二级标题。在线手册可能滚动更新，版本核对以此处源码标签为准。正文的发行版可用选项仍须使用本机 --help 核实。')
    parent=None;node=''
    for line in snap['links'].splitlines():
        if line.startswith('@node '):node=line[6:]
        elif line.startswith(('@chapter ','@section ')):
            title=re.sub(r'@\w+\{([^}]+)\}',r'\1',line.split(' ',1)[1])
            slug=''.join(c if c.isalnum() or c=='-' else '-' if c==' ' else '_'+format(ord(c),'04x') for c in node)
            current=add(b,title,base+slug+'.html',parent if line.startswith('@section') else None)
            if line.startswith('@chapter'):parent=current

# Bash 目录取自官方页面，保存最初人工核对的一、二级编号。
b=book('bash','linux','GNU Bash 参考手册','5.3','https://www.gnu.org/software/bash/manual/html_node/index.html','纳入官方目录编号一、二级章节；附录与索引也保留。Bash 5.3 手册不代表 Ubuntu 22.04/24.04 自带该版本，例子使用其共有语法。')
parent=None
for row in snapshot('bash-toc')['rows']:
    current=add(b,row['title'],row['url'],parent if row['depth']==2 else None)
    if row['depth']==1:parent=current

snap=snapshot('openssh')
b=book('openssh','linux','OpenSSH 官方手册索引','2026-09-21 目录快照',snap['url'],'以官方索引列出的 12 份命令/配置手册为章节；协议 RFC、手册内部参数和历史版本不在本索引粒度内。')
seen=set()
for line in snap['links'].splitlines():
    if ' | https://man.openbsd.org/' in line:
        title,url=line.split(' | ')
        if url not in seen and re.search(r'\([158]\)',title):add(b,title,url);seen.add(url)

snap=snapshot('systemd')
b=book('systemd','linux','systemd 管理器手册','在线手册 · 2026-09-21 快照',snap['url'],'以 systemd(1) 手册主体章节为范围；配置指令、信号枚举、环境变量与内核参数不逐项计数，相关独立服务手册由原文继续查阅。')
for title in ['Description','Units','Directories','Signals','Environment','Kernel Command Line','System Credentials','Readiness Protocol','Options','Files','History','See Also']:
    add(b,title,snap['url']+'#'+title.replace(' ','%20'))

rosbase='https://docs.ros.org/en/jazzy/'
groups=[('ros-beginner-cli','Beginner: CLI tools','Tutorials/Beginner-CLI-Tools'),('ros-beginner-client','Beginner: Client libraries','Tutorials/Beginner-Client-Libraries'),('ros-intermediate','Intermediate','Tutorials/Intermediate'),('ros-advanced','Advanced','Tutorials/Advanced'),('ros-demos','Demos','Tutorials/Demos'),('ros-misc','Miscellaneous','Tutorials/Miscellaneous'),('ros-basic-concepts','Basic Concepts','Concepts/Basic'),('ros-intermediate-concepts','Intermediate Concepts','Concepts/Intermediate'),('ros-advanced-concepts','Advanced Concepts','Concepts/Advanced')]
b=book('ros2','ros','ROS 2 教程与概念','Jazzy',snapshot('ros2')['url'],'纳入 Tutorials 的全部分组及其直接子章、Concepts 的全部分组及其直接子章。网页访问受限时以官方 jazzy 分支 RST 目录核对；不展开子教程内部步骤。')
add(b,'First Steps',rosbase+'First-Steps.html')
for key,title,path in groups:
    parent=add(b,title,rosbase+path+'.html')
    text=snapshot(key)['links'];intoc=False
    for line in text.splitlines():
        if line.startswith('.. toctree::'):intoc=True;continue
        if not line.strip():continue
        if intoc and not line.startswith(' '):intoc=False
        if intoc and line.startswith('   ') and not line.strip().startswith(':'):
            rel=line.strip(); original=rel.rsplit('/',1)[-1].replace('-',' ')
            add(b,original,urljoin(rosbase+path+'.html',rel+'.html'),parent,label_key='ros2|'+rel)
b=book('ros2-how','ros','ROS 2 实践指南','Jazzy',snapshot('roshow')['url'],'官方 How-To-Guides 目录中全部直接章节；迁移和发布的更深层专题可从各章节继续访问。')
for line in snapshot('roshow')['links'].splitlines():
    if line.startswith('   How-To-Guides/'):
        path=line.strip();add(b,path.rsplit('/',1)[-1].replace('-',' '),rosbase+path+'.html',label_key='ros2-how|'+path)
b=book('ros1','ros','ROS 1 核心入门教程','Noetic · 历史教程','https://wiki.ros.org/ROS/Tutorials','保留 ROS 1 核心入门教程目录。官方 Wiki 当前访问验证阻止完整核对，以下条目均显式标为待核对，不能计作已经确认的目录快照。','pending')
for title,path in [('安装与配置','InstallingandConfiguringROSEnvironment'),('文件系统','NavigatingTheFilesystem'),('创建功能包','CreatingPackage'),('构建功能包','BuildingPackages'),('理解节点','UnderstandingNodes'),('理解话题','UnderstandingTopics'),('理解服务与参数','UnderstandingServicesParams'),('日志与启动','UsingRqtconsoleRoslaunch'),('创建消息与服务','CreatingMsgAndSrv'),('Python 发布订阅','WritingPublisherSubscriber(python)'),('C++ 发布订阅','WritingPublisherSubscriber(c++)'),('测试发布订阅','ExaminingPublisherSubscriber'),('Python 服务客户端','WritingServiceClient(python)'),('C++ 服务客户端','WritingServiceClient(c++)'),('记录与回放','Recording and playing back data'),('roswtf 检查','Getting started with roswtf')]:
    add(b,path,'https://wiki.ros.org/ROS/Tutorials/'+path.replace(' ','%20'),label_key='ros1|'+title)

# GitHub 为滚动文档，没有发行版号；记录取样日期与导航粒度，不声称固定 API 版本。
ghnames={'get-started':'入门','authentication':'认证','repositories':'仓库','pull-requests':'拉取请求','actions':'自动化','issues':'问题与项目','code-security':'代码安全','pages':'静态站点','rest':'REST API','github-cli':'命令行'}
for key,title in ghnames.items():
    snap=snapshot('gh-'+key)
    b=book('gh-'+key,'github','GitHub · '+title,'2026-09-21 目录快照',snap['url'],'纳入本产品导航的一级分组；作为 GitHub 总文档的二级章节。分组按钮无独立链接时，官方入口指向该分组第一篇文章。更深层文章与 API 端点不逐项计数。')
    for row in snap['rows']:add(b,row['title'],row['url'])

if UNMAPPED:
    (ROOT/'data/chapter-unmapped.json').write_text(json.dumps(UNMAPPED,ensure_ascii=False,indent=2)+'\n')
    print(f'待填写 {len(UNMAPPED)} 个中文章节映射')
else:
    (ROOT/'data/chapters.json').write_text(json.dumps(dict(books=BOOKS,chapters=CHAPTERS),ensure_ascii=False,indent=2)+'\n')
    print(f'已生成 {len(CHAPTERS)} 个章节 / {len(BOOKS)} 份目录')
