from __future__ import unicode_literals

import hashlib
import os
import mimetypes
import logging
import random
import re
import shutil
import json
import zipfile

from hashids import Hashids
from babel.numbers import format_number

from django.conf import settings

from email_validator import validate_email
from email_validator import EmailNotValidError


logger = logging.getLogger(__name__)


def display_rupiah(number):
    return "Rp " + format_number(number, locale='id_ID')


def check_email(email):
    if email.endswith("tempat.com"):
        return True
    # verify the email format
    match = re.match(
        '^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', email)
    if match is None:
        return False
    # validate the domain using email_validator
    try:
        v = validate_email(email)

    except EmailNotValidError:
        return False

    if 'mx-fallback' in v:
        if v['mx-fallback'] != False:
            return False
    if 'unknown-deliverability' in v:
        if v['unknown-deliverability'] == 'timeout':
            return False

    return True


def generate_email_key(email):
    """
    Create a hash that will be concatinated in
    verification url to confirm email addrees.
    """
    salt = os.urandom(32).hex()
    # salt = hashlib.sha1(str(random.random())).hexdigest()
    if isinstance(email, str):
        email = email.encode('utf-8')
    # activation_key = hashlib.sha1(salt + email).hexdigest()

    hash = hashlib.sha512()
    hash.update(('%s%s' % (salt, email)).encode('utf-8'))
    activation_key = hash.hexdigest()

    logger.debug({
        'activation_key': activation_key,
        'email': email
    })
    return activation_key


def generate_referral_code(id_here):
    customer_base_id = 10000000000
    salt = "tempat.com Referral Code"
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
    min_length = 5

    logger.debug({
        'method': 'generate_referral_code',
        'action': 'generating'
    })

    hashids = Hashids(salt=salt, alphabet=alphabet, min_length=min_length)
    print(f'hashids : {hashids}')
    # Since customer table primary key starts from 1 billion, subtracting
    # it from 1 billion still maintains uniqueness. The smaller the
    # uniqueness, the smaller the generated code.
    unique_id = customer_base_id - id_here
    print(f'unique_id : {unique_id}')
    referral_code = hashids.encode(unique_id)
    print(f'referral_code : {referral_code}')

    logger.info({
        'unique_id': unique_id,
        'self_referral_code': referral_code,
        'status': 'generated'
    })
    return referral_code

# def format_e164_indo_phone_number(phone_number):
#     parsed_phone_number = phonenumbers.parse(phone_number, "ID")
#     e164_indo_phone_number = phonenumbers.format_number(
#         parsed_phone_number, phonenumbers.PhoneNumberFormat.E164)
#     logger.debug({
#         'phone_number': phone_number,
#         'formatted_phone_number': e164_indo_phone_number
#     })
#     return e164_indo_phone_number
