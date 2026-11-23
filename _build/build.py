"""Generates the static pages of hamraahadvisors.com.

Run:  python3 _build/build.py   (from the repo root)
Edit content here, rebuild, commit the generated .html files.
"""
import json, os, datetime, html, re, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://www.hamraahadvisors.com"
BRAND = "Hamraah Advisors"
LEGAL = "Hamraah Advisors (SMC-Private) Limited"
EMAIL = "info@hamraahadvisors.com"
WHATSAPP = "923354471262"
WHATSAPP_DISPLAY = "+92 335 4471262"
ADDRESS = "Office 12, Business Avenue, Islamabad"  # placeholder
TODAY = datetime.date.today().isoformat()

NAV = [
    ("/", "Home"),
    ("/how-it-works", "How it works"),
    ("/services", "Services"),
    ("/experts", "Experts"),
    ("/pricing", "Pricing"),
    ("/about", "About"),
    ("/faq", "FAQ"),
    ("/blog", "Blog"),
]

# ---------------------------------------------------------------- data
JOURNEY = [
    ("Profile Evaluation", "Academic and financial assessment",
     "We review your grades, CGPA, English test scores, finances and goals, then tell you honestly where you stand."),
    ("Career & Country Selection", "Choose the right study destination",
     "Together we match your goals and budget to the right country, degree and career path."),
    ("University Admissions", "University selection and applications",
     "A balanced shortlist, strong applications, and SOP and recommendation guidance from people who were admitted themselves."),
    ("Financial Documentation", "Genuine proof-of-funds guidance",
     "We explain exactly what banks, sponsors and affidavits must show, and check your genuine documents before you submit."),
    ("Scholarships & Funding", "Funding and scholarship opportunities",
     "We help you find and apply for scholarships, assistantships and university funding you actually qualify for."),
    ("Visa Documentation", "DS-160 and supporting documents",
     "Step-by-step DS-160 guidance, SEVIS and appointment help, and a complete document checklist."),
    ("Visa Interview Preparation", "Mock interviews with US-based experts",
     "Practise the F-1 interview with experts who passed it, and learn how to answer clearly and honestly."),
    ("Post-Arrival Support", "Accommodation, travel and student life",
     "Housing, flights, airport arrival, your first week, and connections to Pakistani students on campus."),
]

SERVICES = [
    ("student-assessment", "Student Assessment",
     "Know exactly where you stand before you spend a rupee on applications.",
     ["Academic profile and CGPA review", "English proficiency (IELTS, TOEFL, Duolingo)",
      "Financial capacity assessment", "Career goals and university shortlist"], None),
    ("university-admissions", "University Admissions",
     "Applications that tell your story, guided by people who were admitted to US universities.",
     ["University and program selection", "SOP and personal statement guidance",
      "Recommendation letter guidance", "Application submission and scholarships"], None),
    ("financial-documentation", "Financial Documentation",
     "Clear guidance on proving you can fund your studies, the honest way.",
     ["Bank statement and sponsor requirements", "Affidavit of support guidance",
      "Tuition and living cost planning", "Document verification checklist"],
     "We help you prepare <strong>genuine</strong> documents only. We never create or alter bank statements or financial records."),
    ("us-visa-preparation", "US Visa Preparation",
     "Walk into your F-1 interview prepared and confident.",
     ["DS-160 form guidance", "F-1 interview mock sessions",
      "Common questions and 214(b) refusals explained", "Visa documentation checklist"], None),
    ("pre-departure-arrival", "Pre-Departure & Arrival",
     "Everything you need to sort out between your visa and your first class.",
     ["Accommodation guidance", "Flights and travel preparation",
      "Airport arrival and first-week checklist", "Understanding university policies"], None),
    ("life-in-the-usa", "Life in the USA",
     "Settle in faster with a mentor who is living it right now.",
     ["On-campus employment guidance", "Banking, phone and daily essentials",
      "Connecting with Pakistani student communities", "A mentor who is a current US student"], None),
]

EXPERTS = [
    ("US Admissions Expert", "University applications · Scholarships · SOP", "cap",
     "Helps you choose universities, build a balanced list and write applications that stand out."),
    ("F-1 Visa Guidance Expert", "Visa interviews · DS-160 · Documentation", "card",
     "Prepares you for the DS-160 and the F-1 interview with realistic mock sessions."),
    ("Financial Documentation Expert", "Proof of funds · Sponsorship · Budget planning", "bank",
     "Explains what your bank statements and sponsor documents must show, and checks them with you."),
    ("Current US Student Mentor", "Student life · Housing · Campus experience", "person",
     "A Pakistani student in the USA right now, who answers the questions nobody else can."),
]

ICONS = {
    "cap": '<path d="M12 3 1 9l11 6 9-4.9V17h2V9zM5 13.2v4L12 21l7-3.8v-4L12 17z"/>',
    "card": '<path d="M4 4h16a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2zm2 4v2h5V8zm0 4v2h8v-2zm10-4a2 2 0 1 0 0 4 2 2 0 0 0 0-4z"/>',
    "bank": '<path d="M3 10h18v2H3zm2 3h2v6H5zm4 0h2v6H9zm4 0h2v6h-2zm4 0h2v6h-2zM3 20h18v2H3zM12 1l10 5v2H2V6z"/>',
    "person": '<path d="M12 12a4 4 0 1 0 0-8 4 4 0 0 0 0 8zm0 2c-4 0-8 2-8 5v1h16v-1c0-3-4-5-8-5z"/>',
}

SESSIONS = [  # key, label, duration, price, description
    ("30-minute consultation", "Quick consultation", "30 min", 25,
     "Ask your key questions and leave with a clear next step."),
    ("60-minute consultation", "In-depth consultation", "60 min", 45,
     "A full review of your profile, options and plan, with written notes."),
    ("Visa interview mock session", "Visa interview mock", "45 min", 40,
     "Practise the F-1 interview with a US-based expert and get honest feedback."),
    ("Financial documentation session", "Financial documentation review", "45 min", 40,
     "Check your proof of funds and sponsor documents before you submit."),
    ("University admission strategy session", "Admission strategy", "60 min", 50,
     "Build your university list and a step-by-step application plan."),
]

