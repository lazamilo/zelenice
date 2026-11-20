#!/usr/bin/env python3
"""Generates the Zelenice redesign pages into ./site from shared templates."""
import os, re, json, html as H

ON = ' class="on"'
JOB = ' data-job'
ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(ROOT, 'site')
LOGO = open(os.path.join(SITE, 'assets/img/logo.svg')).read()
LOGO = re.sub(r'<svg ', '<svg aria-hidden="true" ', LOGO, 1)

ARR = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 12h15M13 5l7 7-7 7"/></svg>'
CARET = '<svg class="caret" viewBox="0 0 12 12" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M2 4l4 4 4-4"/></svg>'
SNOW = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><path d="M12 2v20M4 6.5l16 11M20 6.5l-16 11M9 3.5l3 2.5 3-2.5M9 20.5l3-2.5 3 2.5"/></svg>'
DOWN = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 4v14M6 12l6 6 6-6M5 21h14"/></svg>'
CLOSE = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 5l14 14M19 5L5 19"/></svg>'

ACTS = [
 dict(id='urejanje-zelenih-povrsin', t='Urejanje zelenih površin', img='b-park', short='Košnja zelenic, nega dreves in grmovnic, urejanje parkov in zasaditev skozi vse leto.',
      p=['Skrbimo za urejene, varne in prijetne zelene površine v Mestni občini Celje. Izvajamo košnjo zelenic, nego dreves in grmovnic, urejanje parkov, zasaditev ter vzdrževanje javnih površin skozi vse leto.',
         'V jesenskem času izvajamo čiščenje listja in vejevja.',
         'Z uporabo sodobne opreme in strokovnim pristopom prispevamo k urejenemu, zelenemu in kakovostnemu življenjskemu okolju.']),
 dict(id='vrtnarstvo', t='Vrtnarstvo', img='b-cvet', short='Cvetlične grede, rondoji, živе meje in mestno drevje, ki izboljšuje kakovost bivanja.',
      p=['S strokovnim znanjem skrbimo za urejeno in zeleno podobo Mestne občine Celje. Izvajamo nego dreves, grmovnic, živih mej, cvetličnih zasaditev, trajnih nasadov ter drugih zelenih površin.',
         'Posebno pozornost namenjamo mestnemu drevju, ki izboljšuje kakovost bivanja, prispeva k čistejšemu zraku in ustvarja prijetnejše urbano okolje.',
         'S sezonskimi zasaditvami, urejanjem rondojev, cvetličnih gred in mestnega sadovnjaka skrbimo za privlačno podobo mesta skozi vse leto.',
         'Pri delu sledimo trajnostnim rešitvam ter postopoma uvajamo zasaditve, ki so prijaznejše okolju in dolgoročno učinkovitejše.']),
 dict(id='ciscenje-in-hisniska-opravila', t='Čiščenje in hišniška opravila', img='b-igrala', short='Čisti objekti, varna igrišča, urejene klopi, koši in mestna oprema.',
      p=['Skrbimo za čiste, urejene in varne javne ter poslovne prostore v Mestni občini Celje. Izvajamo redna in občasna čiščenja objektov, javnih površin, sanitarij ter drugih prostorov.',
         'Na področju hišniških opravil zagotavljamo vzdrževanje objektov, otroških in športnih igrišč, pešpoti ter urbane opreme. Skrbimo za popravila igral, urejanje varnostnih površin ter postavitev in vzdrževanje klopi, košev za odpadke in druge mestne opreme.',
         'Posebno skrb namenjamo priljubljenim rekreacijskim območjem, kot je Šmartinsko jezero, kjer prispevamo k urejenemu, varnemu in prijetnemu okolju za obiskovalce.',
         'Z odgovornim pristopom, natančnostjo in kakovostno izvedbo storitev skrbimo za prijetno bivalno okolje vseh generacij.']),
 dict(id='gradbena-operativa', t='Gradbena operativa', img='b-kosarka', short='Igrišča, pešpoti, sanacije javnih površin, ograje in zaključna dela.',
      p=['Izvajamo različna gradbena, vzdrževalna in obrtniška dela, s katerimi prispevamo k urejenemu, varnemu in funkcionalnemu javnemu prostoru v Mestni občini Celje.',
         'Sodelujemo pri obnovi in izgradnji otroških ter športnih igrišč, urejanju pešpoti, sanacijah javnih površin in vzdrževanju objektov. Izvajamo tudi manjša gradbena dela, popravila, montaže urbane opreme, izdelavo ograj ter zaključna dela v objektih.',
         'Z uporabo ustrezne mehanizacije in strokovnim pristopom skrbimo za kakovostno izvedbo del ter izboljšanje prostora za vsakodnevno uporabo občanov in obiskovalcev mesta.']),
 dict(id='pokopaliske-in-pogrebne-dejavnosti', t='Pokopališke in pogrebne dejavnosti', img='pok-veza', short='Upravljanje Mestnega pokopališča Celje in pokopališča Teharje ter pogrebne storitve.',
      p=['V podjetju Zelenice d. o. o. izvajamo pokopališko dejavnost v Mestni občini Celje, ki obsega upravljanje, urejanje in vzdrževanje pokopališč ter skrb za uporabnike pokopaliških storitev.',
         'Upravljamo in vzdržujemo Mestno pokopališče Celje ter pokopališče Teharje. Skrbimo za urejenost pokopaliških površin, poti in spremljajoče infrastrukture ter zagotavljamo izvajanje pogrebnih storitev s spoštljivim in dostojanstvenim pristopom.']),
 dict(id='gozdarska-dejavnost', t='Gozdarska dejavnost', img='drevored', short='Trajnostno upravljanje mestnih gozdov, gozdnih in učnih poti.',
      p=['Skrbimo za trajnostno upravljanje in urejenost mestnih gozdov Mestne občine Celje, ki predstavljajo pomemben prostor za sprostitev, rekreacijo, izobraževanje ter stik z naravo.',
         'Naše delo obsega vzdrževanje gozdnih in učnih poti, skrb za urbano opremo, sanacijo poškodovanih dreves, čiščenje podrasti ter izvajanje drugih ukrepov za varen in urejen gozdni prostor.',
         'Pri upravljanju sodelujemo s strokovnimi institucijami ter skrbimo za ohranjanje biotske raznovrstnosti in naravnega ravnovesja.',
         'Z odgovornim gospodarjenjem zagotavljamo, da mestni gozdovi ostajajo prijeten, varen in dostopen prostor za vse obiskovalce.']),
 dict(id='zimska-sluzba', t='Zimska služba', img='n-zima', short='Pluženje in posipavanje od 15. novembra do 15. marca. Dežurni telefon 041 966 800.',
      p=['Skrbimo za urejene, varne in dostopne javne površine skozi vse leto. Izvajamo redno vzdrževanje cest, pešpoti, pločnikov, parkirišč ter drugih javnih površin v Mestni občini Celje.',
         'V zimskem času zagotavljamo izvajanje zimske službe, ki poteka od 15. novembra do 15. marca in vključuje pluženje snega, posipavanje proti poledici, pripravo cest na zimske razmere ter čiščenje posipnega materiala po koncu sezone. Odstranjevanje snega se začne, ko višina snega na glavnih cestah doseže približno 10 cm, na ostalih cestah pa približno 15 cm.',
         'Z ustrezno mehanizacijo, organiziranimi ekipami in pravočasnim ukrepanjem skrbimo za varno mobilnost občanov ter nemoteno uporabo javnih površin v zimskih razmerah.']),
]

