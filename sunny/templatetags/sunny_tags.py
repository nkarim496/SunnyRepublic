from django import template
from SunnyRepublic.settings import MEDIA_URL

register = template.Library()


@register.inclusion_tag('sunny/menu.html')
def get_menu(authenticated_user):
    """renders specialized menu whether for student or teacher"""
    menu_context = {}
    print("User in the Students group: {}".format(authenticated_user.groups.filter(name="Students").exists()))
    if authenticated_user.groups.filter(name='Students').exists():
        menu_context['students'] = True
    elif authenticated_user.groups.filter(name='Teachers').exists():
        menu_context['teachers'] = True
    menu_context['user'] = authenticated_user
    menu_context['MEDIA_URL'] = MEDIA_URL
    return menu_context


@register.inclusion_tag('sunny/slide_menu.html')
def get_slide_menu(authenticated_user):
    """renders slide menu whether for student or teacher"""
    menu_context = {}
    if authenticated_user.groups.filter(name='Students').exists():
        menu_context['students'] = True
    elif authenticated_user.groups.filter(name='Teachers').exists():
        menu_context['teachers'] = True
    menu_context['user'] = authenticated_user
    menu_context['MEDIA_URL'] = MEDIA_URL
    return menu_context