PACKAGES = [  # name, price, lede, items, featured
    ("Basic", 79, "Know where you stand.",
     ["Full profile evaluation", "One 60-minute expert session", "Written recommendations and next steps"], False),
    ("Standard", 349, "Get admitted.",
     ["Everything in Basic", "University shortlist (up to 6)", "Application support for up to 4 universities",
      "SOP review, two rounds", "Scholarship search"], False),
    ("Premium", 649, "From admission to visa.",
     ["Everything in Standard", "Financial documentation guidance", "DS-160 and visa document checklist",
      "Two F-1 mock interviews with US-based experts"], True),
    ("Complete", 999, "With you all the way.",
     ["Everything in Premium", "A dedicated expert from start to finish", "Applications for up to 8 universities",
      "Pre-departure preparation", "Three months of post-arrival support"], False),
]

PROMISES = [
    ("Verified experts", "Real qualifications, current location and experience, checked by us."),
    ("Transparent pricing", "Prices on our website and in writing. No hidden charges."),
    ("No visa guarantees", "Visa decisions belong only to the embassy or consulate. Anyone who guarantees a visa is not being honest with you."),
    ("Written agreement", "You know exactly what we will do before you start."),
    ("Genuine documents only", "We guide you to prepare real records. We never fabricate or alter anything."),
    ("Secure document handling", "Your passport, bank statements and personal details stay private."),
    ("A dedicated coordinator", "One person who knows your file and answers your questions."),
    ("Clear refund policy", "Cancellation and refund conditions explained upfront."),
]

FAQS = [
    ("Who are the experts?",
     "Pakistani graduates, working professionals and current students living in the USA. Each one has been through US admissions and the F-1 visa process personally, and we verify their background before they join Hamraah."),
    ("Can you guarantee my visa?",
     "No, and nobody honestly can. Visa decisions are made only by the US embassy or consulate. We make sure your application, documents and interview preparation are as strong and as genuine as possible."),
    ("How do sessions work?",
     "Choose a session type and, if you like, an expert. We confirm a time that suits both of you and send a Zoom or Google Meet link. Sessions are available in Pakistan and US time zones."),
    ("How much does it cost?",
     "Single sessions start at $25 and packages start at $79. Every price is listed on our pricing page, and you receive it in writing before you pay."),
    ("Can I pay in Pakistani rupees?",
     "Yes. Prices are listed in US dollars, and you can pay the equivalent in PKR at the current exchange rate."),
    ("Are university and visa fees included?",
     "No. University application fees, English test fees, the SEVIS fee and the US visa fee are paid directly by you to the relevant organisation. We tell you exactly which fees apply to you."),
    ("Which countries do you cover?",
     "Our main focus is the USA. We also guide students applying to selected countries and universities in Europe. Ask us about your destination."),
    ("Do you help with bank statements?",
     "We explain exactly what your financial documents must show and check your genuine documents with you. We never create, edit or arrange financial documents. Doing so is fraud and can lead to a permanent visa ban."),
    ("What if I want to cancel?",
     "Single sessions can be rescheduled or refunded with at least 24 hours' notice. Package cancellation and refund terms are set out in your written service agreement before you pay."),
    ("I live in the USA. Can I become a Hamraah expert?",
     "Yes. If you are a Pakistani graduate, professional or student in the USA and want to guide students, email us with your background and we will be in touch."),
]

# ---------------------------------------------------------------- helpers
e = html.escape


def svg_icon(name):
    return f'<svg viewBox="0 0 24 24">{ICONS[name]}</svg>'


def section_head(eyebrow, title, sub=None, left=False):
    s = f'<div class="section-head{" left" if left else ""}"><p class="eyebrow">{eyebrow}</p><h2>{title}</h2><span class="rule"></span>'
    if sub:
        s += f'<p class="sub">{sub}</p>'
    return s + "</div>"


def journey(detailed=False):
    items = "".join(
        f'<li><h3>{e(t)}</h3><p>{e(long if detailed else short)}</p></li>' for t, short, long in JOURNEY)
    return f'<ol class="journey{" detailed" if detailed else ""}">{items}</ol>'


def services_grid(detailed=True, link=False):
    out = []
    for i, (slug, title, intro, bullets, note) in enumerate(SERVICES, 1):
        body = f'<p class="svc-intro">{e(intro)}</p>' if detailed else ""
        body += "<ul>" + "".join(f"<li>{e(b)}</li>" for b in bullets) + "</ul>"
        if note and detailed:
            body += f'<p class="note">{note}</p>'
        if link:
            body += f'<a class="more" href="/services#{slug}">Learn more</a>'
        out.append(f'<article class="service" id="{slug}"><span class="idx">{i:02d}</span><h3>{e(title)}</h3>{body}</article>')
    return f'<div class="services three">{"".join(out)}</div>'


def experts_grid(detailed=False):
    cards = []
    for name, tags, icon, desc in EXPERTS:
        q = name.replace(" ", "+")
        extra = f'<p class="desc">{e(desc)}</p>' if detailed else ""
        cards.append(
            f'<article class="expert"><div class="avatar" aria-hidden="true">{svg_icon(icon)}</div>'
            f'<h3>{e(name)}</h3><p class="tags">{e(tags)}</p>{extra}<p class="verified">Verified profile</p>'
            f'<a class="btn btn-outline" href="/book?expert={q}">Book this expert</a></article>')
    return f'<div class="experts">{"".join(cards)}</div>'


