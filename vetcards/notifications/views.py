from django.shortcuts import render
from django.apps import apps

from django.http import JsonResponse

from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST

from django.views.decorators.cache import cache_page
from django.core.cache import cache

from .forms import NotificationForm

# Create your views here.


@require_POST
def create_notification(request):

    '''Создание уведомления'''

    Notification = apps.get_model('notifications.Notification')
    Pet = apps.get_model('pets.Pet')
    User = apps.get_model('users.User')


    form = NotificationForm(request.POST)

    if form.is_valid():
    
        pet = Pet.objects.filter(id=int(form.cleaned_data['pet'].id)).first()
        user = User.objects.filter(id=int(form.cleaned_data['user'].id)).first()
        
        if pet.user.id != form.cleaned_data['user'].id and not user.vet:
            return JsonResponse({"errors": "you aren't a veterinar or owner of this pet"})

        notification = Notification.objects.create(pet_id=form.cleaned_data['pet'].id,
                                                user_id=form.cleaned_data['user'].id,
                                                notif_type=form.cleaned_data['notif_type'],
                                                description=form.cleaned_data['description'],
                                                repeat=form.cleaned_data['repeat'])
        
        notif = {'id': notification.id, 'pet_id': notification.pet_id, 'user_id': notification.user_id,
                'description': notification.description, 'repeat': notification.repeat, 'notif_date': notification.notif_date}

        pid = notification.pet.id

        notifs = cache.get(f'notif_list_{pid}')
        if notifs:
            cache.delete(f'notif_list_{pid}')
        
        return JsonResponse({"notification": notif})
        
    return JsonResponse({"errors": form.errors})

@csrf_exempt
@require_POST
def delete_notification(request):

    '''Удаление уведомления'''
    
    Notification = apps.get_model('notifications.Notification')
    
    uid = int(request.POST['uid'])
    nid = int(request.POST['nid'])
    
    notif = Notification.objects.filter(id=int(nid)).first()
    
    if notif.user.id == uid:

        pid = notif.pet.id
        notif.delete()

        notifs = cache.get(f'notif_list_{pid}')
        if notifs:
            cache.delete(f'notif_list_{pid}')
        
        return JsonResponse({"status": "ok"})
    
    return JsonResponse({"status": "fail"})


@require_GET
def notifications_list(request):

    '''Список уведомлений, установленных владельцем питомца'''

    Pet = apps.get_model('pets.Pet')
    Notification = apps.get_model('notifications.Notification')

    pid = int(request.GET['pid'])
    uid = int(request.GET['uid'])
    
    pet = Pet.objects.filter(id=int(pid)).first()

    if pet.user.id != uid:
        return JsonResponse({"errors": "you aren't owner of this pet"})

    notifications = cache.get(f'notif_list_{pid}')
    if notifications:
        return JsonResponse({'notifications': notifications})
    
    notifications = Notification.objects.filter(pet_id=int(pid)).values('id', 'pet_id', 'user_id', 'notif_type', 'description', 'repeat', 'notif_date')
    cache.set(f'notif_list_{pid}', list(notifications))
    
    return JsonResponse({'notifications': list(notifications)})