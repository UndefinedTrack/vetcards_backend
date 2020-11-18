from django.shortcuts import render
from django.apps import apps

from django.http import JsonResponse, HttpResponse
from django.middleware.csrf import get_token
from django.contrib.auth.hashers import make_password
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST

from django.contrib.auth.decorators import login_required

from django.views.decorators.cache import cache_page
from django.core.cache import cache

from rest_framework_simplejwt.authentication import JWTAuthentication

from .forms import SignUpForm, UpdateUserForm, UserAvatarForm

# Create your views here.

@require_GET
def csrf(request):
    return JsonResponse({'csrfToken': get_token(request)})

@csrf_exempt
@require_POST
def create_user(request):
    
    '''Создание пользователя'''
    
    User = apps.get_model('users.User')
    form = SignUpForm(request.POST)
    
    if form.is_valid():

        user = User.objects.filter(username=form.cleaned_data['username']).first()

        if user != None:
            return JsonResponse({"error": "User with such username already exists"})

        user = User.objects.filter(email=form.cleaned_data['email']).first()

        if user != None:
            return JsonResponse({"error": "User with such email already exists"})
        
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

    auth = None
    authenticator = JWTAuthentication()
    
    try:
        auth = authenticator.authenticate(request)
    except Exception:
        print("Invalid token")

    if auth == None:
        return JsonResponse({"error": "You aren't authenticated"})
        
    uid = auth[0].id
    
    if form.is_valid():
        
        user = auth[0] # User.objects.filter(id=uid)[0] # form.cleaned_data['pk'])[0]
        
        if user == None:
            return JsonResponse({"errors": "User not found"})
        
        for k in form.cleaned_data.keys():
            print(k)
            if k != 'pk' and form.cleaned_data[k] != '':
                print(user.__dict__[k])
                user.__dict__[k] = form.cleaned_data[k]
                
        user.save()

        avatar = user.avatar.url.replace('http://hb.bizmrg.com/undefined/',  '/users/avatars/') if user.avatar else ''

        usr = {'id': user.id, 'username': user.username, 'first_name': user.first_name,
               'patronymic': user.patronymic, 'last_name': user.last_name,
               'phone': user.phone, 'email': user.email, 'avatar': avatar}
        
        return JsonResponse({"user": usr})
            
    return JsonResponse({"errors": form.errors})
    
    
@require_GET
def get_user_info(request):

    '''Получение информации о пользователе'''
    
    User = apps.get_model('users.User')

    auth = None
    authenticator = JWTAuthentication()
    
    try:
        auth = authenticator.authenticate(request)
    except Exception:
        print("Invalid token")

    if auth == None:
        return JsonResponse({"error": "You aren't authenticated"})
        
    uid = auth[0].id
    
    user = auth[0] # User.objects.filter(id=uid).first()

    if user == None:
        return JsonResponse({"errors": "User not found " + str(uid)})

    avatar = user.avatar.url.replace('http://hb.bizmrg.com/undefined/',  '/users/avatars/') if user.avatar else ''

    usr = {'id': user.id, 'username': user.username, 'first_name': user.first_name,
               'patronymic': user.patronymic, 'last_name': user.last_name,
               'phone': user.phone, 'email': user.email, 'avatar': avatar, 'vet': user.vet}
    
    return JsonResponse({"user": usr})

@cache_page(60*5)
@require_GET
def vets_list(request):

    '''Выдает список ветеринаров'''

    User = apps.get_model('users.User')

    auth = None
    authenticator = JWTAuthentication()
    
    try:
        auth = authenticator.authenticate(request)
    except Exception:
        print("Invalid token")

    if auth == None:
        return JsonResponse({"error": "You aren't authenticated"})
        
    uid = auth[0].id
    
    vets = User.objects.filter(vet=True).values('id', 'first_name', 'patronymic', 
                                                   'last_name')

    return JsonResponse({"vets": list(vets)})

@csrf_exempt
@require_POST
def upload_user_avatar(request):
    
    User = apps.get_model('users.User')
    
    form = UserAvatarForm(request.POST, request.FILES)

    auth = None
    authenticator = JWTAuthentication()
    
    try:
        auth = authenticator.authenticate(request)
    except Exception:
        print("Invalid token")

    if auth == None:
        return JsonResponse({"error": "You aren't authenticated"})
        
    uid = auth[0].id
    
    if form.is_valid():
        
        user = auth[0] # User.objects.filter(id=uid).first() # form.cleaned_data['pk']).first()
        
        if user == None:
            return JsonResponse({"error": "User not found"})
        
        user.avatar = form.cleaned_data['avatar']
        user.save()
        
        user_avatar = {'id': user.id,
                      'avatar': user.avatar.url.replace('http://hb.bizmrg.com/undefined/',  '/users/avatars/')}
        
        return JsonResponse({'user_avatar': user_avatar})
    
    
    return JsonResponse({'errors': form.errors}, status=400)

@require_GET
def protected_file(request):

    auth = None
    authenticator = JWTAuthentication()
    
    try:
        auth = authenticator.authenticate(request)
    except Exception:
        print("Invalid token")

    if auth == None:
        return HttpResponse('<h1>File not found</h1>', status=404)
        
    uid = auth[0].id

    url = request.path.replace('/users/avatars', '/s3_files')
    print(url)
    response = HttpResponse(status=200)
    response['X-Accel-Redirect'] = url
    print(response.has_header('X-Accel-Redirect'))
    
    if 'Expires' in request.GET.keys():
        response['X-Accel-Expires'] = request.GET['Expires']
    response['Content-type'] = ''
    response['Access-Control-Allow-Origin'] = 'https://undefinedtrack.github.io'
    response['Access-Control-Allow-Credentials'] = 'true'
    response['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    response['Access-Control-Allow-Headers'] =  'Accept,Authorization,Cache-Control,Content-Type,DNT,If-Modified-Since,Keep-Alive,Origin,User-Agent,X-Requested-With'

    return response

        

# @login_required
@require_GET
def test(request):
    authenticator = JWTAuthentication()
    user, token = authenticator.authenticate(request)
    return JsonResponse({"user": user.id})