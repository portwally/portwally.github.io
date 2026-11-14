/* The three looks of the TileTown 2 page: a small switcher, fixed at the
   bottom right, on every one of them. */
(function () {
    var looks = [
        { file: 'index.html', name: 'Blueprint' },
        { file: 'gazette.html', name: 'Gazette' },
        { file: 'box.html', name: 'Box' }
    ];
    var here = location.pathname.split('/').pop() || 'index.html';
    var css = document.createElement('style');
    css.textContent =
        '.tt2-switch{position:fixed;right:12px;bottom:12px;z-index:9999;display:flex;align-items:center;gap:2px;' +
        'padding:4px;background:rgba(18,18,22,.92);border:1px solid rgba(255,255,255,.25);border-radius:999px;' +
        'box-shadow:0 6px 20px rgba(0,0,0,.4);font:600 12px/1 system-ui,-apple-system,"Segoe UI",sans-serif;letter-spacing:.3px}' +
        '.tt2-switch span{color:#bbb;padding:0 8px 0 10px}' +
        '.tt2-switch a{color:#fff;text-decoration:none;padding:7px 11px;border-radius:999px}' +
        '.tt2-switch a:hover{background:rgba(255,255,255,.14)}' +
        '.tt2-switch a:focus-visible{outline:2px solid #ffd23f;outline-offset:1px}' +
        '.tt2-switch a[aria-current]{background:#ffd23f;color:#111}' +
        '@media (max-width:480px){.tt2-switch span{display:none}.tt2-switch{right:8px;bottom:8px}}' +
        '@media print{.tt2-switch{display:none}}';
    document.head.appendChild(css);
    var nav = document.createElement('nav');
    nav.className = 'tt2-switch';
    nav.setAttribute('aria-label', 'Page design');
    nav.innerHTML = '<span>Design</span>' + looks.map(function (l) {
        var cur = l.file === here || (here === '' && l.file === 'index.html');
        return '<a href="' + l.file + '"' + (cur ? ' aria-current="page"' : '') + '>' + l.name + '</a>';
    }).join('');
    document.body.appendChild(nav);
})();
