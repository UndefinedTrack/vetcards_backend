from django.shortcuts import render
from django.apps import apps

from django.http import JsonResponse, HttpResponse

from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST

from rest_framework_simplejwt.authentication import JWTAuthentication

from django.views.decorators.cache import cache_page
from django.core.cache import cache

from .forms import ProcedureForm, OwnerProcedureForm, UpdateProcedureForm, UpdateOwnerProcedureForm, VetAttForm, OwnerAttForm
from .documents import OwnerProcedureDocument, VetProcedureDocument

from elasticsearch_dsl.query import Q

import datetime
# Create your views here.

@csrf_exempt
@require_POST
def create_vet_procedure(request):

    '''Добавить процедуру, проведённую ветеринаром'''

    User = apps.get_model('users.User')
    Procedure = apps.get_model('cards.Procedure')

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

    
    form = ProcedureForm(request.POST)
    
    if form.is_valid():

        # user = User.objects.filter(id=uid).first() # int(form.cleaned_data['user'].id)).first()
        
        if not user.vet:
            return JsonResponse({"errors": "you aren't a veterinar"})

        proc = Procedure.objects.create(pet_id=form.cleaned_data['pet'].id,
                                        user_id=uid,
                                        purpose=form.cleaned_data['purpose'],
                                        name=form.cleaned_data['name'],
                                        symptoms=form.cleaned_data['symptoms'],
                                        diagnosis=form.cleaned_data['diagnosis'],
                                        recomms=form.cleaned_data['recomms'],
                                        recipe=form.cleaned_data['recipe'],
                                        proc_date=form.cleaned_data['proc_date'])
        
        procedure = {'id': proc.id, 'pet_id': proc.pet_id, 'user_id': proc.user_id,
                'purpose': proc.purpose, 'name': proc.name,
                'symptoms': '' if proc.symptoms is None else proc.symptoms,
                'diagnosis': '' if proc.diagnosis is None else proc.diagnosis, 
                'recomms': '' if proc.recomms is None else proc.recomms,
                'recipe': '' if proc.recipe is None else proc.recipe, 
                'proc_date': proc.proc_date,}

        pid = int(form.cleaned_data['pet'].id)

        procs = cache.get(f'vet_procs_{pid}')
        if procs:
            cache.delete(f'vet_procs_{pid}')
        
        return JsonResponse({"procedure": procedure})
        
    return JsonResponse({"errors": form.errors})


@csrf_exempt
@require_POST
def create_owner_procedure(request):

    '''Добавить процедуру, проведённую владельцем'''

    Pet = apps.get_model('pets.Pet')
    User = apps.get_model('users.User')
    OwnerProcedure = apps.get_model('cards.OwnerProcedure')

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

    
    form = OwnerProcedureForm(request.POST)
    
    if form.is_valid():

        pet = Pet.objects.filter(id=int(form.cleaned_data['pet'].id)).first()
        # user = User.objects.filter(id=uid).first() # int(form.cleaned_data['user'].id)).first()
        
        if pet.user.id != uid and not user.vet:
            return JsonResponse({"errors": "you aren't a veterinar or owner of this pet"})

        procedure = OwnerProcedure.objects.create(pet_id=form.cleaned_data['pet'].id,
                                                  user_id=uid,
                                                  name=form.cleaned_data['name'],
                                                  description=form.cleaned_data['description'],
                                                  proc_date=form.cleaned_data['proc_date'])
        
        proc = {'id': procedure.id, 'pet_id': procedure.pet_id, 'user_id': procedure.user_id,
                'name': procedure.name, 'description': '' if procedure.description is None else procedure.description, 
                'proc_date': procedure.proc_date}

        pid = int(form.cleaned_data['pet'].id)
        procs = cache.get(f'owner_procs_{pid}')
        if procs:
            cache.delete(f'owner_procs_{pid}')
        
        return JsonResponse({"procedure": proc})
        
    return JsonResponse({"errors": form.errors})


