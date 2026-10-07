/* 本地静态应用：不依赖 CDN、远程接口或浏览器模块加载。 */
(() => {
  'use strict';
  const K = window.KNOWLEDGE;
  const $ = s => document.querySelector(s);
  const esc = v => String(v ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const paths = {
    branch:'M6 3v12a4 4 0 0 0 4 4h2M6 8h8a4 4 0 0 0 4-4M8 3a2 2 0 1 1-4 0 2 2 0 0 1 4 0M20 3a2 2 0 1 1-4 0 2 2 0 0 1 4 0M16 19a2 2 0 1 1-4 0 2 2 0 0 1 4 0', terminal:'m4 6 6 6-6 6M13 18h7', book:'M4 4h6a3 3 0 0 1 3 3v14a4 4 0 0 0-4-2H4zM13 7a3 3 0 0 1 3-3h5v15h-4a4 4 0 0 0-4 2',
    box:'m12 3 9 5v9l-9 5-9-5V8zM3 8l9 5 9-5M12 13v9M7.5 5.5l9 5',
    layers:'m12 3 10 6-10 6L2 9zM2 13l10 6 10-6M2 17l10 6 10-6',
    network:'M9 3h6v6H9zM2 16h6v6H2zM16 16h6v6h-6zM12 9v4M5 16v-3h14v3',
    cpu:'M6 6h12v12H6zM9 9h6v6H9zM9 2v4M15 2v4M9 18v4M15 18v4M2 9h4M2 15h4M18 9h4M18 15h4',
    search:'M21 21l-5-5M18 10a8 8 0 1 1-16 0 8 8 0 0 1 16 0',
    star:'m12 3 2.8 5.7 6.2.9-4.5 4.4 1.1 6.2-5.6-3-5.6 3 1.1-6.2L3 9.6l6.2-.9z',
    arrow:'M5 12h14M14 7l5 5-5 5', chevron:'m9 5 7 7-7 7', link:'M14 3h7v7M21 3l-10 10M10 3H4v17h17v-6',
    check:'m5 12 4 4L19 6', copy:'M8 8h13v13H8zM16 4V2H2v14h2', menu:'M3 6h18M3 12h18M3 18h18',
    clock:'M12 7v5l4 2M22 12a10 10 0 1 1-20 0 10 10 0 0 1 20 0', info:'M12 11v6M12 7h.01M22 12a10 10 0 1 1-20 0 10 10 0 0 1 20 0',
    close:'m6 6 12 12M6 18 18 6', grid:'M3 3h7v7H3zM14 3h7v7h-7zM3 14h7v7H3zM14 14h7v7h-7z', down:'m6 9 6 6 6-6'
  };
  const icon = (name, cls='') => `<svg class="icon ${cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="${paths[name] || paths.book}"/></svg>`;
  const moduleById = id => K.modules.find(m=>m.id===id);
  const articleById = id => K.entries.find(e=>e.id===id);
  const storage = {get(key, fallback){try{const value=JSON.parse(localStorage.getItem('yanzhi-'+key));return Array.isArray(value)?value:fallback;}catch{return fallback;}},set(key,value){try{localStorage.setItem('yanzhi-'+key,JSON.stringify(value));return true;}catch{return false;}}};
  let favorites = new Set(storage.get('favorites',[]).filter(articleById));
  let recent = storage.get('recent',[]).filter(articleById).slice(0,8);
  let state, toastTimer, searchTimer, errorLog='';
  const searchText = new Map(K.entries.map(e=>[e.id, [e.title,e.englishTitle||'',...(e.keywords||[]),e.tools||'',...(e.sources||[]).flatMap(r=>[...(K.sources[r.key]||[]),r.version,r.checked]),e.category,e.summary,e.principle,e.code,...e.explain,e.pitfall,e.version,e.prerequisites||moduleById(e.module).prerequisites,...(e.sections||[]).flatMap(s=>[s.title,s.body,s.code||'']),moduleById(e.module).name,moduleById(e.module).subtitle,JSON.stringify(e.troubleshooting||{}),...(e.project?.files||[]).flatMap(f=>[f.path,f.content])].join(' ').normalize('NFKC').toLowerCase()]));
  const aliases = {il:'imitation learning',rl:'reinforcement learning',bc:'behavior cloning',act:'action chunking with transformers',vla:'vision language action',mujoko:'mujoco',mujoco:'mujoco',issac:'isaac',issaclab:'isaac',isaaclab:'isaac',ros1:'ros 1',ros2:'ros 2','强化学习':'强化学习',gazebo11:'classic'};
  function terms(q){return q.normalize('NFKC').toLowerCase().trim().split(/\s+/).filter(Boolean).map(t=>aliases[t]||t);}
  function queryEntries(options={}){
    const tt=terms(options.q||'');
    return K.entries.filter(e=>(!options.module||e.module===options.module)&&(!options.category||e.category===options.category)&&(!options.kind||e.kind===options.kind)&&(!options.level||e.level===options.level)&&(!options.version||e.version===options.version)&&(!options.saved||favorites.has(e.id))&&tt.every(t=>searchText.get(e.id).includes(t)))
      .map(e=>({e,score:tt.reduce((s,t)=>s+(e.title.toLowerCase().includes(t)?20:0)+(e.category.toLowerCase().includes(t)?5:0),0)})).sort((a,b)=>b.score-a.score).map(x=>x.e);
  }
  function parse(){
    const [path,qs=''] = location.hash.slice(1).split('?');
    const [view='home',id=''] = path.split('/');
    const p = new URLSearchParams(qs);
    return {view:view||'home',id,q:p.get('q')||'',module:view==='module'?id:p.get('module')||'',category:p.get('category')||'',kind:p.get('kind')||'',level:p.get('level')||'',version:p.get('version')||'',status:p.get('status')||'',book:p.get('book')||'',page:Math.max(1,Math.floor(Number(p.get('page')))||1)};
  }
  function url(view='search',options={}){
    const p = new URLSearchParams();
    for(const key of ['q','module','category','kind','level','version','status','book','page']) if(options[key] && !(key==='module'&&view.startsWith('module/'))) p.set(key,options[key]);
    return '#'+view+(p.size?'?'+p.toString():'');
  }
  function go(hash){if(location.hash===hash) render();else location.hash=hash;}
  function toast(message){clearTimeout(toastTimer);$('#toast').textContent=message;$('#toast').classList.add('show');toastTimer=setTimeout(()=>$('#toast').classList.remove('show'),2600);}
  function shell(){
    $('#app').innerHTML=`<div class="shade" data-action="menu" aria-hidden="true"></div><aside class="sidebar" aria-label="主导航">
      <a class="brand" href="#home"><span class="brand-symbol">${icon('terminal')}</span><span>研知<span class="brand-sub">机器人科研手册</span></span></a>
      <div class="nav-section">我的知识库</div><nav><a class="nav-link" data-nav="home" href="#home">${icon('grid')}<span>知识库总览</span></a><a class="nav-link" data-nav="saved" href="#saved">${icon('star')}<span>我的收藏</span><span class="count" id="saved-count">${favorites.size}</span></a></nav>
      <div class="nav-section nav-section-mod">研究模块 <span>${String(K.modules.length).padStart(2,'0')}</span></div><nav class="module-nav">${K.modules.map(m=>`<a class="nav-link" data-nav="${m.id}" href="#module/${m.id}">${icon(m.icon)}<span>${esc(m.name)}${m.id==='embodied'?'<small class="nav-subtitle">具身智能科研技能</small>':''}</span><span class="count">${m.count}</span></a>`).join('')}</nav>
      <div class="nav-section">科研工作台</div><nav class="workbench-nav"><a class="nav-link" data-nav="learn" href="#learn">${icon('book')}<span>学习路线</span><span class="count">4</span></a><a class="nav-link" data-nav="errors" href="#errors">${icon('info')}<span>报错库</span><span class="count">72</span></a><a class="nav-link" data-nav="practice" href="#practice">${icon('terminal')}<span>完整实战</span><span class="count">12</span></a></nav><div class="nav-section">参考资料</div><nav><a class="nav-link" data-nav="coverage" href="#coverage">${icon('book')}<span>官方章节覆盖表</span></a><a class="nav-link" data-nav="sources" href="#sources">${icon('link')}<span>官方文档索引</span></a></nav>
      <div class="sidebar-bottom"><div class="local-label">${icon('check')} 离线内容已就绪</div><p>本地阅读 · 无需登录</p><span>内容基线 · ${K.updated}</span></div>
    </aside><div class="workspace"><header class="topbar"><button class="icon-btn mobile-menu" data-action="menu" aria-label="展开导航">${icon('menu')}</button><form id="search-form" role="search"><label for="global-search" class="sr-only">搜索全部中文内容</label>${icon('search')}<input id="global-search" autocomplete="off" placeholder="搜索命令、功能或问题，例如：话题、接触力、显存…"><button type="button" class="search-clear" data-action="clear-search" aria-label="清空搜索">${icon('close')}</button><kbd>Ctrl K</kbd></form><span class="topbar-label">中文科研知识库</span></header><main id="main" tabindex="-1"></main><footer class="footer">研知 · 本地科研参考 <span>中文讲解与示例可离线阅读 · 官方链接需联网</span></footer></div><div id="toast" class="toast" role="status" aria-live="polite"></div>`;
    $('#search-form').addEventListener('submit',e=>{e.preventDefault();go(url('search',{q:$('#global-search').value.trim()}));});
    $('#global-search').addEventListener('input',e=>{clearTimeout(searchTimer);const q=e.target.value;searchTimer=setTimeout(()=>{const h=url('search',{q});history.replaceState(null,'',h);state=parse();renderContent();window.scrollTo(0,0);},140);});
    document.addEventListener('click',click);
    document.addEventListener('input',e=>{if(e.target.id==='error-log')errorLog=e.target.value;});
    document.addEventListener('submit',e=>{if(e.target.id==='error-form'){e.preventDefault();errorLog=$('#error-log').value;go(url('errors',{...state,q:'',page:1}));}if(e.target.id==='chapter-form'){e.preventDefault();go(url('coverage',{...state,q:$('#chapter-query').value,page:1}));}});
    document.addEventListener('change',e=>{if(e.target.matches('[data-filter]')){const next={...state,[e.target.dataset.filter]:e.target.value,page:1};if(e.target.dataset.filter==='module'){next.category='';next.version='';next.book='';}go(url(['errors','practice','coverage','saved'].includes(state.view)?state.view:state.view==='module'?'module/'+state.module:'search',next));}});
    document.addEventListener('keydown',e=>{if((e.ctrlKey||e.metaKey)&&e.key.toLowerCase()==='k'){e.preventDefault();$('#global-search').focus();$('#global-search').select();}if(e.key==='/'&&!['INPUT','TEXTAREA','SELECT'].includes(document.activeElement.tagName)){e.preventDefault();$('#global-search').focus();}if(e.key==='Escape'){document.body.classList.remove('menu-open');$('#global-search').blur();}});
    window.addEventListener('hashchange',()=>{clearTimeout(searchTimer);render();window.scrollTo(0,0);document.body.classList.remove('menu-open');});
  }
  function tag(text,cls=''){return `<span class="tag ${cls}">${esc(text)}</span>`;}
  function favoriteButton(e,full=false){return `<button class="${full?'button':'icon-btn save-button'} ${favorites.has(e.id)?'is-saved':''}" data-action="save" data-id="${e.id}" aria-pressed="${favorites.has(e.id)}" aria-label="${favorites.has(e.id)?'取消收藏':'收藏'} ${esc(e.title)}">${icon('star')}${full?`<span>${favorites.has(e.id)?'已收藏':'收藏词条'}</span>`:''}</button>`;}
  function card(e){const m=moduleById(e.module);return `<article class="result-card"><div class="card-meta"><span class="module-dot ${m.color}"></span>${esc(m.name)}<span class="separator">/</span>${esc(e.category)}${favoriteButton(e)}</div><a class="card-title" href="#article/${e.id}">${esc(e.title)}${icon('arrow')}</a><p>${esc(e.summary)}</p><div class="card-bottom">${tag(e.kind)}${tag(e.level)}${e.project?tag(e.project.verification.status,'accent'):''}<span>${esc(e.version)}</span></div></article>`;}
  function heading(eyebrow,title,description,extra=''){return `<div class="page-heading"><div><div class="eyebrow">${eyebrow}</div><h1>${title}</h1>${description?`<p>${description}</p>`:''}</div>${extra}</div>`;}
  const learningKey='yanzhi-learning-progress-v1';
  const learningPaths=K.learningPaths;
  const learningPath=id=>learningPaths.find(p=>p.id===id);
  const stageKey=(p,s)=>p.id+'/'+s.id;
  const blankProgress=()=>({read:false,exercise:false,answers:[null,null,null],submitted:false});
  let learningNotice='',learningSessionOnly=false;
  const learningProgress=loadLearning();
  function loadLearning(){
    const clean={};
    try{
      const raw=localStorage.getItem(learningKey);
      if(raw!==null){
        const saved=JSON.parse(raw);
        if(!saved||saved.version!==1||!saved.stages||typeof saved.stages!=='object'||Array.isArray(saved.stages))throw new Error('invalid');
        for(const p of learningPaths)for(const s of p.stages){
          const key=stageKey(p,s),v=saved.stages[key];if(v===undefined)continue;
          if(!v||typeof v.read!=='boolean'||typeof v.exercise!=='boolean'||typeof v.submitted!=='boolean'||!Array.isArray(v.answers)||v.answers.length!==3||!v.answers.every((a,i)=>a===null||Number.isInteger(a)&&a>=0&&a<s.quiz[i].options.length)){
            learningNotice='部分学习记录损坏，已重置异常阶段；其他有效记录仍保留。';continue;
          }
          clean[key]={read:v.read,exercise:v.exercise,answers:[...v.answers],submitted:v.submitted&&v.answers.every(a=>a!==null)};
        }
      }
    }catch{learningNotice='无法读取学习记录，已从空进度开始；当前会话仍可学习。';}
    try{localStorage.setItem(learningKey,JSON.stringify({version:1,stages:clean}));}
    catch{learningSessionOnly=true;}
    return clean;
  }
  function progressFor(p,s){return learningProgress[stageKey(p,s)]||blankProgress();}
  function quizScore(s,v){return s.quiz.filter((q,i)=>q.answer===v.answers[i]).length;}
  function quizPassed(s,v){return v.submitted&&quizScore(s,v)===3;}
  function stageComplete(p,s){const v=progressFor(p,s);return v.read&&v.exercise&&quizPassed(s,v);}
  function pathCompleted(p){return p.stages.filter(s=>stageComplete(p,s)).length;}
  function stageUrl(p,s){return '#path/'+p.id+'?stage='+s.id;}
  function continueUrl(p){return stageUrl(p,p.stages.find(s=>!stageComplete(p,s))||p.stages[0]);}
  function learningWarning(){return `<div class="learning-storage" role="status">${learningSessionOnly?'浏览器未允许持久保存学习记录；当前会话内仍可使用，关闭或刷新页面后可能丢失。':esc(learningNotice)}</div>`;}
  function saveLearning(){
    try{localStorage.setItem(learningKey,JSON.stringify({version:1,stages:learningProgress}));}
    catch{learningSessionOnly=true;}
    const notice=$('.learning-storage');if(notice)notice.outerHTML=learningWarning();
  }
  function localArticle(id){return `<a href="#article/${id}">${esc(articleById(id).title)}</a>`;}
  function learningOverview(){
    return heading('循序学习 / 阅读 · 练习 · 自测','学习路线','4 条路线 · 16 个阶段 · 16 项练习 · 48 道自测题。可自由跳转，按自己的节奏完成。')+learningWarning()+`<div class="learning-note">阶段完成 = 已阅读 + 练习已完成（个人自记）+ 自测三题全对。记录仅保存在当前浏览器；打开文章不会自动完成阶段。<br>内容可离线阅读，运行工程需事先准备对应软件与依赖。</div><div class="learning-grid">${learningPaths.map((p,i)=>{const count=pathCompleted(p);return `<article class="learning-card"><div class="eyebrow">路线 0${i+1} · 4 个阶段</div><h2><a href="#path/${p.id}">${esc(p.title)}</a></h2><p>${esc(p.description)}</p><p class="learning-audience">适合：${esc(p.audience)}</p><ol>${p.stages.map(s=>`<li><a href="${stageUrl(p,s)}">${esc(s.title)}</a><span>${stageComplete(p,s)?'已完成':'待完成'}</span></li>`).join('')}</ol><label class="learning-meter">已完成 ${count} / 4 阶段<progress value="${count}" max="4">${count}/4</progress></label><a class="button primary" href="${continueUrl(p)}">${count===4?'复习路线':'继续学习'} ${icon('arrow')}</a></article>`;}).join('')}</div>`;
  }
  function learningRoute(){
    const p=learningPath(state.id);if(!p)return empty('没有找到这条学习路线','请从学习路线总览选择已有路线。')+'<a class="button" href="#learn">学习路线总览</a>';
    const requested=new URLSearchParams(location.hash.split('?')[1]||'').get('stage');
    const s=p.stages.find(s=>s.id===requested)||p.stages[0],index=p.stages.indexOf(s),v=progressFor(p,s),ex=s.exercise;
    return `<div class="breadcrumb"><a href="#learn">学习路线</a>${icon('chevron')}<span>${esc(p.title)}</span></div>`+heading('路线 / '+esc(p.audience),esc(p.title),esc(p.description),`<a class="button" href="${continueUrl(p)}">${pathCompleted(p)===4?'复习路线':'继续学习'}</a>`)+learningWarning()+`<p class="learning-path-progress" aria-live="polite">已完成 ${pathCompleted(p)} / 4 阶段 · 可自由跳转，不锁课</p><nav class="stage-nav" aria-label="学习阶段">${p.stages.map((x,i)=>`<a href="${stageUrl(p,x)}" ${x===s?'aria-current="step"':''}><small>阶段 ${i+1} · ${esc(x.level)}</small><strong>${esc(x.title)}</strong><span data-stage-status="${x.id}">${stageComplete(p,x)?'已完成':'待完成'}</span></a>`).join('')}</nav>${requested&&requested!==s.id?'<p role="status">未找到指定阶段，已显示第一阶段。</p>':''}<article class="learning-stage" data-stage="${s.id}"><header><div class="eyebrow">阶段 ${index+1} / 4 · ${esc(s.level)}</div><h2>${esc(s.title)}</h2><p>${esc(s.goal)}</p></header><dl class="stage-context"><dt>前置知识</dt><dd>${esc(s.prerequisites)}</dd><dt>环境要求</dt><dd>${esc(s.environment)}</dd><dt>建议先学</dt><dd>${s.suggested.length?s.suggested.map(ref=>{const pp=learningPath(ref.path),ss=pp.stages.find(x=>x.id===ref.stage);return `<a href="${stageUrl(pp,ss)}">${esc(pp.title)} · ${esc(ss.title)}</a>`;}).join('、'):'可直接开始'}</dd></dl><section><h3>01 · 按顺序阅读</h3><ol class="learning-readings">${s.readings.map(id=>`<li>${localArticle(id)}</li>`).join('')}</ol><label class="progress-check"><input type="checkbox" data-learning-mark="read" ${v.read?'checked':''}> 已阅读本阶段文章（个人自记）</label></section><section><h3>02 · 练习</h3><p class="exercise-task">${esc(ex.task)}</p>${ex.projects.length?`<div class="learning-projects"><h4>配套工程与已有验证证据</h4>${ex.projects.map(id=>{const e=articleById(id),pr=e.project;return `<div>${localArticle(id)} <a class="button" href="${esc(pr.download)}" download>下载 ZIP</a><p><strong>${esc(pr.verification.status)}</strong> · ${esc(pr.verification.date)}<br>${esc(pr.verification.environment)}<br>${esc(pr.verification.evidence)}</p></div>`;}).join('')}<p>以上为工程已有验证记录，与您的练习勾选分别保存。本阶段的扩展任务不自动继承工程验证结论。</p></div>`:'<p class="learning-note">本阶段为数据、接口或实验方案练习，无配套训练工程。完成分析不代表完成模型训练或真机验证。</p>'}<h4>操作步骤</h4><ol class="explain-list">${ex.steps.map(x=>`<li>${esc(x)}</li>`).join('')}</ol><div class="acceptance"><strong>预期结果</strong><p>${esc(ex.expected)}</p></div><h4>验收清单</h4><ul class="acceptance-list">${ex.checklist.map(x=>`<li>${esc(x)}</li>`).join('')}</ul><div class="learning-hints">${ex.hints.map((x,i)=>`<details><summary>提示 ${i+1} · ${i?'进一步检查':'从这里开始'}</summary><p>${esc(x)}</p></details>`).join('')}<details><summary>参考解答 · 完成尝试后展开</summary><p>${esc(ex.solution)}</p></details></div><h4>相关排障</h4><ul>${ex.troubleshooting.map(id=>`<li>${localArticle(id)}</li>`).join('')}</ul><label class="progress-check"><input type="checkbox" data-learning-mark="exercise" ${v.exercise?'checked':''}> 练习已完成（个人自记）</label><p class="learning-note">仅在按本阶段验收完成后勾选，可随时取消。此标记不是网站对实验成功的验证。</p></section><section><h3>03 · 自测</h3><p>三题均为单选；全部答对才通过。答案选择也会保存在本地。</p><form id="learning-quiz">${s.quiz.map((q,i)=>`<fieldset><legend>${i+1}. ${esc(q.question)} <span class="tag">${esc(q.kind)}</span></legend>${q.options.map((x,j)=>`<label class="quiz-option"><input type="radio" name="quiz-${i}" value="${j}" data-learning-question="${i}" ${v.answers[i]===j?'checked':''} required> <span>${esc(x)}</span></label>`).join('')}<div class="quiz-feedback" data-feedback="${i}">${v.submitted?questionFeedback(q,v.answers[i]):''}</div></fieldset>`).join('')}<div class="learning-actions"><button class="button primary" type="submit">提交自测</button><button class="button" type="button" data-action="learning-reset">重新作答</button><span id="quiz-result" role="status">${quizResult(s,v)}</span></div></form></section><div class="learning-actions"><a class="button" href="#learn">路线总览</a>${index?`<a class="button" href="${stageUrl(p,p.stages[index-1])}">上一阶段</a>`:''}${index<3?`<a class="button" href="${stageUrl(p,p.stages[index+1])}">下一阶段 ${icon('arrow')}</a>`:''}</div></article>`;
  }
  function questionFeedback(q,answer){return `<p><strong>${answer===q.answer?'回答正确':'回答错误'} · 正确答案：${esc(q.options[q.answer])}</strong></p><p>${esc(q.explanation)} ${localArticle(q.reading)}</p>`;}
  function quizResult(s,v){return v.submitted?`${quizScore(s,v)} / 3 正确 · ${quizPassed(s,v)?'自测已通过':'尚未通过，可修改答案再提交'}`:'尚未提交';}
  function currentLearning(){const p=state.view==='path'&&learningPath(state.id),s=p?.stages.find(x=>x.id===$('.learning-stage')?.dataset.stage);return s?{p,s}:null;}
  function updateLearningStatus(p,s){
    $('.learning-path-progress').textContent=`已完成 ${pathCompleted(p)} / 4 阶段 · 可自由跳转，不锁课`;
    document.querySelectorAll('[data-stage-status]').forEach(el=>{const x=p.stages.find(x=>x.id===el.dataset.stageStatus);el.textContent=stageComplete(p,x)?'已完成':'待完成';});
    const next=$('.page-heading .button');next.href=continueUrl(p);next.textContent=pathCompleted(p)===4?'复习路线':'继续学习';
    const v=progressFor(p,s);$('#quiz-result').textContent=quizResult(s,v);
    document.querySelectorAll('[data-feedback]').forEach(el=>{const i=Number(el.dataset.feedback);el.innerHTML=v.submitted?questionFeedback(s.quiz[i],v.answers[i]):'';});
  }
  function learningChange(event){
    const el=event.target;if(!el.matches('[data-learning-mark], [data-learning-question]'))return;
    const current=currentLearning();if(!current)return;const {p,s}=current;
    const v=learningProgress[stageKey(p,s)]??=blankProgress();
    if(el.dataset.learningMark)v[el.dataset.learningMark]=el.checked;
    else{v.answers[Number(el.dataset.learningQuestion)]=Number(el.value);v.submitted=false;}
    saveLearning();updateLearningStatus(p,s);
  }
  function submitLearning(event){
    if(event.target.id!=='learning-quiz')return;event.preventDefault();
    const {p,s}=currentLearning(),v=learningProgress[stageKey(p,s)]??=blankProgress();
    if(v.answers.some(a=>a===null)){$('#quiz-result').textContent='请先完成全部三题再提交。';return;}
    v.submitted=true;saveLearning();updateLearningStatus(p,s);
  }
  function resetLearning(){
    const current=currentLearning();if(!current)return;const {p,s}=current,v=learningProgress[stageKey(p,s)]??=blankProgress();
    v.answers=[null,null,null];v.submitted=false;
    document.querySelectorAll('[data-learning-question]').forEach(el=>{el.checked=false;});
    saveLearning();updateLearningStatus(p,s);$('#learning-quiz input')?.focus();
  }

  function home(){
    const picks=['linux-find','mujoco-quickstart','gazebo-quickstart','ros-ros2-topic','isaac-train','github-research-release'].map(articleById).filter(Boolean);
    const tasks=[['搭建第一个仿真实验','最小仿真实验','box'],['查看机器人通信数据','话题','network'],['配置接触与碰撞','接触','layers'],['开始强化学习训练','训练','cpu'],['排查显存与运行性能','显存','terminal']];
    return heading('实验室 / 知识库','机器人科研手册','从第一条命令，到一场可复现的实验。',`<span class="date-badge">${icon('clock')} ${K.updated}</span>`)+
      `<div class="overview-stats"><span><strong>${K.entries.length}</strong> 篇中文词条</span><i></i><span><strong>${K.modules.length}</strong> 个研究模块</span><i></i><span>原理 · 示例 · 参数 · 排障</span><a href="#coverage">查看内容范围 ${icon('arrow')}</a></div>
      <div class="learning-home"><div><strong>学习路线与练习</strong><p>4 条路线 · 16 个阶段，从顺序阅读走向练习与自测</p></div><a class="button primary" href="#learn">开始学习 ${icon('arrow')}</a></div><div class="workbench-links"><a href="#errors">${icon('info')}<div><strong>报错库</strong><span>72 个案例 · 粘贴日志匹配</span></div>${icon('arrow')}</a><a href="#practice">${icon('terminal')}<div><strong>完整实战</strong><span>12 套工程 · 查看源码与下载</span></div>${icon('arrow')}</a><a href="#coverage">${icon('book')}<div><strong>官方章节覆盖表</strong><span>按版本核对已收录与空缺</span></div>${icon('arrow')}</a></div><section aria-labelledby="modules-heading"><div class="section-title"><h2 id="modules-heading">选择研究模块</h2><span>按工具与技能找到所需知识</span></div><div class="module-grid">${K.modules.map((m,i)=>`<a class="module-card ${m.color}" href="#module/${m.id}"><div class="module-card-top"><span class="module-icon">${icon(m.icon)}</span><span class="module-number">0${i+1}</span></div><h3>${esc(m.name)}</h3><p>${esc(m.subtitle)}</p><div class="module-card-bottom"><span>${m.count} 篇词条</span>${icon('arrow')}</div></a>`).join('')}</div></section>
      <div class="home-columns"><section><div class="section-title"><h2>常用参考</h2><a href="#search">全部词条 ${icon('arrow')}</a></div><div class="reference-list">${picks.map(e=>`<a class="reference-row" href="#article/${e.id}"><span class="row-icon ${moduleById(e.module).color}">${icon(moduleById(e.module).icon)}</span><div><strong>${esc(e.title)}</strong><p>${esc(e.summary)}</p></div>${icon('chevron')}</a>`).join('')}</div></section><section><div class="section-title"><h2>从研究任务出发</h2></div><div class="task-list">${tasks.map(([title,q,ic])=>`<a href="${url('search',{q})}">${icon(ic)}<span>${title}</span>${icon('arrow')}</a>`).join('')}</div><div class="research-note"><span class="note-kicker">读懂，再运行</span><h3>不止记住命令</h3><p>每篇词条都说明它为什么这样工作、参数改变什么，以及需要注意的边界。</p><a href="#coverage">了解版本与内容基线 ${icon('arrow')}</a></div></section></div>
      ${recent.length?`<section class="recent-section"><div class="section-title"><h2>最近阅读</h2><span>仅记录在当前浏览器</span></div><div class="recent-links">${recent.slice(0,4).map(id=>`<a href="#article/${id}">${icon('clock')}${esc(articleById(id).title)}</a>`).join('')}</div></section>`:''}`;
  }
  function select(label,key,values,value){return `<label class="filter-select"><span class="sr-only">${label}</span><select data-filter="${key}"><option value="">全部${label}</option>${values.map(v=>`<option value="${esc(typeof v==='string'?v:v.id)}" ${(typeof v==='string'?v:v.id)===value?'selected':''}>${esc(typeof v==='string'?v:v.name)}</option>`).join('')}</select>${icon('down')}</label>`;}
  function results(){
    const isModule=state.view==='module', isSaved=state.view==='saved', m=moduleById(state.module);
    if(isModule&&!m)return empty('没有这个研究模块','返回总览选择已有的模块。');
    const pool=K.entries.filter(e=>(!state.module||e.module===state.module)&&(!isSaved||favorites.has(e.id)));
    const cats=[...new Set(pool.map(e=>e.category))], versions=[...new Set(pool.map(e=>e.version))];
    const list=queryEntries({...state,saved:isSaved});
    const page=Math.min(state.page,Math.max(1,Math.ceil(list.length/12))), pages=Math.ceil(list.length/12);
    const currentView=isModule?'module/'+m.id:isSaved?'saved':'search';
    return (isModule?heading(`知识模块 / ${esc(m.subtitle)}`,esc(m.name),esc(m.description),`<span class="module-icon large ${m.color}">${icon(m.icon)}</span>`):heading(isSaved?'个人阅读 / 本地收藏':'知识库 / 全文检索',isSaved?'我的收藏':state.q?`搜索“${esc(state.q)}”`:'全部词条',isSaved?'把常用内容留在手边，收藏仅保存在当前浏览器。':'支持中文、命令名和代码检索；多个关键词按同时匹配搜索。'))+
      (isModule?`<div class="version-strip">${icon('info')}<span>${esc(m.version)}</span><a href="#coverage">版本说明 ${icon('arrow')}</a></div><div class="category-chips"><a class="chip ${!state.category?'selected':''}" href="${url(currentView,{...state,category:'',page:1})}">全部分类 <span>${pool.length}</span></a>${cats.map(c=>`<a class="chip ${state.category===c?'selected':''}" href="${url(currentView,{...state,category:c,page:1})}">${esc(c)} <span>${pool.filter(e=>e.category===c).length}</span></a>`).join('')}</div>`:'')+
      `<div class="results-toolbar"><span class="results-count">找到 <strong>${list.length}</strong> 篇词条</span><div class="filters">${!isModule?select('模块','module',K.modules,state.module)+select('分类','category',cats,state.category):''}${select('类型','kind',['命令','配置','指南','实战','报错','技能'],state.kind)}${select('难度','level',['基础','进阶'],state.level)}${versions.length>1?select('版本','version',versions,state.version):''}${[state.category,state.kind,state.level,state.version,state.q,(!isModule?state.module:'')].some(Boolean)?`<a class="reset-link" href="${url(currentView)}">重置筛选</a>`:''}</div></div>
      ${list.length?`<div class="results-grid">${list.slice((page-1)*12,page*12).map(card).join('')}</div>`:empty(isSaved&&!favorites.size?'还没有收藏的词条':'没有找到匹配内容',isSaved&&!favorites.size?'点击词条上的星标，即可在这里快速找到它。':'试试减少关键词，或重置分类、类型和版本筛选。')}
      ${pages>1?`<nav class="pagination" aria-label="结果分页">${page>1?`<a class="button" href="${url(currentView,{...state,page:page-1})}">上一页</a>`:'<span></span>'}<span>第 ${page} / ${pages} 页</span>${page<pages?`<a class="button" href="${url(currentView,{...state,page:page+1})}">下一页 ${icon('arrow')}</a>`:'<span></span>'}</nav>`:''}`;
  }
  function empty(title,body){return `<div class="empty-state">${icon('search')}<h2>${title}</h2><p>${body}</p><a class="button" href="#home">返回知识库</a></div>`;}
  function article(){
    const e=articleById(state.id); if(!e)return empty('没有找到这篇词条','链接可能已失效，请通过搜索或分类导航重新查找。');
    const m=moduleById(e.module);
    recent=[e.id,...recent.filter(id=>id!==e.id)].slice(0,8); storage.set('recent',recent);
    const related=e.related?.length?e.related.map(articleById).filter(Boolean):K.entries.filter(x=>x.id!==e.id&&x.module===e.module).sort((a,b)=>Number(b.category===e.category)-Number(a.category===e.category)).slice(0,3);
    const sections=e.kind==='技能'?[...skillSections,['source','深入阅读']]:[['use','适用场景'],['principle','执行原理'],['example','使用示例'],['parameters','参数与步骤'],['pitfalls','常见问题'],...(e.sections||[]).map((s,i)=>['extra-'+i,s.title]),...(e.troubleshooting?[['diagnosis','检查与修复']]:[]),...(e.project?[['project-files','完整工程文件']]:[]),['source','官方参考']];
    return `<div class="breadcrumb"><a href="#home">知识库</a>${icon('chevron')}<a href="#module/${m.id}">${esc(m.name)}</a>${icon('chevron')}<a href="${url('module/'+m.id,{category:e.category})}">${esc(e.category)}</a></div><div class="reading-layout"><article class="article-content"><div class="article-heading"><div class="article-badges">${tag(e.kind,'accent')}${tag(e.level)}<span>${esc(e.version)}</span></div><h1>${esc(e.title)}</h1>${e.englishTitle?`<p class="english-title">${esc(e.englishTitle)}</p>`:''}<p class="article-lead">${esc(e.summary)}</p><div class="article-actions">${favoriteButton(e,true)}<button class="button" data-action="copy-link" data-id="${e.id}">${icon('link')} 复制链接</button><span>${Math.max(2,Math.ceil((e.principle.length+(e.code||'').length+e.explain.join('').length+(e.tools||'').length+(e.prerequisites||'').length+(e.sections||[]).reduce((s,x)=>s+x.body.length,0))/350))} 分钟阅读</span></div></div>
      ${e.kind==='技能'?skillBody(e):`${e.project?projectSummary(e):''}<section id="use"><h2><span>01</span>适用场景</h2><p>${esc(e.summary)}</p><div class="prerequisite"><strong>使用前提</strong><p>${esc(e.prerequisites||m.prerequisites)}</p></div></section>
      <section id="principle"><h2><span>02</span>执行原理</h2><p>${esc(e.principle)}</p></section>
      <section id="example"><h2><span>03</span>使用示例</h2><div class="code-block"><div class="code-bar"><span>${esc({bash:'终端命令',python:'Python 代码',xml:'XML 配置',yaml:'YAML 配置',cmake:'CMake 配置',text:'流程与检查项'}[e.language]||e.language)}</span><button data-action="copy-code" data-id="${e.id}">${icon('copy')} 复制代码</button></div><pre tabindex="0"><code>${esc(e.code)}</code></pre></div>${e.language!=='bash'&&e.kind!=='实战'?'<p class="snippet-note">这是项目内的示例片段，请先准备上文所述对象与环境。</p>':''}</section>
      <section id="parameters"><h2><span>04</span>参数与步骤</h2><ol class="explain-list">${e.explain.map(x=>`<li>${esc(x)}</li>`).join('')}</ol></section>
      <section id="pitfalls"><h2><span>05</span>常见问题与边界</h2><div class="pitfall">${icon('info')}<p>${esc(e.pitfall)}</p></div></section>
      ${(e.sections||[]).map((s,i)=>`<section id="extra-${i}"><h2><span>${String(i+6).padStart(2,'0')}</span>${esc(s.title)}</h2>${s.body.split('\n\n').map(p=>`<p>${esc(p)}</p>`).join('')}${s.code?`<div class="code-block"><pre tabindex="0"><code>${esc(s.code)}</code></pre></div>`:''}</section>`).join('')}`}
      ${e.troubleshooting?troubleshooting(e):''}${e.project?projectFiles(e):''}<section id="source"><h2>${e.kind==='技能'?'07 · 深入阅读':'官方参考'}</h2>${sourceLinks(e)}<p class="source-note">${e.kind==='技能'?'本页是常用技能速查，不代表已经完成实验验证。固定版本与动态文档索引日期分别标注；上游页面可能继续更新。':'本页为独立编写的中文学习笔记与示例，不是官方文档的全文翻译。以标注版本为基线，完整选项与平台差异请核对官方参考。'}</p></section><div class="article-related"><h2>继续查阅</h2>${related.map(r=>`<a href="#article/${r.id}">${esc(r.title)}${icon('arrow')}</a>`).join('')}</div></article>
      <aside class="toc"><span class="toc-title">本页目录</span>${sections.map(([id,title])=>`<a href="#${id}" data-action="section" data-section="${id}">${title}</a>`).join('')}<div class="toc-note">${icon(m.icon)}<strong>${esc(m.name)}</strong><span>${esc(e.category)}</span><a href="${url('module/'+m.id,{category:e.category})}">查看同类词条 ${icon('arrow')}</a></div></aside></div>`;
  }
  const skillSections=[['use','解决什么问题'],['principle','核心原理'],['prerequisites','前置知识'],['parameters','常用流程'],['tools','工具与输入输出'],['pitfalls','常见误区']];
  function skillBody(e){
    const content={use:e.summary,principle:e.principle,prerequisites:e.prerequisites,tools:e.tools,pitfalls:e.pitfall};
    return `<div class="skill-label">技能速查 · 学习与操作参考</div>`+skillSections.map(([id,title],i)=>`<section id="${id}" class="skill-section"><h2><span>${String(i+1).padStart(2,'0')}</span>${title}</h2>${id==='parameters'?`<ol class="explain-list">${e.explain.map(step=>`<li>${esc(step)}</li>`).join('')}</ol>`:`<p>${esc(content[id])}</p>`}</section>`).join('');
  }
  function sourceLinks(e){return (e.sources||[{key:e.source}]).map(ref=>{const src=K.sources[ref.key];return `<a class="source-link" href="${esc(src[1])}" target="_blank" rel="noopener noreferrer">${icon('book')}<span>${esc(src[0])}<small>${ref.version?`${esc(ref.version)} · 索引核对 ${esc(ref.checked)} · `:''}打开原文需联网</small></span>${icon('link')}</a>`;}).join('');}
  const statusNames={detailed:'详解',overview:'概述',missing:'未收录'};
  function codeBlock(code,label='终端命令'){return `<div class="code-block"><div class="code-bar"><span>${esc(label)}</span><button data-action="copy-block">${icon('copy')} 复制代码</button></div><pre tabindex="0"><code>${esc(code)}</code></pre></div>`;}
  function projectSummary(e){const p=e.project,v=p.verification;return `<div class="project-summary"><div><strong>完整项目 · ${p.files.length} 个文件</strong><p>${esc(v.status)} · ${esc(v.date)}</p></div><a class="button primary" href="${esc(p.download)}" download>${icon('down')} 下载工程 ZIP · ${(p.size/1024).toFixed(1)} KB</a><p class="verification-note"><strong>验证环境：</strong>${esc(v.environment)}<br>${esc(v.evidence)}</p></div>`;}
  function projectFiles(e){const p=e.project;return `<section id="project-files"><h2>完整工程文件</h2><p>网页源码与 ZIP 从同一组文件生成。展开文件即可阅读和复制；下载后按 README 逐步执行。</p><p class="file-hash">ZIP SHA-256：${esc(p.sha256)}</p><div class="project-files">${p.files.map(f=>`<details><summary>${icon('terminal')} ${esc(f.path)}</summary>${codeBlock(f.content,f.path)}</details>`).join('')}</div></section>`;}
  function troubleshooting(e){const t=e.troubleshooting;const projects=K.entries.filter(x=>x.project&&x.related?.includes(e.id));return `<section id="diagnosis"><h2>检查与修复</h2><h3>可匹配的原始错误或症状</h3><div class="error-patterns">${t.patterns.map(p=>`<code>${esc(p)}</code>`).join('')}</div>${t.diagnosis.map(d=>`<div class="diagnostic-step"><h3>${esc(d.title)}</h3><p>${esc(d.reason)}</p><dl><dt>正常结果</dt><dd>${esc(d.normal)}</dd><dt>异常线索</dt><dd>${esc(d.abnormal)}</dd></dl></div>`).join('')}<h3>按检查结果选择修复</h3><ol class="explain-list">${t.fixes.map(f=>`<li>${esc(f)}</li>`).join('')}</ol><h3>修复后验证</h3>${codeBlock(t.verification.code)}<div class="acceptance"><strong>通过条件</strong><p>${esc(t.verification.expected)}</p></div>${projects.length?`<h3>在完整项目中排查</h3><div class="recent-links">${projects.map(p=>`<a href="#article/${p.id}">${esc(p.title)} ${icon('arrow')}</a>`).join('')}</div>`:''}</section>`;}
  function normalizeLog(text){return text.normalize('NFKC').toLowerCase().replace(/["'`“”‘’]/g,'').replace(/\s+/g,' ').trim();}
  function matchErrors(query,options={}){
    const clean=normalizeLog(query), pool=K.entries.filter(e=>e.troubleshooting&&(!options.module||e.module===options.module)&&(!options.category||e.category===options.category)&&(!options.version||e.version===options.version));
    if(!clean)return pool.map(e=>({e,score:0,matches:[]}));
    const words=terms(query.replace(/\b\d{4}-\d{2}-\d{2}[^\s]*|\b\d{2}:\d{2}:\d{2}(?:[.,]\d+)?|(?:\/[^\s]+)+|\b0x[\da-f]+/gi,' ')).filter(t=>t.length>1&&!/^\d+$/.test(t));
    return pool.map(e=>{const matches=e.troubleshooting.patterns.filter(p=>{const key=normalizeLog(p);return key.length<=3?/^[a-z]+$/.test(key)&&clean.split(/[^a-z]+/).includes(key):clean.includes(key);});const hits=words.filter(w=>searchText.get(e.id).includes(w));const score=(matches.length?1000+100*Math.max(...matches.map(p=>normalizeLog(p).length))+Math.min(matches.length,5):0)+Math.min(hits.length,20);return {e,score,matches};}).filter(r=>r.matches.length||words.length&&words.length<9&&r.score>=Math.min(2,words.length)).sort((a,b)=>b.score-a.score);
  }
  function errorLibrary(){
    const query=errorLog||state.q, list=matchErrors(query,state),pool=K.entries.filter(e=>e.troubleshooting&&(!state.module||e.module===state.module));
    const pages=Math.ceil(list.length/12),page=Math.min(state.page,Math.max(1,pages));
    return heading('科研工作台 / 本地诊断','报错库','粘贴错误原文或多行日志，优先匹配已收录的错误特征；结果是排查候选，不是自动判断根因。')+`<form id="error-form" class="log-search"><label for="error-log">错误文本或症状</label><textarea id="error-log" rows="5" maxlength="20000" placeholder="例如：ModuleNotFoundError: No module named 'mujoco'">${esc(query)}</textarea><div class="log-actions"><button class="button primary" type="submit">${icon('search')} 匹配报错</button><button class="button" type="button" data-action="clear-log">清空日志</button><button class="button" type="button" data-action="sample-log">试用 ROS QoS 示例</button><span>仅在当前页面内存中处理，不上传、不保存日志</span></div></form><div class="results-toolbar"><span class="results-count">${query?'匹配到':'收录'} <strong>${list.length}</strong> 个案例</span><div class="filters">${select('模块','module',K.modules,state.module)}${select('分类','category',[...new Set(pool.map(e=>e.category))],state.category)}${select('版本','version',[...new Set(pool.map(e=>e.version))],state.version)}</div></div>${list.length?`<div class="results-grid">${list.slice((page-1)*12,page*12).map(r=>`<div class="error-candidate">${r.matches.length?`<div class="match-reason">匹配特征：${r.matches.map(esc).join(' · ')}</div>`:query?'<div class="match-reason">关键词相关 · 请核对实际症状</div>':''}${card(r.e)}</div>`).join('')}</div>`:empty('没有找到已收录的错误特征','可尝试只保留最后一条异常、选择对应模块，或搜索中文症状。本地匹配不会生成未核实的修复方案。')}${pages>1?`<nav class="pagination" aria-label="报错分页">${page>1?`<a class="button" href="${url('errors',{...state,page:page-1})}">上一页</a>`:'<span></span>'}<span>第 ${page} / ${pages} 页</span>${page<pages?`<a class="button" href="${url('errors',{...state,page:page+1})}">下一页</a>`:'<span></span>'}</nav>`:''}`;
  }
  function practice(){
    const pool=K.entries.filter(e=>e.project),list=queryEntries({...state,kind:'实战'}).filter(e=>e.project&&(!state.status||e.project.verification.status===state.status));
    return heading('科研工作台 / 从运行到复现','完整实战','原有六个工具模块各两套完整工程，附源码、步骤、验收和关联排障。安装依赖可能需要网络。')+`<div class="coverage-intro">${icon('info')}<div><strong>每套项目都标明验证证据</strong><p>“静态检查通过”只表示语法、文件和结构检查通过；“目标环境运行通过”仅指注明的环境与范围。ROS、Gazebo 和 Isaac Lab 的完整运行结果需在相应环境核验。</p></div></div><div class="results-toolbar"><span class="results-count">找到 <strong>${list.length}</strong> 套工程</span><div class="filters">${select('模块','module',K.modules,state.module)}${select('难度','level',['基础','进阶'],state.level)}${select('验证状态','status',['未运行','静态检查通过','目标环境运行通过'],state.status)}</div></div><div class="results-grid">${list.map(e=>`<div class="practice-card">${card(e)}<div class="project-card-foot"><span>${e.project.files.length} 个文件</span><a href="${esc(e.project.download)}" download>${icon('down')} 下载 ZIP</a></div></div>`).join('')||empty('没有匹配的实战','请调整模块、难度或验证状态。')}</div>`;
  }
  function coverage(){
    const C=K.coverage,tt=terms(state.q),list=C.chapters.filter(c=>(!state.module||c.module===state.module)&&(!state.book||c.book===state.book)&&(!state.status||c.status===state.status)&&tt.every(t=>[c.title,c.originalTitle,c.version,moduleById(c.module).name].join(' ').toLowerCase().includes(t)));
    const counts=Object.fromEntries(Object.keys(statusNames).map(k=>[k,list.filter(c=>c.status===k).length]));
    const books=C.books.filter(b=>(!state.module||b.module===state.module)&&(!state.book||b.id===state.book));
    const row=c=>`<tr class="chapter-row"><td><strong class="${c.parent?'child-chapter':''}">${c.parent?'↳ ':''}${esc(c.title)}</strong><small>${esc(c.originalTitle)}</small></td><td>${tag(statusNames[c.status],c.status)}<p>${esc(c.reason)}</p></td><td>${c.entries.map(id=>`<a class="chapter-entry" href="#article/${id}">${esc(articleById(id).title)}</a>`).join('')||'<span>暂无本地对应条目</span>'}</td><td><a href="${esc(c.url)}" target="_blank" rel="noopener noreferrer">官方章节 ${icon('link')}</a><small>${esc(c.version)}</small><small>${c.verification==='checked'?'目录已核对':'待核对'} · ${esc(c.checked)}</small></td></tr>`;
    return heading('参考资料 / 章节级内容地图','官方章节覆盖表','按固定文档版本逐章核对。下表计数基于实际列出的章节，父章与子章独立评估。')+`<div class="coverage-intro">${icon('book')}<div><strong>${C.chapters.length} 个章节记录 · ${C.books.length} 份文档目录</strong><p>详解：本地步骤、原理和验收与该章节范围相符；概述：只覆盖章节中的部分主题；未收录：尚无对应本地正文。官方 API 按参考章节记录，不逐函数计数。每份目录说明其纳入范围；这不是所有官方文档的离线镜像。</p><p>Embodied · 具身智能科研技能是 96 项跨工具学习索引，不计入这 797 条官方章节覆盖记录。阅读技能不代表已完成实验验证。<a href="#module/embodied">浏览技能目录</a></p></div></div><form id="chapter-form" class="chapter-search"><label for="chapter-query">搜索章节</label><input id="chapter-query" value="${esc(state.q)}" placeholder="中文章名、原文章名或版本"><button class="button" type="submit">搜索</button></form><div class="results-toolbar"><span class="results-count">当前 ${list.length} 章：<strong>${counts.detailed}</strong> 详解 / <strong>${counts.overview}</strong> 概述 / <strong>${counts.missing}</strong> 未收录</span><div class="filters">${select('模块','module',K.modules,state.module)}${select('覆盖状态','status',Object.entries(statusNames).map(([id,name])=>({id,name})),state.status)}${select('文档','book',C.books.filter(b=>!state.module||b.module===state.module).map(b=>({id:b.id,name:b.title})),state.book)}</div></div>${books.map(b=>{const rows=list.filter(c=>c.book===b.id);return rows.length?`<details class="chapter-book" open><summary><span>${esc(b.title)}</span><span>${rows.length} 章 · ${esc(b.version)}</span></summary><p class="book-scope">${esc(b.scope)}<br>目录核对：${esc(b.snapshotDate)} · ${b.verification==='checked'?'已取得官方目录':'官方访问受限，待核对'} <a href="${esc(b.url)}" target="_blank" rel="noopener noreferrer">查看目录 ${icon('link')}</a></p><div class="coverage-table-wrap"><table><thead><tr><th>中文 / 原文章节</th><th>覆盖状态与依据</th><th>本地内容</th><th>版本与来源</th></tr></thead><tbody>${rows.map(row).join('')}</tbody></table></div></details>`:'';}).join('')||empty('没有匹配的章节','调整文档、模块或状态筛选。')}<p class="source-note">目录快照与中文映射保存在 data/，构建时核验条目引用。日期是本次目录核对日期，不代表所有上游内容都在该日发布。</p>`;
  }
  function sources(){const groups=[['GitHub',Object.keys(K.sources).filter(k=>k.startsWith('gh-'))],['Linux 与科研工具',Object.keys(K.sources).filter(k=>!k.startsWith('emb-')&&!k.startsWith('gh-')&&!k.startsWith('mj-')&&!k.startsWith('gz-')&&!k.startsWith('il-')&&!['sdf','ros1','ros2','ros2-concept','ros2-how','ros2-raw','ros-rep','ros-control','nav2','moveit'].includes(k))],['MuJoCo',Object.keys(K.sources).filter(k=>k.startsWith('mj-'))],['Gazebo',Object.keys(K.sources).filter(k=>k.startsWith('gz-')||k==='sdf')],['ROS 1 / 2',Object.keys(K.sources).filter(k=>k.startsWith('ros')||['nav2','moveit'].includes(k))],['Isaac Lab',Object.keys(K.sources).filter(k=>k.startsWith('il-'))],['Embodied · 官方文档与原始论文',Object.keys(K.sources).filter(k=>k.startsWith('emb-'))]];return heading('参考资料 / 官方来源','官方文档索引','按主题继续查阅完整原文。以下均为外部链接，需要联网；官方页面可能以英文为主。')+groups.map(([title,keys])=>`<section class="source-group"><h2>${title} <span>${keys.length} 个入口</span></h2><div class="source-grid">${keys.map(k=>`<a class="source-item" href="${esc(K.sources[k][1])}" target="_blank" rel="noopener noreferrer">${icon('book')}<span>${esc(K.sources[k][0])}<small>${esc(new URL(K.sources[k][1]).hostname)}</small></span>${icon('link')}</a>`).join('')}</div></section>`).join('');}
  function renderContent(){
    const view={home,learn:learningOverview,path:learningRoute,search:results,module:results,saved:results,article,coverage,sources,errors:errorLibrary,practice}[state.view];
    $('#main').innerHTML=view?view():empty('页面不存在','请通过左侧导航继续阅读。');
    const active=state.view==='path'?'learn':state.view==='module'?state.id:state.view==='article'?articleById(state.id)?.module:state.view;
    document.querySelectorAll('[data-nav]').forEach(el=>{el.classList.toggle('active',el.dataset.nav===active);if(el.dataset.nav===active)el.setAttribute('aria-current','page');else el.removeAttribute('aria-current');});
    $('#saved-count').textContent=favorites.size;
    document.title=(state.view==='learn'?'学习路线':state.view==='path'?learningPath(state.id)?.title||'学习路线':state.view==='article'?articleById(state.id)?.title:state.view==='module'?moduleById(state.id)?.name:state.view==='search'?'全文搜索':state.view==='saved'?'我的收藏':state.view==='errors'?'报错库':state.view==='practice'?'完整实战':state.view==='coverage'?'官方章节覆盖表':'机器人科研手册')+' · 研知';
    $('#search-form').classList.toggle('has-value',Boolean($('#global-search').value));
  }
  function render(){state=parse();$('#global-search').value=state.q;renderContent();}
  async function copy(text){if(navigator.clipboard&&window.isSecureContext){try{await navigator.clipboard.writeText(text);toast('已复制到剪贴板');return;}catch{}}const el=document.createElement('textarea');el.value=text;el.style.position='fixed';el.style.opacity='0';document.body.appendChild(el);el.select();let ok=false;try{ok=document.execCommand('copy');}catch{}el.remove();toast(ok?'已复制到剪贴板':'浏览器禁止自动复制，请手动选择并复制内容');}
  function click(event){
    const b=event.target.closest('[data-action]');if(!b)return;
    const action=b.dataset.action;
    if(action==='learning-reset'){resetLearning();return;}
    if(action==='menu'){document.body.classList.toggle('menu-open');return;}
    if(action==='clear-search'){$('#global-search').value='';go('#search');$('#global-search').focus();return;}
    if(action==='save'){const e=articleById(b.dataset.id);if(!e)return;favorites.has(e.id)?favorites.delete(e.id):favorites.add(e.id);const stored=storage.set('favorites',[...favorites]);renderContent();toast(stored?(favorites.has(e.id)?'已加入收藏':'已取消收藏'):'浏览器未允许持久保存，本次会话内仍可使用收藏');}
    if(action==='clear-log'){errorLog='';go(url('errors',{...state,q:'',page:1}));return;}
    if(action==='sample-log'){errorLog='[2026-09-21 10:23:41] [WARN] /tmp/robot/run.py: incompatible QoS. Last incompatible policy: RELIABILITY_QOS_POLICY';go(url('errors',{module:'ros'}));return;}
    if(action==='copy-block')copy(b.closest('.code-block').querySelector('code').textContent);
    if(action==='copy-code')copy(articleById(b.dataset.id).code);
    if(action==='copy-link')copy(location.href.split('#')[0]+'#article/'+b.dataset.id);
    if(action==='section'){event.preventDefault();document.getElementById(b.dataset.section)?.scrollIntoView({behavior:window.matchMedia('(prefers-reduced-motion: reduce)').matches?'auto':'smooth',block:'start'});}
  }
  document.addEventListener('change',learningChange);
  document.addEventListener('submit',submitLearning);
  shell();render();
  // WebMCP 是可选增强，普通浏览器和 file:// 阅读均不依赖它。
  const context=document.modelContext;
  if(context?.registerTool){const lifecycle=new AbortController();const definitions=[{name:'search_research_knowledge',title:'搜索科研手册',description:'在本地中文词条中全文搜索，并导航到可见结果。',inputSchema:{type:'object',properties:{query:{type:'string',maxLength:500}},required:['query'],additionalProperties:false},annotations:{readOnlyHint:false,untrustedContentHint:false},execute(input){if(!input||typeof input.query!=='string'||input.query.length>500)throw new Error('query 必须是 500 字符以内的字符串');const list=queryEntries({q:input.query});history.replaceState(null,'',url('search',{q:input.query}));render();return {count:list.length,results:list.slice(0,12).map(e=>({id:e.id,title:e.title,module:e.module}))};}},{name:'open_research_article',title:'阅读科研词条',description:'打开指定本地词条，并返回中文内容。',inputSchema:{type:'object',properties:{id:{type:'string'}},required:['id'],additionalProperties:false},annotations:{readOnlyHint:false,untrustedContentHint:false},execute(input){const e=input&&articleById(input.id);if(!e)throw new Error('词条不存在');history.replaceState(null,'','#article/'+e.id);render();return {id:e.id,title:e.title,kind:e.kind,summary:e.summary,principle:e.principle,prerequisites:e.prerequisites,code:e.code,explain:e.explain,tools:e.tools,pitfall:e.pitfall,sources:e.sources||[{key:e.source}]};}}];for(const definition of definitions){try{Promise.resolve(context.registerTool(definition,{signal:lifecycle.signal})).catch(()=>{});}catch{}}window.addEventListener('pagehide',()=>lifecycle.abort(),{once:true});}
})();
