from django import template
from django.utils.safestring import mark_safe
from libnav.models import UserProfile
from libnav.miscs.locations_keeper import locations
import json

register = template.Library()

@register.simple_tag(takes_context=True)
def get_user(context):
    request = context['request']
    try:
        return request.user
    except KeyError:
        return None
        
@register.filter(is_safe=True)
def set_variables(input_dict):
    # make sure the string isn't weird
    # and convert python dict to json string
    return mark_safe(json.dumps(input_dict))
    
@register.inclusion_tag('friend_list.html')
def show_friends(user, floor):
    friends = user.userprofile.friends.all()
    friends = [friend for friend in friends if locations.get_floor(friend) == floor]
    return {'friends': friends}

@register.filter()
def floor_range(r):
    return range(r,0,-1)