@require_GET
def vet_procs_list(request):

    '''Список процедур, проведённых ветеринаром'''

    Pet = apps.get_model('pets.Pet')
    User = apps.get_model('users.User')
    Procedure = apps.get_model('cards.Procedure')
    VetAttachment = apps.get_model('cards.VetAttachment')

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
    
    pet = Pet.objects.filter(id=int(pid)).first()
    # user = User.objects.filter(id=int(uid)).first()
    
    if pet.user.id != uid and not user.vet:
        return JsonResponse({"errors": "you aren't a veterinar or owner of this pet"})

    procedures = cache.get(f'vet_procs_{pid}')

    if procedures:
        return JsonResponse({'procedures': procedures})

    procedures = []
    
    procs = Procedure.objects.filter(pet_id=int(pid)) #.values('id', 'pet_id', 'user_id', 'purpose', 'symptoms',
                                                      #            'diagnosis', 'recomms', 'recipe', 'proc_date')

    for proc in procs:

        atts = VetAttachment.objects.filter(proc_id=proc.id)

        proc_atts = []

        for att in atts:
            proc_atts.append(att.url.url.replace('http://hb.bizmrg.com/undefined/',  '/cards/attachments/'))

        procedure = {'id': proc.id, 'pet_id': proc.pet_id, 'user_id': proc.user_id,
                    'purpose': proc.purpose, 'name': proc.name,
                    'symptoms': '' if proc.symptoms is None else proc.symptoms,
                    'diagnosis': '' if proc.diagnosis is None else proc.diagnosis, 
                    'recomms': '' if proc.recomms is None else proc.recomms,
                    'recipe': '' if proc.recipe is None else proc.recipe, 
                    'proc_date': proc.proc_date, 'attachments': proc_atts}

        procedures.append(procedure)


    cache.set(f'vet_procs_{pid}', procedures)
    
    return JsonResponse({'procedures': procedures})

@require_GET
def owner_procs_list(request):

    '''Список процедур, проведенных владельцем'''

    Pet = apps.get_model('pets.Pet')
    OwnerProcedure = apps.get_model('cards.OwnerProcedure')
    OwnerAttachment = apps.get_model('cards.OwnerAttachment')

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
    
    pet = Pet.objects.filter(id=int(pid)).first()
    
    if pet.user.id != uid:
        return JsonResponse({"errors": "you aren't owner of this pet"})

    procedures = cache.get(f'owner_procs_{pid}')

    if procedures:
        return JsonResponse({'procedures': procedures})

    procedures = []
    
    procs = OwnerProcedure.objects.filter(pet_id=int(pid)) # .values('id', 'pet_id', 'user_id', 'name', 'description', 'proc_date')

    for proc in procs:
    
        atts = OwnerAttachment.objects.filter(proc_id=proc.id)

        proc_atts = []

        for att in atts:
            proc_atts.append(att.url.url.replace('http://hb.bizmrg.com/undefined/',  '/cards/attachments/'))

        procedure = {'id': procedure.id, 'pet_id': procedure.pet_id, 'user_id': procedure.user_id,
                'name': procedure.name, 'description': '' if procedure.description is None else procedure.description, 
                'proc_date': procedure.proc_date, 'attachments': proc_atts}

        procedures.append(procedure)
    
    cache.set(f'owner_procs_{pid}', procedures)
    
    return JsonResponse({'procedures': procedures})


