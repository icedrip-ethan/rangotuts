from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, HttpResponseRedirect
from .models import Category, Page
from .forms import CategoryForm, PageForm, UserForm, UserProfileForm
from django.contrib.auth import authenticate, login

def index(request):
  category_list = Category.objects.order_by('-likes')[:5]
  page_list = Page.objects.order_by('-views')[:5]
  context_dict = {'categories': category_list, 'pages': page_list}
  return render(request, 'rango/index.html', context_dict)

def about(request):
  print(request.method)
  print(request.user)
  return render(request, 'rango/about.html')

def show_category(request, category_name_slug):
  context_dict = {}

  try:
    category = Category.objects.get(slug=category_name_slug)

    pages = Page.objects.filter(category=category)

    context_dict['pages'] = pages

    context_dict['category'] = category

  except Category.DoesNotExist:
    context_dict['category'] = None
    context_dict['pages'] = None

  return render(request, 'rango/category.html', context_dict)

def add_category(request):
  form = CategoryForm()

  if request.method == "POST":
    form = CategoryForm(request.POST)
    if form.is_valid():
      form.save(commit=True)

      return redirect('index')
    else:
      print(form.errors)

  return render(request, 'rango/add_category.html', {'form':form})

def add_page(request, category_name_slug):

  try:
    category = Category.objects.get(slug=category_name_slug)
  except Category.DoesNotExist:
    # category = None
    return redirect('index')

  form = PageForm()

  if request.method == 'POST':
    form = PageForm(request.POST)
    if form.is_valid():
      if category:
        page = form.save(commit=False)
        page.category = category
        page.views = 0
        page.save()
        # return show_category(request, category_name_slug)
        return HttpResponseRedirect(reverse('rango:show_category', args=(category_name_slug,)))

    else:
      print(form.errors)
  context_dict = {'form': form, 'category': category}
  return render(request, 'rango/add_page.html', context_dict)

def register(request):
  registered = False

  if request.method == 'POST':
    user_form = UserForm(data=request.POST)
    profile_form = UserProfileForm(data=request.POST)

    if user_form.is_valid() and profile_form.is_valid():
      user = user_form.save()
      user.set_password(user.password)
      user.save()

      profile = profile_form.save(commit=False)
      profile.user = user

      if 'picture' in request.FILES:
        profile.picture = request.FILES['picture']

      profile.save()

      registered = True
      return render(request, 'rango/register.html', {'registered': registered})
    else:
      print(user_form.errors, profile_form.errors)
  else:
    user_form = UserForm()
    profile_form = UserProfileForm()

    return render(request, 'rango/register.html',{'user_form': user_form, 'profile_form': profile_form, 'registered': registered})

def user_login(request):
  if request.method == 'POST':
    username = request.POST.get('username')
    password = request.POST.get('password')

    # authenticate() returns User Object or None
    user = authenticate(username=username, password=password)

    if user:
      if user.is_active():
        login(request, user)
        return HttpResponseRedirect(reverse('index'))
      else:
        return HttpResponse('Your rango account is disabled')
    else:
      # print("Invalid login details")
      return HttpResponse('Invalid login details')
  else:
    return render(request, 'rango/login.html')