# Django csv and xml Match App.

# How to deploy project?

1. Clone project to your machine
2. Setup your virtual environment with python3.8
3. Install packages from requirements.txt
4. Save somewhere else settings.py and urls.py from "core" folder
5. Remove "core" folder 
6. Start new project via command "django-admin startproject core ."
7. Replace settings.py and urls.py in new "core" folder BUT save django SECRET_KEY in settings.py
8. Create migrations via commands "python manage.py makemigrations match_app" and "python manage.py makemigrations users_app"
9. Apply migrations and create sqlite database "python manage.py migrate"
10. Create superuser and runserver to start testing app


# Short description of App

This app allows to match user's data from csv and xml files (strict structure) by last_name field. It ignores users with empty last_name or with first_name/last_name fields which includes brackets ([] or()). 

After finding coincidences it creates intermediate user objects in db with an opportunity for editing by admin users from django admin panel. If it's not necessary admin users can create new real users from this intermediate user objects. App also checks the uniqueness of username before creation of real user. After it admin user will be able to match csv and xml files again.

It was used AbstractBaseUser for extending user model as it was needed for app's purposes.