def sessions_grid():
    cards = []
    for key, name, dur, price, desc in SESSIONS:
        q = key.replace(" ", "+")
        cards.append(
            f'<a class="session" href="/book?session={q}"><span class="dur">{dur}</span>'
            f'<span class="name">{e(name)}</span><span class="price">${price}</span>'
            f'<span class="desc">{e(desc)}</span><span class="go">Book now</span></a>')
    return f'<div class="sessions">{"".join(cards)}</div>'


def packages_grid():
    cards = []
    for name, price, lede, items, featured in PACKAGES:
        badge = '<span class="badge">Most chosen</span>' if featured else ""
        btn = "btn-gold" if featured else "btn-outline"
        cards.append(
            f'<article class="pkg{" featured" if featured else ""}">{badge}<h3>{name}</h3>'
            f'<p class="amount"><span class="cur">$</span>{price}<span class="per">one-time</span></p>'
            f'<p class="pkg-lede">{e(lede)}</p><ul>{"".join(f"<li>{e(i)}</li>" for i in items)}</ul>'
            f'<a class="btn {btn}" href="/book?session=Package:+{name}">Choose {name}</a></article>')
    return f'<div class="packages">{"".join(cards)}</div>'


def promises_grid(items=PROMISES):
    return '<div class="promises">' + "".join(
        f"<div><h3>{e(t)}</h3><p>{e(d)}</p></div>" for t, d in items) + "</div>"


def compare():
    return '''<div class="compare">
  <div class="compare-col them"><p class="kicker">A typical consultancy</p><ul>
    <li>One general agent for every student</li>
    <li>Advice second-hand, from people who never studied abroad</li>
    <li>Fees and "guarantees" that change later</li>
    <li>Support ends when the visa is stamped</li></ul></div>
  <div class="compare-col us"><p class="kicker">Hamraah</p><ul>
    <li>You choose the expert who fits your goals</li>
    <li>Guidance from Pakistanis living and working in the USA</li>
    <li>Written agreement, clear prices, no false promises</li>
    <li>Support continues after you land</li></ul></div>
</div>'''


def faq_list(items):
    return '<div class="faq">' + "".join(
        f"<details><summary>{e(q)}</summary><p>{e(a)}</p></details>" for q, a in items) + "</div>"


def cta_band(title="Your journey is easier with the right companion.", button="Book a session", href="/book"):
    return f'''<section class="band"><div class="pattern" aria-hidden="true"></div>
<div class="wrap band-inner"><h2>{title}</h2><a class="btn btn-gold" href="{href}">{button}</a></div></section>'''


def page_hero(eyebrow, title, lede, crumb):
    return f'''<section class="hero page-hero"><div class="pattern" aria-hidden="true"></div>
<div class="wrap"><nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a><span aria-hidden="true">/</span><span aria-current="page">{e(crumb)}</span></nav>
<p class="eyebrow">{eyebrow}</p><h1>{title}</h1><p class="lede">{lede}</p></div></section>'''


def section(inner, cls="", sid=None, pattern=False):
    idattr = f' id="{sid}"' if sid else ""
    pat = '<div class="pattern" aria-hidden="true"></div>' if pattern else ""
    return f'<section class="section {cls}"{idattr}>{pat}<div class="wrap">{inner}</div></section>'


# ---------------------------------------------------------------- structured data
ORG = {
    "@type": "EducationalOrganization",
    "@id": SITE + "/#organization",
    "name": BRAND,
    "legalName": LEGAL,
    "url": SITE + "/",
    "logo": SITE + "/assets/logo/hamraah-crest-full-colour.png",
    "image": SITE + "/assets/og-image.jpg",
    "email": EMAIL,
    "slogan": "Learn from people already living your dream.",
    "description": "Expert-led study-abroad consultancy in Pakistan connecting students with Pakistani experts living in the USA for admissions, scholarships, financial documentation, F-1 visa preparation and post-arrival support.",
    "areaServed": {"@type": "Country", "name": "Pakistan"},
    "knowsAbout": ["Study in the USA", "F-1 student visa", "US university admissions", "Scholarships", "Study in Europe"],
}
WEBSITE = {"@type": "WebSite", "@id": SITE + "/#website", "url": SITE + "/", "name": BRAND,
           "publisher": {"@id": SITE + "/#organization"}, "inLanguage": "en"}


def breadcrumbs(path, name):
    trail = [("Home", "/")]
    if isinstance(name, tuple):  # (parent_name, parent_path, name)
        trail.append((name[0], name[1]))
        name = name[2]
    trail.append((name, path))
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i, "name": n, "item": SITE + u} for i, (n, u) in enumerate(trail, 1)]}


def faq_schema(items):
    return {"@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in items]}


def offers_schema():
    offers = [{"@type": "Offer", "name": n, "price": str(p), "priceCurrency": "USD",
               "url": SITE + "/pricing", "description": d} for _, n, _, p, d in SESSIONS]
    offers += [{"@type": "Offer", "name": f"{n} package", "price": str(p), "priceCurrency": "USD",
                "url": SITE + "/pricing", "description": "; ".join(items)} for n, p, _, items, _ in PACKAGES]
    return {"@type": "Service", "serviceType": "Study abroad consultancy",
            "provider": {"@id": SITE + "/#organization"}, "areaServed": "Pakistan",
            "offers": offers}


# ---------------------------------------------------------------- layout
def layout(path, title, desc, body, schema=(), crumb=None, og_type="website", image=None):
    canonical = SITE + (path if path != "/" else "/")
    nav = "".join(
        f'<a href="{href}"{" aria-current=\"page\"" if href == path or (href != "/" and path.startswith(href + "/")) else ""}>{label}</a>' for href, label in NAV)
    image = image or SITE + "/assets/og-image.jpg"
    graph = [ORG, WEBSITE] + list(schema)
    if crumb:
        graph.append(breadcrumbs(path, crumb))
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, indent=1)
    year = datetime.date.today().year
    return f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{e(title)}</title>
  <meta name="description" content="{e(desc)}">
  <link rel="canonical" href="{canonical}">
  <meta name="robots" content="index, follow, max-image-preview:large">
  <meta name="theme-color" content="#6B1E2E">
  <link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
  <link rel="icon" href="/assets/favicon-32.png" sizes="32x32" type="image/png">
  <link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
  <meta property="og:type" content="{og_type}">
  <meta property="og:site_name" content="{BRAND}">
  <meta property="og:locale" content="en_PK">
  <meta property="og:url" content="{canonical}">
  <meta property="og:title" content="{e(title)}">
  <meta property="og:description" content="{e(desc)}">
  <meta property="og:image" content="{image}">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="Hamraah Advisors crest and logo">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{e(title)}">
  <meta name="twitter:description" content="{e(desc)}">
  <meta name="twitter:image" content="{image}">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=Inter:wght@400;500;600&family=Noto+Nastaliq+Urdu:wght@500&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/styles.css">
  <script type="application/ld+json">
{ld}
  </script>
