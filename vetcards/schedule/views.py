from django.shortcuts import render
from django.apps import apps

from django.http import JsonResponse

from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST

from .forms import SlotCreateForm, SlotAppointForm, SlotDisappointForm

# Create your views here.

@csrf_exempt
@require_POST
def create_slot(request):
    '''Создание слота'''

    Slot = apps.get_model('schedule.Slot')
    
    form = SlotCreateForm(request.POST)
    
    if form.is_valid():
        slot = Slot.objects.create(vet_id=form.cleaned_data['vet'].id, 
                                 slot_date=form.cleaned_data['slot_date'], 
                                 slot_time=form.cleaned_data['slot_time'])
        
        slt = { 'id': slot.id, 'user_id': slot.vet.id, 'slot_date': slot.slot_date, 
                'slot_time': slot.slot_time, 'purpose': slot.purpose, 'pet': -1, 'appointed': slot.appointed }
        
        return JsonResponse({"slot": slt})
        
    return JsonResponse({"errors": form.errors})

@csrf_exempt
@require_POST
def remove_slot(request):
    '''Удаление слота'''
    
    Slot = apps.get_model('schedule.Slot')
    
    uid = int(request.POST['uid'])
    sid = int(request.POST['sid'])
    
    slot = Slot.objects.filter(id=int(sid)).first()
    
    if slot.vet.id == uid:
        slot.delete()
        
        return JsonResponse({"status": "ok"})
    
    return JsonResponse({"status": "fail"})

@csrf_exempt
@require_POST
def appoint_to_slot(request):

    '''Запись в слот'''
    
    Pet = apps.get_model('pets.Pet')
    Slot = apps.get_model('schedule.Slot')
    User = apps.get_model('users.User')
    
    form = SlotAppointForm(request.POST)
    
    if form.is_valid():
        
        slot = Slot.objects.filter(id=form.cleaned_data['id']).first()
        pet = Pet.objects.filter(id=form.cleaned_data['pet'].id).first()
        # user = User.objects.filter(id=form.cleaned_data['owner'].id).first()
        
        if pet == None:
            return JsonResponse({"errors": "Pet not found"})

        '''if pet.user.id != form.cleaned_data['pet'] and not user.vet:
            return JsonResponse({"error": "You aren't veterinar or owner of the pet"})'''

        if slot == None or slot.appointed:
            return JsonResponse({"errors": "Slot not found or had been appointed"})
        
        for k in form.cleaned_data.keys():
            if k != 'user' and k != 'id' and form.cleaned_data[k] != '':
                pet.__dict__[k] = form.cleaned_data[k]

        slot.purpose = form.cleaned_data['purpose']
        slot.pet = form.cleaned_data['pet'].id
        slot.owner = form.cleaned_data['owner'].id
        slot.appointed = True
        slot.save()

        slt = { 'id': slot.id, 'user_id': slot.vet.id, 'slot_date': slot.slot_date, 
                'slot_time': slot.slot_time, 'purpose': slot.purpose, 'pet': slot.pet.id, 'appointed': slot.appointed }
        
        return JsonResponse({"slot": slt})
            
    return JsonResponse({"errors": form.errors})

@csrf_exempt
@require_POST
def disappoint_from_slot(request):

    '''Отмена записи в слот'''

    Pet = apps.get_model('pets.Pet')
    Slot = apps.get_model('schedule.Slot')
    User = apps.get_model('users.User')
    
    form = SlotDisappointForm(request.POST)
    
    if form.is_valid():
        
        slot = Slot.objects.filter(id=form.cleaned_data['id']).first()
        pet = Pet.objects.filter(id=form.cleaned_data['pet'].id).first()
        # user = User.objects.filter(id=form.cleaned_data['owner'].id).first()
        
        if pet == None:
            return JsonResponse({"errors": "Pet not found"})

        '''if pet.user.id != form.cleaned_data['pet'] and not user.vet:
            return JsonResponse({"error": "You aren't veterinar or owner of the pet"})'''

        if slot == None or not slot.appointed:
            return JsonResponse({"errors": "Slot not found or had not been appointed"})
        
        for k in form.cleaned_data.keys():
            if k != 'user' and k != 'id' and form.cleaned_data[k] != '':
                pet.__dict__[k] = form.cleaned_data[k]

        slot.purpose = ''
        slot.pet = None
        slot.appointed = False
        slot.save()

        slt = { 'id': slot.id, 'user_id': slot.vet.id, 'slot_date': slot.slot_date, 
                'slot_time': slot.slot_time, 'purpose': slot.purpose, 'pet': -1, 'appointed': slot.appointed }
        
        return JsonResponse({"slot": slt})
            
    return JsonResponse({"errors": form.errors})

