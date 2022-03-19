from django import template
from libnav.models import UserProfile

register = template.Library()

@register.simple_tag(takes_context=True)
def get_username(context):
    request = context['request']
    try:
        return UserProfile.objects.get(user_id=request.session['user_id']).user.username
    except KeyError:
        return None

# @register.inclusion_tag('libnav/floors.html')
# def get_floor_list(current_floor=None):
#     # return {'floors': Floor.objects.all(),
#     #         'current_floor': current_floor}
#     return {'floors': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 'current_floor': current_floor}