</head>
<body>
  <a class="skip" href="#main">Skip to content</a>
  <header class="site-header" id="top">
    <div class="wrap header-inner">
      <a class="brand" href="/" aria-label="Hamraah Advisors home">
        <img class="brand-light" src="/assets/logo/hamraah-horizontal-full-colour.svg" alt="Hamraah Advisors" width="729" height="230">
        <img class="brand-dark" src="/assets/logo/hamraah-horizontal-reversed.svg" alt="" width="729" height="230" aria-hidden="true">
      </a>
      <button class="nav-toggle" aria-expanded="false" aria-controls="nav" aria-label="Open menu"><span></span><span></span><span></span></button>
      <nav class="nav" id="nav" aria-label="Main">{nav}<a class="btn btn-small" href="/book">Book a session</a></nav>
    </div>
  </header>
  <main id="main">
{body}
  </main>
  <footer class="site-footer">
    <div class="wrap footer-inner">
      <div class="footer-brand">
        <img src="/assets/logo/hamraah-horizontal-gold-foil.svg" alt="Hamraah Advisors" width="729" height="230">
        <p>Your global education partner</p>
      </div>
      <nav class="footer-nav" aria-label="Footer">{nav}<a href="/book">Book a session</a></nav>
      <div class="footer-contact">
        <a href="mailto:{EMAIL}">{EMAIL}</a>
        <a href="https://wa.me/{WHATSAPP}" target="_blank" rel="noopener">WhatsApp {WHATSAPP_DISPLAY}</a>
        <p class="urdu" lang="ur" dir="rtl">ہمراہ ۔ آپ کے ہر قدم کے ساتھ</p>
      </div>
    </div>
    <div class="wrap legal">
      <p>© {year} {LEGAL}. All rights reserved.</p>
      <p>Visa decisions are made solely by the relevant embassy or consulate. Hamraah does not guarantee admission or visa outcomes.</p>
    </div>
  </footer>
  <a class="wa-float" href="https://wa.me/{WHATSAPP}" target="_blank" rel="noopener" aria-label="Chat with Hamraah on WhatsApp"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm5.3 14.1c-.2.6-1.3 1.2-1.8 1.3-.5 0-1 .2-3.3-.7a11.6 11.6 0 0 1-4.6-4c-.4-.5-1.1-1.6-1.1-3s.7-2 1-2.3a1 1 0 0 1 .8-.4h.6c.2 0 .4 0 .6.5l.9 2.1c.1.2.1.4 0 .6l-.4.6-.4.5c-.1.1-.3.3-.1.6a8.7 8.7 0 0 0 4.3 3.8c.3.1.5.1.6-.1l.9-1.1c.2-.3.4-.2.6-.1l2 1c.3.1.5.2.5.3a2.4 2.4 0 0 1-.1 1.3z"/></svg></a>
  <script src="/main.js" defer></script>
</body>
</html>
'''


# ---------------------------------------------------------------- pages
PAGES = {}


def page(path, filename, title, desc, crumb=None, schema=(), priority="0.8"):
    def deco(fn):
        PAGES[filename] = (path, title, desc, fn, crumb, schema, priority)
        return fn
    return deco


@page("/", "index.html",
      "Study in the USA with Pakistani Experts | Hamraah Advisors",
      "Study-abroad consultancy in Pakistan. Book 1:1 sessions with Pakistani experts living in the USA for admissions, scholarships and F-1 visa preparation.",
      priority="1.0")
def home():
    hero = f'''<section class="hero"><div class="pattern" aria-hidden="true"></div>