PROJ = [
 ('p-medlog','OKTOBER 2026','Zelena cona Medlog, nov prostor za druženje in rekreacijo','Na območju nekdanje drevesnice v Medlogu je nastal nov zeleni prostor za rekreacijo, druženje in preživljanje prostega časa. Pri urejanju območja smo sodelovali z gradbenimi in vrtnarskimi deli.'),
 ('p-smartinsko','AVGUST 2026','Šmartinsko jezero bogatejše za nove rekreacijske površine','Ob Šmartinskem jezeru smo sodelovali pri ureditvi balinišča, ruskega kegljišča in površin za namizni tenis ter izvedli obnovitvena dela na brvi in lesenih elementih.'),
 ('p-golovec','SEPTEMBER 2026','Prenovljene garderobe in kopalnice v dvorani Golovec','V poletnih mesecih smo sodelovali pri obnovi notranjih prostorov športne dvorane Golovec, kjer smo izvajali dela pri ureditvi kopalnic in garderob.'),
 ('p-lopata','JULIJ 2026','Obnovljeno športno igrišče in urejene igralne površine na Lopati','Na Lopati smo sodelovali pri urejanju športnega in otroškega igrišča, ki krajanom omogočata boljše pogoje za šport, igro in druženje.'),
 ('p-gabri','SEPTEMBER 2026','Na Bežigrajski cesti zasadili 80 črnih gabrov','Naša vrtnarska ekipa je marca 2026 na Bežigrajski cesti v Celju zasadila 80 črnih gabrov, ki bodo prispevali k bolj zeleni podobi mesta.'),
 ('p-vrtci','AVGUST 2026','Obnovitvena dela na objektih celjskih vrtcev','V letu 2026 smo sodelovali pri obnovitvenih delih na objektih celjskih vrtcev, med drugim pri urejanju notranjih prostorov, mansarde in strehe.'),
 ('p-zelene-ureditve','MAJ 2026','Nove zelene ureditve na več lokacijah v Celju','V okviru participativnega proračuna Mestne občine Celje smo izvajali nove zasaditve in ureditve zelenih površin, med drugim tudi pri vrtcu Mehurček.'),
 ('p-pespot','MAJ 2026','Ureditev peš poti okoli Šmartinskega jezera',''),
 ('p-krozisca','MAJ 2026','Spomladansko urejanje krožišč',''),
 ('p-stari-grad','MAJ 2026','Stari grad',''),
 ('p-igrisca','MAJ 2026','Ureditev otroških igrišč',''),
 ('p-zoga','MAJ 2026','Izdelava nogometne žoge',''),
 ('p-drevesa','MAJ 2026','Zasaditev dreves',''),
 ('p-cvetje','MAJ 2026','Ocvetličenje',''),
]

NEWS = [
 ('job','18. 11. 2026','Sporočilo o prostem delovnem mestu','Naziv delovnega mesta oz. vrsta dela: Pogrebnik 2, M/Ž.'),
 ('n-zima','17. 11. 2026','Zimska služba v Celju pripravljena na prihajajočo zimo','V javnem podjetju Zelenice smo pripravljeni na prihajajočo zimsko sezono. Zagotovili smo potrebno mehanizacijo, posipne materiale in organizirali dežurstva.'),
 ('n-sol','17. 11. 2026','Brezplačen prevzem soli za večstanovanjske stavbe','Tudi letos stanovalcem večstanovanjskih stavb omogočamo brezplačen prevzem soli za posipavanje.'),
 ('n-celebus','28. 10. 2026','Dodatne vožnje Celebusa ob dnevu spomina na mrtve','Za lažji dostop do Mestnega pokopališča Celje bomo ob dnevu spomina na mrtve organizirali dodatne vožnje Celebusa na linijah 12A in 12B.'),
 ('n-drevo','24. 12. 2025','Drevo hvaležnosti','Dne 15. 12. 2025 smo na Pokopališču Celje slovesno prižgali prvo drevo hvaležnosti. Drevo z lučkami simbolizira spomin, hvaležnost in povezanost ter vabi k tihemu razmisleku.'),
 ('n-pr','16. 10. 2025','Vsak korak med grobovi je korak med zgodbami, ki še živijo','Med mirnimi potmi in stoletnimi drevesi Mestnega pokopališča Celje od marca letos pišemo novo poglavje.'),
 ('n-zima2','06. 10. 2025','Povabilo k sodelovanju izvajanja zimske službe, sezona 2025/2026','Podjetje Zelenice d. o. o., ki se ukvarja z izvajanjem zimske službe (strojnim in ročnim čiščenjem snega, odstranitvijo snega, pluženjem ter posipom proti poledici), vabi zunanje izvajalce k sodelovanju.'),
]

def img(name, alt='', cls='', lazy=True):
    lz = ' loading="lazy"' if lazy else ''
    cl = ' class="%s"' % cls if cls else ''
    return f'<img src="assets/img/{name}.jpg" alt="{H.escape(alt)}"{lz}{cl}>'

def header(active='', light=False, pk=False):
    mega_items = ''.join(f'<li><a href="dejavnosti.html#{a["id"]}" data-img="{a["img"]}">{a["t"]}{ARR}</a></li>' for a in ACTS)
    mega_imgs = ''.join(f'<img src="assets/img/{a["img"]}.jpg" alt="" data-k="{a["img"]}"{ON if i==0 else ""}>' for i,a in enumerate(ACTS))
    def on(k): return ' class="on"' if active==k else ''
    sub = ''.join(f'<a href="dejavnosti.html#{a["id"]}">{a["t"]}</a>' for a in ACTS)
    return f'''
<a class="skip" href="#vsebina" style="position:absolute;left:-9999px">Skoči na vsebino</a>
<header class="hdr{' light' if light else ''}" id="hdr">
  <a class="logo" href="index.html" aria-label="Zelenice, domov">{LOGO}</a>
  <nav class="nav" aria-label="Glavni meni">
    <a href="o-podjetju.html"{on('o')}>O podjetju</a>
    <button type="button" id="megaBtn" aria-expanded="false">Dejavnosti{CARET}</button>
    <a href="projekti.html"{on('p')}>Projekti</a>
    <a href="aktualno.html"{on('a')}>Aktualno</a>
    <a href="kontakt.html"{on('k')}>Kontakt</a>
  </nav>
  <div class="hdr-r">
    <a class="btn btn-pok" href="pogrebne-storitve.html">Pokopališče in pogrebne storitve</a>
    <button class="burger" id="burger" aria-label="Meni"><i></i><i></i></button>
  </div>
</header>
<div class="mega" id="mega">
  <ul>{mega_items}</ul>
  <div class="mega-media">{mega_imgs}
    <div class="mega-card"><span>Dežurni telefon zimske službe</span><b><a href="tel:041966800">041 966 800</a></b></div>
  </div>
</div>
<div class="scrim" id="scrim"></div>
<div class="mnav" id="mnav">
  <div>
    <a class="big" href="index.html">Domov</a>
    <a class="big" href="o-podjetju.html">O podjetju</a>
    <a class="big" href="dejavnosti.html">Dejavnosti</a>
    <div class="sub">{sub}</div>
    <a class="big" href="projekti.html">Projekti</a>
    <a class="big" href="aktualno.html">Aktualno</a>
    <a class="big" href="kontakt.html">Kontakt</a>
    <a class="btn btn-w" style="margin-top:28px" href="pogrebne-storitve.html">Pokopališče in pogrebne storitve{ARR}</a>
  </div>
  <div class="foot">Cinkarniška pot 19, 3000 Celje<br><a href="tel:082052466">082 052 466</a> · <a href="mailto:info.zelenice@celje.si">info.zelenice@celje.si</a></div>
</div>'''

