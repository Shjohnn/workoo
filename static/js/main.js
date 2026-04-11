/* ===================================
   IshTop — Main JavaScript
   Scroll reveal, ripple, hamburger
   =================================== */

document.addEventListener('DOMContentLoaded', function () {

    // ========================
    // 1. Page scroll progress
    // ========================
    const progressBar = document.getElementById('pageProgress');
    if (progressBar) {
        window.addEventListener('scroll', function () {
            const scrolled = window.scrollY;
            const maxScroll = document.documentElement.scrollHeight - window.innerHeight;
            const pct = maxScroll > 0 ? (scrolled / maxScroll) * 100 : 0;
            progressBar.style.width = pct + '%';
        }, { passive: true });
    }

    // ========================
    // 2. Scroll reveal (Intersection Observer)
    // ========================
    const revealEls = document.querySelectorAll('.reveal, .stagger');
    if (revealEls.length > 0) {
        const observer = new IntersectionObserver(function (entries) {
            entries.forEach(function (entry) {
                if (entry.isIntersecting) {
                    entry.target.classList.add('revealed');
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' });

        revealEls.forEach(function (el) {
            observer.observe(el);
        });
    }

    // ========================
    // 3. Button ripple effect
    // ========================
    document.querySelectorAll('.btn').forEach(function (btn) {
        btn.addEventListener('click', function (e) {
            const rect = btn.getBoundingClientRect();
            const ripple = document.createElement('span');
            const size = Math.max(rect.width, rect.height);
            ripple.className = 'btn-ripple';
            ripple.style.cssText = [
                'width:' + size + 'px',
                'height:' + size + 'px',
                'left:' + (e.clientX - rect.left - size / 2) + 'px',
                'top:' + (e.clientY - rect.top - size / 2) + 'px',
            ].join(';');
            btn.appendChild(ripple);
            setTimeout(function () { ripple.remove(); }, 600);
        });
    });

    // ========================
    // 4. Navbar hamburger
    // ========================
    const hamburger = document.getElementById('navHamburger');
    const navLinks = document.getElementById('navLinks');
    if (hamburger && navLinks) {
        hamburger.addEventListener('click', function () {
            navLinks.classList.toggle('open');
            hamburger.classList.toggle('active');
        });
        document.addEventListener('click', function (e) {
            if (!hamburger.contains(e.target) && !navLinks.contains(e.target)) {
                navLinks.classList.remove('open');
                hamburger.classList.remove('active');
            }
        });
    }

    // ========================
    // 5. Alert auto dismiss
    // ========================
    document.querySelectorAll('.alert').forEach(function (alert) {
        setTimeout(function () {
            alert.style.opacity = '0';
            alert.style.transform = 'translateX(120%)';
            alert.style.transition = 'all .3s ease';
            setTimeout(function () { alert.remove(); }, 350);
        }, 5000);
    });

    // ========================
    // 6. Filter form selects auto-submit
    // ========================
    const filterForm = document.getElementById('filterForm');
    if (filterForm) {
        filterForm.querySelectorAll('select').forEach(function (sel) {
            sel.addEventListener('change', function () { filterForm.submit(); });
        });
    }

    // ========================
    // 7. Star rating UI
    // ========================
    const starBtns = document.querySelectorAll('.star-btn');
    if (starBtns.length > 0) {
        starBtns.forEach(function (btn, idx) {
            btn.addEventListener('mouseenter', function () {
                starBtns.forEach(function (b, i) {
                    b.classList.toggle('hover', i <= idx);
                });
            });
            btn.addEventListener('mouseleave', function () {
                starBtns.forEach(function (b) { b.classList.remove('hover'); });
            });
            btn.addEventListener('click', function () {
                const val = btn.dataset.value;
                document.querySelector('[name="score"]').value = val;
                starBtns.forEach(function (b, i) {
                    b.classList.toggle('active', i < parseInt(val));
                });
            });
        });
    }

    // ========================
    // 8. Smooth card hover tilt (subtle)
    // ========================
    document.querySelectorAll('.job-card').forEach(function (card) {
        card.addEventListener('mousemove', function (e) {
            const rect = card.getBoundingClientRect();
            const x = ((e.clientX - rect.left) / rect.width - 0.5) * 6;
            const y = ((e.clientY - rect.top) / rect.height - 0.5) * -6;
            card.style.transform = 'translateY(-6px) rotateX(' + y + 'deg) rotateY(' + x + 'deg)';
        });
        card.addEventListener('mouseleave', function () {
            card.style.transform = '';
        });
    });
});
