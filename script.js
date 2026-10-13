'use strict';
(() => {
  const menu = document.querySelector('.menu-toggle');
  const nav = document.getElementById('navigation');
  function closeMenu() {
    menu.setAttribute('aria-expanded', 'false');
    nav.classList.remove('open');
    menu.lastElementChild.textContent = '+';
  }
  menu.addEventListener('click', () => {
    const open = menu.getAttribute('aria-expanded') !== 'true';
    menu.setAttribute('aria-expanded', String(open));
    nav.classList.toggle('open', open);
    menu.lastElementChild.textContent = open ? '−' : '+';
  });
  nav.querySelectorAll('a').forEach(link => link.addEventListener('click', closeMenu));
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && nav.classList.contains('open')) {
      closeMenu();
      menu.focus();
    }
  });
  window.matchMedia('(min-width: 601px)').addEventListener('change', closeMenu);
  document.getElementById('year').textContent = String(new Date().getFullYear());

  const albums = {
    zzz: {
      title: 'ZZZombie Assault',
      pixel: false,
      images: [
        ['assets/zzzombie-snow-dawn.webp', 'Aurora Refuge at dawn: warm light and long shadows across the snow.'],
        ['assets/zzzombie-neon.webp', 'Neo-Vale: neon lights in a rain-soaked city.'],
        ['assets/zzzombie-wilderness.webp', 'Deep wilderness, shifting weather, and the road ahead.'],
        ['assets/zzzombie-desert.webp', 'Desert roads beyond the towns and forests.']
      ]
    },
    floki: {
      title: 'FlokiHeaven',
      pixel: true,
      images: [
        ['assets/floki-action.webp', 'Small rabbit, floating island, and a very unfriendly encounter.'],
        ['assets/floki-frost.webp', 'Frost, crystals, and a traveler on a floating island.'],
        ['assets/floki-boss.webp', 'Floki facing the Root Guardian and its attack patterns.'],
        ['assets/floki-ash.webp', 'An ash-colored island: another place to explore on the next run.']
      ]
    }
  };
  const dialog = document.getElementById('gallery-dialog');
  const picture = document.getElementById('gallery-image');
  const title = document.getElementById('gallery-title');
  const caption = document.getElementById('gallery-caption');
  const count = document.getElementById('gallery-count');
  let currentAlbum = 'zzz';
  let currentIndex = 0;
  let lastTrigger = null;
  function renderImage() {
    const album = albums[currentAlbum];
    const [src, description] = album.images[currentIndex];
    picture.src = src;
    picture.alt = description;
    picture.classList.toggle('pixel-art', album.pixel);
    const snow = src.endsWith('zzzombie-snow-dawn.webp');
    picture.width = album.pixel ? 640 : (snow ? 1600 : 1365);
    picture.height = album.pixel ? 360 : (snow ? 900 : 768);
    title.textContent = album.title;
    caption.textContent = description;
    count.textContent = `${currentIndex + 1} / ${album.images.length}`;
  }
  function nextImage(direction) {
    const length = albums[currentAlbum].images.length;
    currentIndex = (currentIndex + direction + length) % length;
    renderImage();
  }
  document.querySelectorAll('[data-gallery]').forEach(trigger => {
    trigger.addEventListener('click', () => {
      if (!albums[trigger.dataset.gallery]) return;
      lastTrigger = trigger;
      currentAlbum = trigger.dataset.gallery;
      currentIndex = Number(trigger.dataset.index) || 0;
      if (currentIndex < 0 || currentIndex >= albums[currentAlbum].images.length) currentIndex = 0;
      renderImage();
      dialog.showModal();
      document.body.classList.add('modal-open');
      dialog.querySelector('.lightbox-close').focus();
    });
  });
  dialog.querySelector('.lightbox-close').addEventListener('click', () => dialog.close());
  dialog.querySelector('.lightbox-prev').addEventListener('click', () => nextImage(-1));
  dialog.querySelector('.lightbox-next').addEventListener('click', () => nextImage(1));
  dialog.addEventListener('close', () => {
    document.body.classList.remove('modal-open');
    lastTrigger?.focus({preventScroll: true});
  });
  dialog.addEventListener('click', event => {
    if (event.target !== dialog) return;
    const rect = dialog.getBoundingClientRect();
    if (event.clientX < rect.left || event.clientX > rect.right || event.clientY < rect.top || event.clientY > rect.bottom) dialog.close();
  });
  document.addEventListener('keydown', event => {
    if (!dialog.open) return;
    if (event.key === 'ArrowRight' || event.key === 'ArrowLeft') {
      event.preventDefault();
      nextImage(event.key === 'ArrowRight' ? 1 : -1);
    }
  });
})();
