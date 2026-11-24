const menu = document.querySelector('.menubtn');
const nav = document.querySelector('nav');
function closeMenu() {
  nav.classList.remove('open');
  menu.setAttribute('aria-expanded','false');
  menu.setAttribute('aria-label','Open menu');
}
menu.addEventListener('click', () => {
  if (nav.classList.contains('open')) return closeMenu();
  nav.classList.add('open');
  menu.setAttribute('aria-expanded','true');
  menu.setAttribute('aria-label','Close menu');
});
document.addEventListener('keydown', e => {
  if (e.key === 'Escape' && nav.classList.contains('open')) {closeMenu();menu.focus();}
});
const search = document.querySelector('#find');
if (search) {
  const lang=document.querySelector('#language');
  function update(){
    let count=0;
    for(const book of document.querySelectorAll('.card')){
      book.hidden = !book.dataset.title.includes(search.value.toLowerCase().trim()) || Boolean(lang?.value && book.dataset.lang !== lang.value);
      if (!book.hidden) count++;
    }
    document.querySelector('#count').textContent=count+' '+(count===1?'book':'books');
    document.querySelector('#empty').hidden=count!==0;
  }
  search.addEventListener('input',update);
  lang?.addEventListener('change',update);
  document.querySelector('#clear').addEventListener('click',()=>{search.value='';if(lang)lang.value='';update();search.focus();});
}

for (const button of document.querySelectorAll('.preview-toggle')) {
  const well = button.parentElement;
  const panel = document.getElementById(button.getAttribute('aria-controls'));
  panel.tabIndex = 0;
  function show(open) {
    button.setAttribute('aria-expanded', String(open));
    panel.hidden = !open;
  }
  well.addEventListener('pointerenter', event => {
    if (event.pointerType === 'mouse') show(true);
  });
  well.addEventListener('pointerleave', event => {
    if (event.pointerType === 'mouse' && !well.contains(document.activeElement)) show(false);
  });
  button.addEventListener('focus', () => {
    if (button.matches(':focus-visible')) show(true);
  });
  button.addEventListener('click', () => {
    show(true);
    panel.focus({preventScroll:true});
  });
  panel.querySelector('.close-preview').addEventListener('click', () => {
    button.focus({preventScroll:true});
    show(false);
  });
  well.addEventListener('focusout', event => {
    if (!well.contains(event.relatedTarget)) show(false);
  });
  well.addEventListener('keydown', event => {
    if (event.key === 'Escape') {
      button.focus({preventScroll:true});
      show(false);
    }
  });
}
