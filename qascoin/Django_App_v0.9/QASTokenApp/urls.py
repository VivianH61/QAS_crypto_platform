from django.urls import path, re_path

from .views import *


urlpatterns = [
    path('signup/', SignUpView, name='signup'),
    path('login/', login_view, name='login'),
    path('home/', real_home, name='real_home'),
    path('account/', private_key, name='account'),
    path('hand_private_key/', handle_private_key, name='handle_private_key'),
    #path('register/', RegistrationView, name='register'),
    re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,32})/$', activate, name='activate'),
    #path('verify/<str:token>', verify),
]