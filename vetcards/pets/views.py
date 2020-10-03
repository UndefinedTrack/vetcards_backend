from django.shortcuts import render
from django.apps import apps

from django.http import JsonResponse

from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST

from .forms import PetForm

# Create your views here.

@csrf_exempt
@require_POST
def create_pet(request):

    '''Создание питомца'''

    Pet = apps.get_model('pets.Pet')
    
    form = PetForm(request.POST)
    
    if form.is_valid():
        pet = Pet.objects.create(user_id=form.cleaned_data['user'].id, 
                                 name=form.cleaned_data['name'], 
                                 species=form.cleaned_data['species'], 
                                 color=form.cleaned_data['color'],
                                 birth_date=form.cleaned_data['birth_date'],
                                 gender=form.cleaned_data['gender'],
                                 chip=form.cleaned_data['chip'])
        
        pt = {'id': pet.id, 'user_id': pet.user.id, 'name': pet.name,
              'species': pet.species, 'color': pet.color, 'birth_date': pet.birth_date, 
              'gender': pet.gender, 'chip': pet.chip}
        
        return JsonResponse({"pet": pt})
        
    return JsonResponse({"errors": form.errors})

@csrf_exempt
@require_POST
def update_pet_info(request):

    '''Обновление информации о питомце'''
    
    Pet = apps.get_model('pets.Pet')
    
    form = PetForm(request.POST)
    
    if form.is_valid():
        
        pet = Pet.objects.filter(user_id=form.cleaned_data['user'], name=form.cleaned_data['name']).first()
        
        if pet == None:
            return JsonResponse({"errors": "Pet not found"})
        
        for k in form.cleaned_data.keys():
            if k != 'user' and form.cleaned_data[k] != '':
                pet.__dict__[k] = form.cleaned_data[k]
                
        pet.save()

        pt = {'id': pet.id, 'user_id': pet.user.id, 'name': pet.name,
              'species': pet.species, 'color': pet.color, 'birth_date': pet.birth_date, 
              'gender': pet.gender, 'chip': pet.chip}
        
        return JsonResponse({"pet": pt})
            
    return JsonResponse({"errors": form.errors})


@csrf_exempt
@require_POST
def delete_pet(request):

    '''Удаление питомца'''
    
    Pet = apps.get_model('pets.Pet')
    
    uid = int(request.POST['uid'])
    pid = int(request.POST['pid'])
    
    pet = Pet.objects.filter(id=int(pid)).first()
    
    if pet.user.id == uid:
        pet.delete()
        
        return JsonResponse({"status": "ok"})
    
    return JsonResponse({"status": "fail"})

@require_GET
def pets_list(request):

    '''Выдает список питомцев'''

    Pet = apps.get_model('pets.Pet')
    
    pets = Pet.objects.filter(user_id=int(request.GET['uid'])).values('id', 'user_id', 'name', 
                                                       'species', 'color', 'birth_date',
                                                       'gender', 'chip')
    
    return JsonResponse({'pets': list(pets)})

@require_GET
def pet_info(request):

    '''Выдает информацию о заданном питомце для указанного пользователя'''

    Pet = apps.get_model('pets.Pet')
    User = apps.get_model('users.User')

    uid = int(request.GET['uid'])
    pid = int(request.GET['pid'])
    
    pet = Pet.objects.filter(id=pid).first()
    user = User.objects.filter(id=uid).first()
    
    if pet.user.id != uid and not user.vet:
        return JsonResponse({"error": "You aren't veterinar or owner of the pet"})
    
    pt = {'id': pet.id, 'name': pet.name, 'species': pet.species, 'color': pet.color,
          'birth_date': pet.birth_date, 'gender': pet.gender, 'chip': pet.chip}
    
    return JsonResponse({'pet': pt})