<div class="wrap hero-inner"><div class="hero-copy">
<p class="eyebrow">Study abroad consultancy · Pakistan to USA &amp; Europe</p>
<h1>Learn from people already <em>living your dream</em></h1>
<p class="lede">Get one-on-one guidance from <strong>Pakistani graduates and professionals living in the USA</strong>, people who have been through admissions, the F-1 visa interview and their first semester themselves. Hamraah walks with you from your first question to your first week on campus.</p>
<div class="hero-cta"><a class="btn btn-gold" href="/book">Book a session from $25</a><a class="btn btn-ghost" href="/how-it-works">See how it works</a></div>
<ul class="hero-badges"><li>US-based experts</li><li>One-on-one sessions</li><li>A-to-Z guidance</li><li>Transparent prices</li></ul>
</div><div class="hero-mark" aria-hidden="true"><img src="/assets/logo/hamraah-crest-gold-foil.svg" alt="" width="500" height="500"><p class="tagline">Hamraah · fellow traveller</p></div></div></section>
<section class="strip" aria-label="Highlights"><div class="wrap strip-inner">
<div><span class="num">USA</span><span class="lbl">Our main focus: F-1 student visas</span></div>
<div><span class="num">Europe</span><span class="lbl">Selected countries and universities</span></div>
<div><span class="num">1:1</span><span class="lbl">Sessions on Zoom or Google Meet</span></div>
<div><span class="num">$25</span><span class="lbl">Expert sessions start from</span></div>
</div></section>'''
    return "\n".join([
        hero,
        section(section_head("Why Hamraah", "Real guidance, not just application processing",
                             "Most consultants file forms. Our experts have sat in the same visa interview, written the same SOP and opened their first US bank account. That experience is what you get.")
                + compare() + '<p class="center-link"><a href="/about">More about Hamraah</a></p>'),
        section(section_head("Your A-to-Z journey", "Eight steps, one companion") + journey()
                + '<p class="center-link"><a href="/how-it-works">See each step in detail</a></p>', "tint"),
        section(section_head("What we do", "Everything you need, <em>in one place</em>")
                + services_grid(detailed=False, link=True), "dark", pattern=True),
        section(section_head("Meet our US-based experts", "Choose the expert who fits your goals",
                             "Every expert is a Pakistani graduate, professional or current student in the USA, verified by us.")
                + experts_grid() + '<p class="center-link"><a href="/experts">About our experts</a></p>'),
        section(section_head("Pricing", "From a first session to full support",
                             "Clear prices in US dollars. Pay the equivalent in PKR if you prefer.")
                + packages_grid() + '<p class="center-link"><a href="/pricing">See all prices and single sessions</a></p>', "tint"),
        cta_band(),
    ])


@page("/how-it-works", "how-it-works.html",
      "Your 8-Step Study Abroad Journey | Hamraah Advisors",
      "From profile evaluation to post-arrival support: how Hamraah guides Pakistani students through admissions, finances and the F-1 visa, step by step.",
      crumb="How it works")
def how():
    steps = [("Tell us about you", "Fill in the booking form or message us on WhatsApp."),
             ("Choose your session or package", "Pick a single session or a package, and an expert if you like."),
             ("Meet online", "We confirm a time and send a Zoom or Google Meet link."),
             ("Get your plan", "You leave every session with clear next steps in writing.")]
    simple = '<ol class="steps">' + "".join(f"<li><h3>{e(a)}</h3><p>{e(b)}</p></li>" for a, b in steps) + "</ol>"
    return "\n".join([
        page_hero("How it works", "Your journey, <em>step by step</em>",
                  "Eight clear steps from your first question to your first week on campus, with a US-based expert beside you at each one.", "How it works"),
        section(section_head("Your A-to-Z journey", "Eight steps, one companion") + journey(detailed=True)),
        section(section_head("Getting started", "How a session works") + simple, "tint"),
        cta_band("Ready for step one?", "Book your profile evaluation", "/book?session=Package:+Basic"),
    ])


@page("/services", "services.html",
      "Admissions, F-1 Visa & Scholarship Help | Hamraah Advisors",
      "University admissions, SOP help, scholarships, financial documentation guidance, DS-160 and F-1 visa interview preparation for Pakistani students.",
      crumb="Services")
def services():
    dest = '''<div class="dest">
<div><h3>United States</h3><p>Our main focus. Bachelor's, Master's and PhD admissions, scholarships and assistantships, and complete F-1 student visa preparation with experts who live there.</p></div>
<div><h3>Europe</h3><p>Guidance for selected countries and universities in Europe, from choosing a program to student visa documentation. Ask us about your destination.</p></div>
</div>'''
    return "\n".join([
        page_hero("Services", "Everything you need, <em>in one place</em>",
                  "Six areas of support, delivered by Pakistani experts who studied and work in the USA.", "Services"),
        section(services_grid(detailed=True), "dark", pattern=True),
        section(section_head("Destinations", "Where we can take you") + dest),
        cta_band("Not sure which service you need?", "Book a 30-minute consultation", "/book?session=30-minute+consultation"),
    ])


@page("/experts", "experts.html",
      "Meet Our US-Based Pakistani Experts | Hamraah Advisors",
      "Book 1:1 sessions with verified Pakistani experts in the USA: admissions, F-1 visa and financial documentation experts, and current US student mentors.",
      crumb="Experts")
def experts():
    verify = [("Identity and location", "We confirm who they are and that they live in the USA."),
              ("Education and work", "We check their US degree, enrolment or employment."),
              ("Real experience", "They have been through admissions and the F-1 process themselves."),
              ("Student feedback", "Every session is reviewed, and only well-rated experts stay.")]
    join = f'''<div class="join"><div><p class="eyebrow">For Pakistanis in the USA</p><h2>Become a Hamraah expert</h2><span class="rule"></span>
<p class="sub left">Are you a Pakistani graduate, professional or student in the USA? Help the next generation make the journey you made, on your own schedule.</p></div>
<a class="btn btn-maroon" href="mailto:{EMAIL}?subject=Become%20a%20Hamraah%20expert">Apply to join</a></div>'''
    return "\n".join([
        page_hero("Our experts", "Choose the expert who <em>fits your goals</em>",
                  "Every expert is a Pakistani graduate, working professional or current student in the USA. They have lived the journey you are starting.", "Experts"),
        section(experts_grid(detailed=True) + '<p class="center-note">Full expert profiles with photos, universities and reviews are coming soon.</p>'),
        section(section_head("How we verify", "Every expert is checked") + promises_grid(verify), "dark", pattern=True),
        section(join),
    ])


@page("/pricing", "pricing.html",
      "Study Abroad Pricing from $25 | Hamraah Advisors",
      "Transparent USD prices: expert sessions from $25 and packages from $79 to $999 for admissions, financial documentation, F-1 visa prep and arrival support.",
      crumb="Pricing", schema=(offers_schema(),))
def pricing():
    excl = '''<div class="excl"><div><h3>Not included</h3><ul>
