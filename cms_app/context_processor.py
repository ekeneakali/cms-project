from cms_app.models import *

def category_menu(request):
    return {'menu':Category.objects.all()}