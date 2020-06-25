import socket
import logging

from datetime import datetime

from .models import AuditTrail

logger = logging.getLogger(__name__)

def record_audit(message, obj=None, request=None, remote_address=None, is_alert=False):
    """Create an audit trail record
        sample :
        record_audit(
                    '%s logs-in to the system' % request.user.username,
                     user_obj, is_alert=True)
        record_audit(
                'Password reset: \'%s\'' % account_obj.username,
                account_obj, is_alert=True)
    """
    params = {
        'obj_model': None,
        'remote_address': None,
        'server': socket.gethostname(),
        'ref_type': None,
        'ref_value': None
    }
    MAX_LENGTH = 50
    if obj:
        params['obj_model'] = obj
       
        params['ref_type'] = obj.__class__.__name__[:MAX_LENGTH]
        try:
            params['ref_value'] = int(getattr(obj, 'id', ''))
        except ValueError:
            params['ref_value'] = None

    if remote_address:
        params['remote_address'] = remote_address
    elif request:
        client_ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR', '')).split(',')[0].strip()
        params['remote_address'] = f'{client_ip}'

    params['remote_address'] = params['remote_address'][:MAX_LENGTH]
    
    # print(message, params)
    audit_obj = AuditTrail(
        message=message, **params)
    audit_obj.save()

    logging.info("Audit Trail success created with id {}".format(audit_obj.pk))
    return audit_obj


def test_record_audit():
    from django.contrib.auth.models import User 
    
    account_objs = User.objects.filter(username='admin')
    print(f'account_objs.count(): {account_objs.count()}')
    if account_objs.count() >= 1:
        account_obj = account_objs[0]
        obj_out = record_audit(
                    'User Login Sukses: \'%s\'' % account_obj.username,
                    account_obj, is_alert=True)
        print(f'AuditTrail Sukses {obj_out}, test SUCCESS')
    else:
        print(f'User not found, test FAIL')