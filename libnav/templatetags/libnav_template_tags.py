from django import template
from django.utils.safestring import mark_safe
from libnav.models import UserProfile
import json

register = template.Library()

@register.simple_tag(takes_context=True)
def get_username(context):
    request = context['request']
    try:
        return UserProfile.objects.get(user_id=request.session['user_id']).user.username
    except KeyError:
        return None
        
@register.filter(is_safe=True)
def set_variables(input_dict):
    # make sure the string isn't weird
    # and convert python dict to json string
    return mark_safe(json.dumps(input_dict))

# @register.inclusion_tag('libnav/floors.html')
# def get_floor_list(current_floor=None):
#     # return {'floors': Floor.objects.all(),
#     #         'current_floor': current_floor}
#     return {'floors': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 'current_floor': current_floor}
