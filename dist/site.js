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
