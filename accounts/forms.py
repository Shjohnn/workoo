from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _

from .models import UserProfile, REGIONS, ROLES


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=50, required=True, label=_('First name'))
    last_name = forms.CharField(max_length=50, required=True, label=_('Last name'))
    email = forms.EmailField(required=False, label=_('Email (optional)'))
    region = forms.ChoiceField(
        choices=[('', _('— Select region —'))] + list(REGIONS),
        label=_('Region'),
        required=False,
    )
    phone = forms.CharField(max_length=20, required=False, label=_('Phone (optional)'))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
        labels = {
            'username': _('Username'),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].label = _('Password')
        self.fields['password2'].label = _('Password confirmation')

    def save(self, commit=True, role='worker'):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data.get('email', '')
        if commit:
            user.save()
            UserProfile.objects.create(
                user=user,
                role=role,
                region=self.cleaned_data.get('region', ''),
                phone=self.cleaned_data.get('phone', ''),
            )
        return user


class ProfileEditForm(forms.ModelForm):
    first_name = forms.CharField(max_length=50, required=True, label=_('First name'))
    last_name = forms.CharField(max_length=50, required=True, label=_('Last name'))
    email = forms.EmailField(required=False, label=_('Email'))

    class Meta:
        model = UserProfile
        fields = ['avatar', 'region', 'bio', 'phone']
        labels = {
            'avatar': _('Profile photo'),
            'region': _('Region'),
            'bio': _('About you'),
            'phone': _('Phone'),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name
            self.fields['email'].initial = user.email
