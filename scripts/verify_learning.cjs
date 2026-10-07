/* 学习进度与故障存储回归；参数与 verify.cjs 相同。 */
const fs=require('node:fs'),path=require('node:path'),vm=require('node:vm'),assert=require('node:assert/strict');
const {parseHTML}=require(process.argv[2]||'linkedom');
const root=path.resolve(__dirname,'..'),K=JSON.parse(fs.readFileSync(path.join(root,'dist/knowledge.json'),'utf8'));
const source=fs.readFileSync(path.join(root,'dist/app.js'),'utf8'),html=fs.readFileSync(path.join(root,'dist/index.html'),'utf8');
const key='yanzhi-learning-progress-v1';
function boot(local=new Map(),blocked=false,initial='#learn'){
 const {document,window:dom}=parseHTML(html),listeners=new Map();let hash=initial;
 const context={document,KNOWLEDGE:K,URL,URLSearchParams,console,AbortController,navigator:{},setTimeout:()=>1,clearTimeout:()=>{},scrollTo:()=>{},matchMedia:()=>({matches:true}),addEventListener:(n,f)=>listeners.set(n,f),localStorage:{getItem:k=>{if(blocked===true)throw Error('denied');return local.get(k)??null},setItem:(k,v)=>{if(blocked)throw Error('denied');local.set(k,v)}}};
 context.location={get hash(){return hash},set hash(v){hash=v;listeners.get('hashchange')?.()},get href(){return 'file:///index.html'+hash}};
 context.history={replaceState(_a,_b,v){hash=v}};context.window=context;vm.runInNewContext(source,context);
 const $=s=>document.querySelector(s),event=(s,type)=>$(s).dispatchEvent(new dom.Event(type,{bubbles:true,cancelable:true}));
 return {local,document,$,route:h=>context.location.hash=h,mark:(name,value)=>{const el=$(`[data-learning-mark="${name}"]`);el.checked=value;event(`[data-learning-mark="${name}"]`,'change')},choose:(i,j)=>{const sel=`[data-learning-question="${i}"][value="${j}"]`;$(sel).checked=true;event(sel,'change')},submit:()=>event('#learning-quiz','submit'),click:s=>event(s,'click'),text:()=>$('#main').textContent};
}
let checks=0;function check(name,fn){fn();checks++;console.log('PASS',name)}
const p=K.learningPaths[0],s=p.stages[0],route=(p,s)=>`#path/${p.id}?stage=${s.id}`;
check('四路线、16 阶段深链接与工程证据、提示和答案结构',()=>{
 const a=boot();assert.equal(a.document.querySelectorAll('.learning-card').length,4);
 a.route('#home');assert(a.$('.learning-home [href="#learn"]'));assert(a.$('[data-nav="learn"]'));
 for(const p of K.learningPaths)for(const s of p.stages){a.route(route(p,s));assert.equal(a.$('.learning-stage').dataset.stage,s.id);assert.equal(a.document.querySelectorAll('.stage-nav a').length,4);assert.equal(a.document.querySelectorAll('#learning-quiz fieldset').length,3);assert.equal(a.document.querySelectorAll('.learning-hints details').length,s.exercise.hints.length+1);assert(a.text().includes('个人自记'));for(const id of s.exercise.projects)assert(a.text().includes(K.entries.find(e=>e.id===id).project.verification.evidence));}
 a.route('#path/missing');assert(a.text().includes('没有找到'));a.route('#path/'+p.id+'?stage=missing');assert(a.text().includes('未找到指定阶段'));
});
check('未答不能提交、错题解释、修改撤销通过、重新作答保留勾选',()=>{
 const a=boot();a.route(route(p,s));a.submit();assert(a.text().includes('请先完成全部三题'));
 a.mark('read',true);a.mark('exercise',true);s.quiz.forEach((q,i)=>a.choose(i,(q.answer+1)%3));a.submit();assert(a.text().includes('0 / 3 正确'));assert.equal(a.document.querySelectorAll('.quiz-feedback a').length,3);assert(a.text().includes('已完成 0 / 4'));
 s.quiz.forEach((q,i)=>a.choose(i,q.answer));a.submit();assert(a.text().includes('自测已通过'));assert(a.text().includes('已完成 1 / 4'));a.choose(0,(s.quiz[0].answer+1)%3);assert(a.text().includes('已完成 0 / 4'));assert.equal(a.$('.quiz-feedback').textContent,'');
 a.click('[data-action="learning-reset"]');assert(a.$('[data-learning-mark="read"]').checked);assert(a.$('[data-learning-mark="exercise"]').checked);assert(JSON.parse(a.local.get(key)).stages[p.id+'/'+s.id].answers.every(x=>x===null));
});
check('草稿答案、通过结果和勾选刷新保留，文章阅读不自动完成',()=>{
 const local=new Map([['yanzhi-favorites','["ros-tf2"]']]);let a=boot(local);a.route(route(p,s));a.choose(0,s.quiz[0].answer);a=boot(local,false,route(p,s));assert(a.$(`[data-learning-question="0"][value="${s.quiz[0].answer}"]`).hasAttribute('checked'));
 a.route('#article/'+s.readings[0]);a.route(route(p,s));assert(!a.$('[data-learning-mark="read"]').hasAttribute('checked'));a.mark('read',true);a.mark('exercise',true);s.quiz.forEach((q,i)=>a.choose(i,q.answer));a.submit();a=boot(local,false,route(p,s));assert(a.text().includes('自测已通过'));assert(a.text().includes('已完成 1 / 4'));assert.equal(local.get('yanzhi-favorites'),'["ros-tf2"]');
 a.mark('exercise',false);assert(a.text().includes('已完成 0 / 4'));a=boot(local,false,route(p,s));assert(!a.$('[data-learning-mark="exercise"]').hasAttribute('checked'));
});
check('全部完成后复习入口、取消与继续学习定位首个未完成阶段',()=>{
 const a=boot();for(const p of K.learningPaths){for(const s of p.stages){a.route(route(p,s));a.mark('read',true);a.mark('exercise',true);s.quiz.forEach((q,i)=>a.choose(i,q.answer));a.submit();}assert.equal(a.$('.page-heading .button').textContent,'复习路线');}
 a.route('#learn');assert.equal([...a.document.querySelectorAll('.learning-card .button')].filter(x=>x.textContent.includes('复习路线')).length,4);
 const stage=p.stages[2];a.route(route(p,stage));a.mark('read',false);assert.equal(a.$('.page-heading .button').getAttribute('href'),route(p,stage));a.route('#learn');assert.equal(a.$('.learning-card .button').getAttribute('href'),route(p,stage));
});
check('损坏 JSON、错误结构、越界答案与伪造通过不会导致崩溃或误完成',()=>{
 for(const raw of ['{bad','null','[]','{"version":2,"stages":{}}']){const a=boot(new Map([[key,raw]]));assert(a.text().includes('无法读取学习记录'));assert.equal(a.document.querySelectorAll('.learning-card').length,4);}
 const stages={};stages[p.id+'/'+s.id]={read:true,exercise:true,answers:[999,0,0],submitted:true};stages[p.id+'/'+p.stages[1].id]={read:true,exercise:false,answers:[null,null,null],submitted:false};const a=boot(new Map([[key,JSON.stringify({version:1,stages})]]));assert(a.text().includes('部分学习记录损坏'));a.route(route(p,p.stages[1]));assert(a.$('[data-learning-mark="read"]').hasAttribute('checked'));
 const b=boot(new Map([[key,JSON.stringify({version:1,stages:{[p.id+'/'+s.id]:{read:true,exercise:true,answers:[null,null,null],submitted:true,passed:true}}})]]),false,route(p,s));assert(b.text().includes('已完成 0 / 4'));
});
check('读写存储均被禁用时保留会话进度并持续提示',()=>{
 const a=boot(new Map(),true,route(p,s));assert(a.text().includes('当前会话内仍可使用'));a.mark('read',true);a.mark('exercise',true);s.quiz.forEach((q,i)=>a.choose(i,q.answer));a.submit();a.route('#learn');assert(a.text().includes('已完成 1 / 4'));a.route(route(p,s));assert(a.text().includes('自测已通过'));assert(a.text().includes('浏览器未允许持久保存'));
});
check('仅读取成功而写入失败时同样保留会话答案',()=>{
 const a=boot(new Map(),'write');assert(a.text().includes('浏览器未允许持久保存')); a.route(route(p,s));a.mark('read',true);a.mark('exercise',true);s.quiz.forEach((q,i)=>a.choose(i,q.answer));a.submit();a.route('#learn');assert(a.text().includes('已完成 1 / 4'));a.route(route(p,s));a.click('[data-action="learning-reset"]');assert(a.text().includes('已完成 0 / 4'));
});
console.log(`${checks} 组学习行为检查通过`);
