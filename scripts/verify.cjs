/* 非浏览器行为检查；运行：node scripts/verify.cjs /tmp/yanzhi-qa/node_modules/linkedom */
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const assert = require('node:assert/strict');
const {parseHTML} = require(process.argv[2] || 'linkedom');
const root = path.resolve(__dirname, '..');
const data = JSON.parse(fs.readFileSync(path.join(root,'dist/knowledge.json'),'utf8'));
const html = fs.readFileSync(path.join(root,'dist/index.html'),'utf8');
const source = fs.readFileSync(path.join(root,'dist/app.js'),'utf8');
const {document,window:dom} = parseHTML(html);
const listeners = new Map(), local = new Map(), timers = new Map(), registered = new Map();
let address = new URL('file://' + path.join(root, 'dist/index.html'));
let timerId = 0;
const location = {get href(){return address.href},get hash(){return address.hash},set hash(value){address.hash=value;listeners.get('hashchange')?.()}};
const history = {replaceState(_a,_b,value){address = new URL(value,address)}};
const context = {document, location, history, URL, URLSearchParams, console, AbortController,
  navigator:{}, setTimeout(fn){timers.set(++timerId,fn);return timerId},clearTimeout(id){timers.delete(id)},
  localStorage:{getItem:key=>local.get(key)??null,setItem:(key,value)=>local.set(key,value)},
  addEventListener:(name,fn)=>listeners.set(name,fn), scrollTo:()=>{},matchMedia:()=>({matches:true}),
  KNOWLEDGE:data,isSecureContext:false};
context.window=context;
document.modelContext={registerTool:definition=>registered.set(definition.name,definition)};
document.execCommand=()=>true;
dom.HTMLTextAreaElement.prototype.select=()=>{};
vm.runInNewContext(source, context, {filename:'app.js'});
const main = ()=>document.querySelector('#main');
const route = value=>{location.hash=value};
const click = node=>node.dispatchEvent(new dom.Event('click',{bubbles:true}));
const flush = ()=>{for(const [id,fn] of [...timers]){timers.delete(id);fn()}};
let checks = 0;
function check(name,fn){fn();checks++;console.log('PASS',name)}

