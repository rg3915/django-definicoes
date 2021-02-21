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
    path('person/<int:pk>/', v.person_detail, name='person_detail'),
    path('person/redirected/<int:pk>/', v.person_redirected, name='person_redirected'),
    path('person/', v.persons, name='persons'),
    path('person/redirected/', v.persons_redirected, name='persons_redirected'),
    path('book/', v.BookListView.as_view(), name='book_list'),
    path('book/<int:pk>/', v.book_detail, name='book_detail'),
    path('book/add/', v.BookCreateView.as_view(), name='book_create'),
    path('book/redirected/', v.book_redirected, name='book_redirected'),
]
