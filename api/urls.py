from django.urls import URLPattern, path
from . import views

urlpatterns = [    
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('job_titles/', views.titles, name='job_titles'),
    path('abilities/', views.abilities, name='abilities'),
    path('getempolyers/', views.getemployers, name='employers'),
    path('changedata/', views.changedata, name='changedata'),
    path('changepassword/', views.changepassword, name='changepassword')
]