check('数据完整与七模块计数',()=>{
 assert.equal(data.modules.length,7);
 assert.equal(new Set(data.entries.map(e=>e.id)).size,data.entries.length);
 for(const m of data.modules){assert(m.count>0);assert.equal(m.count,data.entries.filter(e=>e.module===m.id).length)}
 for(const e of data.entries){for(const k of ['summary','principle','pitfall','source'])assert(e[k]);assert(e.explain.length);assert(data.sources[e.source]);}
});
check('首页全部模块与实战入口',()=>{assert.equal(main().querySelectorAll('.module-card').length,7);assert(main().textContent.includes(String(data.entries.length)));assert(main().textContent.includes('科研发布流程'))});
check('七模块路由、分类及分页',()=>{
 for(const m of data.modules){route('#module/'+m.id);assert(main().querySelector('h1').textContent.includes(m.name));assert.equal(main().querySelectorAll('.result-card').length,12);assert(main().querySelector('.category-chips'));}
 route('#module/linux?page=2');assert(main().textContent.includes('第 2 /'));
 route('#module/ros?category='+encodeURIComponent('ROS 1 通信'));assert(main().textContent.includes('ROS 1 Noetic'));assert.equal(main().querySelectorAll('.result-card').length,4);
});
check('中文、命令、别名与多关键词搜索',()=>{
 for(const q of ['显存','nvidia-smi','mujoko','issac','ros2','GitHub','MuJoCo 接触']){route('#search?q='+encodeURIComponent(q));assert(main().querySelectorAll('.result-card').length>0,q)}
 route('#search?q='+encodeURIComponent('符号链接'));assert(main().textContent.includes('符号链接'));
 route('#search?q='+encodeURIComponent('完全没有匹配zxq123'));assert(main().textContent.includes('没有找到匹配内容'));
});
check('实时输入保持焦点元素，更新全文结果',()=>{
 const input=document.querySelector('#global-search');input.value='科研发布流程';input.dispatchEvent(new dom.Event('input',{bubbles:true}));flush();assert.equal(input,document.querySelector('#global-search'));assert(main().textContent.includes('从实验分支到论文版本'));
});
check('搜索范围包括实战附加正文',()=>{route('#search?q='+encodeURIComponent('统计可复现'));assert(main().querySelectorAll('.result-card').length);route('#search?q='+encodeURIComponent('逐行验证'));assert(main().querySelectorAll('.result-card').length)});
check('所有文章深链接、代码与来源可渲染',()=>{
 for(const e of data.entries){route('#article/'+e.id);assert.equal(main().querySelector('h1').textContent,e.title);if(e.kind==='技能'){assert.equal(main().querySelector('pre'),null);assert.equal(main().querySelector('[data-action="copy-code"]'),null)}else{assert.equal(main().querySelector('pre code').textContent,e.code);}assert(main().querySelector('.source-link').getAttribute('href')===data.sources[e.source][1]);}
});
check('收藏添加、筛选、取消与本地持久化',()=>{
 route('#article/github-research-release');click(main().querySelector('[data-action="save"]'));assert(local.get('yanzhi-favorites').includes('github-research-release'));
 route('#saved');assert.equal(main().querySelectorAll('.result-card').length,1);click(main().querySelector('[data-action="save"]'));assert(main().textContent.includes('还没有收藏'));assert.equal(local.get('yanzhi-favorites'),'[]');
});
check('复制代码回退与内容转义',()=>{
 route('#article/mujoco-quickstart');click(main().querySelector('[data-action="copy-code"]'));assert(document.querySelector('#toast').textContent.includes('已复制'));assert.equal(main().querySelectorAll('mujoco').length,0);
 route('#search?q='+encodeURIComponent('<img src=x onerror=alert(1)>'));assert.equal(main().querySelectorAll('img').length,0);
});
check('错误路由与越界分页',()=>{route('#article/missing');assert(main().textContent.includes('没有找到这篇词条'));route('#module/missing');assert(main().textContent.includes('没有这个研究模块'));route('#module/linux?page=9999');const pages=Math.ceil(data.modules.find(m=>m.id==='linux').count/12);assert(main().textContent.includes(`第 ${pages} / ${pages} 页`));});
check('覆盖表、来源分组与静态资源完整',()=>{
 route('#coverage');assert.equal(main().querySelectorAll('tbody tr').length,data.coverage.chapters.length);assert(main().textContent.includes('GitHub'));
 route('#sources');assert.equal(main().querySelectorAll('.source-group').length,7);assert.equal(main().querySelectorAll('.source-item').length,Object.keys(data.sources).length);
 for(const ref of ['styles.css','app.js','knowledge.js','icon.svg'])assert(fs.existsSync(path.join(root,'dist',ref)));
});
check('可选 WebMCP 合约模拟（不代表真实浏览器注册验证）',()=>{
 const search=registered.get('search_research_knowledge'),open=registered.get('open_research_article');
 assert(search&&open);assert(search.execute({query:'接触力'}).count>0);assert(main().querySelector('h1').textContent.includes('接触力'));
 assert.equal(open.execute({id:'github-auth'}).title,data.entries.find(e=>e.id==='github-auth').title);
 assert.throws(()=>search.execute({query:42}));assert.throws(()=>open.execute({id:'missing'}));
});
check('报错库数量、模块、版本和结构完整',()=>{
 const errors=data.entries.filter(e=>e.kind==='报错');assert.equal(errors.length,72);
 for(const m of data.modules.filter(m=>m.id!=='embodied'))assert.equal(errors.filter(e=>e.module===m.id).length,12);
 assert.equal(errors.filter(e=>e.module==='embodied').length,0);
 assert.equal(errors.filter(e=>e.module==='ros'&&e.version==='ROS 1 Noetic').length,4);
 for(const e of errors){const t=e.troubleshooting;assert(t.patterns.length);assert(t.fixes.length>=2,e.id);assert(t.diagnosis.every(d=>d.normal&&d.abnormal&&d.reason&&d.code));assert(t.verification.code&&t.verification.expected);}
 route('#errors?module=isaac');assert.equal(main().querySelectorAll('.result-card').length,12);
 route('#errors?module=ros&version='+encodeURIComponent('ROS 1 Noetic'));assert.equal(main().querySelectorAll('.result-card').length,4);
});
check('多行日志容忍时间戳和临时路径，日志不进入地址或存储',()=>{
 route('#errors');const input=main().querySelector('#error-log');
 input.value='2026-09-21T08:42:10 [ERROR] /tmp/run-5934/a.py:3\nModuleNotFoundError: No module named "mujoco"';
 input.dispatchEvent(new dom.Event('input',{bubbles:true}));main().querySelector('#error-form').dispatchEvent(new dom.Event('submit',{bubbles:true,cancelable:true}));
 assert.equal(main().querySelector('.card-title').getAttribute('href'),'#article/mujoco-error-import');
 assert(!location.hash.includes('ModuleNotFoundError'));assert(![...local.values()].some(v=>v.includes('/tmp/run-5934')));
 route('#errors?module=mujoco');assert(main().querySelector('#error-log').value.includes('ModuleNotFoundError'));
 click(main().querySelector('[data-action="clear-log"]'));assert.equal(main().querySelectorAll('.result-card').length,12);
 click(main().querySelector('[data-action="sample-log"]'));assert.equal(main().querySelector('.card-title').getAttribute('href'),'#article/ros-error-qos');
 click(main().querySelector('[data-action="clear-log"]'));
 route('#errors?q=unlisted_failure_zx919');assert(main().textContent.includes('没有找到已收录的错误特征'));
});
check('新条目参与搜索、收藏与历史，故障案例关联实战',()=>{
 route('#search?kind='+encodeURIComponent('报错')+'&q=GH006');assert(main().querySelector('[href="#article/github-error-protected"]'));
 route('#article/gazebo-error-sensor');assert(main().querySelector('#diagnosis'));assert(main().querySelector('[href="#article/gazebo-diffdrive-project"]'));
 click(main().querySelector('[data-action="save"]'));route('#saved');assert(main().querySelector('[href="#article/gazebo-error-sensor"]'));
 assert(local.get('yanzhi-recent').includes('gazebo-error-sensor'));
 click(main().querySelector('[data-action="save"]'));
});
check('完整实战数量、下载路径与同源文件展示',()=>{
 const projects=data.entries.filter(e=>e.project);assert.equal(projects.length,12);
 route('#practice');assert.equal(main().querySelectorAll('.practice-card').length,12);
 route('#practice?module=ros');assert.equal(main().querySelectorAll('.practice-card').length,2);
 for(const e of projects){
  assert(fs.existsSync(path.join(root,'dist',e.project.download)));
  route('#article/'+e.id);assert.equal(main().querySelectorAll('.project-files details').length,e.project.files.length);
  for(const f of e.project.files)assert.equal(f.content,fs.readFileSync(path.join(root,'projects',e.project.directory,f.path),'utf8'));
  const button=main().querySelector('.project-files [data-action="copy-block"]');click(button);assert(document.querySelector('#toast').textContent.includes('已复制'));
 }
 route('#search?q='+encodeURIComponent('aggregate.json'));assert(main().querySelector('[href="#article/linux-sweep"]'));
});
check('章节覆盖状态、筛选、原文章名与父子引用',()=>{
 const chapters=data.coverage.chapters;const ids=new Set(chapters.map(c=>c.id));
 for(const c of chapters){assert(/[\u4e00-\u9fff]/.test(c.title),c.title);assert(c.originalTitle&&c.version&&c.url&&c.checked);assert.equal(Boolean(c.entries.length),c.status!=='missing');if(c.parent)assert(ids.has(c.parent));for(const id of c.entries)assert(data.entries.some(e=>e.id===id));}
 route('#coverage?module=ros&status=missing');assert.equal(main().querySelectorAll('.chapter-row').length,chapters.filter(c=>c.module==='ros'&&c.status==='missing').length);
 route('#coverage?book=mujoco-nav&q='+encodeURIComponent('Fluid forces'));assert.equal(main().querySelectorAll('.chapter-row').length,1);
 route('#coverage?book=ros1');assert(main().textContent.includes('待核对'));
});
check('日志与工程文件输出保持转义，无远程运行请求',()=>{
 route('#errors');const input=main().querySelector('#error-log');input.value='<img src=x onerror=alert(1)> incompatible QoS';input.dispatchEvent(new dom.Event('input',{bubbles:true}));
 main().querySelector('#error-form').dispatchEvent(new dom.Event('submit',{bubbles:true,cancelable:true}));assert.equal(main().querySelectorAll('img').length,0);
 route('#article/mujoco-arm-project');assert.equal(main().querySelectorAll('mujoco').length,0);
 assert(!/\b(fetch|XMLHttpRequest|WebSocket)\s*\(/.test(source));
});
check('96 项技能、12 类与专用无代码正文',()=>{
 const skills=data.entries.filter(e=>e.kind==='技能');assert.equal(skills.length,96);
 const categories=[...new Set(skills.map(e=>e.category))];assert.equal(categories.length,12);
 for(const category of categories){
  assert.equal(skills.filter(e=>e.category===category).length,8);
  route('#module/embodied?category='+encodeURIComponent(category)+'&kind='+encodeURIComponent('技能'));
  assert.equal(main().querySelectorAll('.result-card').length,8);
 }
 for(const e of skills){
  route('#article/'+e.id);assert.equal(main().querySelector('.english-title').textContent,e.englishTitle);
  assert.equal(main().querySelectorAll('.skill-section').length,6);
  assert.equal(main().querySelectorAll('.source-link').length,e.sources.length);
  for(const section of ['use','principle','prerequisites','parameters','tools','pitfalls','source'])assert(main().querySelector('#'+section).textContent.length>10);
  assert(main().textContent.includes('不代表已经完成实验验证'));
  for(const ref of e.sources){assert(main().querySelector('.source-link[href="'+data.sources[ref.key][1]+'"]'));assert(main().textContent.includes(ref.version));}
  for(const ref of e.related)assert(main().querySelector('[href="#article/'+ref+'"]'));
 }
});
check('技能中文、缩写、工具与多来源全文检索',()=>{
 for(const [q,id] of [['具身智能','embodied-frames'],['embodied','embodied-frames'],['IL','embodied-bc'],['RL','embodied-mdp-pomdp'],['BC','embodied-bc'],['ACT','embodied-act'],['VLA','embodied-vla-interface'],['手眼标定','embodied-hand-eye'],['SLERP','embodied-quaternion'],['projectPoints','embodied-calibration-validation'],['Hu et al.','embodied-lora']]){
  route('#search?q='+encodeURIComponent(q)+'&kind='+encodeURIComponent('技能'));
  assert(main().querySelector('[href="#article/'+id+'"]'),q);
 }
 route('#search?q='+encodeURIComponent('OpenCV 手眼')+'&kind='+encodeURIComponent('技能'));
 assert(main().querySelector('[href="#article/embodied-hand-eye"]'));
 route('#search?kind='+encodeURIComponent('技能'));assert(main().querySelector('.results-count').textContent.includes('96'));
 assert(main().querySelector('option[value="技能"]'));
});
check('技能分页、难度筛选与控件事件',()=>{
 route('#module/embodied');assert(main().textContent.includes('第 1 / 8 页'));
 const first=[...main().querySelectorAll('.card-title')].map(a=>a.getAttribute('href'));
 const next=main().querySelector('.pagination a');assert(next.getAttribute('href').includes('page=2'));
 route(next.getAttribute('href'));assert(main().textContent.includes('第 2 / 8 页'));
 for(const a of main().querySelectorAll('.card-title'))assert(!first.includes(a.getAttribute('href')));
 for(const level of ['基础','进阶']){
  route('#module/embodied?level='+encodeURIComponent(level));
  const count=data.entries.filter(e=>e.module==='embodied'&&e.level===level).length;
  assert(main().querySelector('.results-count').textContent.includes(String(count)));
  for(const card of main().querySelectorAll('.result-card'))assert(card.textContent.includes(level));
 }
 route('#search');const select=main().querySelector('[data-filter="kind"]');
 for(const option of select.querySelectorAll('option'))option.removeAttribute('selected');
 select.querySelector('[value="技能"]').setAttribute('selected','');select.dispatchEvent(new dom.Event('change',{bubbles:true}));
 assert(main().querySelector('.results-count').textContent.includes('96'));
});
check('新旧收藏共存、最近阅读与技能深链接',()=>{
 for(const id of ['ros-tf2','embodied-act']){route('#article/'+id);click(main().querySelector('[data-action="save"]'));}
 route('#saved');assert.equal(main().querySelectorAll('.result-card').length,2);
 route('#saved?kind='+encodeURIComponent('技能'));assert.equal(main().querySelectorAll('.result-card').length,1);
 assert(main().querySelector('[href="#article/embodied-act"]'));assert(local.get('yanzhi-recent').includes('embodied-act'));
 route('#home');assert(main().querySelector('.recent-links [href="#article/embodied-act"]'));
 for(const id of ['ros-tf2','embodied-act']){route('#article/'+id);click(main().querySelector('[data-action="save"]'));}
 assert.equal(local.get('yanzhi-favorites'),'[]');
});
check('覆盖与实战独立计数，技能全文不引入网络依赖',()=>{
 assert.equal(data.coverage.chapters.length,797);assert(!data.coverage.chapters.some(c=>c.module==='embodied'));
 route('#coverage?module=embodied');assert(main().textContent.includes('不计入这 797 条'));assert.equal(main().querySelectorAll('.chapter-row').length,0);
 route('#practice');assert(main().textContent.includes('原有六个工具模块'));assert.equal(main().querySelectorAll('.practice-card').length,12);
 for(const match of html.matchAll(/(?:src|href)="([^"]+)"/g))assert(!/^https?:/.test(match[1]));
 assert(!/\b(fetch|XMLHttpRequest|WebSocket)\s*\(/.test(source));
 const css=fs.readFileSync(path.join(root,'dist/styles.css'),'utf8');assert(!/@import|url\(['"]?https?:/i.test(css));
 const open=registered.get('open_research_article');const result=open.execute({id:'embodied-act'});assert(result.tools&&result.prerequisites&&result.sources.length===2);
});
console.log(`\n${checks} 组行为检查通过；${data.entries.length} 篇文章可渲染。未执行浏览器视觉测试。`);
