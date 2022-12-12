from django.http import JsonResponse
from database_conf import load_database
from django.views.decorators.csrf import csrf_exempt
import json

AUTH, DATABASE = load_database()

@csrf_exempt
def check_signIn(request):
    if request.method == 'POST':
        
        body_unicode = request.body.decode('UTF-8')
        body = json.loads(body_unicode)
        email = body['email']
        password = body['password']
        
        try:
            user = dict(AUTH.sign_in_with_email_and_password(email=email, password=password))
        except:
            return JsonResponse({'success': False, 'error': 'Não foi possível logar com o usuário, verifique com o suporte!'})
        
        name = DATABASE.child('users').child(user.get('localId')).get().val()['name']
        user.update({"name": name})

        return  JsonResponse({'sucess': True, 'data': user})        
