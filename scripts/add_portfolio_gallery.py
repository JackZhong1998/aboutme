"""Add portfolio gallery and evidence-backed project highlights to existing site."""
from pathlib import Path
import re, html
ROOT=Path(__file__).resolve().parent.parent
p=ROOT/'index.html'
s=p.read_text(encoding='utf-8')
if 'id="work-gallery"' in s:
 raise SystemExit('Gallery already installed; edit existing markup for subsequent changes.')

# Preserve existing images and visual language; avoid nested anchors.
products=[
 ('NowBuild.ai','营销 Agent Team','nowbuild.ai','https://www.nowbuild.ai','nowbuild-hero.png','https://github.com/JackZhong1998/N0707',
  '主控 Agent 分派专业任务，后台队列承接长任务，用每日待办管理执行进程。',
  '角色契约 · Skill 按需加载 · 断点续跑'),
 ('todoAgent','任务协作 Agent','todoagent.cc','https://www.todoagent.cc/','todoagent-hero.png','https://github.com/JackZhong1998/todoagent',
  '以项目和待办组织上下文，将任务分工、工具调用与结果验收放进已有工作流。',
  '动态 Context · 有界工具循环 · 增量 SOP'),
 ('VoiceMind','实时语音交互','voicemind.cc','https://www.voicemind.cc/','voicemind-hero.png','https://github.com/JackZhong1998/voicemind',
  '实时语音中梳理思路，对话 Agent 更新任务清单，执行 Agent 逐项生成结果。',
  '对话／执行分离 · Schema · 任务状态'),
 ('bewithyou','声音与 Personal Agent','bewithyou.online','https://www.bewithyou.online','bewithyou-hero.jpg','',
  '以声音和角色作为交互入口，已实现英语学习场景；进一步探索声音导向的个人应用。',
  '声音交互 · 角色陪伴 · 英语学习')]
items=[]
for name,tag,domain,url,img,repo,desc,tech in products:
 items.append(f'''<article class="product"><a class="product-main" href="{url}" target="_blank" rel="noopener noreferrer"><div class="browser-frame"><span class="dots" aria-hidden="true"><i></i><i></i><i></i></span><span>{domain}</span></div><div class="product-image"><img src="assets/img/{img}" alt="{name} 官网首屏" width="1400" height="875" loading="lazy"></div><div class="product-text"><div class="product-heading"><h3>{name}</h3><span class="product-arrow" aria-hidden="true">↗</span></div><span class="product-tag">{tag}</span><p>{desc}</p><p class="technical-caption">{tech}</p></div></a><div class="project-links"><a href="{url}" target="_blank" rel="noopener noreferrer">访问官网</a>{f'<a href="{repo}" target="_blank" rel="noopener noreferrer">查看代码</a>' if repo else ''}</div></article>''')
expertise='''<div class="expertise"><h3>Agent 架构与 Harness 设计</h3><div class="expertise-grid"><div><h4>任务编排</h4><p>明确主控与 Worker 的职责、读写范围和确认边界，让对话与执行各司其职。</p></div><div><h4>上下文工程</h4><p>组织项目、用户与任务记忆，按需加载 Skill，区分确认事实与推断。</p></div><div><h4>可恢复执行</h4><p>通过持久化步骤、幂等键、租约和重试，处理长任务中断与状态恢复。</p></div><div><h4>质量与成本</h4><p>结合结构化输出、校验、调用 Trace 与预算约束，设计可观察的运行过程。</p></div></div></div>'''
start=s.index('<div class="products">')
end=s.index('<section class="panel" id="job">',start)
s=s[:start]+'<div class="products">'+''.join(items)+'</div>'+expertise+'</section>\n'+s[end:]

files=[
 ('jianying-image-editor.png','图片 Web','画板编辑与 AI 设计'),
 ('jianying-image-home.png','图片 Web','创作入口与模板发现'),
 ('jianying-cover-generation.png','智能封面','参考视频画面生成封面'),
 ('jianying-cover-entry.png','智能封面','剪辑流程中的封面设计入口'),
 ('jianying-agent-entry.png','剪辑 Agent','视频创作中的 Agent 入口'),
 ('jianying-agent-skill.png','剪辑 Agent','从历史草稿生成可复用技能')]
