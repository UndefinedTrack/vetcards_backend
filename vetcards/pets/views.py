from django.shortcuts import render
from django.apps import apps

from django.http import JsonResponse, HttpResponse

from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST

from rest_framework_simplejwt.authentication import JWTAuthentication

from django.views.decorators.cache import cache_page
from django.core.cache import cache

from .forms import PetForm, PetUpdateForm, PetAvatarForm
from .documents import PetDocument

from elasticsearch_dsl.query import Q
# Create your views here.

@csrf_exempt
@require_POST
def create_pet(request):

    '''Создание питомца'''

    Pet = apps.get_model('pets.Pet')

    auth = None
    authenticator = JWTAuthentication()
    
    try:
        auth = authenticator.authenticate(request)
    except Exception:
        print("Invalid token")

    if auth == None:
        return JsonResponse({"error": "You aren't authenticated"})
        
    uid = auth[0].id
    user = auth[0]
    
    form = PetForm(request.POST)
    
    if form.is_valid():
        pet = Pet.objects.create(user_id=uid, 
                                 name=form.cleaned_data['name'], 
                                 species=form.cleaned_data['species'],
                                 breed=form.cleaned_data['breed'],  
                                 color=form.cleaned_data['color'],
                                 birth_date=form.cleaned_data['birth_date'],
                                 gender=form.cleaned_data['gender'],
                                 chip=form.cleaned_data['chip'])
        
        pt = {'id': pet.id, 'user_id': pet.user.id, 'name': pet.name,
              'species': pet.species, 'breed': pet.breed, 'color': pet.color,
              'birth_date': pet.birth_date, 'gender': pet.gender, 'chip': pet.chip, 'sterilized': pet.sterilized,
              'vaccinated': pet.vaccinated, 'contraindications': pet.contraindications, 'notes': pet.notes, 'weight': pet.weight,}

        # uid = pet.user.id

        pets = cache.get(f'pets_list_{uid}')

        if pets:
            cache.delete(f'pets_list_{uid}')
        
        return JsonResponse({"pet": pt})
        
    return JsonResponse({"errors": form.errors})

@csrf_exempt
@require_POST
def update_pet_info(request):

    '''Обновление информации о питомце'''
    
    Pet = apps.get_model('pets.Pet')
    User = apps.get_model('users.User')
    
    form = PetUpdateForm(request.POST)

    auth = None
    authenticator = JWTAuthentication()
    
    try:
        auth = authenticator.authenticate(request)
    except Exception:
        print("Invalid token")

    if auth == None:
        return JsonResponse({"error": "You aren't authenticated"})
        
    uid = auth[0].id
    user = auth[0]
    
    if form.is_valid():
        
        pet = Pet.objects.filter(id=form.cleaned_data['pk']).first()
        # user = User.objects.filter(id=form.cleaned_data['user'].id).first()
        
        if pet == None:
            return JsonResponse({"errors": "Pet not found"})

        if pet.user.id != user.id and not user.vet:
            return JsonResponse({"error": "You aren't veterinar or owner of the pet"})
        
        for k in form.cleaned_data.keys():
            if k != 'user' and k != 'pk' and form.cleaned_data[k] != '':
                pet.__dict__[k] = form.cleaned_data[k]
                
        pet.save()

        avatar = pet.avatar.url.replace('http://hb.bizmrg.com/undefined/',  '/pets/avatars/') if pet.avatar else ''

        pt = {'id': pet.id, 'user_id': pet.user.id, 'name': pet.name,
              'species': pet.species, 'breed': pet.breed, 'color': pet.color, 
              'birth_date': pet.birth_date, 'gender': pet.gender, 'chip': pet.chip, 'sterilized': pet.sterilized,
              'vaccinated': pet.vaccinated, 'contraindications': pet.contraindications, 'notes': pet.notes, 'weight': pet.weight,'avatar': avatar}

        pets = cache.get(f'pets_list_{uid}')

        if pets:
            cache.delete(f'pets_list_{uid}')

        patients = cache.get('patients')
        if patients:
            cache.delete('patients')
        
        return JsonResponse({"pet": pt})
            
    return JsonResponse({"errors": form.errors})


