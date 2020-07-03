from django.conf.urls import url,include

from django.urls import path
from blog import views

# SET THE NAMESPACE!
app_name = 'basic_app'
urlpatterns = [
    url(r'register/',views.register,name='register'),
    path('user_login/',views.user_login,name='user_login'),
    

]


