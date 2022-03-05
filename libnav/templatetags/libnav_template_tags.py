from django import template

register = template.Library()

# @register.inclusion_tag('rango/floors.html')
# def get_floor_list(current_floor=None):
#    return {'floors': Floor.objects.all(),
#            'current_floor': current_floor}
