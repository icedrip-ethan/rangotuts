import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tango_with_django_project.settings')

import django
django.setup()
from rango.models import Category, Page

def populate():
  python_pages = [
  {"title": 'Official Python Tutorial', "url": 'http://docs.python.org/2/tutorial/', 'views':50},
  {'title': 'How to Thing Like a Computer Scientist', 'url': 'http://www.greeteapress.com/thingpython/', 'views':60}
  ]

  django_pages = [
  {"title":"Official Django Tutorial",
  "url":"https://docs.djangoproject.com/en/1.9/intro/tutorial01/", 'views':70},
  {"title":"Django Rocks",
  "url":"http://www.djangorocks.com/", 'views':80},
  {"title":"How to Tango with Django",
  "url":"http://www.tangowithdjango.com/", 'views':90} 
  ]

  other_pages = [
  {"title":"Bottle",
  "url":"http://bottlepy.org/docs/dev/", 'views':100},
  {"title":"Flask",
  "url":"http://flask.pocoo.org", 'views':110} 
  ]


  cats = {"Python": {"pages": python_pages, 'views':128, 'likes':64},
  "Django": {"pages": django_pages, 'views':64, 'likes':32},
  "Other Frameworks": {"pages": other_pages, 'views':32, 'likes':16}}

  for cat, cat_data in cats.items():
    c = add_cat(cat, cat_data['views'], cat_data['likes'])
    for p in cat_data["pages"]:
      add_page(c, p["title"], p["url"], p['views'])
  
  # Print out the categories we have added.
  for c in Category.objects.all():
    for p in Page.objects.filter(category=c):
      print("- {0} - {1}".format(str(c), str(p)))


def add_page(cat, title, url, views=0):
  p = Page.objects.get_or_create(category=cat, title=title)[0]
  p.url=url

  p.views=views

  p.save()
  return p
def add_cat(name, views, likes):
  # get_or_create() returns tuple of form object, created ... obj, bool
  c = Category.objects.get_or_create(name=name)[0]
  c.views = views
  c.likes = likes
  
  # if c.name == 'Python':
  #   c.views = 128
  #   c.likes = 64
  # elif c.name == 'Django':
  #   c.views = 64
  #   c.likes = 32
  # elif c.name == 'Other Frameworks':
  #   c.views = 32
  #   c.likes = 16

  c.save()
  return c

# Start execution here!
if __name__ == '__main__':
  print("Starting Rango population script...")
  populate()
