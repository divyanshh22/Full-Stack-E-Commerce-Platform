/* ============================================================
   Django Shop — Modern UI JS
   ============================================================ */
(function () {
  'use strict';

  /* Sticky header shadow */
  var header = document.querySelector('.site-header');
  var onScroll = function () {
    if (header && window.scrollY > 10) header.classList.add('scrolled');
    else if (header) header.classList.remove('scrolled');

    var topBtn = document.getElementById('backToTop');
    if (topBtn) {
      if (window.scrollY > 400) topBtn.classList.add('show');
      else topBtn.classList.remove('show');
    }
  };
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  /* Back to top */
  var topBtn = document.getElementById('backToTop');
  if (topBtn) {
    topBtn.addEventListener('click', function () {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }

  /* Mobile menu */
  var burger = document.getElementById('menuToggle');
  var mobileMenu = document.getElementById('mobileMenu');
  if (burger && mobileMenu) {
    burger.addEventListener('click', function () {
      burger.classList.toggle('open');
      mobileMenu.classList.toggle('open');
    });
    mobileMenu.querySelectorAll('a').forEach(function (link) {
      link.addEventListener('click', function () {
        burger.classList.remove('open');
        mobileMenu.classList.remove('open');
      });
    });
  }

  /* Toasts auto-dismiss */
  document.querySelectorAll('.toast').forEach(function (toast) {
    var close = toast.querySelector('.toast-close');
    if (close) {
      close.addEventListener('click', function () {
        toast.remove();
      });
    }
    setTimeout(function () {
      toast.style.transition = 'opacity .4s ease, transform .4s ease';
      toast.style.opacity = '0';
      toast.style.transform = 'translateX(16px)';
      setTimeout(function () { toast.remove(); }, 400);
    }, 4500);
  });

  /* Hero slideshow */
  var slides = document.querySelectorAll('.hero-slide');
  var dots = document.querySelectorAll('.hero-dots button');
  if (slides.length > 1) {
    var current = 0;
    var timer = null;
    var goTo = function (index) {
      current = (index + slides.length) % slides.length;
      slides.forEach(function (s, i) {
        s.classList.toggle('active', i === current);
      });
      dots.forEach(function (d, i) {
        d.classList.toggle('active', i === current);
      });
    };
    var start = function () {
      timer = setInterval(function () { goTo(current + 1); }, 6000);
    };
    var stop = function () { clearInterval(timer); };
    dots.forEach(function (d, i) {
      d.addEventListener('click', function () {
        stop(); goTo(i); start();
      });
    });
    start();
  }

  /* Quantity stepper (product detail) */
  document.querySelectorAll('.qty').forEach(function (qty) {
    var input = qty.querySelector('input');
    var dec = qty.querySelector('.qty-dec');
    var inc = qty.querySelector('.qty-inc');
    if (!input || !dec || !inc) return;
    var clamp = function (v) {
      var min = parseInt(input.min || '1', 10);
      var max = parseInt(input.max || '99', 10);
      if (isNaN(v)) v = min;
      return Math.min(Math.max(v, min), max);
    };
    dec.addEventListener('click', function () { input.value = clamp(parseInt(input.value || '1', 10) - 1); });
    inc.addEventListener('click', function () { input.value = clamp(parseInt(input.value || '1', 10) + 1); });
    input.addEventListener('change', function () { input.value = clamp(parseInt(input.value || '1', 10)); });
  });

  /* Checkout payment radio cards */
  document.querySelectorAll('.radio-card input[type="radio"]').forEach(function (radio) {
    radio.addEventListener('change', function () {
      document.querySelectorAll('.radio-card').forEach(function (card) {
        card.classList.remove('selected');
      });
      radio.closest('.radio-card').classList.add('selected');
    });
  });
})();