figs=[];large=[]
for i,(name,cat,caption) in enumerate(files):
 from PIL import Image
 with Image.open(ROOT/'assets'/'img'/name) as im:w,h=im.size
 figs.append(f'''<figure class="work-capture" data-group="{cat}" {'hidden' if i>1 else ''}><button class="capture-open {'portrait-capture' if i>=4 else ''}" type="button" data-image="{i}" aria-label="查看大图：{caption}"><img src="assets/img/{name}" width="{w}" height="{h}" alt="{cat}：{caption}" loading="lazy"><span class="zoom-hint">查看大图</span></button><figcaption>{caption}</figcaption></figure>''')
 large.append(f'<img class="lightbox-image" src="assets/img/{name}" width="{w}" height="{h}" alt="{cat}：{caption}" loading="lazy" hidden>')
gallery='''<div class="business-gallery" id="work-gallery"><div class="gallery-heading"><h3>产品界面</h3><div class="gallery-tabs" role="tablist" aria-label="剪映作品分类">'''+''.join(f'<button type="button" class="gallery-tab" role="tab" aria-selected="{str(i==0).lower()}" data-gallery="{t}">{t}</button>' for i,t in enumerate(['图片 Web','智能封面','剪辑 Agent']))+'''</div></div><div class="capture-grid">'''+''.join(figs)+'''</div></div>'''
anchor='<div class="cases">'
s=s.replace(anchor,gallery+anchor,1)
lightbox='''<dialog id="image-viewer" class="image-viewer" aria-labelledby="viewer-title"><div class="viewer-toolbar"><span id="viewer-title">产品界面</span><button id="viewer-prev" type="button" aria-label="上一张图片">上一张</button><button id="viewer-next" type="button" aria-label="下一张图片">下一张</button><button id="viewer-close" type="button">关闭</button></div><div class="viewer-content">'''+''.join(large)+'''</div></dialog>'''
s=s.replace('<script>',lightbox+'\n<script>',1)
css='''
/* Product proof and compact capability overview */
.product{display:flex;flex-direction:column}.product-main{display:block;flex:1}.technical-caption{color:#4a5d73!important;font-size:14px!important}.project-links{display:flex;gap:24px;padding:0 22px 18px}.project-links a{display:inline-flex;align-items:center;min-height:44px;color:var(--accent);font-size:14px}.project-links a:hover{text-decoration:underline}.expertise{margin-top:34px;padding-top:28px;border-top:1px solid #e0e3e8}.expertise h3,.gallery-heading h3{font-size:21px;letter-spacing:-.5px;font-weight:600}.expertise-grid{display:grid;grid-template-columns:1fr;gap:22px;margin-top:22px}.expertise-grid h4{font-size:16px;font-weight:600;margin-bottom:7px}.expertise-grid p{color:var(--muted);font-size:14px;line-height:1.9}
.business-gallery{margin:10px 0 32px}.gallery-heading{display:flex;justify-content:space-between;align-items:center;gap:18px;flex-wrap:wrap;margin-bottom:20px}.gallery-tabs{display:flex;flex-wrap:wrap;gap:7px}.gallery-tab{border:1px solid #dfe2e7;padding:10px 14px;min-height:44px;background:#fff;border-radius:24px;color:var(--muted);font-size:14px}.gallery-tab[aria-selected="true"]{background:var(--ink);color:#fff;border-color:var(--ink)}.capture-grid{display:grid;grid-template-columns:1fr;gap:18px}.work-capture{min-width:0;margin:0;background:#fff;border:1px solid #e2e5ea;border-radius:20px;overflow:hidden}.capture-open{width:100%;display:flex;align-items:center;justify-content:center;border:0;background:#edf0f4;padding:10px;position:relative;aspect-ratio:1.14;cursor:zoom-in}.capture-open img{width:100%;height:100%;object-fit:contain;transition:transform .3s var(--ease)}.capture-open:hover img{transform:scale(1.01)}.capture-open.portrait-capture{height:370px;aspect-ratio:auto;background:#eff1f4;padding:16px}.zoom-hint{position:absolute;right:14px;bottom:14px;background:rgba(255,255,255,.96);color:#373940;border:1px solid #dce0e5;border-radius:20px;font-size:13px;padding:5px 10px}.work-capture figcaption{font-size:14px;color:#51515a;padding:14px 18px}.image-viewer{border:0;background:white;color:var(--ink);border-radius:20px;max-width:96vw;width:1500px;max-height:94vh;padding:0;margin:auto}.image-viewer::backdrop{background:rgba(17,20,27,.7)}.viewer-toolbar{position:sticky;top:0;background:#fff;display:flex;align-items:center;flex-wrap:wrap;gap:8px;padding:12px 18px;border-bottom:1px solid var(--line);z-index:2}.viewer-toolbar span{margin-right:auto;font-size:14px;flex-basis:100%}.viewer-toolbar button{background:#f5f6f8;border:1px solid #e1e3e8;border-radius:22px;padding:10px 16px;min-height:44px;font-size:14px}.viewer-content{padding:12px;min-height:160px;display:flex;justify-content:center;align-items:center;background:#f4f5f7}.lightbox-image{max-width:100%;height:auto;width:auto;max-height:76vh;object-fit:contain}.lightbox-image[hidden]{display:none}.capture-open:focus-visible,.viewer-toolbar button:focus-visible,.gallery-tab:focus-visible{outline:2px solid var(--accent);outline-offset:-3px}
@media(min-width:600px){.capture-grid{grid-template-columns:repeat(2,minmax(0,1fr))}.expertise-grid{grid-template-columns:repeat(2,minmax(0,1fr))}.capture-open.portrait-capture{height:460px}.viewer-toolbar span{flex-basis:auto}.capture-open{aspect-ratio:1.14}}@media(min-width:900px){.expertise-grid{grid-template-columns:repeat(4,minmax(0,1fr))}}
'''
s=s.replace('</style>',css+'</style>',1)
js='''
/* Artwork gallery: source URLs remain in static img attributes. */
const galleryTabs=[...document.querySelectorAll('.gallery-tab')];
galleryTabs.forEach(button=>button.addEventListener('click',()=>{galleryTabs.forEach(t=>t.setAttribute('aria-selected',String(t===button)));document.querySelectorAll('.work-capture').forEach(f=>f.hidden=f.dataset.group!==button.dataset.gallery)}));
const viewer=document.getElementById('image-viewer'), viewerImages=[...document.querySelectorAll('.lightbox-image')];let currentImage=0;let lastCapture=null;
function showImage(index){currentImage=(index+viewerImages.length)%viewerImages.length;viewerImages.forEach((im,i)=>im.hidden=i!==currentImage);document.getElementById('viewer-title').textContent=viewerImages[currentImage].alt;viewer.scrollTop=0;}
document.querySelectorAll('.capture-open').forEach(button=>button.addEventListener('click',()=>{lastCapture=button;showImage(Number(button.dataset.image));viewer.showModal();document.body.style.overflow='hidden'}));
document.getElementById('viewer-close').addEventListener('click',()=>viewer.close());document.getElementById('viewer-prev').addEventListener('click',()=>showImage(currentImage-1));document.getElementById('viewer-next').addEventListener('click',()=>showImage(currentImage+1));viewer.addEventListener('close',()=>{document.body.style.overflow='';lastCapture?.focus()});viewer.addEventListener('keydown',e=>{if(e.key==='ArrowLeft'){e.preventDefault();showImage(currentImage-1)}if(e.key==='ArrowRight'){e.preventDefault();showImage(currentImage+1)}});viewer.addEventListener('click',e=>{if(e.target===viewer){const r=viewer.getBoundingClientRect();if(e.clientX<r.left||e.clientX>r.right||e.clientY<r.top||e.clientY>r.bottom)viewer.close()}});
'''
s=s.replace('</script>',js+'</script>',1)
p.write_text(s,encoding='utf-8')
print('Homepage updated: 4 product cards, 3 repository links, 6 gallery images.')