@require_GET
def search_owner_procs(request):
    Pet = apps.get_model('pets.Pet')
    OwnerAttachment = apps.get_model('cards.OwnerAttachment')

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
    
    pet = Pet.objects.filter(id=int(pid)).first()
    
    if pet.user.id != uid:
        return JsonResponse({"errors": "you aren't owner of this pet"})

    name = str(request.GET['name'])
    months = ["январь","февраль","март","апрель","май","июнь","июль","август","сентябрь","октябрь","ноябрь","декабрь"]
    days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    owner_procs = []

    idx = -1
    counter = -1

    if len(name) > 1:
        for m in months:
            counter += 1
            if m.__contains__(name) or len(name) > 2 and m.__contains__(name[:-1]):
                idx = counter
                break

    if idx > -1:
        now = datetime.datetime.now()

        day = days[idx]

        month = "0" + str(idx+1) if (idx + 1) < 10 else str(idx + 1)

        if idx == 1:
            if now.year % 4 == 0 or now.year % 100 != 0 or now.year % 100 == 0 and now.year % 400 == 0:
                day = 29
        first = str(now.year) + "-" + month + "-01T00:00:00"
        last = str(now.year) + "-" + month + "-" + str(day) + "T23:59:59"
        owner_procs = OwnerProcedureDocument.search().filter("term", pet_id=pid).query(Q('range', proc_date={'gte': first, 'lte': last}) | 
                                                                                       Q('wildcard', name='*' + name + '*') |
                                                                                       Q('match', name=name))
    else:
        owner_procs = OwnerProcedureDocument.search().filter("term", pet_id=pid).query(Q('wildcard', name='*' + name + '*') | Q('match', name=name))
    
    procs = owner_procs.to_queryset() #.values('id', 'pet_id', 'user_id', 'name', 'description', 'proc_date')

    procedures = []

    for proc in procs:
        
        atts = OwnerAttachment.objects.filter(proc_id=proc.id)

        proc_atts = []

        for att in atts:
            proc_atts.append(att.url.url.replace('http://hb.bizmrg.com/undefined/',  '/cards/attachments/'))

        procedure = {'id': procedure.id, 'pet_id': procedure.pet_id, 'user_id': procedure.user_id,
                'name': procedure.name, 'description': '' if procedure.description is None else procedure.description, 
                'proc_date': procedure.proc_date, 'attachments': proc_atts}

        procedures.append(procedure)
    
    return JsonResponse({'procedures': list(procedures)})

@require_GET
def search_vet_procs(request):
    
    Pet = apps.get_model('pets.Pet')
    User = apps.get_model('users.User')
    VetAttachment = apps.get_model('cards.VetAttachment')

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
    
    pet = Pet.objects.filter(id=int(pid)).first()
    # user = User.objects.filter(id=int(uid)).first()
    
    if pet.user.id != uid and not user.vet:
        return JsonResponse({"errors": "you aren't a veterinar or owner of this pet"})

    vet_procs = []
    name = str(request.GET['name'])
    months = ["январь","февраль","март","апрель","май","июнь","июль","август","сентябрь","октябрь","ноябрь","декабрь"]
    days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    idx = -1
    counter = -1

    if len(name) > 1:
        for m in months:
            counter += 1
            if m.__contains__(name) or len(name) > 2 and m.__contains__(name[:-1]):
                idx = counter
                break
    
    if idx > -1:
        now = datetime.datetime.now()
        day = days[idx]

        month = "0" + str(idx+1) if (idx + 1) < 10 else str(idx + 1)

        if idx == 1:
            if now.year % 4 == 0 or now.year % 100 != 0 or now.year % 100 == 0 and now.year % 400 == 0:
                day = 29
        first = str(now.year) + "-" + month + "-01T00:00:00"
        last = str(now.year) + "-" + month + "-" + str(day) + "T23:59:59"
        vet_procs = VetProcedureDocument.search().filter("term", pet_id=pid).query(Q('range', proc_date={'gte': first, 'lte': last}) | 
                                                                                   Q('wildcard', name='*' + name + '*') |
                                                                                   Q('match', name=name))
    else:
        vet_procs = VetProcedureDocument.search().filter("term", pet_id=pid).query(Q('wildcard', purpose='*' + name + '*') | Q('match', name=name))

    procedures = []
    procs = vet_procs.to_queryset()#.values('id', 'pet_id', 'user_id', 'purpose', 'name', 'symptoms', 
    #                                              'diagnosis', 'recomms', 'recipe', 'proc_date') 

    for proc in procs:
    
        atts = VetAttachment.objects.filter(proc_id=proc.id)

        proc_atts = []

        for att in atts:
            proc_atts.append(att.url.url.replace('http://hb.bizmrg.com/undefined/',  '/cards/attachments/'))

        procedure = {'id': proc.id, 'pet_id': proc.pet_id, 'user_id': proc.user_id,
                'purpose': proc.purpose, 'name': proc.name,
                'symptoms': '' if proc.symptoms is None else proc.symptoms,
                'diagnosis': '' if proc.diagnosis is None else proc.diagnosis, 
                'recomms': '' if proc.recomms is None else proc.recomms,
                'recipe': '' if proc.recipe is None else proc.recipe, 
                'proc_date': proc.proc_date, 'attachments': proc_atts}

        procedures.append(procedure)
    
    
    return JsonResponse({'procedures': list(procedures)})


