from django.urls import path
from .views import profilePage, logoutPage


app_name = 'users_app'

urlpatterns = [
    path('profile/', profilePage, name='profile'),
    path('logout/', logoutPage, name='logout'),
    # path('createds/', createDataSet, name='create-dataset'),

]