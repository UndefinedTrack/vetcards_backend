from django.shortcuts import render
from django.apps import apps

from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.contrib.auth.hashers import make_password
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST

from .forms import UserForm, UpdateUserForm

# Create your views here.

@require_GET
def csrf(request):
    return JsonResponse({'csrfToken': get_token(request)})

@csrf_exempt
@require_POST
def create_user(request):
    
    '''Создание пользователя'''
    
    User = apps.get_model('users.User')
    form = UserForm(request.POST)
    
    if form.is_valid():
        
        user = User.objects.create(username=form.cleaned_data['username'],
                                   password=make_password(form.cleaned_data['password']),
                                   first_name=form.cleaned_data['first_name'],
                                   patronymic=form.cleaned_data['patronymic'],
                                   last_name=form.cleaned_data['last_name'],
                                   phone=form.cleaned_data['phone'],
                                   email=form.cleaned_data['email'])
        
        usr = {'id': user.id, 'username': user.username, 'first_name': user.first_name,
               'patronymic': user.patronymic, 'last_name': user.last_name,
               'phone': user.phone, 'email': user.email}
        
        return JsonResponse({"user": usr})
        
    return JsonResponse({"errors": form.errors})


@csrf_exempt
@require_POST
def update_user_info(request):

    '''Обновление информации о пользователе'''
    
    User = apps.get_model('users.User')
    form = UpdateUserForm(request.POST)
    
    if form.is_valid():
        
        user = User.objects.filter(id=form.cleaned_data['id']).first()
        
        if user == None:
            return JsonResponse({"errors": "User not found"})
        
        for k in form.cleaned_data.keys():
            print(k)
            if k != 'id' and form.cleaned_data[k] != '':
                print(user.__dict__[k])
                user.__dict__[k] = form.cleaned_data[k]
                
        user.save(force_update=True)

        usr = {'id': user.id, 'username': user.username, 'first_name': user.first_name,
               'patronymic': user.patronymic, 'last_name': user.last_name,
               'phone': user.phone, 'email': user.email}
        
        return JsonResponse({"user": usr})
            
    return JsonResponse({"errors": form.errors})
    
    
@require_GET
def get_user_info(request):

    '''Получение информации о пользователе'''
    
    User = apps.get_model('users.User')
    
    user = User.objects.filter(id=int(request.GET['uid'])).values('id', 'username', 'first_name', 'patronymic', 
                                                   'last_name', 'phone', 'email')
    
    return JsonResponse({"user": list(user)[0]})

@require_GET
def vets_list(request):

    '''Выдает список ветеринаров'''

    User = apps.get_model('users.User')
    
    vets = User.objects.filter(vet=True).values('id', 'first_name', 'patronymic', 
                                                   'last_name')

    return JsonResponse({"vets": list(vets)})