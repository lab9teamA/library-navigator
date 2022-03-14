from django import template

register = template.Library()


# @register.inclusion_tag('libnav/floors.html')
# def get_floor_list(current_floor=None):
#     # return {'floors': Floor.objects.all(),
#     #         'current_floor': current_floor}
#     return {'floors': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 'current_floor': current_floor}
