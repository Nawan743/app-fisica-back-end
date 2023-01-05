from django.urls import path
from user.views import signIn, signUp

app_name = "user"

urlpatterns = [
    path('signin/', signIn, name='login'),
    path('signup/', signUp, name='register')
]