FOOTER = f'''
<footer class="ftr">
  <div class="ftr-top">
    <div><p class="claim">Skrb za urejen prostor. Za vsakdan ljudi.</p></div>
    <div><h5>Podjetje</h5><ul><li><a href="o-podjetju.html">O podjetju</a></li><li><a href="dejavnosti.html">Dejavnosti</a></li><li><a href="projekti.html">Projekti</a></li><li><a href="aktualno.html">Aktualno</a></li><li><a href="aktualno.html#zaposlovanje">Zaposlovanje</a></li><li><a href="kontakt.html">Kontakt</a></li></ul></div>
    <div><h5>Pokopališča</h5><ul><li><a href="pogrebne-storitve.html">Pogrebne storitve</a></li><li><a href="pogrebne-storitve.html#napotki">Napotki v primeru smrti</a></li><li><a href="pogrebne-storitve.html#pokopalisca">Mestno pokopališče Celje</a></li><li><a href="pogrebne-storitve.html#pokopalisca">Pokopališče Teharje</a></li><li><a href="pogrebne-storitve.html#obrazci">Vloge, obrazci in ceniki</a></li></ul></div>
    <div><h5>Kontakt</h5><ul><li>Cinkarniška pot 19<br>3000 Celje</li><li><a href="tel:082052466">082 052 466</a></li><li><a href="mailto:info.zelenice@celje.si">info.zelenice@celje.si</a></li><li style="margin-top:10px;color:rgba(255,255,255,.6);font-size:16px">Pon–pet, poleti 6.00–14.00<br>pozimi 7.00–15.00</li></ul></div>
  </div>
  <div class="ftr-logo">{LOGO}</div>
  <div class="ftr-bot"><span>© Javno podjetje Zelenice d.o.o., družba Mestne občine Celje</span><span><a href="#">Pravila varstva zasebnosti in piškotkov</a> · <a href="#">Pogoji uporabe</a> · <a href="#">Izjava o dostopnosti</a></span></div>
</footer>'''

def page(fn, title, body, active='', light=False, desc='', extra_cls=''):
    doc = f'''<!doctype html>
<html lang="sl" class="no-js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<meta name="description" content="{H.escape(desc or 'Javno podjetje Zelenice d.o.o., družba Mestne občine Celje za urejanje zelenih in javnih površin.')}">
<meta name="robots" content="noindex">
<link rel="icon" href="assets/img/favicon.svg" type="image/svg+xml">
<link rel="preload" href="assets/fonts/switzer-500.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="assets/css/style.css">
<script>document.documentElement.classList.remove('no-js');if(matchMedia('(prefers-reduced-motion: reduce)').matches)document.documentElement.classList.add('reduce')</script>
</head>
<body class="{extra_cls}">
{header(active, light)}
<main id="vsebina">
{body}
</main>
{FOOTER}
<script src="assets/js/vendor/gsap.min.js"></script>
<script src="assets/js/vendor/ScrollTrigger.min.js"></script>
<script src="assets/js/vendor/lenis.min.js"></script>
<script src="assets/js/main.js"></script>
</body>
</html>'''
    open(os.path.join(SITE, fn), 'w').write(doc)

def proj_card(p, cls='', i=0):
    k,d,t,txt = p
    return f'<a class="pc {cls}" href="projekti.html#p{i}" data-i="{i}">{img(k,t)}<span class="go">{ARR}</span><div class="pi"><div class="dt">{d.capitalize()}</div><h3>{t}</h3></div></a>'

def news_card(n, i=0):
    k,d,t,txt = n
    media = f'<div class="job"><span>Zaposlovanje</span><b>Pogrebnik 2</b><span>M/Ž · Pogrebna dejavnost</span></div>' if k=='job' else f'<div class="pframe">{img(k,t)}</div>'
    return f'<a class="nc rv" href="aktualno.html#n{i}">{media}<div class="dt">{d}</div><h3>{t}</h3><p>{txt}</p></a>'

CONTACT = f'''
<section class="sec wrap" id="kontakt">
  <div class="contact">
    <div>
      <h2 class="d2 rv">Imate vprašanje?</h2>
      <p class="lead mute rv" style="margin-top:20px">Pišite nam in z veseljem vam bomo odgovorili.</p>
      <form class="form rv" onsubmit="event.preventDefault();this.classList.add('sent');this.reset()">
        <div class="fld"><input id="f1" required placeholder=" "><label for="f1">Vaše ime</label></div>
        <div class="fld"><input id="f2" type="email" required placeholder=" "><label for="f2">Vaš e-mail naslov</label></div>
        <div class="fld full"><input id="f3" required placeholder=" "><label for="f3">Zadeva</label></div>
        <div class="fld full"><textarea id="f4" required placeholder=" "></textarea><label for="f4">Sporočilo</label></div>
        <label class="chk full"><input type="checkbox" required> Strinjam se s&nbsp;<a href="#">pravili in pogoji uporabe</a></label>
        <div class="full"><button class="btn btn-g" type="submit">Pošlji sporočilo{ARR}</button></div>
        <div class="form-ok">Hvala. Vaše sporočilo smo prejeli in vam odgovorimo v najkrajšem možnem času.</div>
      </form>
    </div>
    <div class="cinfo">
      <div class="rv"><h4>Sprejemna pisarna</h4><a class="big" href="tel:082052466">082 052 466</a><a class="big" href="mailto:info.zelenice@celje.si">info.zelenice@celje.si</a></div>
      <div class="rv"><h4>Naslov</h4><p>Javno podjetje Zelenice, družba za urejanje zelenih in drugih javnih površin, d.o.o.<br>Cinkarniška pot 19, 3000 Celje</p></div>
      <div class="rv"><h4>Delovni čas, ponedeljek do petek</h4><div class="hours"><div><small>Poletni</small><b>6.00–14.00</b></div><div><small>Zimski</small><b>7.00–15.00</b></div></div></div>
      <div class="rv"><h4>Dežurni telefon zimske službe</h4><a class="big" href="tel:041966800">041 966 800</a></div>
    </div>
  </div>
</section>'''

