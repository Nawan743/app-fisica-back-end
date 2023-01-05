from django.http import JsonResponse
from database_conf import load_database
from django.views.decorators.csrf import csrf_exempt
import time
import json

AUTH, DATABASE = load_database()

@csrf_exempt
def signIn(request):
    if request.method == 'POST':
        
        body_unicode = request.body.decode('UTF-8')
        body = json.loads(body_unicode)
        email = body['email']
        password = body['password']
        
        user = _checkUser(email, password, 'authenticate')
        
        name = DATABASE.child('users').child(user.get('localId')).get().val()['name']
        user.update({"name": name})

        return  JsonResponse({'sucess': True, 'data': user})        


@csrf_exempt
def signUp(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('UTF-8')
        body = json.loads(body_unicode)
        name = body['name']
        email = body['email']
        password = body['password']
        
        user = _checkUser(email, password, 'create')
        DATABASE.child('users').child(user.get('localId')).set({'name':name, 'creation_time': time.ctime()})
        user.update({'name': name})
      
        return JsonResponse({'sucess': True, 'data': user})


def _checkUser(email: str, password: str, operation: str):
    operations = {
        'create': AUTH.create_user_with_email_and_password(email=email, password=password),
        'authenticate': AUTH.sign_in_with_email_and_password(email=email, password=password)
    }
    try:
        operations['operation']
    except:
        return JsonResponse({'success': False, 'error': 'Unable to ' + operation + ' user, check with support!'})
        