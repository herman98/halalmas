from __future__ import unicode_literals

from django import forms

from .models import AuditTrail


class AuditTrailModelForm(forms.ModelForm):

    is_alert = forms.BooleanField(
        widget=forms.CheckboxInput, required=False)

    message = forms.CharField(
        widget=forms.Textarea, required=False)

    class Meta:
        model = AuditTrail
        exclude = ('cdate', 'udate',)
        # widgets = {
        #     'creator': AutocompleteWidget(url='user-profiles:user-auth-autocomplete'),
        # }

