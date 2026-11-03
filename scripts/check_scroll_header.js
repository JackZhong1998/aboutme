const bar=document.querySelector('.scroll-header');if(!bar)throw Error('Missing header');
const wait=()=>new Promise(r=>setTimeout(r,320));
window.scrollTo({top:0,behavior:'instant'});await wait();
if(bar.classList.contains('is-hidden'))throw Error('Header hidden at page top');
window.scrollTo({top:400,behavior:'instant'});await wait();
if(!bar.classList.contains('is-hidden')||!bar.inert)throw Error('Swipe up did not hide header');
window.scrollTo({top:310,behavior:'instant'});await wait();
if(bar.classList.contains('is-hidden')||bar.inert)throw Error('Swipe down did not show header');
window.scrollTo({top:600,behavior:'instant'});await wait();
if(!bar.classList.contains('is-hidden'))throw Error('Second hide failed');
window.scrollTo({top:0,behavior:'instant'});await wait();
if(bar.classList.contains('is-hidden'))throw Error('Header not restored at page top');
const isResume=location.pathname.endsWith('resume.html');
if(isResume){const back=bar.querySelector('.back');if(!back||back.getAttribute('href')!=='./')throw Error('Missing return homepage link');if(bar.querySelectorAll('a,button').length!==2)throw Error('Unexpected resume controls');}
return {passed:true,swipeUp:'hidden',swipeDown:'visible',top:'visible',returnButton:isResume};