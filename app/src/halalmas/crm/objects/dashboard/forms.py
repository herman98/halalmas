from django import forms
from django.forms import ModelForm
from django.forms.widgets import Select, RadioSelect
from django.contrib.gis import admin

from dal import autocomplete
from halalmas.core.forms import AutocompleteWidget

from .functions import create_or_update_defaultrole
from .models import CRMSetting


class CRMSettingModelForm(forms.ModelForm):

    class Meta:
        model = CRMSetting
        exclude = ('cdate', 'udate',)
        widgets = {
            'user': AutocompleteWidget(url='user-profiles:user-auth-autocomplete'),
        }


class DefaultRoleForm(forms.Form):

    role_default = forms.CharField(
        max_length=CRMSetting._meta.get_field('role_default').max_length,
        widget=forms.Select(attrs={'class': 'form-control',
                                   'required': "",
                                   }),
        label='Pilih Default Role')

    def __init__(self, user_instance, *args, **kwargs):
        super(DefaultRoleForm, self).__init__(*args, **kwargs)
        self.user = user_instance
        qs = self.user.groups.all()
        self.fields['role_default'] = forms.ChoiceField(
            choices=[(str(o), str(o)) for o in qs])

    def clean_role_default(self):
        if 'role_default' in self.cleaned_data:
            # check if they not null each other
            role_default = self.cleaned_data['role_default']
            if role_default:
                return role_default
            else:
                raise forms.ValidationError("Role Default harus dipilih !!!")
        raise role_default

    def save(self, commit=True):
        if commit:
            return create_or_update_defaultrole(self.user, self.cleaned_data['role_default'])
        return None
