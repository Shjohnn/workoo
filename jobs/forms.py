from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Job, JobApplication, JOB_CATEGORIES
from accounts.models import REGIONS


class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'description', 'category', 'salary', 'salary_type',
                  'region', 'address', 'lat', 'lng', 'image', 'workers_needed',
                  'work_date', 'status']
        labels = {
            'title': _('Job title'),
            'description': _('Job description'),
            'category': _('Category'),
            'salary': _('Payment amount (UZS)'),
            'salary_type': _('Payment type'),
            'region': _('Region'),
            'address': _('Address'),
            'lat': '',
            'lng': '',
            'image': _('Image (optional)'),
            'workers_needed': _('Workers needed'),
            'work_date': _('Work date'),
            'status': _('Status'),
        }
        widgets = {
            'lat': forms.HiddenInput(),
            'lng': forms.HiddenInput(),
            'work_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 5}),
        }


class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = ['message']
        labels = {'message': _('Additional message (optional)')}
        widgets = {
            'message': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': _('Briefly describe yourself...'),
            })
        }
