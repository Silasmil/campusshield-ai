from django import forms
from .models import Incident

class IncidentReportForm(forms.ModelForm):
    """Form for users to report incidents"""
    
    class Meta:
        model = Incident
        fields = [
            'title',
            'description',
            'incident_type',
            'severity',
            'source_ip',
            'target_system',
            'affected_assets',
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Brief title of the incident',
                'required': True
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Detailed description of what happened',
                'rows': 5,
                'required': True
            }),
            'incident_type': forms.Select(attrs={
                'class': 'form-control',
                'required': True
            }),
            'severity': forms.Select(attrs={
                'class': 'form-control',
                'required': True
            }),
            'source_ip': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., 192.168.1.100 (optional)'
            }),
            'target_system': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Server-01, Database-01 (optional)'
            }),
            'affected_assets': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'List of affected systems/assets (optional)',
                'rows': 3
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make optional fields not required in form
        self.fields['source_ip'].required = False
        self.fields['target_system'].required = False
        self.fields['affected_assets'].required = False


class IncidentUpdateForm(forms.ModelForm):
    """Form for updating incident status and notes"""
    
    class Meta:
        model = Incident
        fields = ['status', 'notes', 'resolved_at']
        widgets = {
            'status': forms.Select(attrs={
                'class': 'form-control'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Add updates about this incident...',
                'rows': 4
            }),
            'resolved_at': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['resolved_at'].required = False