def topo():
    # generated contour lines for the facts band
    import math
    paths=[]
    for k in range(18):
        pts=[]
        for x in range(0,1601,40):
            y=60+k*42+math.sin(x/170+k*.55)*28+math.sin(x/61+k)*9+math.cos(x/330-k*.3)*36
            pts.append(f'{x},{y:.1f}')
        paths.append('<polyline points="'+' '.join(pts)+'"/>')
    return '<svg class="topo" viewBox="0 0 1600 820" preserveAspectRatio="none" fill="none" stroke="#7fb06a" stroke-width="1.2">'+''.join(paths)+'</svg>'

# ---------------- HOME ----------------
acts_list = ''.join(f'''<a class="act{' on' if i==0 else ''}" href="dejavnosti.html#{a['id']}" data-img="{a['img']}"><div class="act-t"><h3>{a['t']}</h3><span class="arr">{ARR}</span></div><p>{a['short']}</p><div class="mimg">{img(a['img'],a['t'])}</div></a>''' for i,a in enumerate(ACTS))
acts_media = ''.join(f'<img src="assets/img/{a["img"]}.jpg" alt="" data-k="{a["img"]}"{ON if i==0 else ""}>' for i,a in enumerate(ACTS))

home = f'''
<div class="loader" id="loader"><div class="loader-in"><div class="lg">{LOGO}</div><div class="bar"><i></i></div></div></div>
<section class="hero" id="hero">
  <div class="hero-media">{img('hero-celje','Cvetlična ureditev I love Celje',lazy=False)}{img('hero-park','Park v Celju z otroškim igriščem',lazy=False)}{img('b-medlog','Zelena cona Medlog',lazy=False)}</div>
  <div class="hero-video" id="heroVideo" aria-hidden="true"><video muted playsinline preload="auto"></video><video muted playsinline preload="auto"></video></div>
  <div class="hero-dots"><i class="on"></i><i></i><i></i></div>
  <div class="hero-in">
    <div>
      <h1 class="d1"><span class="l"><span>Skrb za urejen prostor.</span></span><span class="l"><span class="soft">Za vsakdan ljudi.</span></span></h1>
      <div class="hero-sub">
        <a class="btn btn-w" href="dejavnosti.html">Naše dejavnosti{ARR}</a>
        <p>Javno podjetje Mestne občine Celje za urejanje zelenih in javnih površin.</p>
      </div>
    </div>
    <aside class="hero-card" aria-label="Zimska služba">
      <div class="row"><span>Zimska služba je aktivna</span><span class="snow">{SNOW}</span></div>
      <h3>15. november do 15. marec</h3>
      <span>Dežurni telefon za nujne primere</span>
      <a class="tel" href="tel:041966800">041 966 800</a>
      <div class="bar"><i id="winterBar"></i></div>
    </aside>
  </div>
</section>

<section class="sec wrap" id="o-nas">
  <p class="statement" data-words>Skrbimo za urejeno, čisto in prijetno podobo Celja. Urejamo parke <span class="chip">{img('b-cvet')}</span> in zasaditve, igrišča <span class="chip">{img('igrala')}</span> in pešpoti, pozimi pa ceste in pločnike <span class="chip">{img('n-zima2')}</span> za vse generacije.</p>
  <div class="intro-grid">
    <p class="body-l rv">Kot izvajalec gospodarske javne službe za Mestno občino Celje urejamo, vzdržujemo in varujemo zelene ter druge javne površine, naše storitve pa izvajamo tudi za zunanje naročnike v širši regiji.</p>
    <div class="rv"><a class="link-a" href="o-podjetju.html">Spoznajte podjetje{ARR}</a></div>
  </div>
  <div class="trio">
    <div class="pframe" data-par>{img('b-medlog','Zelena cona Medlog')}</div>
    <div class="pframe" data-par>{img('p-gabri','Zasaditev črnih gabrov na Bežigrajski cesti')}</div>
    <div class="pframe" data-par>{img('drevored','Drevored v mestnem parku')}</div>
  </div>
</section>

<section class="acts sec wrap" id="dejavnosti">
  <div class="acts-head"><h2 class="d2 rv">Sedem področij,<br><span class="mute">eno mesto.</span></h2><a class="link-a rv" href="dejavnosti.html">Vse dejavnosti{ARR}</a></div>
  <div class="acts-grid">
    <div class="acts-media" id="actsMedia">{acts_media}<span class="tag">Mestna občina Celje</span></div>
    <div class="acts-list" id="actsList">{acts_list}</div>
  </div>
</section>

<section class="seasons" id="seasons">
  <div class="seasons-pin">
    <div class="seasons-head"><h2 class="d2">Mesto skozi <span>vse leto</span></h2><div class="s-progress"><span class="on">Pomlad</span><span>Poletje</span><span>Jesen</span><span>Zima</span></div></div>
    <div class="s-track" id="sTrack">
      <article class="s-panel spring"><div class="img">{img('hero-celje','Spomladanska cvetlična zasaditev')}</div><div class="txt"><div><div class="when">Pomlad</div><h3>Mesto zacveti</h3></div><p>S sezonskimi zasaditvami, urejanjem rondojev, cvetličnih gred in mestnega sadovnjaka skrbimo za privlačno podobo mesta. Spomladi uredimo krožišča in ocvetličimo mestne ulice.</p><div class="fact"><div><b>80</b><small>črnih gabrov na Bežigrajski</small></div></div></div></article>
      <article class="s-panel summer"><div class="img">{img('hero-park','Poletje v mestnem parku')}</div><div class="txt"><div><div class="when">Poletje</div><h3>Prostor za igro in druženje</h3></div><p>Košnja zelenic, varna otroška in športna igrišča ter urejeno Šmartinsko jezero. Skrbimo, da so priljubljena rekreacijska območja prijetna za vse obiskovalce.</p><div class="fact"><div><b>Šmartinsko jezero</b><small>nove rekreacijske površine</small></div></div></div></article>
      <article class="s-panel autumn"><div class="img">{img('p-drevesa','Jesenska zasaditev dreves')}</div><div class="txt"><div><div class="when">Jesen</div><h3>Listje, vejevje in nova drevesa</h3></div><p>V jesenskem času izvajamo čiščenje listja in vejevja ter skrbimo za mestno drevje, ki izboljšuje kakovost bivanja in prispeva k čistejšemu zraku.</p><div class="fact"><div><b>Mestni gozdovi</b><small>gozdne in učne poti</small></div></div></div></article>
      <article class="s-panel winter"><div class="img">{img('n-zima','Pluženje snega ponoči')}</div><div class="txt"><div><div class="when">Zima · 15. 11. do 15. 3.</div><h3>Varne ceste in pločniki</h3></div><p>Pluženje snega, posipavanje proti poledici in priprava cest na zimske razmere. Odstranjevanje snega se začne pri približno 10 cm na glavnih in 15 cm na ostalih cestah.</p><div class="fact"><div><b>041 966 800</b><small>dežurni telefon</small></div></div></div></article>
    </div>
  </div>
</section>

<section class="sec wrap" id="projekti">
  <div class="proj-head"><h2 class="d2 rv">Prostor, ki ga uporabljamo vsak dan</h2><div class="rv"><p class="body-l">Naše delo je vidno v številnih ureditvah po Celju. Med njimi so igrišča, parkovne ureditve, pešpoti in nove zelene površine.</p><p style="margin-top:24px"><a class="link-a" href="projekti.html">Vsi projekti{ARR}</a></p></div></div>
  <div class="bento">
    {proj_card(PROJ[0],'b1 rv',0)}{proj_card(PROJ[1],'b2 rv',1)}
    {proj_card(PROJ[4],'b3 rv',4)}{proj_card(PROJ[3],'b4 rv',3)}{proj_card(PROJ[2],'b5 rv',2)}
  </div>
</section>

<section class="facts sec-s wrap">
  {topo()}
  <h2 class="d3 rv">Javno podjetje, ki skrbi za podobo Celja</h2>
  <div class="facts-in">
    <div class="fact-i rv"><b data-count="2020">2020</b><span>leto ustanovitve družbe</span></div>
    <div class="fact-i rv"><b data-count="7">7</b><span>dejavnosti pod eno streho</span></div>
    <div class="fact-i rv"><b data-count="2">2</b><span>mestni pokopališči v upravljanju</span></div>
    <div class="fact-i rv"><b data-count="80">80</b><span>novih črnih gabrov na Bežigrajski cesti</span></div>
    <div class="fact-i rv"><b data-count="24">24</b><span>ur na dan dežurna pogrebna služba</span></div>
  </div>
</section>

<section class="cem sec wrap" id="pokopalisca">
  <div class="cem-grid">
    <div>
      <h2 class="d2 rv">Z vami v najtežjih trenutkih</h2>
      <p class="lead rv">Z razumevanjem in spoštovanjem svojcem nudimo pomoč pri organizaciji ter izvedbi pogrebnih storitev. Skrbimo za urejen in spoštljiv prostor spomina.</p>
      <div class="rv" style="margin-top:36px;display:flex;gap:12px;flex-wrap:wrap"><a class="btn btn-w" href="pogrebne-storitve.html">Pogrebne storitve{ARR}</a><a class="btn btn-glass" href="pogrebne-storitve.html#napotki">Napotki v primeru smrti</a></div>
    </div>
    <div class="pframe cem-img" data-par>{img('pok-arkade','Arkade Mestnega pokopališča Celje')}</div>
  </div>
  <div class="cem-cards">
    <a class="cc rv" href="pogrebne-storitve.html#pokopalisca"><h3>Mestno pokopališče Celje</h3><p>Celje, Babno, Dobrova, Košnica pri Celju, Lokrovec, Lopata, Medlog, Ostrožno, Pečovnik, Polule, Trnovlje pri Celju, Zgornja Hudinja, Lisce, Zagrad ter druga pripadajoča območja.</p></a>
    <a class="cc rv" href="pogrebne-storitve.html#pokopalisca"><h3>Pokopališče Teharje</h3><p>Teharje, Bukovžlak, Slance, Vrhe, Pečovje ter pripadajoči deli okoliških naselij.</p></a>
    <div class="cc hl rv"><div><p>Dežurna pogrebna služba</p><h3 style="margin-top:6px">Dosegljivi 24 ur na dan</h3></div><a class="tel" href="tel:041748904">041 748 904</a></div>
  </div>
</section>

<section class="sec wrap" id="aktualno">
  <div class="news-head"><h2 class="d2 rv">Aktualno</h2><a class="link-a rv" href="aktualno.html">Vse novice{ARR}</a></div>
  <div class="news">{news_card(NEWS[1],1)}{news_card(NEWS[2],2)}{news_card(NEWS[0],0)}</div>
</section>

<section class="bigcta">
  {img('nova-igrala','Nova igrala Nova vas')}
  <div class="in"><h2 class="d1">Nova igrala<br>Nova vas</h2><a class="btn btn-w" href="projekti.html">Preberi več{ARR}</a></div>
</section>
{CONTACT}
'''
page('index.html','Zelenice · Skrb za urejen prostor v Celju', home)