<li>University application fees</li><li>English test fees (IELTS, TOEFL, Duolingo)</li><li>SEVIS I-901 fee</li><li>US visa application fee</li><li>Flights and accommodation costs</li></ul>
<p>These are paid directly by you to the relevant organisation. We tell you exactly which ones apply.</p></div>
<div><h3>Good to know</h3><ul>
<li>Prices are in US dollars. Pay the equivalent in PKR at the current exchange rate.</li>
<li>You sign a written service agreement before paying for a package.</li>
<li>Sessions can be rescheduled or refunded with 24 hours' notice.</li>
<li>Already booked a session? Its fee is deducted if you upgrade to a package within 30 days.</li></ul></div></div>'''
    pfaq = [f for f in FAQS if f[0] in ("Can I pay in Pakistani rupees?", "Are university and visa fees included?", "What if I want to cancel?", "Can you guarantee my visa?")]
    return "\n".join([
        page_hero("Pricing", "From a first session <em>to full support</em>",
                  "Clear prices in US dollars, no hidden charges. Start with a single session or choose a package.", "Pricing"),
        section(section_head("Packages", "Choose your level of support") + packages_grid()),
        section(section_head("Single sessions", "Pay only for the help you need",
                             "Online one-on-one sessions with a US-based expert, on Zoom or Google Meet.") + sessions_grid(), "tint"),
        section(excl),
        section(section_head("Questions", "About payments") + faq_list(pfaq), "tint narrow-wrap"),
        cta_band(),
    ])


@page("/about", "about.html",
      "About Hamraah Advisors: Your Global Education Partner",
      "Hamraah means fellow traveller. Why we connect Pakistani students with experts living in the USA, and the promises we make to students and families.",
      crumb="About")
def about():
    story = '''<div class="about-grid">
<article class="mv"><p class="kicker">Our name</p><h3>Hamraah means fellow traveller.</h3><p>Studying abroad is one of the biggest journeys a student and their family will make. We believe nobody should make it alone, or rely on advice from people who have never made it themselves.</p></article>
<article class="mv"><p class="kicker">Our idea</p><h3>Guidance from people already living your dream.</h3><p>Hamraah connects students in Pakistan with Pakistani graduates, professionals and students in the USA, who share real, first-hand experience at every step.</p></article>
<article class="mv"><p class="kicker">Our vision</p><h3>To be Pakistan's most trusted companion for studying abroad.</h3><p>A consultancy students and parents recommend to their friends, because we were honest with them from day one.</p></article>
<article class="mv"><p class="kicker">Our mission</p><h3>Clear, practical advice, delivered with care and complete honesty.</h3><p>We make admissions, finances and visas simple to understand and act on, and we stay accountable for the help we give.</p></article>
</div>'''
    return "\n".join([
        page_hero("About us", "Your global <em>education partner</em>",
                  f"{LEGAL} is a study-abroad consultancy registered in Pakistan, built around one promise: real guidance from people who have lived the journey.", "About"),
        section(story),
        section(section_head("The difference", "Real guidance, not just application processing") + compare(), "tint"),
        section(section_head("Our promise to students and families", "Honest advice you <em>can trust</em>") + promises_grid(), "dark", pattern=True),
        cta_band(),
    ])


@page("/faq", "faq.html",
      "Study Abroad & F-1 Visa FAQ | Hamraah Advisors",
      "Answers for Pakistani students: who our US-based experts are, prices, paying in PKR, visa guarantees, financial documents and cancellations.",
      crumb="FAQ", schema=(faq_schema(FAQS),))
def faq():
    return "\n".join([
        page_hero("FAQ", "Frequently asked <em>questions</em>",
                  "Straight answers about our experts, prices and process. Can't find yours? Message us on WhatsApp.", "FAQ"),
        section(faq_list(FAQS), "narrow-wrap"),
        cta_band("Still have a question?", "Ask us on WhatsApp", f"https://wa.me/{WHATSAPP}"),
    ])


@page("/book", "book.html",
      "Book a Session with a US-Based Expert | Hamraah Advisors",
      "Book a one-on-one online session with a Pakistani expert in the USA, or enquire about a study-abroad package. Send your request by WhatsApp or email.",
      crumb="Book a session", priority="0.9")
def book():
    sess_opts = "".join(f"<option>{e(k)} (${p})</option>" for k, _, _, p, _ in SESSIONS)
    pkg_opts = "".join(f"<option>Package: {n} (${p})</option>" for n, p, *_ in PACKAGES)
    exp_opts = "<option>No preference</option>" + "".join(f"<option>{e(n)}</option>" for n, *_ in EXPERTS)
    return "\n".join([
        page_hero("Get started", "Book a <em>session</em>",
                  "Tell us about yourself and the help you need. Our coordinator confirms your time and expert within one working day.", "Book a session"),
        f'''<section class="section"><div class="wrap contact-grid">
