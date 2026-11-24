from pathlib import Path
from html import escape as esc
import json
root=Path(__file__).resolve().parent
out=root/'dist'
books=json.loads((root/'books.json').read_text())
pages=json.loads((root/'pages.json').read_text())
original=json.loads((root/'original-pages.json').read_text())
pages['translations']['books'].extend(original['additionalTranslations'])
def icon(name):
    paths={'book':'<path d="M3 5q5-2 9 1 4-3 9-1v14q-5-2-9 1-4-3-9-1z M12 6v14"/>','mail':'<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m4 7 8 6 8-6"/>','sun':'<circle cx="12" cy="12" r="4"/><path d="M12 1v3m0 16v3M1 12h3m16 0h3M4 4l2 2m12 12 2 2M4 20l2-2M18 6l2-2"/>','menu':'<path d="M3 6h18M3 12h18M3 18h18"/>','search':'<circle cx="10" cy="10" r="6"/><path d="m15 15 6 6"/>','heart':'<path d="M12 20S2 14 2 8a5 5 0 0 1 10-1 5 5 0 0 1 10 1c0 6-10 12-10 12Z"/>'}
    return '<svg class="icon" aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round" stroke-linecap="round">'+paths[name]+'</svg>'
def link(url,label,cls=''):
    return f'<a class="{cls}" href="{esc(url,quote=True)}">{label}</a>'
