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
            user = __authOperations(email, password, 'authenticate')
        except Exception as error:
            return JsonResponse({'success': False, 'error': str(error)})
        
        try:
            data = __getDatabaseRegister(user.get('localId'))
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
            user = __authOperations(email, password, 'create')
        except Exception as error:
            return JsonResponse({'success': False, 'error': str(error)})
        
        try:
            __createDatabaseRegister(user.get('localId'), data)
        except Exception as error:
            AUTH.delete_user_account(user.get('idToken'))
            return JsonResponse({'success': False, 'error': str(error)})
           
        
        return JsonResponse({'sucess': True, 'data': data}) 


def __authOperations(email: str, password: str, operation: str):
    if not AUTH:
        raise Exception('Unable to ' + operation + ' user, probably our system of authentication are unavailable, please check with support!')
    
    if operation == 'create':
        try:
            return AUTH.create_user_with_email_and_password(email=email, password=password)
        except:
            raise Exception('Email already exist in our database, please check with support!')    
    elif operation == 'authenticate':
        try:
            return AUTH.sign_in_with_email_and_password(email=email, password=password)
        except:
            raise Exception('Email or password is incorrect!')
    
    
def __createDatabaseRegister(userId, data):
    if not DATABASE:
        raise Exception('Database was encountered unavailable, please check with support!')
    
    try:
        DATABASE.child('users').child(userId).set(data)
    except:
        raise Exception('Unable to create user register, please check with support!')
        
def __getDatabaseRegister(userId):
    if not DATABASE:
        raise Exception('Database was encountered unavailable, please check with support!')
    
    try:
        return DATABASE.child('users').child(userId).get().val()
    except:
        raise Exception('Unable to get user data, please check with support!')
        