# ---------------- O PODJETJU ----------------
about = f'''
<section class="phero">
  <div class="crumbs"><a href="index.html">Domov</a><span>/</span><span>O podjetju</span></div>
  <div class="phero-grid"><h1 class="d1 rv">Naše delo je del podobe mesta</h1><p class="lead rv">Javno podjetje Zelenice d. o. o., Celje skrbi za urejeno, čisto in prijetno podobo mesta.</p></div>
</section>
<div class="pframe wide-img" data-par>{img('b-medlog','Zelena cona Medlog',lazy=False)}</div>
<section class="sec wrap">
  <div class="intro-grid" style="margin-top:0;align-items:start">
    <h2 class="d3 rv">Skrbno za urejeno, čisto in prijetno podobo mesta</h2>
    <div class="rv"><p class="body-l">Kot izvajalec gospodarske javne službe za Mestno občino Celje urejamo, vzdržujemo in varujemo zelene ter druge javne površine, naše storitve pa izvajamo tudi za zunanje naročnike v širši regiji.</p>
    <p class="body-l" style="margin-top:18px">Naše glavne dejavnosti obsegajo vzdrževanje zelenih površin, nego dreves in grmovnic, urejanje trat, parkov in cvetličnih zasaditev, skrb za otroška igrišča, urbano opremo ter javne površine. Izvajamo tudi zimsko službo, čiščenje objektov, hišniška in vzdrževalna dela, pogrebno in pokopališko dejavnost ter razvijamo programe na področju gozdarstva.</p>
    <p class="body-l" style="margin-top:18px">Z izkušenim kadrom, strokovnim znanjem in sodobno opremo zagotavljamo kakovostne, zanesljive in trajnostno usmerjene storitve.</p></div>
  </div>
</section>
<section class="wrap">
  <div class="mv">
    <div class="m rv"><h2 class="d3">Poslanstvo</h2><div><p>Poslanstvo Javnega podjetja Zelenice d. o. o. je usmerjeno v skrb za urejanje in vzdrževanje zelenih in drugih javnih površin z namenom zagotavljanja kakovostnega življenjskega okolja.</p><p>S krepitvijo dolgoročnih partnerstev in vključevanjem v krožno gospodarstvo si prizadevamo za večjo prisotnost na trgu dela. Naša strategija delovanja temelji na načelih trajnostnega razvoja.</p></div></div>
    <div class="v rv"><h2 class="d3">Vizija</h2><div><p>Želimo biti prepoznani kot vodilni in zanesljiv izvajalec storitev urejanja ter vzdrževanja zelenih in drugih javnih površin. Sledimo sodobnim trendom, uvajamo učinkovite rešitve ter zagotavljamo kakovostne, okolju in uporabnikom prijazne storitve.</p><p>Poseben poudarek namenjamo zadovoljstvu uporabnikov in odprti komunikaciji z občankami in občani.</p></div></div>
  </div>
  <div class="values rv"><span>Strokovnost</span><span>Odgovornost</span><span>Zanesljivost</span><span>Inovativnost</span><span>Skrb za okolje</span></div>
</section>
<section class="sec wrap">
  <div class="trio" style="margin-top:0">
    <div class="pframe" data-par>{img('about-team','Ekipa Zelenice')}</div>
    <div class="pframe" data-par>{img('b-cvet','Cvetlična greda v parku')}</div>
    <div class="pframe" data-par>{img('b-pot','Pešpot ob potoku')}</div>
  </div>
</section>
<section class="sec-s wrap" style="padding-top:0">
  <div class="idcard">
    <div><h2 class="d3 rv">Osebna izkaznica</h2>
      <a class="dl rv" style="margin-top:40px" href="assets/docs/Zelenice-predstavitvena-brosura.pdf" target="_blank"><div><div class="d4">Predstavitvena brošura</div><p class="mute" style="font-size:16px;margin-top:6px">PDF · 1 MB</p></div><span class="ic">{DOWN}</span></a>
    </div>
    <div class="idt rv">
      <div><small>Naziv podjetja</small><span>Javno podjetje Zelenice, družba za urejanje zelenih in drugih javnih površin d.o.o.</span></div>
      <div><small>Skrajšani naziv</small><span>JP Zelenice d.o.o.</span></div>
      <div><small>Naslov</small><span>Cinkarniška pot 19, 3000 Celje</span></div>
      <div><small>Leto ustanovitve</small><span>2020</span></div>
      <div><small>Matična številka</small><span>8557217000</span></div>
      <div><small>Davčna številka</small><span>SI 85060453</span></div>
      <div><small>TRR, Delavska hranilnica d. d.</small><span>SI56 6100 0002 3944 797</span></div>
      <div><small>TRR, pogrebna in pokopališka dejavnost</small><span>SI56 6100 0003 0707 055</span></div>
      <div><small>Šifra dejavnosti</small><span>81.300, urejanje in vzdrževanje zelenih površin in okolice</span></div>
      <div><small>Telefon in e-naslov</small><span>082 052 466<br>info.zelenice@celje.si</span></div>
      <div><small>Direktor</small><span>Jože Krulec</span></div>
      <div><small>Predsednik nadzornega sveta</small><span>Boštjan Plevnik</span></div>
    </div>
  </div>
</section>
<section class="sec-s wrap">
  <div class="news-head" id="zaposlovanje"><h2 class="d2 rv">Zaposlovanje</h2></div>
  <div class="news">{news_card(NEWS[0],0)}</div>
</section>
{CONTACT}'''
page('o-podjetju.html','O podjetju · Zelenice', about, 'o', light=True)

