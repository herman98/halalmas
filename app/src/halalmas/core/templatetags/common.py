from datetime import datetime

from django import template
from django.template import NodeList
from django.contrib.auth.models import Group

from halalmas.crm.objects.dashboard.functions import get_selected_role


register = template.Library()


@register.tag()
def ifusergroup(parser, token):
    """ Check to see if the currently logged in user belongs to a specific group.
    Requires the Django authentification contrib app and middleware

    Usage: {% ifusergroup Admins %} ... {% endifusergroup %}, or
           {% ifusergroup Admins %} ... {% else %} ... {% endifusergroup %}
    """
    # try:
    tag, group = token.split_contents()
    # except ValueError:
    #     raise template.TemplateSyntaxError("Tag 'ifusergroup' requires 1 argument.")

    nodelist_true = parser.parse(('else', 'endifusergroup'))
    token = parser.next_token()

    if token.contents == 'else':
        nodelist_false = parser.parse(('endifusergroup'))
        parser.delete_first_token()
    else:
        nodelist_false = NodeList()
    return GroupCheckNode(group, nodelist_true, nodelist_false)


class GroupCheckNode(template.Node):
    def __init__(self, group, nodelist_true, nodelist_false):
        self.group = group
        self.nodelist_true = nodelist_true
        self.nodelist_false = nodelist_false

    def render(self, context):
        user = template.Variable('user').resolve(context)

        if not user.is_authenticated:
            return self.nodelist_false.render(context)

        # print("self.group: {}".format(self.group))
        try:
            group = Group.objects.get(name=self.group)
            # print("self.group 1")
        except Group.DoesNotExist:
            return self.nodelist_false.render(context)

        if group in user.groups.all():
            return self.nodelist_true.render(context)
            # print("self.group 2")
        else:
            return self.nodelist_false.render(context)
            # print("self.group 3")


@register.tag()
def checkusergroup(parser, token):
    """ Check to see if the currently logged in user belongs to a specific group.
    Requires the Django authentification contrib app and middleware

    Usage: {% checkusergroup in [Admins, Client, Courier] %} ... {% endcheckusergroup %}, or
           {% checkusergroup in [Admins, Client, Courier] %} ... {% else %} ... {% endcheckusergroup %}
    """
    try:
        # print "token.split_contents(): ", token.split_contents()
        tag, in_separator, group = token.split_contents()
        # print "checkusergroup: tag, in_separator, group: " , tag, in_separator, group

        if str(in_separator).lower() != "in":
            raise template.TemplateSyntaxError(
                "Tag 'checkusergroup' need 'in' separator between tag and argument.")

    except ValueError:
        raise template.TemplateSyntaxError(
            "Tag 'checkusergroup' requires 2 argument.")

    nodelist_true = parser.parse(('else', 'endcheckusergroup'))
    token = parser.next_token()

    if token.contents == 'else':
        nodelist_false = parser.parse(('endcheckusergroup'))
        parser.delete_first_token()
    else:
        nodelist_false = NodeList()

    return MultiGroupCheckNode(group, nodelist_true, nodelist_false)


class MultiGroupCheckNode(template.Node):
    def __init__(self, group, nodelist_true, nodelist_false):
        self.group = group.strip().replace(
            "[", "").replace("'", "").replace("]", "").split(",")
        self.nodelist_true = nodelist_true
        self.nodelist_false = nodelist_false

    def render(self, context):
        #         user = resolve_variable('user', context)
        user = template.Variable('user').resolve(context)
        if not user.is_authenticated:
            return self.nodelist_false.render(context)

        found_status = False

        for group_item in self.group:
            here_group = None
            try:
                here_group = Group.objects.get(name=group_item)
            except Group.DoesNotExist:
                found_status = False

            if here_group in user.groups.all():
                found_status = True
                break
            else:
                found_status = False

        if found_status == False:
            return self.nodelist_false.render(context)
        else:
            return self.nodelist_true.render(context)


@register.tag()
def ifgroupselected(parser, token):
    """ Check to see if the currently logged in user belongs to a specific group.
    Requires the Django authentification contrib app and middleware

    Usage: {% ifgroupselected Admins %} ... {% endifgroupselected %}, or
           {% ifgroupselected Admins %} ... {% else %} ... {% endifgroupselected %}
    """
    try:
        tag, group = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError(
            "Tag 'ifgroupselected' requires 1 argument.")

    nodelist_true = parser.parse(('else', 'endifgroupselected'))
    token = parser.next_token()

    if token.contents == 'else':
        nodelist_false = parser.parse(('endifgroupselected'))
        parser.delete_first_token()
    else:
        nodelist_false = NodeList()

    return GroupSelectedNode(group, nodelist_true, nodelist_false)


class GroupSelectedNode(template.Node):
    def __init__(self, group, nodelist_true, nodelist_false):
        self.group = group
        self.nodelist_true = nodelist_true
        self.nodelist_false = nodelist_false

    def render(self, context):
        user = template.Variable('user').resolve(context)
        if not user.is_authenticated:
            return self.nodelist_false.render(context)

        if get_selected_role(user) == self.group:
            return self.nodelist_true.render(context)
        else:
            return self.nodelist_false.render(context)
