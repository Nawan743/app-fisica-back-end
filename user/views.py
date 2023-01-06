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
        data = DATABASE.child('users').child(user.get('localId')).get().val()

        return  JsonResponse({'sucess': True, 'data': data})        


@csrf_exempt
def signUp(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('UTF-8')
        body = json.loads(body_unicode)
        name = body['name']
        email = body['email']
        password = body['password']
        data = {
            'name': name,
            'email': email,
            'creation_time': time.ctime()
        }
        
        user = _checkUser(email, password, 'create')
        DATABASE.child('users').child(user.get('localId')).set(data)
        
        return JsonResponse({'sucess': True, 'data': data}) 


def _checkUser(email: str, password: str, operation: str):
    try:
        if operation == 'create':
            return AUTH.create_user_with_email_and_password(email=email, password=password)
        elif operation == 'authenticate':
            return AUTH.sign_in_with_email_and_password(email=email, password=password)
    except:
        AUTH.delete_user_account(email)
        raise Exception('Unable to ' + operation + ' user, check with support!')
        