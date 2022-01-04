from django.urls import path, include

from registration.views import Index, Login, Logout, Register, Profile, \
    EmailConfirm, EmailConfirmSent, EmailConfirmDone, \
    ReservationsView


urlpatterns = [
    path('', Index.as_view(), name='index'),

    path('accounts/', include([
        path('login', Login.as_view(), name='login'),
        path('login/', Login.as_view(), name='login'),
        path('logout', Logout.as_view(), name='logout'),
        path('register', Register.as_view(), name='register'),

        path('confirm_email', EmailConfirm.as_view(), name='email_confirm'),
        path('confirm_email/', include([
            path('sent', EmailConfirmSent.as_view(), name='email_confirm_sent'),
            path('<str:username>', EmailConfirmDone.as_view(), name='email_confirm_done'),
        ])),
    ])),

    path('<str:username>/', include([
        path('profile', Profile.as_view(), name='profile'),
        path('reservations', ReservationsView.as_view(), name='reservations'),
    ])),
]
