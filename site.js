'use strict';
(() => {
  const menu=document.querySelector('.menu-toggle'), nav=document.getElementById('navigation');
  const languages=[...document.querySelectorAll('.language-menu')];
  function closeMenu(){menu.setAttribute('aria-expanded','false');nav.classList.remove('open');menu.lastElementChild.textContent='+';}
  menu.addEventListener('click',()=>{const open=menu.getAttribute('aria-expanded')!=='true';menu.setAttribute('aria-expanded',String(open));nav.classList.toggle('open',open);menu.lastElementChild.textContent=open?'−':'+';languages.forEach(item=>{item.open=false;});});
  nav.querySelectorAll('a').forEach(link=>link.addEventListener('click',closeMenu));
  window.matchMedia('(min-width: 961px)').addEventListener('change',closeMenu);
  document.getElementById('year').textContent=String(new Date().getFullYear());
  languages.forEach(item=>item.addEventListener('toggle',()=>{if(item.open)closeMenu();}));
  document.addEventListener('click',event=>languages.forEach(item=>{if(!item.contains(event.target))item.open=false;}));

  // Gallery captions are supplied by the translated static page.
  const albums=new Map(), triggers=[...document.querySelectorAll('button[data-shot]')];
  triggers.forEach(button=>{
    const name=button.dataset.album;
    if(!albums.has(name))albums.set(name,[]);
    const album=albums.get(name);let index=album.findIndex(image=>image.src===button.dataset.shot);
    if(index<0){index=album.length;album.push({src:button.dataset.shot,caption:button.dataset.caption,width:Number(button.dataset.width),height:Number(button.dataset.height)});}
    button.dataset.galleryIndex=String(index);
  });
  const dialog=document.getElementById('gallery-dialog'), picture=document.getElementById('gallery-image');
  const title=document.getElementById('gallery-title'), caption=document.getElementById('gallery-caption'), count=document.getElementById('gallery-count');
  let active=null,index=0,lastTrigger=null;
  function render(){const image=active[index];picture.src=image.src;picture.alt=image.caption;picture.width=image.width;picture.height=image.height;caption.textContent=image.caption;count.textContent=`${index+1} / ${active.length}`;}
  function advance(direction){index=(index+direction+active.length)%active.length;render();}
  triggers.forEach(button=>button.addEventListener('click',()=>{lastTrigger=button;active=albums.get(button.dataset.album);index=Number(button.dataset.galleryIndex);title.textContent=button.dataset.album.split('-')[0]==='zzz'?'ZZZombie Assault':'Floki Heaven';render();dialog.showModal();document.body.classList.add('modal-open');dialog.querySelector('.lightbox-close').focus();}));
  dialog.querySelector('.lightbox-close').addEventListener('click',()=>dialog.close());
  dialog.querySelector('.lightbox-prev').addEventListener('click',()=>advance(-1));
  dialog.querySelector('.lightbox-next').addEventListener('click',()=>advance(1));
  dialog.addEventListener('close',()=>{document.body.classList.remove('modal-open');lastTrigger?.focus({preventScroll:true});});
  dialog.addEventListener('click',event=>{if(event.target!==dialog)return;const r=dialog.getBoundingClientRect();if(event.clientX<r.left||event.clientX>r.right||event.clientY<r.top||event.clientY>r.bottom)dialog.close();});
  document.addEventListener('keydown',event=>{
    if(dialog.open&&(event.key==='ArrowRight'||event.key==='ArrowLeft')){event.preventDefault();advance(event.key==='ArrowRight'?1:-1);}
    else if(event.key==='Escape'&&!dialog.open){const language=languages.find(item=>item.open);if(language){language.open=false;language.querySelector('summary').focus();}if(nav.classList.contains('open')){closeMenu();menu.focus();}}
  });

  // Original sprite frames, one shared loop, no work while offscreen.
  const reduced=window.matchMedia('(prefers-reduced-motion: reduce)'), resources=new Map(), states=[];
  const toggles=[...document.querySelectorAll('[data-motion-toggle]')];
  let paused=reduced.matches,raf=null,previous=null;
  function labels(){toggles.forEach(button=>{button.setAttribute('aria-pressed',String(paused));button.textContent=paused?button.dataset.play:button.dataset.pause;});}
  function draw(state,n){const f=state.meta.frames[n];state.ctx.clearRect(0,0,state.canvas.width,state.canvas.height);state.ctx.drawImage(state.image,f.x,f.y,state.meta.width,state.meta.height,0,0,state.canvas.width,state.canvas.height);state.canvas.dataset.frame=String(n);}
  function needed(){return !paused&&!document.hidden&&states.some(state=>state.visible);}
  function sync(){if(needed()&&raf===null){previous=null;raf=requestAnimationFrame(tick);}if(!needed()&&raf!==null){cancelAnimationFrame(raf);raf=null;previous=null;}}
  function tick(now){
    raf=null;const delta=previous===null?0:Math.min(now-previous,100);previous=now;
    states.forEach(state=>{if(!state.visible)return;state.phase=(state.phase+delta)%state.duration;let n=state.meta.frames.length-1;if(state.phase<state.sum)n=state.ends.findIndex(end=>state.phase<end);if(n!==state.index){state.index=n;draw(state,n);}});
    if(needed())raf=requestAnimationFrame(tick);else previous=null;
  }
  function load(name){
    if(!resources.has(name))resources.set(name,fetch(`/assets/sprites/${name}.json`).then(response=>{if(!response.ok)throw new Error('Sprite metadata missing');return response.json();}).then(meta=>new Promise((resolve,reject)=>{const image=new Image();image.onload=()=>resolve({meta,image});image.onerror=reject;image.src=meta.image;})));
    return resources.get(name);
  }
  const observer=new IntersectionObserver(entries=>{entries.forEach(entry=>{const state=states.find(item=>item.canvas===entry.target);if(state)state.visible=entry.isIntersecting;});sync();},{threshold:.05});
  document.querySelectorAll('canvas[data-animation]').forEach(canvas=>load(canvas.dataset.animation).then(({meta,image})=>{
    const ctx=canvas.getContext('2d'),scale=canvas.dataset.animation==='floki-hop'?6:2;
    canvas.width=meta.width*scale;canvas.height=meta.height*scale;ctx.imageSmoothingEnabled=false;
    let sum=0;const ends=meta.frames.map(frame=>(sum+=frame.ms));const state={canvas,ctx,meta,image,ends,sum,duration:sum+meta.hold,phase:0,index:0,visible:false};
    states.push(state);draw(state,0);canvas.hidden=false;canvas.parentElement.querySelector('.sprite-poster').hidden=true;observer.observe(canvas);
  }).catch(()=>{canvas.dataset.failed='true';}));
  toggles.forEach(button=>button.addEventListener('click',()=>{paused=!paused;labels();sync();}));
  reduced.addEventListener('change',()=>{paused=reduced.matches;labels();sync();});
  document.addEventListener('visibilitychange',sync);labels();
})();
