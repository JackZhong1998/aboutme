"""Install identical swipe-aware header behavior on homepage and resume."""
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
css='''
/* Header retreats while swiping up; returns while swiping down. */
.scroll-header{transition:transform .22s ease,visibility .22s;will-change:transform}
.scroll-header.is-hidden{transform:translateY(-110%);visibility:hidden;pointer-events:none}
@media(prefers-reduced-motion:reduce){.scroll-header{transition:none}}
@media print{.scroll-header{display:none!important}}
'''
js='''
(function(){
 const header=document.querySelector('.scroll-header');if(!header)return;
 let lastY=Math.max(0,window.scrollY),travel=0,lastDirection=0,pending=false;
 const show=()=>{header.classList.remove('is-hidden');header.inert=false;};
 const update=()=>{
  pending=false;
  const maxY=Math.max(0,document.documentElement.scrollHeight-window.innerHeight);
  const y=Math.min(maxY,Math.max(0,window.scrollY)),delta=y-lastY;lastY=y;
  if(document.body.style.overflow==='hidden')return;
  if(y<=4){show();travel=0;return;}
  if(Math.abs(delta)<1)return;
  const direction=Math.sign(delta);
  if(direction!==lastDirection){travel=0;lastDirection=direction;}
  travel+=Math.abs(delta);
  if(travel<8)return;
  travel=0;
  if(direction<0){show();}
  else if(y>header.offsetHeight&&!header.contains(document.activeElement)){
   header.classList.add('is-hidden');header.inert=true;
  }
 };
 window.addEventListener('scroll',()=>{if(!pending){pending=true;requestAnimationFrame(update)}},{passive:true});
 header.addEventListener('focusin',show);
 window.addEventListener('pageshow',()=>{show();lastY=Math.max(0,window.scrollY);travel=0;});
})();
'''
for file,old,new in [('index.html','class="topbar"','class="topbar scroll-header"'),('resume.html','class="toolbar"','class="toolbar scroll-header"')]:
 p=ROOT/file;s=p.read_text()
 assert old in s and 'class="scroll-header"' not in s
 s=s.replace(old,new,1).replace('</style>',css+'</style>',1)
 if file=='index.html':s=s.replace('</script>',js+'</script>',1)
 else:
  s=s.replace('<div class="toolbar-inner" style="justify-content:flex-end">','<div class="toolbar-inner"><a class="btn back" href="./" aria-label="返回个人主页">← 返回主页</a>',1)
  s=s.replace('</body>','<script>'+js+'</script></body>',1)
 p.write_text(s)
print('Updated both headers; resume has Back + PDF.')
