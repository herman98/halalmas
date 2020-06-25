import os, re
from datetime import datetime

from django import template
from django.contrib.humanize.templatetags.humanize import intcomma

from babel.numbers import format_decimal

from ..functions import display_name

register = template.Library()


@register.filter(is_safe=True, name='show_filename')
def show_filename(value):
    filename = os.path.basename(value)
    if filename:
        return filename
    else:
        return '-'

@register.filter(is_safe=True, name='f_rupiahs')
def format_rupiahs(rupiahs, arg):
    if rupiahs:
        if arg == 'yes':
        	return "Rp %s.00,-" % (format_decimal(rupiahs, locale='id_ID'))
        elif arg == 'no_currency':
            return "%s" % (format_decimal(rupiahs, locale='id_ID'))
        else:
        	return "Rp %s" % (format_decimal(rupiahs, locale='id_ID'))
    else:
        return '0'

@register.filter(is_safe=True, name='f_phone')
def format_phone(phone_number):
    if phone_number is not None and phone_number != '':
        try:
            aa = int(phone_number)
        except Exception as e:
            print("error phone_number:{}".format(e))
            return '-'

        clean_phone_number = re.sub('[^0-9]+', '', phone_number)
        formatted_phone_number = re.sub("(\d)(?=(\d{3})+(?!\d))", r"\1-", "%d" % int(clean_phone_number[:-1])) + clean_phone_number[-1]
        return "%s" % formatted_phone_number
    else:
        return "-"

@register.filter(name='display_safe')
def display_safe(field):
    return display_name(field)


@register.filter(name='display_img_status')
def display_img_status(field):
    """
        (DELETED, 'Deleted'),
        (CURRENT, 'Current'),
        (RESUBMISSION_REQ, 'Resubmission Required')
    """
    if field==0:
        return "Normal"
    elif field==-1:
        return "Tidak Terpakai"
    else:
        return "Butuh Dikirim Ulang"


@register.filter(name='bapak_or_ibu')
def bapak_or_ibu(field):
    field_check = field.lower()
    if(field_check=='p' or field_check=='pria' or \
        field_check=='l' or field_check=='laki'):
        return 'bapak'.title()
    else:
        return 'ibu'.title()

@register.filter(is_safe=True, name='f_rupiahs_percent')
def f_rupiahs_percent(rupiahs, arg):
    if rupiahs:
        if arg == '':
            return format_rupiahs(rupiahs,'no')
        else:
            ret = '{0:.2f}'.format(((float(arg) * float(rupiahs)) / 100))
            return format_rupiahs(ret,'no')
    else:
        return '-'

@register.filter(is_safe=True, name='no_ktp')
def no_ktp(field):
    if field:
        try:
            return "%s.%s.%s.%s.%s" % (
                    field[:2],
                    field[2:4],
                    field[4:6],
                    field[6:12],
                    field[12:])
        except Exception as e:
            return '-'
    else:
        return '-'

@register.filter(is_safe=True, name='no_hp')
def no_hp(field):
    if field:
        try:
            field_here = str(field).replace(" ",'')
            return "%s %s %s" % (
                    field_here[:4],
                    field_here[4:8],
                    field_here[8:])
        except Exception as e:
            return '-'
    else:
        return '-'

@register.filter(is_safe=True, name='age')
def age(field, d=None):
    if d is None:
        d = datetime.now()
    try:
        ret_val = (d.year - field.year) - int((d.month, d.day) < (field.month, field.day))
    except Exception as e:
        ret_val = ''
    return  ret_val


@register.filter(is_safe=True, name='verification_option')
def verification_option(field, option_list):
    if field:
        ret_val = option_list[field][1]
    else:
        ret_val = 'Blum di Cek'
    return ret_val


@register.filter(is_safe=True, name='f_rupiahs_cek')
def f_rupiahs_cek(rupiahs):
    if rupiahs:
        return format_rupiahs(rupiahs,'no')
    else:
        return 'Blum di Cek'


@register.filter(is_safe=True, name='percentage_100')
def percentage_100(value):
    if value:
        return "%s" % (value * 100)
    else:
        return '-'