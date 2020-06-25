from django.db import models
# from django.utils.safestring import mark_safe
from cuser.fields import CurrentUserField

from halalmas.server.models import TimeStampedModel
from .constants import BankAccountType


class Bank(TimeStampedModel):
    """
    This is data master of Bank 
    """
    code = models.CharField(max_length=50, verbose_name="Kode Bank",
                            help_text="e.g: BCA, Bank Mandiri, BRI, etc")
    name = models.CharField(max_length=125, verbose_name="Nama Bank",
                            blank=True, null=True,
                            help_text="PT. Bank Central Asia, PT. Bank Mandiri")
    country = models.CharField(max_length=125, verbose_name="Negara",
                               default='ID - Indonesia',
                               blank=True, null=True)

    class Meta:
        db_table = "m_bank"
        verbose_name_plural = u'Banks'
        ordering = ['code', 'name']

    @classmethod
    def create(cls, code, name=None):
        if name:
            cls_here = cls(code=code)
        else:
            cls_here = cls(code=code, name=name)
        cls_here.save()
        return cls_here

    def __str__(self):
        return "{}:{}".format(self.code, self.name)


class BankAccount(TimeStampedModel):
    """
    This is data master of Bank Account
    """
    BankAccountType = BankAccountType

    bank = models.ForeignKey(Bank, on_delete=models.CASCADE,
                             verbose_name="Nama Bank")
    account_no = models.CharField(
        max_length=125, verbose_name="Nomor Bank Account")
    account_name = models.CharField(max_length=125, verbose_name="Account Name",
                                    blank=True, null=True,
                                    help_text="PT. Urban Solusi Digital, Anna Chairunissa, Irien Sasoko")
    account_type = models.CharField(max_length=125,
                                    choices=BankAccountType.get_choices(True),
                                    default=BankAccountType.BT,
                                    verbose_name="Tipe Account",
                                    blank=True, null=True)
    bank_branch = models.CharField(max_length=125, verbose_name="Cabang Bank",
                                   blank=True, null=True)
    default_currency = models.CharField(max_length=125, verbose_name="Mata Uang default",
                                        blank=True, null=True,
                                        default='IDR')

    # user identification
    creator = CurrentUserField(related_name="m_bank_account",
                               verbose_name="createby", on_delete=models.DO_NOTHING)

    # objects = BankAccountManager()

    class Meta:
        db_table = "m_bank_account"
        verbose_name_plural = u'BankAcounts'
        ordering = ['bank', 'account_no', 'account_name']

    @classmethod
    def create(cls, account_no, account_name, bank_branch):
        cls_here = cls(account_no=account_no,
                       account_name=account_name, bank_branch=bank_branch)
        cls_here.save()
        return cls_here

    def __str__(self):
        return "[{}]{}:{}".format(self.bank.code,
                                  self.account_no, self.account_name)