@csrf_exempt
@require_POST
def delete_pet(request):

    '''Удаление питомца'''
    
    Pet = apps.get_model('pets.Pet')
    
    auth = None
    authenticator = JWTAuthentication()
    
    try:
        auth = authenticator.authenticate(request)
    except Exception:
        print("Invalid token")

    if auth == None:
        return JsonResponse({"error": "You aren't authenticated"})
        
    uid = auth[0].id
    user = auth[0]

    pid = int(request.POST['pid'])
    
    pet = Pet.objects.filter(id=int(pid)).first()
    
    if pet.user.id == uid:
        pet.delete()

        pets = cache.get(f'pets_list_{uid}')

        if pets:
            cache.delete(f'pets_list_{uid}')

        patients = cache.get('patients')
        if patients:
            cache.delete('patients')
        
        return JsonResponse({"status": "ok"})
    
    return JsonResponse({"status": "fail"})

@require_GET
def pets_list(request):

    auth = None
    authenticator = JWTAuthentication()
    
    try:
        auth = authenticator.authenticate(request)
    except Exception:
        print("Invalid token")

    if auth == None:
        return JsonResponse({"error": "You aren't authenticated"})
        
    uid = auth[0].id
    user = auth[0]

    pts = cache.get(f'pets_list_{uid}')

    if pts:
        return JsonResponse({'pets': pts})

    '''Выдает список питомцев'''

    Pet = apps.get_model('pets.Pet')
    
    pets = Pet.objects.filter(user_id=uid) # request.GET['uid']))

    pts = []
    for pet in pets:

        avatar = pet.avatar.url.replace('http://hb.bizmrg.com/undefined/',  '/pets/avatars/') if pet.avatar else ''

        pt = {'id': pet.id, 'user_id': pet.user.id, 'name': pet.name,
              'species': pet.species, 'breed': pet.breed, 'color': pet.color, 
              'birth_date': pet.birth_date, 'gender': pet.gender, 'chip': pet.chip, 
              'sterilized': pet.sterilized, 'vaccinated': pet.vaccinated, 'contraindications': pet.contraindications, 
              'notes': pet.notes, 'weight': pet.weight, 'avatar': avatar}

        pts.append(pt)

    cache.set(f'pets_list_{uid}', pts)
    
    return JsonResponse({'pets': list(pts)})

@require_GET
def patients_list(request):

    '''Выдает список пациентов'''

    Pet = apps.get_model('pets.Pet')
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
    user = auth[0]

    # user = User.objects.filter(id=uid).first()

    if not user.vet:
        return JsonResponse({"error": "You aren't veterinar"})

    patients = cache.get('patients')

    if patients:
        return JsonResponse({'patients': patients})

    pets = Pet.objects.all()

    patients = []

    for pet in pets:
        patr = pet.user.patronymic[0] if pet.user.patronymic != '' else ''
        name = pet.user.first_name[0] if pet.user.first_name != '' else ''

        owner = f'{pet.user.last_name} {name}.{patr}.'

        if patr == '':
            owner = f'{pet.user.last_name} {name}.'

        if name == '':
            owner = f'{pet.user.last_name}'

        avatar = pet.avatar.url.replace('http://hb.bizmrg.com/undefined/',  '/pets/avatars/') if pet.avatar else ''
        
        pat = {'patient': f'{pet.name}, {pet.species}', 'color': pet.color, 'birth_date': pet.birth_date, 
               'gender': pet.gender, 'chip': pet.chip, 'owner': owner, 'card': pet.id, 'sterilized': pet.sterilized,
               'vaccinated': pet.vaccinated, 'contraindications': pet.contraindications, 'notes': pet.notes, 'weight': pet.weight, 'avatar': avatar}
        patients.append(pat)

    cache.set('patients', patients)

    return JsonResponse({'patients': list(patients)})

@require_GET
def pet_info(request):

    '''Выдает информацию о заданном питомце для указанного пользователя'''

    Pet = apps.get_model('pets.Pet')
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
    user = auth[0]
    pid = int(request.GET['pid'])
    
    pet = Pet.objects.filter(id=pid).first()
    # user = User.objects.filter(id=uid).first()
    
    if pet.user.id != uid and not user.vet:
        return JsonResponse({"error": "You aren't veterinar or owner of the pet"})

    avatar = pet.avatar.url.replace('http://hb.bizmrg.com/undefined/',  '/pets/avatars/') if pet.avatar else ''
    
    pt = {'id': pet.id, 'name': pet.name, 'species': pet.species, 'breed': pet.breed, 'color': pet.color,
          'birth_date': pet.birth_date, 'gender': pet.gender, 'chip': pet.chip, 'sterilized': pet.sterilized,
          'vaccinated': pet.vaccinated, 'contraindications': pet.contraindications, 'notes': pet.notes, 'weight': pet.weight, 'avatar': avatar}
    
    return JsonResponse({'pet': pt})


