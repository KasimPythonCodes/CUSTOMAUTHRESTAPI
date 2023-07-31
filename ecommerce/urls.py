
from django.contrib import admin
from django.urls import path
from app.views import*
# from app.views import Index ,Plus ,SetCookie , GetCookie

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',Registration),
    path('login/',Login_User),
    path('view/',UserViews),
    path('user/api/registration/',RegistraionSerializerApi.as_view()),
    path('user/api/userlogin/' ,UserLoginApi.as_view()),
    path('user/api/profile/',UserProfileApi.as_view()),
    
    
    
    # path('',Index , name='index'),
    # path('plus/',Plus , name='plus'),
    # path('setcookie/',SetCookie , name='SetCookie'),
    # path('getcookie/',GetCookie , name='GetCookie'),

]
