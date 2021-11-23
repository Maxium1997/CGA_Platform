from django.urls import path, include

from registration.views import Index, Login, Logout, Register


urlpatterns = [
    path('', Index.as_view(), name='index'),

    path('login', Login.as_view(), name='login'),
    path('logout', Logout.as_view(), name='logout'),
    path('register', Register.as_view(), name='register'),
]
