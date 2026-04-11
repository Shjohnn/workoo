from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

REGIONS = [
    ('toshkent_shahar', _('Tashkent city')),
    ('toshkent_viloyat', _('Tashkent region')),
    ('andijon', _('Andijan region')),
    ('fargona', _('Fergana region')),
    ('namangan', _('Namangan region')),
    ('samarqand', _('Samarkand region')),
    ('buxoro', _('Bukhara region')),
    ('qashqadaryo', _('Kashkadarya region')),
    ('surxondaryo', _('Surkhandarya region')),
    ('jizzax', _('Jizzakh region')),
    ('sirdaryo', _('Syrdarya region')),
    ('navoiy', _('Navoi region')),
    ('xorazm', _('Khorezm region')),
    ('qoraqalpogiston', _('Republic of Karakalpakstan')),
]

ROLES = [
    ('worker', _('Worker')),
    ('employer', _('Employer')),
]

THEME_CHOICES = [
    ('light', _('Light')),
    ('dark', _('Dark')),
]


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLES, default='worker')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    region = models.CharField(max_length=50, choices=REGIONS, blank=True)
    bio = models.TextField(blank=True, max_length=500)
    phone = models.CharField(max_length=20, blank=True)
    theme_preference = models.CharField(
        max_length=16,
        choices=THEME_CHOICES,
        default='light',
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} ({self.get_role_display()})"

    def get_avatar_url(self):
        if self.avatar:
            return self.avatar.url
        return '/static/img/default_avatar.svg'

    def average_rating(self):
        from ratings.models import Rating
        ratings = Rating.objects.filter(worker=self.user)
        if ratings.exists():
            return round(sum(r.score for r in ratings) / ratings.count(), 1)
        return None

    def rating_count(self):
        from ratings.models import Rating
        return Rating.objects.filter(worker=self.user).count()

    def get_region_display_name(self):
        for key, val in REGIONS:
            if key == self.region:
                return val
        return ''
