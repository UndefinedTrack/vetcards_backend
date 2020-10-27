from django.shortcuts import render
from django.apps import apps

from django.http import JsonResponse

from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST

from .forms import ProcedureForm, OwnerProcedureForm
from .documents import OwnerProcedureDocument, VetProcedureDocument

# Create your views here.

@csrf_exempt
@require_POST
def create_vet_procedure(request):

    '''Добавить процедуру, проведённую ветеринаром'''

    User = apps.get_model('users.User')
    Procedure = apps.get_model('cards.Procedure')
    
    form = ProcedureForm(request.POST)
    
    if form.is_valid():

        user = User.objects.filter(id=int(form.cleaned_data['user'].id)).first()
        
        if not user.vet:
            return JsonResponse({"errors": "you aren't a veterinar"})

        procedure = Procedure.objects.create(pet_id=form.cleaned_data['pet'].id,
                                             user_id=form.cleaned_data['user'].id,
                                             purpose=form.cleaned_data['purpose'],
                                             symptoms=form.cleaned_data['symptoms'],
                                             diagnosis=form.cleaned_data['diagnosis'],
                                             recomms=form.cleaned_data['recomms'],
                                             recipe=form.cleaned_data['recipe'])
        
        proc = {'id': procedure.id, 'pet_id': procedure.pet_id, 'user_id': procedure.user_id,
                'purpose': procedure.purpose, 'symptoms': procedure.symptoms,
                'diagnosis': procedure.recipe, 'recomms': procedure.recomms,
                'recipe': procedure.recipe, 'proc_date': procedure.proc_date}
        
        return JsonResponse({"procedure": proc})
        
    return JsonResponse({"errors": form.errors})


@csrf_exempt
@require_POST
def create_owner_procedure(request):

    '''Добавить процедуру, проведённую владельцем'''

    Pet = apps.get_model('pets.Pet')
    User = apps.get_model('users.User')
    OwnerProcedure = apps.get_model('cards.OwnerProcedure')
    
    form = OwnerProcedureForm(request.POST)
    
    if form.is_valid():

        pet = Pet.objects.filter(id=int(form.cleaned_data['pet'].id)).first()
        user = User.objects.filter(id=int(form.cleaned_data['user'].id)).first()
        
        if pet.user.id != form.cleaned_data['user'].id and not user.vet:
            return JsonResponse({"errors": "you aren't a veterinar or owner of this pet"})

        procedure = OwnerProcedure.objects.create(pet_id=form.cleaned_data['pet'].id,
                                                  user_id=form.cleaned_data['user'].id,
                                                  name=form.cleaned_data['name'],
                                                  description=form.cleaned_data['description'])
        
        proc = {'id': procedure.id, 'pet_id': procedure.pet_id, 'user_id': procedure.user_id,
                'name': procedure.name, 'description': procedure.description, 'proc_date': procedure.proc_date}
        
        return JsonResponse({"procedure": proc})
        
    return JsonResponse({"errors": form.errors})


@require_GET
def vet_procs_list(request):

    '''Список процедур, проведённых ветеринаром'''

    Pet = apps.get_model('pets.Pet')
    User = apps.get_model('users.User')
    Procedure = apps.get_model('cards.Procedure')

    pid = int(request.GET['pid'])
    uid = int(request.GET['uid'])
    
    pet = Pet.objects.filter(id=int(pid)).first()
    user = User.objects.filter(id=int(uid)).first()
    
    if pet.user.id != uid and not user.vet:
        return JsonResponse({"errors": "you aren't a veterinar or owner of this pet"})
    
    procedures = Procedure.objects.filter(pet_id=int(pid)).values('id', 'pet_id', 'user_id', 'purpose', 'symptoms',
                                                                  'diagnosis', 'recomms', 'recipe', 'proc_date')
    
    return JsonResponse({'procedures': list(procedures)})

@require_GET
def owner_procs_list(request):

    '''Список процедур, проведенных владельцем'''

    Pet = apps.get_model('pets.Pet')
    OwnerProcedure = apps.get_model('cards.OwnerProcedure')

    pid = int(request.GET['pid'])
    uid = int(request.GET['uid'])
    
    pet = Pet.objects.filter(id=int(pid)).first()
    
    if pet.user.id != uid:
        return JsonResponse({"errors": "you aren't owner of this pet"})
    
    procedures = OwnerProcedure.objects.filter(pet_id=int(pid)).values('id', 'pet_id', 'user_id', 'name', 'description', 'proc_date')
    
    return JsonResponse({'procedures': list(procedures)})


@require_GET
def search_owner_procs(request):
    Pet = apps.get_model('pets.Pet')
    
    pid = int(request.GET['pid'])
    uid = int(request.GET['uid'])
    
    pet = Pet.objects.filter(id=int(pid)).first()
    
    if pet.user.id != uid:
        return JsonResponse({"errors": "you aren't owner of this pet"})
    
    owner_procs = OwnerProcedureDocument.search().filter("term", pet_id=pid).query('wildcard', name='*' + str(request.GET['name']) + '*')
    procedures = owner_procs.to_queryset().values('id', 'pet_id', 'user_id', 'name', 'description', 'proc_date')
    
    return JsonResponse({'procedures': list(procedures)})

@require_GET
def search_vet_procs(request):
    
    Pet = apps.get_model('pets.Pet')
    User = apps.get_model('users.User')

    pid = int(request.GET['pid'])
    uid = int(request.GET['uid'])
    
    pet = Pet.objects.filter(id=int(pid)).first()
    user = User.objects.filter(id=int(uid)).first()
    
    if pet.user.id != uid and not user.vet:
        return JsonResponse({"errors": "you aren't a veterinar or owner of this pet"})
    
    vet_procs = VetProcedureDocument.search().filter("term", pet_id=pid).query('wildcard', purpose='*' + str(request.GET['name']) + '*')
    procedures = vet_procs.to_queryset().values('id', 'pet_id', 'user_id', 'purpose', 'symptoms', 
                                                  'diagnosis', 'recomms', 'recipe', 'proc_date')
    
    return JsonResponse({'procedures': list(procedures)})