@csrf_exempt
@require_POST
def delete_owner_procedure(request):

    '''Удаление домашней процедуры'''
    
    OwnerProcedure = apps.get_model('cards.OwnerProcedure')
    
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
    
    proc = OwnerProcedure.objects.filter(id=int(pid)).first()
    
    if proc.user.id == uid:
        proc.delete()

        procs = cache.get(f'owner_procs_{pid}')
        if procs:
            cache.delete(f'owner_procs_{pid}')
        
        return JsonResponse({"status": "ok"})
    
    return JsonResponse({"status": "fail"})

@csrf_exempt
@require_POST
def delete_vet_procedure(request):

    '''Удаление процедуры, проведённой ветеринаром'''
    
    Procedure = apps.get_model('cards.Procedure')

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
    
    proc = Procedure.objects.filter(id=int(pid)).first()
    
    if proc.user.id == uid:
        proc.delete()

        procs = cache.get(f'vet_procs_{pid}')
        if procs:
            cache.delete(f'vet_procs_{pid}')
        
        return JsonResponse({"status": "ok"})
    
    return JsonResponse({"status": "fail"})


@csrf_exempt
@require_POST
def update_owner_procedure(request):

    '''Обновление информации о домашней процедуре'''
    
    OwnerProcedure = apps.get_model('cards.OwnerProcedure')
    User = apps.get_model('users.User')
    OwnerAttachment = apps.get_model('cards.OwnerAttachment')

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
    
    form = UpdateOwnerProcedureForm(request.POST)
    
    if form.is_valid():
        
        proc = OwnerProcedure.objects.filter(id=form.cleaned_data['pk']).first()
        # user = User.objects.filter(id=form.cleaned_data['user'].id).first()
        
        if proc == None:
            return JsonResponse({"errors": "Procedure not found"})

        if proc.user.id != user.id: #form.cleaned_data['user'].id:
            return JsonResponse({"error": "You aren't owner of this procedure"})
        
        for k in form.cleaned_data.keys():
            if k != 'user' and k != 'pk':
                proc.__dict__[k] = form.cleaned_data[k]
                
        proc.save()

        atts = OwnerAttachment.objects.filter(proc_id=proc.id)

        proc_atts = []

        for att in atts:
            proc_atts.append(att.url.url.replace('http://hb.bizmrg.com/undefined/',  '/cards/attachments/'))

        procedure = {'id': proc.id, 'pet_id': proc.pet_id, 'user_id': proc.user_id,
                'name': proc.name, 'description': '' if proc.description is None else proc.description, 
                'proc_date': proc.proc_date, 'attachments': proc_atts}

        procs = cache.get(f'owner_procs_{proc.pet.id}')
        if procs:
            cache.delete(f'owner_procs_{proc.pet.id}')

        
        return JsonResponse({"procedure": procedure})
            
    return JsonResponse({"errors": form.errors})

@csrf_exempt
@require_POST
def update_vet_procedure(request):

    '''Обновление информации о процедуре, проведённой ветеринаром'''
    
    Procedure = apps.get_model('cards.Procedure')
    User = apps.get_model('users.User')
    VetAttachment = apps.get_model('cards.VetAttachment')

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
    
    form = UpdateProcedureForm(request.POST)
    
    if form.is_valid():
        
        proc = Procedure.objects.filter(id=form.cleaned_data['pk']).first()
        # user = User.objects.filter(id=form.cleaned_data['user'].id).first()
        
        if proc == None:
            return JsonResponse({"errors": "Procedure not found"})

        if proc.user.id != user.id: # form.cleaned_data['user'].id:
            return JsonResponse({"error": "You aren't owner of this procedure"})
        
        for k in form.cleaned_data.keys():
            if k != 'user' and k != 'pk':
                proc.__dict__[k] = form.cleaned_data[k]
                
        proc.save()

        atts = VetAttachment.objects.filter(proc_id=proc.id)

        proc_atts = []

        for att in atts:
            proc_atts.append(att.url.url.replace('http://hb.bizmrg.com/undefined/',  '/cards/attachments/'))

        procedure = {'id': proc.id, 'pet_id': proc.pet_id, 'user_id': proc.user_id,
                'purpose': proc.purpose, 'name': proc.name,
                'symptoms': '' if proc.symptoms is None else proc.symptoms,
                'diagnosis': '' if proc.diagnosis is None else proc.diagnosis, 
                'recomms': '' if proc.recomms is None else proc.recomms,
                'recipe': '' if proc.recipe is None else proc.recipe, 
                'proc_date': proc.proc_date, 'attachments': proc_atts}

        procs = cache.get(f'vet_procs_{proc.pet.id}')
        if procs:
            cache.delete(f'vet_procs_{proc.pet.id}')

        
        return JsonResponse({"procedure": procedure})
            
    return JsonResponse({"errors": form.errors})