<div>
<h2 class="h-small">What happens next</h2>
<ol class="next-steps"><li>Send your request on WhatsApp or by email.</li><li>We confirm your expert, time and the fee in writing.</li><li>You pay, and we send your Zoom or Google Meet link.</li></ol>
<ul class="contact-list">
<li><span class="ico" aria-hidden="true"><svg viewBox="0 0 24 24"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm5.3 14.1c-.2.6-1.3 1.2-1.8 1.3-.5 0-1 .2-3.3-.7a11.6 11.6 0 0 1-4.6-4c-.4-.5-1.1-1.6-1.1-3s.7-2 1-2.3a1 1 0 0 1 .8-.4h.6c.2 0 .4 0 .6.5l.9 2.1c.1.2.1.4 0 .6l-.4.6-.4.5c-.1.1-.3.3-.1.6a8.7 8.7 0 0 0 4.3 3.8c.3.1.5.1.6-.1l.9-1.1c.2-.3.4-.2.6-.1l2 1c.3.1.5.2.5.3a2.4 2.4 0 0 1-.1 1.3z"/></svg></span><a href="https://wa.me/{WHATSAPP}" target="_blank" rel="noopener">WhatsApp {WHATSAPP_DISPLAY}</a></li>
<li><span class="ico" aria-hidden="true"><svg viewBox="0 0 24 24"><path d="M20 4H4a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V6a2 2 0 0 0-2-2zm0 4-8 5-8-5V6l8 5 8-5z"/></svg></span><a href="mailto:{EMAIL}">{EMAIL}</a></li>
<li><span class="ico" aria-hidden="true"><svg viewBox="0 0 24 24"><path d="M12 2a7 7 0 0 0-7 7c0 5.25 7 13 7 13s7-7.75 7-13a7 7 0 0 0-7-7zm0 9.5A2.5 2.5 0 1 1 12 6.5a2.5 2.5 0 0 1 0 5z"/></svg></span><span>{ADDRESS}</span></li>
</ul>
<p class="hours">Sessions available in Pakistan and US time zones.</p>
</div>
<form class="form" id="book-form" novalidate>
<div class="row2"><label>Full name<input name="name" type="text" autocomplete="name" required></label>
<label>WhatsApp number<input name="phone" type="tel" autocomplete="tel" placeholder="+92 3xx xxxxxxx" required></label></div>
<div class="row2"><label>Email<input name="email" type="email" autocomplete="email" required></label>
<label>City<input name="city" type="text" autocomplete="address-level2"></label></div>
<div class="row2"><label>Destination<select name="destination"><option>USA</option><option>Europe</option><option>Not sure yet</option></select></label>
<label>Study level<select name="level"><option>Bachelor's</option><option>Master's</option><option>PhD</option><option>Other</option></select></label></div>
<label>What would you like to book?<select name="session">{sess_opts}{pkg_opts}</select></label>
<label>Preferred expert<select name="expert">{exp_opts}</select></label>
<label>Anything we should know?<textarea name="message" rows="4" placeholder="Your CGPA, the intake you are targeting, questions..."></textarea></label>
<div class="form-actions"><button class="btn btn-maroon" type="submit" name="via" value="whatsapp">Send on WhatsApp</button>
<button class="btn btn-outline" type="submit" name="via" value="email">Send by email</button></div>
<p class="form-note" role="status" aria-live="polite">Your details are kept strictly confidential.</p>
</form></div></section>''',
    ])


# ---------------------------------------------------------------- blog
# Articles are Markdown files in _build/posts/. Each starts with a header block:
#   ---
#   title: Page title (also the H1)
#   description: 150-160 character summary for Google
#   date: 2026-11-23
#   updated: 2026-11-23        (optional)
#   category: USA visa
#   cta_session: Visa interview mock session   (a SESSIONS key; the article's booking button)
#   ---
# Supported Markdown: ## and ### headings, paragraphs, - and 1. lists, **bold**, *italic*,
# [links](url), > quotes, "!!! note" boxes (one paragraph), "[[cta]]" for a booking box.
POSTS_DIR = os.path.join(ROOT, "_build", "posts")
BLOG_PATH = "/blog"


def _inline(t):
    t = e(t, quote=False)
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?!\w)", r"<em>\1</em>", t)

    def link(m):
        text, url = m.group(1), m.group(2)
        ext = url.startswith("http") and "hamraahadvisors.com" not in url
        rel = ' target="_blank" rel="noopener"' if ext else ""
        return f'<a href="{url}"{rel}>{text}</a>'
    return re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", link, t)


def slugify(t):
    return re.sub(r"[^a-z0-9]+", "-", t.lower()).strip("-")


def md_to_html(src, cta_html):
    blocks, toc = [], []
    for chunk in re.split(r"\n\s*\n", src.strip()):
        lines = chunk.strip().split("\n")
        first = lines[0]
        if first.strip() == "[[cta]]":
            blocks.append(cta_html)
        elif first.startswith("### "):
            blocks.append(f"<h3>{_inline(first[4:])}</h3>")
        elif first.startswith("## "):
            h = first[3:].strip()
            sid = slugify(h)
            toc.append((sid, h))
            blocks.append(f'<h2 id="{sid}">{_inline(h)}</h2>')
        elif first.startswith("!!! "):
            label = first[4:].strip()
            body = " ".join(l.strip() for l in lines[1:])
            blocks.append(f'<aside class="callout"><p class="kicker">{e(label)}</p><p>{_inline(body)}</p></aside>')
        elif first.startswith("> "):
            blocks.append("<blockquote><p>" + _inline(" ".join(l[2:] for l in lines)) + "</p></blockquote>")
        elif re.match(r"^(- |\d+\. )", first):
            tag = "ol" if first[0].isdigit() else "ul"
            items = []
            for l in lines:
                m = re.match(r"^(?:- |\d+\. )(.*)", l)
                if m:
                    items.append(m.group(1))
                elif items:
                    items[-1] += " " + l.strip()
            blocks.append(f"<{tag}>" + "".join(f"<li>{_inline(i)}</li>" for i in items) + f"</{tag}>")
        else:
            blocks.append("<p>" + _inline(" ".join(l.strip() for l in lines)) + "</p>")
    return "\n".join(blocks), toc


def load_posts():
    posts = []
    for f in sorted(glob.glob(os.path.join(POSTS_DIR, "*.md"))):
        raw = open(f, encoding="utf-8").read()
        m = re.match(r"---\n(.*?)\n---\n(.*)", raw, re.S)
        meta = dict(l.split(": ", 1) for l in m.group(1).strip().split("\n"))
        meta["slug"] = os.path.splitext(os.path.basename(f))[0]
        meta["body"] = m.group(2)
        meta.setdefault("updated", meta["date"])
        words = len(re.findall(r"\w+", meta["body"]))
        meta["minutes"] = max(1, round(words / 220))
        posts.append(meta)
    posts.sort(key=lambda p: p["date"], reverse=True)
    return posts


def nice_date(d):
    return datetime.date.fromisoformat(d).strftime("%-d %B %Y")


def post_card(p):
    return (f'<a class="post-card" href="{BLOG_PATH}/{p["slug"]}"><span class="kicker">{e(p["category"])}</span>'
            f'<h3>{e(p["title"])}</h3><p>{e(p["description"])}</p>'
            f'<span class="meta">{nice_date(p["date"])} · {p["minutes"]} min read</span><span class="go">Read article</span></a>')


def article_cta(p):
    key = p.get("cta_session", "30-minute consultation")
    sess = next((s for s in SESSIONS if s[0] == key), SESSIONS[0])
    q = sess[0].replace(" ", "+")
    return (f'<aside class="article-cta"><p class="kicker">Talk to someone who has done it</p>'
            f'<h3>{e(sess[1])} · {sess[2]} · ${sess[3]}</h3><p>{e(sess[4])} Our experts are Pakistanis living in the USA who went through this process themselves.</p>'
            f'<div class="cta-row"><a class="btn btn-gold" href="/book?session={q}">Book this session</a>'
            f'<a class="btn btn-outline" href="https://wa.me/{WHATSAPP}" target="_blank" rel="noopener">Ask on WhatsApp</a></div></aside>')


def build_blog(posts):
    out = []
    for p in posts:
        path = f"{BLOG_PATH}/{p['slug']}"
        cta = article_cta(p)
        body_html, toc = md_to_html(p["body"], cta)
        toc_html = ('<nav class="toc" aria-label="In this article"><p class="kicker">In this article</p><ol>'
                    + "".join(f'<li><a href="#{i}">{e(h)}</a></li>' for i, h in toc) + "</ol></nav>") if len(toc) > 2 else ""
        related = [r for r in posts if r["slug"] != p["slug"]][:3]
        updated = f' · Updated {nice_date(p["updated"])}' if p["updated"] != p["date"] else ""
        hero = f'''<section class="hero page-hero article-hero"><div class="pattern" aria-hidden="true"></div>
