import re
from django.shortcuts import render
from .forms import DataSetForm
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import DataSet, UserFromData
from datetime import datetime

import csv
import xml.etree.ElementTree as ET
from users_app.models import CustomUser
from django.conf import settings
User = settings.AUTH_USER_MODEL
from django.contrib.auth.decorators import user_passes_test


@user_passes_test(lambda u: u.is_staff)
def startPage(request):
    data_set = DataSet.objects.all().first()
    if data_set and data_set.processed_status == False:
        context = {
            'need_to_process': True
        }
    elif data_set and data_set.processed_status == True:
        context = {
            'need_to_import_users': True
        }
    else:
        context = {}
    return render(request, 'match-start.html', context)

@user_passes_test(lambda u: u.is_staff)
def createDataSet(request):
    data_set = DataSet.objects.all()
    users = UserFromData.objects.all()
    if request.method == 'POST':
        form = DataSetForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('match_app:match-start')
    else:
        form = DataSetForm()

    if data_set and not users:
        context = {
            'deny_access': True
        }
    elif users:
        context = {
            'deny_access_users': True
        }
    else:
        context = {
            'form': form
        }
    return render(request, 'create-dataset.html', context)
        

def has_brackets(string):
    regex = re.compile('[()}{]')
    if (regex.search(string) == None):
        return False
    else:
        return True

@user_passes_test(lambda u: u.is_staff)
def matchData(request):
    data_set = DataSet.objects.all().first()
    if data_set:
        if data_set.processed_status == False:
            csv_correct_list = []
            file = open(data_set.csv_file.path)
            csv_reader = csv.reader(file)
            for i in csv_reader:
                if has_brackets(i[0]) or (len(i[0]) == 0):
                    continue
                else:
                    csv_correct_list.append((i[0], i[1], i[2]))
            file.close()

            result_users_list = []

            tree = ET.parse(data_set.xml_file.path)
            root = tree.getroot()

            for user in root.iter('user'):
                user_item = []
                if user[1].text is not None and not has_brackets(user[1].text):
                    if user[0].text is not None:
                        if not has_brackets(user[0].text):
                            for i_csv in csv_correct_list:
                                last_name = i_csv[0].split(".", 1)
                                if len(last_name) >= 2 :
                                    if last_name[1].lower() == user[1].text.lower():
                                        result_users_list.append([i_csv[0], i_csv[1], i_csv[2], user[0].text, user[1].text, user[2].text])
                                else:
                                    if i_csv[0].lower() == user[1].text.lower():
                                        result_users_list.append([i_csv[0], i_csv[1], i_csv[2], user[0].text, user[1].text, user[2].text])
                    else:
                        for i_csv in csv_correct_list:
                            last_name = i_csv[0].split(".", 1)
                            if len(last_name) >= 2 :
                                if last_name[1].lower() == user[1].text.lower():
                                    result_users_list.append([i_csv[0], i_csv[1], i_csv[2], '', user[1].text, user[2].text])
                            else:
                                if i_csv[0].lower() == user[1].text.lower():
                                    result_users_list.append([i_csv[0], i_csv[1], i_csv[2], '', user[1].text, user[2].text])

            for user in result_users_list:
                if (CustomUser.objects.filter(username=user[0]).exists()):
                    UserFromData.objects.create(
                        username=user[0], 
                        first_name=user[3], 
                        last_name=user[4], 
                        date_joined=datetime.fromtimestamp(int(user[2])), 
                        password=user[1], 
                        avatar=user[5],
                        is_unique=False)
                else:
                    UserFromData.objects.create(
                        username=user[0], 
                        first_name=user[3], 
                        last_name=user[4], 
                        date_joined=datetime.fromtimestamp(int(user[2])), 
                        password=user[1], 
                        avatar=user[5])
            data_set.processed_status = True
            data_set.save()

        users = UserFromData.objects.all()
        context = {
            'users': users
        }
        return render(request, 'users-from-data.html', context)
    else:
        context = {
            'nodata': True
        }
        return render(request, 'users-from-data.html', context)

@user_passes_test(lambda u: u.is_staff)
def deleteDataSet(request):
    data_set = DataSet.objects.all().first()
    if data_set:
        data_set.delete()
    UserFromData.objects.all().delete()
    return HttpResponseRedirect(reverse('match_app:match-start'))

@user_passes_test(lambda u: u.is_staff)
def importNewUsers(request):
    users_list = UserFromData.objects.all()
    counter = 0
    if users_list:
        for i in users_list:
            if not (CustomUser.objects.filter(username=i.username).exists()):
                CustomUser.objects.create_user(
                    username=i.username,
                    first_name=i.first_name,
                    last_name=i.last_name,
                    password=i.password,
                    date_joined=i.date_joined,
                    avatar_link=i.avatar
                )
                counter += 1
            i.delete()
        DataSet.objects.all().first().delete()
    context = {
        'imported_users': counter
    }
    return render(request, 'import-success.html', context)

@user_passes_test(lambda u: u.is_staff)
def usersList(request):
    users = CustomUser.objects.all()
    context = {
        'users': users
    }
    return render(request, 'users-list.html', context)