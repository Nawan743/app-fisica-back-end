import time
from django.http import JsonResponse
from database_conf import load_database
from django.views.decorators.csrf import csrf_exempt
import json

AUTH, DATABASE = load_database()

@csrf_exempt
def signUp(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('UTF-8')
        body = json.loads(body_unicode)
        name = body['name']
        email = body['email']
        password = body['password']
        
        try:
            user = dict(AUTH.create_user_with_email_and_password(email=email, password=password))
            DATABASE.child('users').child(user.get('localId')).set({'name':name, 'creation_time': time.ctime()})
        except:
            return JsonResponse({'success': False, 'error': 'Não foi possível criar o usuário, verifique com o suporte!'})
        
        user.update({'name': name})
      
        return JsonResponse({'sucess': True, 'data': user})