# ---------------- DEJAVNOSTI ----------------
dj_nav = ''.join(f'<a href="#{a["id"]}">{a["t"]}</a>' for a in ACTS)
def dj_sec(a):
    ps = a['p']; half=(len(ps)+1)//2
    extra=''
    if a['id']=='zimska-sluzba': extra=f'<div class="callout rv"><div><p style="opacity:.75">Dežurni telefon zimske službe za nujne primere</p><b><a href="tel:041966800">041 966 800</a></b></div><span class="snow" style="width:64px;height:64px;color:var(--lime)">{SNOW}</span></div>'
    if a['id'].startswith('pokopaliske'): extra=f'<div class="callout rv"><div><p style="opacity:.75">Mestno pokopališče Celje in pokopališče Teharje</p><b>Pokopališče in pogrebne storitve</b></div><a class="btn btn-w" href="pogrebne-storitve.html">Odpri{ARR}</a></div>'
    return f'''<section class="dj-sec" id="{a['id']}"><h2 class="d2 rv">{a['t']}</h2><div class="pframe rv" data-par>{img(a['img'],a['t'])}</div>
<div class="dj-cols rv"><div>{''.join(f'<p>{x}</p>' for x in ps[:half])}</div><div>{''.join(f'<p>{x}</p>' for x in ps[half:])}</div></div>{extra}</section>'''
dej = f'''
<section class="phero">
  <div class="crumbs"><a href="index.html">Domov</a><span>/</span><span>Dejavnosti</span></div>
  <div class="phero-grid"><h1 class="d1 rv">Sedem področij,<br><span class="mute">eno mesto</span></h1><p class="lead rv">Od košnje zelenic in cvetličnih gred do gradbenih del, pokopališč in zimske službe.</p></div>
</section>
<section class="wrap" style="padding-bottom:40px">
  <div class="dj"><nav class="dj-nav" id="djNav">{dj_nav}</nav><div>{''.join(dj_sec(a) for a in ACTS)}</div></div>
</section>
<section class="bigcta">{img('nova-igrala','Nova igrala Nova vas')}<div class="in"><h2 class="d1">Nova igrala<br>Nova vas</h2><a class="btn btn-w" href="projekti.html">Projekti{ARR}</a></div></section>
{CONTACT}'''
page('dejavnosti.html','Dejavnosti · Zelenice', dej, 'd', light=True)

# ---------------- PROJEKTI ----------------
cards = ''
for i,p in enumerate(PROJ):
    cards += proj_card(p, 'rv' + (' w' if i in (0,) else ''), i)
proj = f'''
<section class="phero">
  <div class="crumbs"><a href="index.html">Domov</a><span>/</span><span>Projekti</span></div>
  <div class="phero-grid"><h1 class="d1 rv">Prostor, ki ga uporabljamo vsak dan</h1><p class="lead rv">Igrišča, parkovne ureditve, pešpoti in nove zelene površine po Celju. Izpostavljamo nekaj primerov različnih vrst izvedenih del.</p></div>
</section>
<section class="wrap" style="padding-bottom:clamp(96px,10vw,180px)"><div class="pgrid" id="pgrid">{cards}</div></section>
<div class="modal" id="modal"><div class="modal-box" style="position:relative"><button class="modal-x" id="modalX" aria-label="Zapri">{CLOSE}</button><div class="im"><img id="mImg" alt=""></div><div class="tx"><div class="mute" id="mDate" style="font-weight:500"></div><h2 class="d4" id="mTitle"></h2><p class="body-l" id="mText"></p><a class="link-a" href="kontakt.html" style="align-self:flex-start;margin-top:auto">Pišite nam{ARR}</a></div></div></div>
<script>window.PROJ={json.dumps([dict(img=p[0],date=p[1].capitalize(),t=p[2],txt=p[3] or 'Projekt Javnega podjetja Zelenice v Mestni občini Celje.') for p in PROJ],ensure_ascii=False)}</script>
{CONTACT}'''
page('projekti.html','Projekti · Zelenice', proj, 'p', light=True)

# ---------------- AKTUALNO ----------------
rows=''
for i,n in enumerate(NEWS):
    k,d,t,txt=n
    media = '<div class="pframe" style="background:var(--green);color:#fff;display:flex;align-items:flex-end;padding:22px"><b style="font-size:30px;font-weight:500;letter-spacing:-.03em;line-height:1">Pogrebnik 2</b></div>' if k=='job' else f'<div class="pframe">{img(k,t)}</div>'
    rows += f'<article class="nrow rv" id="n{i}"{JOB if k=="job" else ""}><div class="dt">{d}</div><div><h3>{t}</h3><p>{txt}</p></div>{media}</article>'
