(function () {
  var header = document.querySelector('.site-header');
  var toggle = document.querySelector('.nav-toggle');
  var nav = document.getElementById('nav');

  function onScroll() {
    header.classList.toggle('scrolled', window.scrollY > 40);
  }
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
  var targets = document.querySelectorAll('.section-head, .mv, .service, .audience article, .steps li, .values, .band-inner, .contact-grid > *');
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); }
      });
    }, { rootMargin: '0px 0px -8% 0px' });
    targets.forEach(function (el) { el.classList.add('reveal'); io.observe(el); });
  }

  // Contact form: opens the visitor's email app with the enquiry filled in.
  var form = document.getElementById('contact-form');
  var note = form.querySelector('.form-note');
  var TO = 'info@hamraahadvisors.com';
  form.addEventListener('submit', function (e) {
    e.preventDefault();
    var ok = true;
    ['name', 'email'].forEach(function (n) {
      var f = form.elements[n];
      var bad = !f.value.trim() || (n === 'email' && !/^\S+@\S+\.\S+$/.test(f.value));
      f.classList.toggle('invalid', bad);
      if (bad) ok = false;
    });
    if (!ok) { note.textContent = 'Please add your name and a valid email address.'; return; }
    var d = form.elements;
    var subject = 'Consultation enquiry: ' + d.service.value;
    var body = 'Name: ' + d.name.value + '\nEmail: ' + d.email.value + '\nPhone: ' + d.phone.value +
      '\nService: ' + d.service.value + '\n\n' + d.message.value;
    window.location.href = 'mailto:' + TO + '?subject=' + encodeURIComponent(subject) + '&body=' + encodeURIComponent(body);
    note.textContent = 'Thank you. Your email app should open with your enquiry ready to send.';
  });

  var y = document.getElementById('year');
  if (y) y.textContent = new Date().getFullYear();
})();