@require_GET
def vet_day_slots_list(request):

    '''Выдает список доступных слотов для записи на день, для выбранного ветеринара'''

    User = apps.get_model('users.User')
    Slot = apps.get_model('schedule.Slot')
    
    vid = int(request.GET['vid'])
    slot_dt = request.GET['dt']

    vet = User.objects.filter(id=vid).first()

    if not vet.vet:
        return JsonResponse({"error": "Selected vid is not a veterinar"})

    slots = Slot.objects.filter(vet_id=vid, slot_date=slot_dt)

    available_slots = []

    for slot in slots:
        if not slot.appointed:
            slt = {'id': slot.id, 'slot_time': slot.slot_time}
            available_slots.append(slt)

    return JsonResponse({'daily_available_slots': list(available_slots)})

@require_GET
def vet_int_slots_list(request):
    
    '''Выдает список доступных слотов для записи на заданный промежуток, для выбранного ветеринара'''

    User = apps.get_model('users.User')
    Slot = apps.get_model('schedule.Slot')

    vid = int(request.GET['vid'])
    slot_st_dt = request.GET['st_dt']
    slot_end_dt = request.GET['end_dt']

    vet = User.objects.filter(id=vid).first()

    if not vet.vet:
        return JsonResponse({"error": "Selected vid is not a veterinar"})

    slots = Slot.objects.filter(vet_id=vid, slot_date__gte=slot_st_dt, slot_date__lte=slot_end_dt)

    available_slots = []

    for slot in slots:
        if not slot.appointed:
            slt = {'id': slot.id, 'slot_date': slot.slot_date, 'slot_time': slot.slot_time}
            available_slots.append(slt)

    return JsonResponse({'interval_available_slots': list(available_slots)})

@require_GET
def day_slots_list(request):

    '''Выдает список слотов на день, для выбранного ветеринара'''

    User = apps.get_model('users.User')
    Slot = apps.get_model('schedule.Slot')

    uid = int(request.GET['uid'])
    slot_dt = request.GET['dt']

    user = User.objects.filter(id=uid).first()

    if not user.vet:
        return JsonResponse({"error": "You aren't veterinar"})

    slots = Slot.objects.filter(vet_id=uid, slot_date=slot_dt)

    available_slots = []

    for slot in slots:
        slt = {'id': slot.id, 'slot_time': slot.slot_time, 'purpose': slot.purpose, 'pet_id': slot.pet}
        available_slots.append(slt)

    return JsonResponse({'daily_available_slots': list(available_slots)})

@require_GET
def int_slots_list(request):

    '''Выдает список слотов на заданный промежуток, для выбранного ветеринара'''

    User = apps.get_model('users.User')
    Slot = apps.get_model('schedule.Slot')

    uid = int(request.GET['uid'])
    slot_st_dt = request.GET['st_dt']
    slot_end_dt = request.GET['end_dt']

    user = User.objects.filter(id=uid).first()

    if not user.vet:
        return JsonResponse({"error": "You aren't veterinar"})

    slots = Slot.objects.filter(vet_id=uid, slot_date__gte=slot_st_dt, slot_date__lte=slot_end_dt)

    available_slots = []

    for slot in slots:
        slt = {'id': slot.id, 'slot_date': slot.slot_date, 'slot_time': slot.slot_time, 'purpose': slot.purpose, 'pet_id': slot.pet}
        available_slots.append(slt)

    return JsonResponse({'interval_available_slots': list(available_slots)})

@require_GET
def pet_slots_list(request):
    
    '''Выдает список слотов , на кторые записан выбранный питомец'''

    User = apps.get_model('users.User')
    Pet = apps.get_model('pets.Pet')
    Slot = apps.get_model('schedule.Slot')

    uid = int(request.GET['uid'])
    pid = int(request.GET['pid'])

    user = User.objects.filter(id=uid).first()
    pet = Pet.objects.filter(id=pid).first()

    if pet.user.id != uid and not user.vet:
        return JsonResponse({"error": "You aren't owner of this pet or veterinar"})

    slots = Slot.objects.filter(pet_id=pid)

    pet_appointed_slots = []

    for slot in slots:
        slt = { 'id': slot.id, 'vet': f'{slot.vet.last_name} {slot.vet.first_name[0]}.{slot.vet.patronymic[0]}.', 
                'slot_date': slot.slot_date, 'slot_time': slot.slot_time, 'purpose': slot.purpose}
        pet_appointed_slots.append(slt)

    return JsonResponse({'pet_appointed_slots': list(pet_appointed_slots)})