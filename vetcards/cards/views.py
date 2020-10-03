from django.shortcuts import render
from django.apps import apps

from django.http import JsonResponse

from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST

from .forms import ProcedureForm, OwnerProcedureForm

# Create your views here.

@csrf_exempt
@require_POST
def create_vet_procedure(request):
    Procedure = apps.get_model('cards.Procedure')
    
    form = ProcedureForm(request.POST)
    
    if form.is_valid():
        procedure = Procedure.objects.create(pet_id=form.cleaned_data['pet'],
                                             user_id=form.cleaned_data['user'],
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
    OwnerProcedure = apps.get_model('cards.OwnerProcedure')
    
    form = OwnerProcedureForm(request.POST)
    
    if form.is_valid():
        procedure = OwnerProcedure.objects.create(pet_id=form.cleaned_data['pet'],
                                                  user_id=form.cleaned_data['user'],
                                                  name=form.cleaned_data['name'],
                                                  description=form.cleaned_data['description'])
        
        proc = {'id': procedure.id, 'pet_id': procedure.pet_id, 'user_id': procedure.user_id,
                'name': procedure.name, 'description': procedure.description, 'proc_date': procedure.proc_date}
        
        return JsonResponse({"procedure": proc})
        
    return JsonResponse({"errors": form.errors})


@require_GET
def vet_procs_list(request, uid, pid):
    Pet = apps.get_model('pets.Pet')
    Procedure = apps.get_model('cards.Procedure')
    
    pet = Pet.objects.filter(id=int(pid))
    
    if pet.user_id != uid:
        return JsonResponse({"errors": "you aren't owner of this pet"})
    
    procedures = Procedure.objects.filter(pet_id=int(pid)).values('pet_id', 'user_id', 'purpose', 'symptoms',
                                                                  'diagnosis', 'recomms', 'recipe', 'proc_date')
    
    return JsonResponse({'procedures': procedures})


@require_GET
def owner_procs_list(request, uid, pid):
    Pet = apps.get_model('pets.Pet')
    OwnerProcedure = apps.get_model('cards.OwnerProcedure')
    
    pet = Pet.objects.filter(id=int(pid))
    
    if pet.user_id != uid:
        return JsonResponse({"errors": "you aren't owner of this pet"})
    
    procedures = OwnerProcedure.objects.filter(pet_id=int(pid)).values('id', 'pet_id', 'user_id', 'name', 'description', 'proc_date')
    
    return JsonResponse({'procedures': procedures})