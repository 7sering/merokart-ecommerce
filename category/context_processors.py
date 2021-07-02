from .models import Category

def menu_links(request): #Note this function menu_links will must add in setting file as context processor
    links = Category.objects.all() #Fetching All objects
    return dict(links=links) 