from django.urls import path
from register.views import signUp

app_name = "register"

urlpatterns = [
    path('signup/', signUp, name='register')
]