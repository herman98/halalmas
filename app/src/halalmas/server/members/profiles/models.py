import logging
from hashids import Hashids

from datetime import date
from datetime import datetime
from datetime import timedelta

from django.db import models
from django.core import exceptions
from django.contrib.auth.models import User

from cuser.fields import CurrentUserField
from simple_history.models import HistoricalRecords

# from django.utils.safestring import mark_safe
from halalmas.server.models import TimeStampedModel
from .constants import LoginWith, LoginFrom

from halalmas.server.objects.companies.models import Company
from halalmas.server.objects.banks.models import BankAccount


logger = logging.getLogger(__name__)


class GetInstanceMixin(object):
    def get_or_none(self, **kwargs):
        """Extends get to return None if no object is found based on query."""
        try:
            logger.debug(
                "Getting instance for %s with %s" % (self.model, kwargs))
            instance = self.get(**kwargs)
            logger.info(
                "Got instance primary_key=%s for %s" % (instance.pk, self.model))
            return instance
        except exceptions.ObjectDoesNotExist:
            logger.warn(
                "No instance found for %s with %s" % (self.model, kwargs))
            return None


class CustomerUserRole(TimeStampedModel):
    """
    This is Customer User Role
    """
    role_name = models.CharField(max_length=125, blank=True, null=True)

    class Meta:
        db_table = "user_roles"
        verbose_name_plural = u'Customer User Roles'
        ordering = ['role_name', ]

    def __str__(self):
        return "{}".format(self.role_name)


class CustomerUserProfileManager(GetInstanceMixin, models.Manager):
    pass


class CustomerUserProfile(TimeStampedModel):
    """
    This is Customer Profile data
    """
    LoginWith = LoginWith
    LoginFrom = LoginFrom

    role = models.ManyToManyField(CustomerUserRole)

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    salt = models.CharField(max_length=300, blank=True, null=True)

    first_name = models.CharField(max_length=125, blank=True, null=True)
    last_name = models.CharField(max_length=125, blank=True, null=True)
    full_name = models.CharField(max_length=225, blank=True, null=True)

    avatar = models.CharField(max_length=225, blank=True, null=True)
    address_home = models.TextField(blank=True, null=True)
    address_office = models.CharField(max_length=25, blank=True, null=True)
    confirm_date = models.DateTimeField(blank=True, null=True)

    login_with = models.CharField(max_length=50,
                                  choices=LoginWith.get_choices(True),
                                  blank=True, null=True,
                                  default=LoginWith.NORMAL,
                                  verbose_name="Login With",
                                  help_text="this user login with 3rd party app.")
    login_from = models.CharField(max_length=50,
                                  choices=LoginFrom.get_choices(True),
                                  blank=True, null=True,
                                  default=LoginFrom.WEBSITE,
                                  verbose_name="Login From",
                                  help_text="this user login from internal system.")

    is_confirm = models.BooleanField(
        default=False, blank=True, null=True)
    # is_potong_pajak = models.BooleanField(default=False, blank=True, null=True)

    bio = models.TextField(max_length=500, blank=True,
                           verbose_name="Biodata Customer",)
    location = models.CharField(max_length=30, blank=True)
    
    gender = models.CharField(max_length=100, blank=True)

    birth_date = models.DateField(null=True, blank=True)

    email = models.EmailField(blank=True, null=True)
    is_email_verified = models.NullBooleanField()
    phone = models.CharField(max_length=50, blank=True, null=True)
    is_phone_verified = models.NullBooleanField()
    country = models.CharField(max_length=50, blank=True, null=True,
                               default='ID')

    self_referral_code = models.CharField(max_length=20, blank=True, null=True)
    email_verification_key = models.CharField(
        max_length=300, blank=True, null=True)
    email_key_exp_date = models.DateTimeField(blank=True, null=True)
    reset_password_key = models.CharField(
        max_length=300, blank=True, null=True)
    reset_password_exp_date = models.DateTimeField(blank=True, null=True)

    password_social_media = models.CharField(max_length=300, blank=True, null=True)

    hash_user = models.CharField(max_length=300, blank=True, null=True)

    latest_change_password = models.DateField(null=True, blank=True)

    # History
    history = HistoricalRecords(table_name='user_profile_history')

    objects = CustomerUserProfileManager()

    class Meta:
        db_table = "user_profile"
        verbose_name_plural = u'Customer Profiles'
        ordering = ['user__username', 'full_name', 'salt']

    def set_full_name(self):
        _full_name_ = ""
        if self.first_name:
            _full_name_ = self.first_name
        if self.last_name:
            _full_name_ += " " + self.last_name
        self.full_name = _full_name_

    def save(self, *args, **kwargs):
        # self.set_full_name()
        super().save(*args, **kwargs)

    def __str__(self):
        return "{}:{}".format(self.user.username, self.full_name if self.full_name else "")

    def has_emailkey_expired(self):
        tz_info = self.email_key_exp_date.tzinfo
        return self.email_key_exp_date < datetime.now(tz_info)

    def has_resetkey_expired(self):
        tz_info = self.reset_password_exp_date.tzinfo
        return self.reset_password_exp_date < datetime.now(tz_info)

    def generate_referral_code(self):
        """
        This code will be used for the customer to earn some credit if their
        friends apply using the code and complete a loan.
        """
        if self.self_referral_code != '' and self.self_referral_code is not None:
            logger.debug({
                'self_referral_code': self.self_referral_code,
                'status': 'already_generated'
            })
            return False

        # WARNING: Once deployed, do NOT change the customer base ID, salt,
        # alphabet, or minimum length to avoid referral code collision.

        customer_base_id = 10000000000
        salt = "halalmas.com Referral Code"
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
        min_length = 5

        logger.debug({
            'self_referral_code': self.self_referral_code,
            'action': 'generating'
        })

        hashids = Hashids(salt=salt, alphabet=alphabet, min_length=min_length)
        # Since customer table primary key starts from 1 billion, subtracting
        # it from 1 billion still maintains uniqueness. The smaller the
        # uniqueness, the smaller the generated code.
        unique_id = customer_base_id - self.id
        referral_code = hashids.encode(unique_id)
        self.self_referral_code = referral_code

        logger.info({
            'unique_id': unique_id,
            'self_referral_code': self.self_referral_code,
            'status': 'generated'
        })

        return True


class CustomerCompanyUser(TimeStampedModel):
    """
    This is User Customer Company
    """
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    customer_user = models.ForeignKey(
        CustomerUserProfile, on_delete=models.CASCADE)
    bank_account = models.ForeignKey(
        BankAccount, on_delete=models.CASCADE, blank=True, null=True)

    is_pkp = models.BooleanField(
        default=False, blank=True, null=True)
    is_potong_pajak = models.BooleanField(
        default=False, blank=True, null=True)

    class Meta:
        db_table = "user_profile_company"
        verbose_name_plural = u'Customer User Company '
        ordering = ['company__name', ]

    def __str__(self):
        return "{}-{}".format(self.company.name, self.customer_user.user.username)
