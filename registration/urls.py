from django.urls import path, include

from registration.views import Index, Login, Logout, Register, Profile


urlpatterns = [
    path('', Index.as_view(), name='index'),

    path('accounts/', include([
        path('login', Login.as_view(), name='login'),
        path('login/', Login.as_view(), name='login'),
        path('logout', Logout.as_view(), name='logout'),
        path('register', Register.as_view(), name='register'),
    ])),

    path('<str:username>/', include([
        path('profile', Profile.as_view(), name='profile'),
    ])),
]
