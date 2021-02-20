from django.urls import path
from myproject.core import views as v


app_name = 'core'


urlpatterns = [
    path('', v.index, name='index'),
    path('my_http_response/', v.my_http_response, name='my_http_response'),
    path('my_render_to_response/', v.my_render_to_response, name='my_render_to_response'),
    path('user/', v.users, name='users'),
    path('user/<int:pk>/', v.user_detail, name='user_detail'),
    path('ping/', v.ping, name='ping'),
]
