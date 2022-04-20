from django.urls import path
from . import views
from django.views.generic import RedirectView

urlpatterns = [
    path('', RedirectView.as_view(url='login/', permanent=True)),
    path('login/', views.login),
    path('login/auth/', views.auth_form_check),
    path('logout/', views.logout),
    path('list/', views.bots_list)
]
