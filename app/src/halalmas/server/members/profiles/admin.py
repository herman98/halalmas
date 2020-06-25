from django import forms
from django.contrib.gis import admin

from dal import autocomplete
from halalmas.core.forms import AutocompleteWidget

from .models import CustomerUserProfile, CustomerUserRole, CustomerCompanyUser


class CustomerUserProfileModelForm(forms.ModelForm):

    is_email_verified = is_phone_verified = is_confirm = forms.BooleanField(
        widget=forms.CheckboxInput, required=False)

    location = address_home = address_office = forms.CharField(
        widget=forms.Textarea, required=False)

    class Meta:
        model = CustomerUserProfile
        exclude = ('cdate', 'udate',)
        widgets = {
            'user': AutocompleteWidget(url='user-profiles:user-auth-autocomplete'),
        }


class CustomerUserProfileAdmin(admin.OSMGeoAdmin):
    """ Customer User Data """
    form = CustomerUserProfileModelForm

    list_display = ['user', 'email', 'self_referral_code',  'salt', 'first_name', 'phone', 'country',
                    'login_with', 'login_from', 'is_confirm']
    search_fields = ['salt', 'user__username',
                     'email', 'first_name', 'last_name', 'full_name']

    list_filter = ['login_with', 'login_from', 'is_confirm']

    fieldsets = (
        ('Foreign Key', {
            'fields': ('user', 'role'),
        }),
        ('Data Field', {
            'fields': ('salt', 'email', 'first_name', 'last_name', 'full_name', 'avatar', 'address_home', 'address_office',
                       'phone', 'country', 'login_with', 'login_from', 'bio', 'location', 'birth_date',  'confirm_date', 'is_confirm',),
        }),
        ('Confirmation Field', {
            'fields': ('self_referral_code', 'is_email_verified', 'is_phone_verified', 'email_verification_key', 'email_key_exp_date',
                       'reset_password_key', 'reset_password_exp_date', 'password_social_media',),
        }),
        ('Timestamp', {
            'classes': ('collapse',),  # collapse
            'fields': ('delstatus', 'deldate', 'cdate', 'udate'),
        }),
    )
    readonly_fields = ('cdate', 'udate', 'full_name',)


class CustomerUserRoleAdmin(admin.OSMGeoAdmin):
    """ Customer User Roles Data """

    list_display = ['role_name']
    search_fields = ['role_name']

    fieldsets = (
        ('Data Field', {
            'fields': ('role_name', ),
        }),
        ('Timestamp', {
            'classes': ('collapse',),  # collapse
            'fields': ('delstatus', 'deldate', 'cdate', 'udate'),
        }),
    )
    readonly_fields = ('cdate', 'udate')


class CustomerUserModelForm(forms.ModelForm):

    is_pkp = forms.BooleanField(widget=forms.CheckboxInput, required=False)
    is_potong_pajak = forms.BooleanField(
        widget=forms.CheckboxInput, required=False)
    # first_name = forms.CharField(widget=forms.Textarea, required=False)
    # description = forms.CharField(widget=forms.Textarea, required=False)
    # status = forms.ChoiceField(
    #     choices=InquiryStatusForm.get_choices())

    class Meta:
        model = CustomerUserProfile
        exclude = ('cdate', 'udate',)
        widgets = {
            'customer_user': AutocompleteWidget(url='user-profiles:user-profile-autocomplete'),
            'company': AutocompleteWidget(url='company:company-autocomplete'),
            'bank_account': AutocompleteWidget(url='bank:bank-account-autocomplete'),
        }


class CustomerCompanyUserAdmin(admin.OSMGeoAdmin):
    """ Customer User Roles Data """
    form = CustomerUserModelForm

    list_per_page = 50
    list_display = ['company', 'customer_user',
                    'bank_account', 'is_pkp', 'is_potong_pajak', ]
    search_fields = ['company__name', 'customer_user__user__username', ]
    list_filter = ['is_pkp', 'is_potong_pajak']

    fieldsets = (
        ('Data Field', {
            'fields': ('company', 'customer_user',
                       'bank_account', 'is_pkp', 'is_potong_pajak', ),
        }),
        ('Timestamp', {
            'classes': ('collapse',),  # collapse
            'fields': ('delstatus', 'deldate', 'cdate', 'udate'),
        }),
    )
    readonly_fields = ('cdate', 'udate')


admin.site.register(CustomerUserProfile, CustomerUserProfileAdmin)
admin.site.register(CustomerUserRole, CustomerUserRoleAdmin)
admin.site.register(CustomerCompanyUser, CustomerCompanyUserAdmin)
