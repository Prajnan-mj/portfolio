/* prajnan.dev — motion engine
   parallax mesh · scroll reveals · cursor previews · contact form */
(function () {
  'use strict';

  var reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var finePointer = window.matchMedia('(pointer: fine)').matches;

  /* ---------- parallax background strip ---------- */
  var strip = document.getElementById('bg-strip');
  if (strip && !reducedMotion) {
    var maxShift = 0;
    var ticking = false;

    var measure = function () {
      var h = strip.offsetHeight || window.innerWidth * (8000 / 2560);
      maxShift = Math.max(0, h - window.innerHeight);
    };

    var apply = function () {
      ticking = false;
      var doc = document.documentElement;
      var scrollable = Math.max(1, doc.scrollHeight - window.innerHeight);
      var p = Math.min(1, Math.max(0, window.scrollY / scrollable));
      strip.style.transform = 'translate3d(0, ' + (-maxShift * p) + 'px, 0)';
    };

    var onScroll = function () {
      if (!ticking) {
        ticking = true;
        requestAnimationFrame(apply);
      }
    };

    window.addEventListener('scroll', onScroll, { passive: true });
    window.addEventListener('resize', function () { measure(); onScroll(); }, { passive: true });
    if (strip.complete) { measure(); apply(); }
    strip.addEventListener('load', function () { measure(); apply(); });
    measure();
    apply();
  }

  /* ---------- sticky nav state ---------- */
  var nav = document.getElementById('nav');
  if (nav) {
    var navUpdate = function () {
      nav.classList.toggle('is-scrolled', window.scrollY > 12);
    };
    window.addEventListener('scroll', navUpdate, { passive: true });
    navUpdate();
  }

  /* ---------- scroll reveals ---------- */
  var reveals = document.querySelectorAll('.reveal');
  if (reveals.length) {
    if (reducedMotion || !('IntersectionObserver' in window)) {
      reveals.forEach(function (el) { el.classList.add('is-in'); });
    } else {
      // stagger siblings inside .stagger containers
      document.querySelectorAll('.stagger').forEach(function (group) {
        var children = group.querySelectorAll('.reveal');
        children.forEach(function (el, i) {
          el.style.setProperty('--rd', Math.min(i * 0.09, 0.45) + 's');
        });
      });
      var io = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add('is-in');
            io.unobserve(entry.target);
          }
        });
      }, { threshold: 0.12, rootMargin: '0px 0px -8% 0px' });
      reveals.forEach(function (el) { io.observe(el); });
    }
  }

  /* ---------- cursor-following project preview ---------- */
  var preview = document.getElementById('work-preview');
  if (preview && finePointer && !reducedMotion) {
    var previewImg = preview.querySelector('img');
    var px = 0, py = 0;         // rendered position
    var tx = 0, ty = 0;         // target position
    var rafId = null;
    var active = false;

    var loop = function () {
      px += (tx - px) * 0.16;
      py += (ty - py) * 0.16;
      var tilt = (tx - px) * 0.02;
      preview.style.transform = 'translate3d(' + px + 'px,' + py + 'px,0) rotate(' + tilt + 'deg)' + (active ? ' scale(1)' : ' scale(0.9)');
      if (active || Math.abs(tx - px) > 0.5) {
        rafId = requestAnimationFrame(loop);
      } else {
        rafId = null;
      }
    };

    document.querySelectorAll('[data-preview]').forEach(function (row) {
      row.addEventListener('mouseenter', function (e) {
        previewImg.src = row.getAttribute('data-preview');
        active = true;
        preview.classList.add('is-on');
        tx = e.clientX + 28;
        ty = e.clientY - 120;
        px = tx; py = ty + 16;
        if (!rafId) rafId = requestAnimationFrame(loop);
      });
      row.addEventListener('mousemove', function (e) {
        var w = preview.offsetWidth, h = preview.offsetHeight;
        tx = Math.min(e.clientX + 28, window.innerWidth - w - 16);
        ty = Math.min(Math.max(e.clientY - h / 2, 16), window.innerHeight - h - 16);
      });
      row.addEventListener('mouseleave', function () {
        active = false;
        preview.classList.remove('is-on');
      });
    });

    // transform is driven by JS; keep CSS transition on opacity only
    preview.style.transition = 'opacity 0.3s cubic-bezier(0.22,0.61,0.36,1)';
  }

  /* ---------- contact form (AJAX with graceful fallback) ---------- */
  var form = document.getElementById('contact-form');
  if (form && window.fetch) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var submit = form.querySelector('.contact-form__submit');
      var label = form.querySelector('.contact-form__label');
      var success = form.querySelector('.contact-form__success');
      form.querySelectorAll('.field__error').forEach(function (el) { el.textContent = ''; });

      submit.disabled = true;
      label.textContent = 'Sending…';

      fetch(form.action, {
        method: 'POST',
        body: new FormData(form),
        headers: { 'X-Requested-With': 'fetch' }
      }).then(function (res) {
        return res.json().then(function (data) { return { ok: res.ok, data: data }; });
      }).then(function (result) {
        if (result.ok && result.data.ok) {
          form.querySelectorAll('.field, .contact-form__submit').forEach(function (el) {
            el.style.display = 'none';
          });
          success.hidden = false;
        } else {
          var errors = (result.data && result.data.errors) || {};
          Object.keys(errors).forEach(function (fieldName) {
            var slot = form.querySelector('[data-error-for="' + fieldName + '"]');
            if (slot) slot.textContent = errors[fieldName][0];
          });
          var firstError = form.querySelector('.field__error:not(:empty)');
          if (firstError) {
            var input = firstError.closest('.field').querySelector('input, textarea');
            if (input) input.focus();
          }
          submit.disabled = false;
          label.textContent = 'Send message';
        }
      }).catch(function () {
        // network failure — fall back to a normal POST
        // (native form.submit() bypasses this submit handler)
        form.submit();
      });
    });
  }
})();
