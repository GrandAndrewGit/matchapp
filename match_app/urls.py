from django.urls import path
from .views import startPage, createDataSet, matchData, deleteDataSet, importNewUsers, usersList


app_name = 'match_app'

urlpatterns = [
    path('', startPage, name='match-start'),
    path('createds/', createDataSet, name='create-dataset'),
    path('deleteds/', deleteDataSet, name='delete-dataset'),
    path('matchdata/', matchData, name='match-data'),
    path('importusers/', importNewUsers, name='import-users'),
    path('usersindb/', usersList, name='users-in-db'),
]