@csrf_exempt
@require_POST
def upload_pet_avatar(request):
    
    Pet = apps.get_model('pets.Pet')
    User = apps.get_model('users.User')
    
    form = PetAvatarForm(request.POST, request.FILES)

    auth = None
    authenticator = JWTAuthentication()
    
    try:
        auth = authenticator.authenticate(request)
    except Exception:
        print("Invalid token")

    if auth == None:
        return JsonResponse({"error": "You aren't authenticated"})
        
    uid = auth[0].id
    user = auth[0]
    
    if form.is_valid():
        
        pet = Pet.objects.filter(id=form.cleaned_data['pk']).first()
        
        if pet == None:
            return JsonResponse({"error": "Pet not found"})
        
        if pet.user.id != form.cleaned_data['user']:
            return JsonResponse({"error": "You aren't owner of the pet"})
        
        pet.avatar = form.cleaned_data['avatar']
        pet.save()
        
        pet_avatar = {'id': pet.id, 
                      'user': pet.user.id,
                      'avatar': pet.avatar.url.replace('http://hb.bizmrg.com/undefined/',  '/pets/avatars/')}

        # uid = pet.user.id

        pets = cache.get(f'pets_list_{uid}')

        if pets:
            cache.delete(f'pets_list_{uid}')

        patients = cache.get('patients')
        if patients:
            cache.delete('patients')
        
        return JsonResponse({'pet_avatar': pet_avatar})
    
    
    return JsonResponse({'errors': form.errors}, status=400)


@csrf_exempt
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
    user = auth[0]

    url = request.path.replace('/pets/avatars', '/s3_files')
    print(url)
    response = HttpResponse(status=200)
    response['X-Accel-Redirect'] = url
    print(response.has_header('X-Accel-Redirect'))
    
    if 'Expires' in request.GET.keys():
        response['X-Accel-Expires'] = request.GET['Expires']
    
    response['Content-type'] = ''
    response['Access-Control-Allow-Origin'] = 'http://localhost:3000' #https://undefinedtrack.github.io'
    response['Access-Control-Allow-Credentials'] = 'true'
    response['Access-Control-Allow-Methods'] = 'GET' # , POST, PUT, DELETE, OPTIONS'
    response['Access-Control-Allow-Headers'] =  'Accept,Authorization,Cache-Control,Content-Type,DNT,If-Modified-Since,Keep-Alive,Origin,User-Agent,X-Requested-With'
    
    return response
        

@require_GET
def search(request):
    
    Pet = apps.get_model('pets.Pet')
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
    user = auth[0]

    # user = User.objects.filter(id=uid).first()
    name = request.GET['name']

    if not user.vet:
        return JsonResponse({"error": "You aren't veterinar"})

    if name == '':
        patients = cache.get('patients')

        if patients:
            return JsonResponse({'patients': patients})
    else:
        patients = cache.get(f'patients_{name}')
        if patients:
            return JsonResponse({'patients': patients})
    
    pets = PetDocument.search().query(Q('wildcard', name='*' + str(request.GET['name']) + '*') | 
                                      Q('wildcard', user__first_name='*' + str(request.GET['name']) + '*') |
                                      Q('wildcard', user__last_name='*' + str(request.GET['name']) + '*') |
                                      Q('wildcard', user__patroymic='*' + str(request.GET['name']) + '*'))
    pets = pets.to_queryset()
    
    patients = []
    
    for pet in pets:

        patr = pet.user.patronymic[0] if pet.user.patronymic != '' else ''
        name = pet.user.first_name[0] if pet.user.first_name != '' else ''

        owner = f'{pet.user.last_name} {name}.{patr}.'

        if patr == '':
            owner = f'{pet.user.last_name} {name}.'

        if name == '':
            owner = f'{pet.user.last_name}'

        avatar = pet.avatar.url.replace('http://hb.bizmrg.com/undefined/',  '/pets/avatars/') if pet.avatar else ''
        
        pat = {'patient': f"{pet.name}, {pet.species}", 'color': pet.color, 'birth_date': pet.birth_date, 
        'gender': pet.gender, 'chip': pet.chip, 'owner': owner, 'card': pet.id, 'sterilized': pet.sterilized,
        'vaccinated': pet.vaccinated, 'contraindications': pet.contraindications, 'notes': pet.notes, 'weight': pet.weight, 'avatar': avatar}
        patients.append(pat)

    
    unique_patients = list({p['card']:p for p in patients}.values())

    if name == '':
        cache.set('patients', unique_patients)
    else:
        cache.set(f'patients_{name}', unique_patients)
    
    return JsonResponse({'patients': unique_patients})