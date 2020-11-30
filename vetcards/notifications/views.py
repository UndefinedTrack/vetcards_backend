from django.shortcuts import render
from django.apps import apps

from django.http import JsonResponse

from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST

from rest_framework_simplejwt.authentication import JWTAuthentication

from django.views.decorators.cache import cache_page
from django.core.cache import cache

from .forms import NotificationForm, UpdateNotificationForm, BroadcastNotificationForm, ContactForm

from .tasks import broadcast_notif, contact_notif

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

        if user.vet and uid != int(form.cleaned_data['user'].id):
            uid = int(form.cleaned_data['user'])
        elif not user.vet and uid != int(form.cleaned_data['user'].id):
            return JsonResponse({"errors": "Your id doesn't match the specified"})

        notification = Notification.objects.create(pet_id=form.cleaned_data['pet'].id,
                                                user_id=uid,
                                                notif_type=form.cleaned_data['notif_type'],
                                                description=form.cleaned_data['description'],
                                                repeat=form.cleaned_data['repeat'])
        
        notif = {'id': notification.id, 'pet_id': notification.pet_id, 
                'user_id': notification.user_id, 'notif_type': notification.notif_type,
                'description': '' if notification.description is None else notification.description,
                'repeat': notification.repeat, 'notif_date': notification.notif_date}

        pid = notification.pet.id

        notifs = cache.get(f'notif_list_{pid}')
        if notifs:
            cache.delete(f'notif_list_{pid}')
        
        return JsonResponse({"notification": notif})
        
    return JsonResponse({"errors": form.errors})

@csrf_exempt
@require_POST
def update_notification(request):

    '''Обновление информации о домашней процедуре'''
    
    Notification = apps.get_model('notifications.Notification')
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
    
    form = UpdateNotificationForm(request.POST)
    
    if form.is_valid():
        
        notification = Notification.objects.filter(id=form.cleaned_data['pk']).first()
        # user = User.objects.filter(id=form.cleaned_data['user'].id).first()
        
        if notification == None:
            return JsonResponse({"errors": "Procedure not found"})

        if notification.user.id != user.id: #form.cleaned_data['user'].id:
            return JsonResponse({"error": "You aren't owner of this procedure"})
        
        for k in form.cleaned_data.keys():
            if k != 'pk':
                notification.__dict__[k] = form.cleaned_data[k]
                
        notification.save()

        notif = {'id': notification.id, 'pet_id': notification.pet_id, 
                'user_id': notification.user_id, 'notif_type': notification.notif_type,
                'description': '' if notification.description is None else notification.description, 
                'repeat': notification.repeat, 'notif_date': notification.notif_date}

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
    
    notifs = Notification.objects.filter(pet_id=int(pid)) #.values('id', 'pet_id', 'user_id', 'notif_type', 'description', 'repeat', 'notif_date')
    notifications = []

    for notification in notifs:
        notif = {'id': notification.id, 'pet_id': notification.pet_id, 
                'user_id': notification.user_id, 'notif_type': notification.notif_type,
                'description': '' if notification.description is None else notification.description, 
                'repeat': notification.repeat, 'notif_date': notification.notif_date}

        notifications.append(notif)

    cache.set(f'notif_list_{pid}', notifications)
    
    return JsonResponse({'notifications': notifications})

@csrf_exempt
@require_POST
def broadcast(request):
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

    form = BroadcastNotificationForm(request.POST)

    if form.is_valid():

        if user.vet:
            address = {
                "region": form.cleaned_data["region"], 
                "city": form.cleaned_data["city"], 
                "street": form.cleaned_data["street"]
            }

            broadcast_notif.delay(address, form.cleaned_data["subject"], form.cleaned_data["message"])

            return JsonResponse({"status": "ok"})

        return JsonResponse({"error": "You aren't a veterinar"})
            
    return JsonResponse({"errors": form.errors})

@csrf_exempt
@require_POST
def contact(request):

    form = ContactForm(request.POST)

    if form.is_valid():
        contact_notif.delay(form.cleaned_data['first_name'], form.cleaned_data['last_name'], form.cleaned_data['email'])

        return JsonResponse({"status": "ok"})

    return JsonResponse({"errors": form.errors})