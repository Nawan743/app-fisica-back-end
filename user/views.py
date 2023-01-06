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
        
        try:
            user = _authOperations(email, password, 'authenticate')
        except Exception as error:
            return JsonResponse({'success': False, 'error': str(error)})
        
        try:
            data = _getDatabaseRegister(user.get('localId'))
        except Exception as error:
            return JsonResponse({'success': False, 'error': str(error)})

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
        try:
            user = _authOperations(email, password, 'create')
        except Exception as error:
            return JsonResponse({'success': False, 'error': str(error)})
        
        try:
            _createDatabaseRegister(user.get('localId'), data)
        except Exception as error:
            return JsonResponse({'success': False, 'error': str(error)})
        
        return JsonResponse({'sucess': True, 'data': data}) 


def _authOperations(email: str, password: str, operation: str):
    try:
        if operation == 'create':
            return AUTH.create_user_with_email_and_password(email=email, password=password)
        elif operation == 'authenticate':
            return AUTH.sign_in_with_email_and_password(email=email, password=password)
    except:
        raise Exception('Unable to ' + operation + ' user, check with support!')
    
def _createDatabaseRegister(userId, data):
    if DATABASE:
        try:
            DATABASE.child('users').child(userId).set(data)
        except:
            raise Exception('Unable to create user register, check with support!')
        
def _getDatabaseRegister(userId):
    if DATABASE:
        try:
            return DATABASE.child('users').child(userId).get().val()
        except:
            raise Exception('Unable to get user data, check with support!')
        