akt = f'''
<section class="phero">
  <div class="crumbs"><a href="index.html">Domov</a><span>/</span><span>Aktualno</span></div>
  <div class="phero-grid"><h1 class="d1 rv">Aktualno</h1><p class="lead rv">Obvestila, novice in prosta delovna mesta Javnega podjetja Zelenice.</p></div>
</section>
<section class="wrap" id="zaposlovanje" style="padding-bottom:clamp(96px,10vw,180px)"><div class="nlist">{rows}</div></section>
{CONTACT}'''
page('aktualno.html','Aktualno · Zelenice', akt, 'a', light=True)

# ---------------- KONTAKT ----------------
kon = f'''
<section class="phero" style="padding-bottom:0">
  <div class="crumbs"><a href="index.html">Domov</a><span>/</span><span>Kontakt</span></div>
  <h1 class="d1 rv">Kontakt</h1>
</section>
{CONTACT}
<section class="wrap" style="padding-bottom:clamp(96px,10vw,180px)">
  <div class="cem-cards" style="margin-top:0">
    <a class="cc rv" style="background:var(--navy);color:#fff" href="pogrebne-storitve.html#kontakt"><div><p>Pogrebna dejavnost</p><h3 style="margin-top:6px">03 542 12 00</h3></div><p>Mirna pot 2, 3000 Celje</p></a>
    <a class="cc rv" style="background:var(--navy);color:#fff" href="tel:041748904"><div><p>Dežurna pogrebna služba, 24 ur</p><h3 style="margin-top:6px">041 748 904</h3></div><p>Dosegljivi vsak dan</p></a>
    <a class="cc rv" style="background:var(--lime);color:var(--ink)" href="tel:041966800"><div><p style="color:#24332d">Zimska služba, dežurni telefon</p><h3 style="margin-top:6px">041 966 800</h3></div><p style="color:#24332d">15. november do 15. marec</p></a>
  </div>
</section>'''
page('kontakt.html','Kontakt · Zelenice', kon, 'k', light=True)

# ---------------- POGREBNE STORITVE ----------------
I_HELP = '<svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M8 26c4-2 8-2 12 1l6 4c1.5 1 1 3.5-1 3.5h-7"/><path d="M4 40l8-5c3-2 6-2 9-1l9 3c2 .6 4 .2 5.5-1L44 28"/><path d="M30 8a5 5 0 017 7l-7 7-7-7a5 5 0 017-7z"/></svg>'
I_ORG = '<svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="1.6"><rect x="8" y="10" width="32" height="30" rx="3"/><path d="M8 18h32M16 6v8M32 6v8M15 26h6M15 32h12"/></svg>'
I_GRAVE = '<svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M14 40V20a10 10 0 0120 0v20"/><path d="M8 40h32M24 18v10M20 22h8"/></svg>'
I_FIND = '<svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="1.6"><circle cx="21" cy="21" r="12"/><path d="M30 30l10 10M21 15v12M16 19h10"/></svg>'
docs = [('Izjava o spremembi naslova',None),('Izjava za odstop najemništva',None),('Izjava za prenos najemništva',None),('Najemna pogodba za grob',None),('Pooblastilo kamnoseštva',None),('Vloga za izdajo dovoljenja za prekop ali prenos posmrtnih ostankov',None),('Vloga za pridobitev soglasja za kamnoseška dela',None),
        ('Cenik gospodarske javne službe pokopališke in pogrebne dejavnosti','assets/docs/Cenik-gospodarske-javne-sluzbe-izvajanja-pokopaliske-in-pogrebne-dejavnosti.pdf'),('Cenik tržnih pokopaliških storitev','assets/docs/Cenik-trznih-pokopaliskih-storitev.pdf'),('Priročnik za organizacijo pogreba','assets/docs/Pogrebni-prirocnik.pdf')]