brand=link('/','Mandy Baggot<span>♡</span>','brand')
nav=[('Home','/'),('The Books','/books/'),('About Mandy','/about/'),('Translations','/translations/'),('Book Club','/book-club/'),('Contact','/contact/')]
def page(path,title,body):
    navlinks=''.join(f'<a href="{url}"'+(' aria-current="page"' if path==url or (url!="/" and path.startswith(url)) else '')+f'>{txt}</a>' for txt,url in nav)
    nl=link('/newsletter/',icon('mail')+' Newsletter','newsletter')
    header=f'<header><div class="wrap head">{brand}<nav id="nav">{navlinks}</nav>{nl}<button class="menubtn" aria-label="Open menu" aria-controls="nav" aria-expanded="false">{icon("menu")}</button></div></header>'
    foot='<footer><div class="wrap foot">'+brand+'<div>'+''.join(link(u,t) for t,u in nav[1:])+link('/movie-and-tv/','Movie & TV')+link('/signed-copies/','Signed copies')+link('/home-old/','Archive')+link('/social/','Social updates')+link('/newsletter/','Newsletter')+'</div></div><div class="wrap legal">© 2026 Mandy Baggot</div></footer>'
    target=out/path.strip('/')/'index.html'
    target.parent.mkdir(parents=True,exist_ok=True)
    target.write_text(f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{esc(title)} · Mandy Baggot</title><meta name="theme-color" content="#fcf9f2"><link rel="stylesheet" href="/assets/fonts.css"><link rel="stylesheet" href="/style.css"><script defer src="/site.js"></script></head><body><a class="skip" href="#main">Skip to content</a>{header}<main id="main">{body}</main>{foot}</body></html>')
def card(b,url=None,i=0):
    title = esc(b['title'])
    destination = url or '/books/' + b['slug'] + '/'
    panel_id = 'synopsis-' + destination.strip('/').replace('/', '-')
    panel = f'<div class="blurb" id="{panel_id}" hidden><strong>{title}</strong>{paras(b["description"])}<button type="button" class="close-preview">Close synopsis</button></div>'
    button = f'<button class="preview-toggle" aria-controls="{panel_id}" aria-expanded="false" aria-label="Synopsis for {title}"><img loading="lazy" src="{b["cover"]}" alt=""><span>Synopsis</span></button>'
    shop_url = b['url'] if 'url' in b else b['links'][0]['url']
    buy = 'Pre-order' if b.get('slug') == 'feels-like-summer' else 'Buy this edition'
    return f'<article class="card tone{i%5}" data-title="{esc(b["title"].casefold())}" data-lang="{esc(b.get("language",""))}"><div class="coverwell">{button}{panel}</div><h3>{link(destination,title)}</h3>{link(shop_url,buy,"shoplink")}</article>'
def row(items):
    return '<div class="grid">'+''.join(card(b,i=i) for i,b in enumerate(items))+'</div>'
def over(s):
    return f'<div class="over">{s}</div>'
def paras(t):
    return ''.join('<p>'+esc(x.strip()).replace(' .','.').replace(' !','!')+'</p>' for x in t.split('\n') if x.strip())
def cta(u,t):return link(u,t,'btn')
about=pages['about']
postcard='<div class="post-scene"><div class="postcard"><span class="tape"></span><img fetchpriority="high" src="/assets/corfu.jpg" alt="Bougainvillea overlooking a turquoise Corfu bay"><div class="caption">With love from Corfu <span>♡</span></div></div><div class="postmark" aria-hidden="true"><span>CORFU</span>'+icon('sun')+'<small>GREECE</small></div></div>'
hero='<section class="hero"><div class="wrap hero-grid"><div class="hero-text">'+over(icon('sun')+' BESTSELLING ROMANTIC FICTION')+'<h1>Love stories,<br><em>faraway shores.</em></h1><p>Escape with Mandy Baggot to sun-drenched islands, snow-kissed cities, and a happy ever after.</p><div class="actions">'+cta('/books/',icon('book')+' Explore the books')+link('/about/','Meet Mandy','textlink')+'</div></div>'+postcard+'</div></section>'
shelf='<section class="wrap shelf">'+over('THE BOOKSHELF')+'<div class="sectionhead"><h2>Your next escape</h2>'+link('/books/','View all books','textlink')+'</div>'+row(books[:5])+'</section>'
homemore='<section class="aboutband"><div class="wrap split"><img loading="lazy" src="'+about['portrait']+'" alt="Mandy Baggot"><div>'+over('MEET THE AUTHOR')+'<h2>A note from Mandy</h2>'+paras(about['introduction'])+link('/about/','More about Mandy','textlink')+'</div></div></section>'
m=pages['movie-and-tv']
def trailer():
    return '<div class="trailer"><iframe loading="lazy" title="A Greek Recipe for Romance — official Hallmark preview" src="https://www.youtube.com/embed/CAlGv3y7OEU" referrerpolicy="strict-origin-when-cross-origin" allow="encrypted-media; picture-in-picture; fullscreen" allowfullscreen></iframe></div>'
film_section = '<section class="wrap homefilm"><div>'+over('MOVIE &amp; TV')+'<h2>'+esc(m['film'])+'</h2>'+paras(m['description'])+link('/movie-and-tv/','Explore the film','textlink')+'</div><div>'+trailer()+link(m['trailer'],'Watch on YouTube','shoplink')+'</div></section>'
page('/','Romantic fiction',hero+shelf+film_section+homemore+'<section class="wrap endnote">'+over('THE MANDY BAGGOT BOOK CLUB')+'<h2>What are you reading?</h2><p>Come chat about your favourite reads and see my new covers first.</p>'+cta('/book-club/','Discover the book club')+'</section>')
def intro(label,title,sub=''):
    return over(label)+'<h1>'+esc(title)+'</h1>'+('<p class="lead">'+esc(sub)+'</p>' if sub else '')
def listing(trans=False):
    items=pages['translations']['books'] if trans else books
    sel=''
    if trans:
        sel='<label>Language<select id="language"><option value="">All languages</option>'+''.join('<option>'+esc(x)+'</option>' for x in sorted({b['language'] for b in items}))+'</select></label>'
    controls='<div class="filters"><label>Search by title<span class="searchbox">'+icon('search')+'<input id="find" type="search" placeholder="Find a book…" autocomplete="off"></span></label>'+sel+'<span id="count" role="status">'+str(len(items))+' books</span></div>'
    cards=''.join(card(b,f'/translations/edition-{i+1}/' if trans else None,i) for i,b in enumerate(items))
    return '<section class="wrap inside">'+intro('THE INTERNATIONAL BOOKSHELF' if trans else 'THE BOOKSHELF','Translations' if trans else 'The books', 'Explore Mandy’s stories in translation.' if trans else 'Sunshine, snow and a little romance. Find your next escape.')+controls+'<div class="grid">'+cards+'</div><p id="empty" hidden>No titles match your search. <button id="clear">Clear filters</button></p></section>'
page('/books/','The books',listing())
page('/translations/','Translations',listing(True))
def detail(b,path,back,buttons,tag):
    page(path,b['title'],'<section class="wrap inside">'+link(back,'All '+('translations' if back=='/translations/' else 'books'),'textlink back')+'<div class="detail"><div class="detailcover"><img src="'+b['cover']+'" alt="'+esc(b['title'])+' cover"></div><div>'+intro(tag,b['title'])+paras(b['description'])+'<div class="actions">'+buttons+'</div></div></div></section>')
for i,b in enumerate(books):
    detail(b,'/books/'+b['slug']+'/','/books/',''.join(cta(l['url'],('Pre-order on ' if i==0 else 'Buy on ')+l['label']) for l in b['links'])+link('/signed-copies/','Enquire about a signed copy','textlink'),'MANDY BAGGOT · ROMANTIC FICTION')
for i,b in enumerate(pages['translations']['books']):
    detail(b,f'/translations/edition-{i+1}/','/translations/',cta(b['url'],'Find this edition'),esc(b['language']).upper()+' EDITION')
def editorial(path,title,label,body,img=None,alt=''):
    content=intro(label,title)+body
    if img:content='<div class="editorgrid"><div>'+content+'</div><figure><img src="'+img+'" alt="'+alt+'"></figure></div>'
    else:content='<div class="prose">'+content+'</div>'
    page(path,title,'<section class="wrap inside">'+content+'</section>')
editorial('/about/','Meet Mandy','ABOUT THE AUTHOR',paras(about['introduction'])+''.join(paras(p) for p in about['paragraphs'])+link('/movie-and-tv/','From book to screen','textlink')+'<h2>Inside my stories</h2><p>'+esc(' · '.join(about['tropes']))+'</p><details class="season"><summary>Did you know?</summary>'+paras(about['seasonalUpdate'])+'</details>',about['portrait'],'Author Mandy Baggot')
nl=pages['newsletter']
form=f'<form action="{esc(nl["action"])}" method="post"><label>Your name<input name="NAME" autocomplete="given-name"></label><label>Email address<input name="EMAIL" autocomplete="email" type="email" required></label><div class="trap" aria-hidden="true"><input tabindex="-1" name="{nl["trap"]}" autocomplete="off"></div><button class="btn">Subscribe</button></form>'
editorial('/newsletter/','Letters from Mandy','THE NEWSLETTER','<p>Sign up for book news, cover reveals, offers and competitions, straight from Mandy.</p>'+form,'/assets/corfu.jpg','A postcard view of Corfu')
club=pages['book-club']
editorial('/book-club/','The Mandy Baggot Book Club','READ WITH MANDY','<p>Love feel-good fiction? Join Mandy and fellow readers to talk about books, swap recommendations and play What Are You Drinking Friday.</p><h2>First on the reading list</h2><ul>'+''.join('<li>'+esc(x)+'</li>' for x in club['exclusives'])+'</ul>'+cta(club['link']['url'],'Join the Facebook group'),club['image'],'Mandy at a café in Corfu')
c=pages['contact']
editorial('/contact/','Get in touch','CONTACT MANDY','<h2>Reader messages</h2><p>Send Mandy a message or follow her latest book news.</p>'+cta(c['message']['url'],c['message']['label'])+'<div class="social">'+''.join(link(a['url'],a['label'],'textlink') for a in c['social'])+'</div><h2>Literary enquiries</h2>'+link(c['agent']['url'],c['agent']['label'],'textlink')+'<h2>Signed books</h2>'+link('/signed-copies/','Enquire about a signed copy','textlink'))
editorial('/signed-copies/','Signed copies','FROM MANDY’S BOOKSHELF','<p>Message Mandy with the title you’d like signed and your delivery country to ask about availability and postage.</p>'+cta(c['message']['url'],'Message Mandy on Facebook'))
m=pages['movie-and-tv']
editorial('/movie-and-tv/',m['film'],'FROM BOOK TO SCREEN',paras(m['description'])+trailer()+'<div class="actions">'+cta(m['trailer'],'Watch on YouTube')+link(m['url']+'/videos/sneak-peek-a-greek-recipe-for-romance','Watch the sneak peek on Hallmark','textlink')+link(m['url'],'Film on Hallmark','textlink')+'</div><h2>Read the novel</h2>'+link('/books/desperately-seeking-summer/','Desperately Seeking Summer','textlink'),books[-1]['cover'],'Desperately Seeking Summer book cover')

legacy = original['legacy']
english_by_title = {b['title']: b for b in books}
editions_by_title = {b['title']: (i,b) for i,b in enumerate(pages['translations']['books'],1)}
archived_books = row([english_by_title[t] for t in legacy['englishTitles']])
archived_editions = []
for title in legacy['translationTitles']:
    number, edition = editions_by_title[title]
    archived_editions.append(card(edition,f'/translations/edition-{number}/',number))
archive_links = ''.join(link(url,label,'textlink') for label,url in [
    ('About Mandy','/about/'),('Newsletter','/newsletter/'),('Book Club','/book-club/'),
    ('Social updates','/social/'),('Contact Mandy','/contact/'),('Signed copies','/signed-copies/')])
page('/home-old/','Archive · April 2026','<section class="wrap inside">'+intro('FROM THE ARCHIVE','April 2026')+
     '<div class="archivenote">'+paras(legacy['seasonalUpdate'])+'</div><div class="archive-links">'+archive_links+'</div><h2>The bookshelf</h2>'+
     archived_books+'<h2>Translations</h2><div class="grid">'+''.join(archived_editions)+'</div></section>')
def social_post(post):
    caption=post['caption'].split('#')[0].strip()
    return '<li>'+paras(caption)+link(post['url'],'View on Instagram','textlink')+'</li>'
page('/social/','Social updates','<section class="wrap inside">'+intro('FROM MANDY','Social updates')+
     '<div class="social">'+''.join(link(a['url'],a['label'],'textlink') for a in c['social'])+
     '</div><ul class="post-list">'+''.join(social_post(item) for item in original['socialPosts'])+'</ul></section>')
