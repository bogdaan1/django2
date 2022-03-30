from atexit import register
from django import template 
from .. models import Brand

register = template.Library()

@register.inclusion_tag('brands.html')
def brands():
    brands_list = Brand.objects.all()
    return {'brand': brands_list}