@csrf_exempt
@require_POST
def upload_owner_att(request):
    
    Pet = apps.get_model('pets.Pet')
    User = apps.get_model('users.User')
    OwnerProcedure = apps.get_model('cards.OwnerProcedure')
    OwnerAttachment = apps.get_model('cards.OwnerAttachment')
    
    form = OwnerAttForm(request.POST, request.FILES)

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
        
        proc = OwnerProcedure.objects.filter(id=form.cleaned_data['proc'].id).first()
        
        if proc == None:
            return JsonResponse({"error": "Procedure not found"})
        
        if proc.user.id != form.cleaned_data['user']:
            return JsonResponse({"error": "You aren't owner of the procedure"})
        
        attachment = OwnerAttachment.objects.create(user_id=form.cleaned_data['user'].id,
                                                    proc_id=form.cleaned_data['proc'].id,
                                                    url=form.cleaned_data['url'])
        
        att = {'id': attachment.id, 
                      'user': attachment.user.id,
                      'proc': attachment.proc.id,
                      'url': attachment.url.url.replace('http://hb.bizmrg.com/undefined/',  '/cards/attachments/')}

        procs = cache.get(f'owner_procs_{proc.pet.id}')
        if procs:
            cache.delete(f'owner_procs_{proc.pet.id}')
        
        return JsonResponse({'attachment': att})
    
    
    return JsonResponse({'errors': form.errors}, status=400)

@csrf_exempt
@require_POST
def upload_vet_att(request):
    
    Pet = apps.get_model('pets.Pet')
    User = apps.get_model('users.User')
    Procedure = apps.get_model('cards.Procedure')
    VetAttachment = apps.get_model('cards.VetAttachment')
    
    form = VetAttForm(request.POST, request.FILES)

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
        
        proc = Procedure.objects.filter(id=form.cleaned_data['proc'].id).first()
        
        if proc == None:
            return JsonResponse({"error": "Procedure not found"})
        
        if proc.user.id != form.cleaned_data['user'] and not proc.user.vet:
            return JsonResponse({"error": "You aren't owner of the procedure"})
        
        attachment = VetAttachment.objects.create(user_id=form.cleaned_data['user'].id,
                                                  proc_id=form.cleaned_data['proc'].id,
                                                  url=form.cleaned_data['url'])
        
        att = {'id': attachment.id, 
               'user': attachment.user.id,
               'proc': attachment.proc.id,
               'url': attachment.url.url.replace('http://hb.bizmrg.com/undefined/',  '/cards/attachments/')}

        procs = cache.get(f'owner_procs_{proc.pet.id}')
        if procs:
            cache.delete(f'owner_procs_{proc.pet.id}')
        
        return JsonResponse({'attachment': att})
    
    
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

    url = request.path.replace('/cards/attachments', '/s3_files')
    response = HttpResponse(status=200)
    response['X-Accel-Redirect'] = url
    
    if 'Expires' in request.GET.keys():
        response['X-Accel-Expires'] = request.GET['Expires']
    
    response['Content-type'] = ''
    response['Access-Control-Allow-Origin'] = 'http://localhost:3000' #https://undefinedtrack.github.io'
    response['Access-Control-Allow-Credentials'] = 'true'
    response['Access-Control-Allow-Methods'] = 'GET' # , POST, PUT, DELETE, OPTIONS'
    response['Access-Control-Allow-Headers'] =  'Accept,Authorization,Cache-Control,Content-Type,DNT,If-Modified-Since,Keep-Alive,Origin,User-Agent,X-Requested-With'
    
    return response