<div class="wrap"><nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a><span aria-hidden="true">/</span><a href="{BLOG_PATH}">Blog</a><span aria-hidden="true">/</span><span aria-current="page">{e(p["category"])}</span></nav>
<p class="eyebrow">{e(p["category"])}</p><h1>{e(p["title"])}</h1><p class="lede">{e(p["description"])}</p>
<p class="article-meta">By the Hamraah Advisors team · {nice_date(p["date"])}{updated} · {p["minutes"]} min read</p></div></section>'''
        article = (f'<section class="section"><div class="wrap article-wrap"><article class="prose">{toc_html}{body_html}'
                   f'{cta}<p class="disclaimer">This article is general guidance, checked on {nice_date(p["updated"])}. Fees and rules change, so always confirm on the official website before you pay or apply. Visa decisions are made only by the embassy or consulate.</p></article></div></section>')
        rel_html = section(section_head("Keep reading", "More guides for students") + f'<div class="post-grid">{"".join(post_card(r) for r in related)}</div>', "tint") if related else ""
        schema = {"@type": "BlogPosting", "headline": p["title"], "description": p["description"],
                  "datePublished": p["date"], "dateModified": p["updated"], "inLanguage": "en",
                  "mainEntityOfPage": SITE + path, "image": SITE + "/assets/og-image.jpg",
                  "author": {"@id": SITE + "/#organization"}, "publisher": {"@id": SITE + "/#organization"}}
        title = p["title"] if len(p["title"]) > 50 else p["title"] + " | Hamraah Advisors"
        html_out = layout(path, title, p["description"], "\n".join([hero, article, rel_html, cta_band()]),
                          (schema,), ("Blog", BLOG_PATH, p["title"]), og_type="article")
        out.append((os.path.join("blog", p["slug"] + ".html"), html_out, path, "0.7", p["updated"]))
    # index
    cats = sorted({p["category"] for p in posts})
    index_body = "\n".join([
        page_hero("Blog", "Guides for students <em>going abroad</em>",
                  "Straight answers on US admissions, F-1 visas, costs, scholarships and studying in Europe, written by people who made the journey themselves.", "Blog"),
        section(f'<p class="topics">Topics: {" · ".join(e(c) for c in cats)}</p><div class="post-grid">{"".join(post_card(p) for p in posts)}</div>'),
        cta_band("Have a question an article can't answer?", "Book a 30-minute session", "/book?session=30-minute+consultation"),
    ])
    blog_schema = {"@type": "Blog", "@id": SITE + BLOG_PATH, "name": "Hamraah Advisors Blog", "url": SITE + BLOG_PATH,
                   "publisher": {"@id": SITE + "/#organization"},
                   "blogPost": [{"@type": "BlogPosting", "headline": p["title"], "url": f"{SITE}{BLOG_PATH}/{p['slug']}",
                                 "datePublished": p["date"]} for p in posts]}
    out.insert(0, ("blog/index.html", layout(BLOG_PATH, "Study Abroad Guides for Pakistani Students | Hamraah Blog",
                   "Free guides on F-1 visa interviews, the cost of studying in the USA, scholarships, SOP writing and tuition-free study in Germany.",
                   index_body, (blog_schema,), "Blog"), BLOG_PATH, "0.8", posts[0]["updated"] if posts else TODAY))
    return out


def build():
    urls = []
    for filename, (path, title, desc, fn, crumb, schema, priority) in PAGES.items():
        out = layout(path, title, desc, fn(), schema, crumb)
        with open(os.path.join(ROOT, filename), "w", encoding="utf-8") as f:
            f.write(out)
        urls.append((path, priority, TODAY))
        print("built", filename, f"title={len(title)}ch desc={len(desc)}ch")
    os.makedirs(os.path.join(ROOT, "blog"), exist_ok=True)
    for filename, out, path, priority, lastmod in build_blog(load_posts()):
        with open(os.path.join(ROOT, filename), "w", encoding="utf-8") as f:
            f.write(out)
        urls.append((path, priority, lastmod))
        print("built", filename)
    sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for path, pr, lastmod in urls:
        sm.append(f"  <url><loc>{SITE}{path}</loc><lastmod>{lastmod}</lastmod><priority>{pr}</priority></url>")
    sm.append("</urlset>")
    open(os.path.join(ROOT, "sitemap.xml"), "w").write("\n".join(sm) + "\n")
    open(os.path.join(ROOT, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n")


if __name__ == "__main__":
    build()
