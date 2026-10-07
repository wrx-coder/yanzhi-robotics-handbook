/* 独立无头 Chrome QA，不连接用户浏览器；参数：Playwright 模块路径、可选输出目录。 */
const {chromium}=require(process.argv[2]||'playwright');
const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');
const root=path.resolve(__dirname,'..'),out=process.argv[3]||'/tmp/yanzhi-learning-browser';fs.mkdirSync(out,{recursive:true});
const K=JSON.parse(fs.readFileSync(path.join(root,'dist/knowledge.json'),'utf8'));
const base='file://'+path.join(root,'dist/index.html');
(async()=>{
 const browser=await chromium.launch({executablePath:'/usr/bin/google-chrome',headless:true,args:['--no-sandbox']});
 const context=await browser.newContext({viewport:{width:1440,height:1000}}),page=await context.newPage(),errors=[],requests=[];
 page.on('pageerror',e=>errors.push(e.message));page.on('request',r=>requests.push(r.url()));
 await page.goto('file://'+path.join(root,'index.html')+'#path/ros-mobile?stage=navigation');await page.locator('[data-stage="navigation"]').waitFor();
 await page.goto(base+'#learn');await page.locator('.learning-card').first().waitFor();assert.equal(await page.locator('.learning-card').count(),4);
 await page.screenshot({path:path.join(out,'desktop-overview.png'),fullPage:true});
 await page.locator('.learning-card .button').first().click();await page.locator('.learning-stage').waitFor();
 await page.locator('[data-learning-mark="read"]').check();await page.locator('[data-learning-mark="exercise"]').check();
 const quiz=K.learningPaths[0].stages[0].quiz;
 for(let i=0;i<3;i++)await page.locator(`[data-learning-question="${i}"][value="${(quiz[i].answer+1)%3}"]`).check();
 await page.locator('#learning-quiz button[type="submit"]').click();assert((await page.locator('#quiz-result').innerText()).includes('0 / 3'));
 for(let i=0;i<3;i++)await page.locator(`[data-learning-question="${i}"][value="${quiz[i].answer}"]`).check();
 await page.locator('#learning-quiz button[type="submit"]').click();assert((await page.locator('#quiz-result').innerText()).includes('自测已通过'));
 await page.reload();assert(await page.locator('[data-learning-mark="read"]').isChecked());assert((await page.locator('#quiz-result').innerText()).includes('自测已通过'));
 await page.locator('.learning-hints summary').first().click();assert(await page.locator('.learning-hints details').first().getAttribute('open')!==null);
 await page.locator('.learning-hints summary').last().click();assert(await page.locator('.learning-hints details').last().getAttribute('open')!==null);
 await page.screenshot({path:path.join(out,'desktop-stage.png'),fullPage:true});
 await page.locator('[data-action="learning-reset"]').click();assert.equal(await page.locator('#learning-quiz input:checked').count(),0);assert((await page.locator('.learning-path-progress').innerText()).includes('0 / 4'));
 const overflow=[];
 for(const width of [1440,768,390,320]){
  await page.setViewportSize({width,height:900});
  for(const hash of ['#home','#learn',...K.learningPaths.flatMap(p=>p.stages.map(s=>`#path/${p.id}?stage=${s.id}`))]){
   await page.goto(base+hash);await page.locator('h1').waitFor();
   const dims=await page.evaluate(()=>({scroll:document.documentElement.scrollWidth,width:innerWidth}));if(dims.scroll>dims.width+1)overflow.push({width,hash,...dims});
  }
  if(width===390){await page.goto(base+'#learn');await page.screenshot({path:path.join(out,'mobile-overview.png'),fullPage:true});await page.goto(base+'#path/embodied-learning?stage=vla-evaluation');await page.screenshot({path:path.join(out,'mobile-stage.png'),fullPage:true});await page.locator('button[data-action="menu"]').click();assert(await page.locator('body').evaluate(el=>el.classList.contains('menu-open')));await page.locator('[data-nav="learn"]').click();assert.equal(await page.locator('h1').innerText(),'学习路线');}
 }
 assert.deepEqual(overflow,[]);
 await page.setViewportSize({width:1280,height:900});await page.goto(base+'#path/research-foundations');await page.evaluate(()=>document.documentElement.style.fontSize='32px');assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1));
 const denied=await browser.newContext();await denied.addInitScript(()=>{Object.defineProperty(window,'localStorage',{get(){throw new DOMException('blocked','SecurityError')}})});const d=await denied.newPage();await d.goto(base+'#path/research-foundations');assert((await d.locator('.learning-storage').innerText()).includes('当前会话'));await d.locator('[data-learning-mark="read"]').check();await d.goto(base+'#learn');await d.locator('.learning-card .button').first().click();assert(await d.locator('[data-learning-mark="read"]').isChecked());await denied.close();
 assert.deepEqual(errors,[]);assert(!requests.some(r=>/^https?:/.test(r)));
 fs.writeFileSync(path.join(out,'result.json'),JSON.stringify({browser:await browser.version(),viewports:[1440,768,390,320],routesPerViewport:18,overflow,errors,networkRequests:requests.filter(r=>/^https?:/.test(r)),checks:['file offline','correct and incorrect feedback','refresh','hints and solution','reset','mobile navigation','200% root font','storage denied'],screenshots:['desktop-overview.png','desktop-stage.png','mobile-overview.png','mobile-stage.png']},null,2));
 await browser.close();console.log('PASS 离线 Chrome、72 个视口/路由组合、交互、刷新、禁用存储与截图');
})().catch(e=>{console.error(e);process.exit(1)});
