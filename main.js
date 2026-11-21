(function () {
  // Contact details: update these when the real ones are confirmed.
  var WHATSAPP = '923001234567';
  var EMAIL = 'info@hamraahadvisors.com';

  var header = document.querySelector('.site-header');
  var toggle = document.querySelector('.nav-toggle');
  var nav = document.getElementById('nav');

  function onScroll() { header.classList.toggle('scrolled', window.scrollY > 40); }
  onScroll();
  window.addEventListener('scroll', onScroll, { passive: true });

  toggle.addEventListener('click', function () {
    var open = header.classList.toggle('open');
    toggle.setAttribute('aria-expanded', open);
    toggle.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
  });
  nav.addEventListener('click', function (e) {
    if (e.target.tagName === 'A') {
      header.classList.remove('open');
      toggle.setAttribute('aria-expanded', 'false');
    }
  });

  // Reveal on scroll
  var targets = document.querySelectorAll('.section-head, .compare-col, .journey li, .service, .expert, .session, .pkg, .promises > div, .mv, .steps li, .dest > div, .excl > div, .faq, .contact-grid > *');
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); }
      });
    }, { rootMargin: '0px 0px -8% 0px' });
    targets.forEach(function (el) { el.classList.add('reveal'); io.observe(el); });
  }

  var y = document.getElementById('year');
  if (y) y.textContent = new Date().getFullYear();

  // Booking form (only on /book)
  var form = document.getElementById('book-form');
  if (!form) return;
  var note = form.querySelector('.form-note');

  function setSelect(name, value) {
    var sel = form.elements[name];
    for (var i = 0; i < sel.options.length; i++) {
      var t = sel.options[i].text;
      if (t === value || t.indexOf(value + ' (') === 0) {
        sel.selectedIndex = i;
        sel.classList.remove('flash'); void sel.offsetWidth; sel.classList.add('flash');
        return;
      }
    }
  }

  // Pre-select from links like /book?session=...&expert=...
  var params = new URLSearchParams(window.location.search);
  if (params.get('session')) setSelect('session', params.get('session'));
  if (params.get('expert')) setSelect('expert', params.get('expert'));

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    var via = (e.submitter && e.submitter.value) || 'whatsapp';
    var ok = true;
    ['name', 'phone', 'email'].forEach(function (n) {
      var f = form.elements[n];
      var v = f.value.trim();
      var bad = !v || (n === 'email' && !/^\S+@\S+\.\S+$/.test(v));
      f.classList.toggle('invalid', bad);
      if (bad) ok = false;
    });
    if (!ok) { note.textContent = 'Please add your name, WhatsApp number and a valid email.'; return; }

    var d = form.elements;
    var lines = [
      'Session booking request - Hamraah Advisors',
      'Name: ' + d.name.value,
      'WhatsApp: ' + d.phone.value,
      'Email: ' + d.email.value,
      'City: ' + (d.city.value || '-'),
      'Destination: ' + d.destination.value,
      'Study level: ' + d.level.value,
      'Booking: ' + d.session.value,
      'Preferred expert: ' + d.expert.value
    ];
    if (d.message.value.trim()) lines.push('', d.message.value.trim());
    var text = lines.join('\n');

    if (via === 'email') {
      window.location.href = 'mailto:' + EMAIL + '?subject=' + encodeURIComponent('Session booking: ' + d.session.value) + '&body=' + encodeURIComponent(text);
      note.textContent = 'Thank you. Your email app should open with your request ready to send.';
    } else {
      window.open('https://wa.me/' + WHATSAPP + '?text=' + encodeURIComponent(text), '_blank', 'noopener');
      note.textContent = 'Thank you. WhatsApp should open with your request ready to send.';
    }
  });
})();
