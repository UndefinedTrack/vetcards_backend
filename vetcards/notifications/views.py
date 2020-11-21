from django.shortcuts import render
from django.apps import apps

from django.http import JsonResponse

from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST

from rest_framework_simplejwt.authentication import JWTAuthentication

from django.views.decorators.cache import cache_page
from django.core.cache import cache

from .forms import NotificationForm

# Create your views here.

@csrf_exempt
@require_POST
def create_notification(request):

    '''Создание уведомления'''

    Notification = apps.get_model('notifications.Notification')
    Pet = apps.get_model('pets.Pet')
    User = apps.get_model('users.User')


    form = NotificationForm(request.POST)

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
    
        pet = Pet.objects.filter(id=int(form.cleaned_data['pet'].id)).first()
        # user = User.objects.filter(id=uid).first() # int(form.cleaned_data['user'].id)).first()
        
        if pet.user.id != user.id and not user.vet:
            return JsonResponse({"errors": "you aren't a veterinar or owner of this pet"})

        if user.vet and uid != int(form.cleaned_data['user']):
            uid = int(form.cleaned_data['user'])
        elif not user.vet and uid != int(form.cleaned_data['pk']):
            return JsonResponse({"errors": "Your id doesn't match the specified"})

        notification = Notification.objects.create(pet_id=form.cleaned_data['pet'].id,
                                                user_id=uid,
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

    nid = int(request.POST['nid'])
    
    notif = Notification.objects.filter(id=int(nid)).first()
    
    if notif.user.id == uid or user.vet:

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

    notifications = cache.get(f'notif_list_{pid}')
    if notifications:
        return JsonResponse({'notifications': notifications})
    
    notifications = Notification.objects.filter(pet_id=int(pid)).values('id', 'pet_id', 'user_id', 'notif_type', 'description', 'repeat', 'notif_date')
    cache.set(f'notif_list_{pid}', list(notifications))
    
    return JsonResponse({'notifications': list(notifications)})