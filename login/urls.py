from django.urls import path
from login.views import check_signIn

app_name = "login"

urlpatterns = [
    path('signin/', check_signIn, name='login')
]