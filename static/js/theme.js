/* IshTop — theme toggle (light/dark), sync with backend when logged in */
(function () {
    function getCookie(name) {
        var m = document.cookie.match(new RegExp('(^| )' + name + '=([^;]+)'));
        return m ? decodeURIComponent(m[2]) : '';
    }

    function isDark() {
        return document.documentElement.getAttribute('data-theme') === 'dark';
    }

    function updateToggleUi() {
        var btn = document.getElementById('themeToggle');
        if (!btn || !window.ISHTOP_I18N) return;
        var dark = isDark();
        btn.setAttribute('aria-pressed', dark ? 'true' : 'false');
        btn.setAttribute('aria-label', dark ? window.ISHTOP_I18N.themeSwitchToLight : window.ISHTOP_I18N.themeSwitchToDark);
        btn.classList.toggle('theme-toggle--dark', dark);
    }

    function applyTheme(theme) {
        var el = document.documentElement;
        if (theme === 'dark') el.setAttribute('data-theme', 'dark');
        else el.removeAttribute('data-theme');
        try {
            localStorage.setItem('ishtop-theme', theme);
        } catch (e) {}
        updateToggleUi();
    }

    window.ISHTOP = window.ISHTOP || {};
    window.ISHTOP.applyTheme = applyTheme;

    window.ISHTOP.toggleTheme = function () {
        var next = isDark() ? 'light' : 'dark';
        applyTheme(next);
        var body = document.body;
        var url = body.getAttribute('data-theme-url');
        var authed = body.getAttribute('data-user-authenticated') === '1';
        if (!authed || !url) return;
        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken'),
            },
            body: JSON.stringify({ theme: next }),
            credentials: 'same-origin',
        }).catch(function () {});
    };

    document.addEventListener('DOMContentLoaded', function () {
        updateToggleUi();
        var btn = document.getElementById('themeToggle');
        if (btn) btn.addEventListener('click', window.ISHTOP.toggleTheme);
    });
})();
