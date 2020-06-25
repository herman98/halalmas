import os
from datetime import datetime
from django.template import Library
from django.contrib.auth.models import Group

from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe

from ..functions import display_name as _display_name

register = Library()

@register.filter
def display_name(value):
    result = value
    if isinstance(value, (str, unicode)):
        result = _display_name(value)
    return result


@register.filter
def display_filename(value):
    if value:
        return os.path.basename(value.name)
    else:
        return ''

@register.filter
def filesize(value):
    """Returns the filesize of the filename given in value"""
    return os.path.getsize(value)

@register.filter
def display_value(value, object):
#     print value
#     print object.choices
    
#     if isinstance(value, (str, unicode)):
#         print 'data okay'
    try:
        _choices = object.choices
        for item in _choices:
            if item[0]==value:
                result = item[1]
        result = _display_name(result)
    except:
        result = value
    return result

@register.filter()
@stringfilter
def linebreaksodt(value, autoescape=None):
    """
    Converts all newlines in a piece of plain text to XML line breaks
    (``<text:line-break />``).
    """
#     autoescape = autoescape and not isinstance(value, SafeData)
#     value = normalize_newlines(value)
#     if autoescape:
#         value = escape(value)
    return mark_safe(value.replace('\n', '<text:line-break />'))

@register.filter
def datetime_now(value):
    return datetime.now()

from PIL import Image
# from django.conf import settings

register = Library()

@register.filter
def thumbnail(file, size='104x104'):
    # defining the size
    x, y = [int(x) for x in size.split('x')]
    # defining the filename and the miniature filename
    filehead, filetail = os.path.split(file.path)
    basename, format = os.path.splitext(filetail)
    miniature = basename + '_' + size + format
    filename = file.path
    miniature_filename = os.path.join(filehead,     miniature)
    filehead, filetail = os.path.split(file.url)
    miniature_url = filehead + '/' + miniature
    if os.path.exists(miniature_filename) and    os.path.getmtime(filename)>os.path.getmtime(miniature_filename):
        os.unlink(miniature_filename)
    # if the image wasn't already resized, resize it
    if not os.path.exists(miniature_filename):
        image = Image.open(filename)
        image.thumbnail([x, y], Image.ANTIALIAS)
    try:
        image.save(miniature_filename, image.format, quality=90, optimize=1)
    except:
        image.save(miniature_filename, image.format, quality=90)

    return miniature_url

@register.filter(name='has_group')
def has_group(user, group_name): 
    group = Group.objects.get(name=group_name) 
    return True if group in user.groups.all() else False