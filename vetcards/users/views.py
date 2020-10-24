from django.shortcuts import render
from django.apps import apps

from django.http import JsonResponse, HttpResponse
from django.middleware.csrf import get_token
from django.contrib.auth.hashers import make_password
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST

from .forms import UserForm, UpdateUserForm, UserAvatarForm

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
        
        user = User.objects.filter(id=form.cleaned_data['pk']).first()
        
        if user == None:
            return JsonResponse({"errors": "User not found"})
        
        for k in form.cleaned_data.keys():
            print(k)
            if k != 'pk' and form.cleaned_data[k] != '':
                print(user.__dict__[k])
                user.__dict__[k] = form.cleaned_data[k]
                
        user.save()

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

@csrf_exempt
@require_POST
def upload_user_avatar(request):
    
    User = apps.get_model('users.User')
    
    form = UserAvatarForm(request.POST, request.FILES)
    
    if form.is_valid():
        
        user = User.objects.filter(id=form.cleaned_data['pk']).first()
        
        if user == None:
            return JsonResponse({"error": "Pet not found"})
        
        user.avatar = form.cleaned_data['avatar']
        user.save()
        
        user_avatar = {'id': user.id,
                      'avatar': user.avatar.url.replace('http://hb.bizmrg.com/undefined/',  '/users/avatars/')}
        
        return JsonResponse({'user_avatar': user_avatar})
    
    
    return JsonResponse({'errors': form.errors}, status=400)


@csrf_exempt
@require_GET
def protected_file(request):
    if request.user.is_authenticated:
        url = request.path.replace('/users/avatars', '/protected')
        print(url)
        response = HttpResponse(status=200)
        response['X-Accel-Redirect'] = url
        print(response.has_header('X-Accel-Redirect'))
        
        if 'Expires' in request.GET.keys():
            response['X-Accel-Expires'] = request.GET['Expires']
        response['Content-type'] = ''
        return response
    else:
        return HttpResponse('<h1>File not found</h1>', status=404)