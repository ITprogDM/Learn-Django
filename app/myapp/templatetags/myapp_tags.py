from django import template
from django.db.models import Count, F

from myapp.models import Category

register = template.Library()



@register.simple_tag(name='get_list_categories')
def get_categories():
    return Category.objects.all()



@register.inclusion_tag('myapp/list_categories.html')
def show_categories():
    #categories = Category.objects.all()
    #categories = Category.objects.annotate(cnt=Count('myapp')).filter(cnt__gt=0)
    categories = Category.objects.annotate(cnt=Count('myapp', filter=F('myapp__is_published'))).filter(cnt__gt=0)
    return {'categories': categories}