docs_html = ''.join(f'<a class="doc rv" href="{u or "https://www.zelenice.si/pogrebne-storitve/storitve/pokopalisca-in-grobovi"}" target="_blank"><span>{t}<small>PDF</small></span>{DOWN}</a>' for t,u in docs)
pk = f'''
<section class="pk-hero">
  {img('pok-hero','Vhod na Mestno pokopališče Celje',lazy=False)}
  <div class="in">
    <h1 class="d1 rv">Z vami<br><span class="soft">v najtežjih trenutkih</span></h1>
    <div class="pk-24 rv"><small>Dežurna pogrebna služba, 24 ur na dan</small><a href="tel:041748904">041 748 904</a><small>Sprejemna pisarna: 03 542 12 00</small></div>
  </div>
</section>
<section class="sec wrap" style="color:var(--navy)">
  <div class="phero-grid" style="margin-bottom:clamp(48px,5vw,96px)"><h2 class="d2 rv">Kako vam lahko pomagamo?</h2><p class="lead rv" style="color:#4c6380">V podjetju Zelenice d. o. o. z odgovornostjo in spoštovanjem izvajamo pogrebno in pokopališko dejavnost. Svojcem nudimo pomoč pri organizaciji pogrebnih slovesnosti ter skrbimo za urejena in dostojna pokopališča.</p></div>
  <div class="pk-help">
    <a class="ph rv" href="#napotki">{I_HELP}<div><h3>Napotki v primeru smrti</h3><p>Informacije o prvih korakih in ureditvi pogreba.</p></div></a>
    <a class="ph rv" href="#organizacija">{I_ORG}<div><h3>Organizacija pogreba</h3><p>Pomagamo pri pripravi in izvedbi pogrebne slovesnosti.</p></div></a>
    <a class="ph rv" href="#pokopalisca">{I_GRAVE}<div><h3>Pokopališča in grobovi</h3><p>Informacije o pokopališčih, najemu in urejanju grobnih mest.</p></div></a>
    <a class="ph rv" href="https://www.zelenice.si/pogrebne-storitve/pokopalisca" target="_blank">{I_FIND}<div><h3>Iskalnik grobov</h3><p>Hitro in enostavno poiščite lokacijo grobnega mesta.</p></div></a>
  </div>
</section>
<section class="wrap" style="color:var(--navy)">
  <div class="acc on rv" id="napotki"><button>Ko nastopi smrt na domu<i></i></button><div class="ab"><div><div class="inner"><p>V primeru smrti na domu je treba obvestiti dežurnega zdravnika oziroma mrliškega preglednika, ki opravi pregled pokojnika, ugotovi vzrok smrti in izda potrebno dokumentacijo. Za območje Mestne občine Celje je mrliški preglednik dosegljiv na telefonski številki <b>031 869 928</b>.</p><p>V primeru suma na nasilno smrt ali druge izredne okoliščine pokličite <b>112</b>. Po opravljenem mrliškem pregledu se lahko obrnete na pogrebno službo Zelenice d. o. o., kjer poskrbimo za prevzem in prevoz pokojnika ter vam pomagamo pri nadaljnjih postopkih.</p></div></div></div></div>
  <div class="acc rv"><button>Ko nastopi smrt v bolnišnici ali domu starejših<i></i></button><div class="ab"><div><div class="inner"><p>Če smrt nastopi v bolnišnici ali domu starejših, svojci prejmejo obvestilo ustanove, kjer je pokojnik umrl.</p><p>Za ureditev nadaljnjih postopkov se lahko obrnete na našo pogrebno službo, kjer vam bomo pomagali pri prevozu pokojnika, pripravi dokumentacije ter organizaciji pogrebne slovesnosti.</p></div></div></div></div>
  <div class="acc rv" id="organizacija"><button>Ureditev pogreba<i></i></button><div class="ab"><div><div class="inner"><div><p>V sprejemni pisarni pogrebne in pokopališke dejavnosti lahko svojci uredijo vse potrebno za izvedbo pogreba na enem mestu. Pomagamo vam pri:</p><ul><li>izbiri vrste pogreba,</li><li>določitvi kraja, dneva in ure pogrebne slovesnosti,</li><li>izbiri pogrebne opreme,</li><li>pripravi poslovilne slovesnosti,</li><li>objavi osmrtnice,</li><li>urejanju potrebnih postopkov.</li></ul></div><div><p>Za lažjo ureditev postopkov s seboj imejte:</p><ul><li>zdravniško potrdilo o smrti,</li><li>poročilo o vzroku smrti,</li><li>osebni dokument pokojnika,</li><li>podatek o obstoječem grobnem mestu (če obstaja),</li><li>fotografijo pokojnika za pripravo osmrtnice.</li></ul></div></div></div></div></div>
  <div class="acc rv"><button>Najem in prenos grobnega prostora<i></i></button><div class="ab"><div><div class="inner"><p>Grobni prostor se odda v najem na podlagi sklenjene najemne pogodbe. Najemnina se obračunava enkrat letno skladno z veljavnim cenikom. Najem se uredi ob potrebi oziroma v skladu s pokopališkim redom.</p><p>Prenos najemništva grobnega prostora se uredi v sprejemni pisarni podjetja Zelenice d. o. o. Obstoječi najemnik poda izjavo o prenosu, na podlagi katere se pripravi nova najemna pogodba.</p></div></div></div></div>
</section>
<section class="sec wrap" style="color:var(--navy)">
  <h2 class="d2 rv" style="margin-bottom:clamp(40px,4vw,72px)">Oblike pokopov</h2>
  <div class="burial">
    <div class="rv"><div class="pframe">{img('b-grobovi','Grobna polja')}</div><div class="t"><h3>Pokop s krsto</h3><p>Pokojnik je položen v krsto in pokopan v grob ali grobnico.</p></div></div>
    <div class="rv"><div class="pframe">{img('pok-right','Žarni grobovi')}</div><div class="t"><h3>Žarni pokop</h3><p>Upepeljeni ostanki pokojnika se shranijo v žaro in položijo v grob, grobnico ali žarno nišo.</p></div></div>
    <div class="rv"><div class="pframe">{img('n-raztros','Raztros pepela')}</div><div class="t"><h3>Raztros pepela</h3><p>Raztros pepela se opravi na posebej določenem prostoru pokopališča.</p></div></div>
  </div>
</section>
<section class="cem sec wrap" id="pokopalisca">
  <div class="cem-grid"><div><h2 class="d2 rv">Pokopališča v našem upravljanju</h2><p class="lead rv">Skrbimo za upravljanje, urejanje in vzdrževanje pokopališč ter zagotavljamo urejen in spoštljiv prostor spomina.</p></div><div class="pframe cem-img" data-par>{img('pok-left','Mestno pokopališče Celje')}</div></div>
  <div class="cem-cards">
    <div class="cc rv"><h3>Mestno pokopališče Celje</h3><p>Celje, Babno, Dobrova, Košnica pri Celju, Lokrovec, Lopata, Medlog, Ostrožno, Pečovnik, Polule, Trnovlje pri Celju, Zgornja Hudinja, Lisce, Zagrad ter druga pripadajoča območja.</p></div>
    <div class="cc rv"><h3>Pokopališče Teharje</h3><p>Teharje, Bukovžlak, Slance, Vrhe, Pečovje ter pripadajoči deli okoliških naselij.</p></div>
    <div class="cc hl rv"><div><p>Sredstva iz najemnin so namenjena</p><h3 style="margin-top:6px">poti, zelenim površinam, drevesom, urbani opremi, vodnjakom, odvozu odpadkov in zimski službi</h3></div></div>
  </div>
</section>
<section class="sec wrap" style="color:var(--navy)">
  <div class="phero-grid" style="margin-bottom:clamp(40px,4vw,72px)"><h2 class="d2 rv">Vzdrževanje in urejanje grobov</h2><p class="lead rv" style="color:#4c6380">Za grobno mesto lahko poskrbimo namesto vas. Izberite paket, ki vam ustreza.</p></div>
  <div class="pack"><div class="top rv"><h3>Premium paket</h3><div><b>12×</b><p>letno vzdrževanje</p></div></div><div class="rv"><h3>Standardni paket</h3><div><b>6×</b><p>letno čiščenje</p></div></div><div class="rv"><h3>Osnovni paket</h3><div><b>3×</b><p>letno čiščenje</p></div></div></div>
</section>
<section class="sec-s wrap" id="obrazci" style="padding-top:0;color:var(--navy)">
  <h2 class="d3 rv" style="margin-bottom:40px">Vloge, obrazci in ceniki</h2>
  <div class="docs">{docs_html}</div>
</section>
<section class="cem sec wrap" id="kontakt">
  <h2 class="d2 rv" style="margin-bottom:clamp(40px,4vw,72px)">Kontakti</h2>
  <div class="pk-contacts">
    <div class="rv"><h3>Pogrebna dejavnost</h3><p>Informacije in pomoč pri organizaciji pogrebnih storitev</p><a href="tel:035421200">T 03 542 12 00</a><a href="tel:041748904">M 041 748 904</a><a href="mailto:jerneja.pogrebnik@gmail.com">jerneja.pogrebnik@gmail.com</a></div>
    <div class="rv"><h3>Pokopališka dejavnost</h3><p>Informacije o grobnih mestih ter urejanje pokopališča</p><a href="tel:035421201">T 03 542 12 01</a><a href="tel:041847000">M 041 847 000</a><a href="mailto:pokopalisce@celje.si">pokopalisce@celje.si</a></div>
    <div class="rv"><h3>Sprejemna pisarna</h3><p>Mirna pot 2, 3000 Celje<br>Ponedeljek do petek: 8. do 15. ure<br>Sobota: po dogovoru<br>Nedelja in prazniki: zaprto</p><a href="https://maps.google.com/?q=Mirna+pot+2,+3000+Celje" target="_blank">Poglej na zemljevidu</a></div>
  </div>
</section>'''
page('pogrebne-storitve.html','Pokopališče in pogrebne storitve · Zelenice', pk, '', light=False, extra_cls='pk')
print('built')
