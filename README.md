- Django is a Python web framework
- Build web applications quickly w/ less code

Has batteries included:
- ORM (Object relational mapper): Enables you to interact with your database, creating SQL queries
- Admin: Provides admin interface
- Templates: Used for generating webpages
- URL mapping: Helps create understandable urls
- Forms: Web forms like html forms
- Packages: Many 3rd party packages for free


After installing django in your virtual environment, you can create a new project using this command
```
django-admin startproject <project_name>
```
You can then run the django server with:
```
python manage.py runserver
```


# Creating our first webpage
```
python -m manage.py startapp website
```
This creates a new folder for the website contents
> The views.py file is where I will create the website
> I've deleted all python files within the website folder except for views.py, urls.py, and \__init__.py 


views.py
```python
from datetime import datetime  
from django.shortcuts import render  
from django.http import HttpResponse  
  
  
def welcome(request):  
    return HttpResponse("Welcome to the Meeting Planner!")  
  
  
def date(request):  
    return HttpResponse("This page was served at " \+ str(datetime.now()))  
  
  
def about(request):  
    return HttpResponse("My name is Joshua Eom. Welcome to my first webpage using Django!")
```
urls.py
```python
"""meeting\_planner URL Configuration  
  
The \`urlpatterns\` list routes URLs to views. For more information please see:  
 https://docs.djangoproject.com/en/3.1/topics/http/urls/Examples:  
Function views  
 1. Add an import:  from my\_app import views 2. Add a URL to urlpatterns:  path('', views.home, name='home')Class-based views  
 1. Add an import:  from other\_app.views import Home 2. Add a URL to urlpatterns:  path('', Home.as\_view(), name='home')Including another URLconf  
 1. Import the include() function: from django.urls import include, path 2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))"""  
from django.contrib import admin  
from django.urls import path  
  
from website.views import welcome, date, about  
  
urlpatterns = \[  
    path('admin/', admin.site.urls),  
 path('', welcome),  
 path('date', date),  
 path('about', about)  
\]
```


# Setting up a Data Model
How to see current migrations
```
python manage.py showmigrations
```
Migrate
```
python manage.py migrate
```
Get an sql shell
```
python manage.py dbshell
```
Another way to see migrations
```sql
.table
select * from django_migrations;
.exit -- (If you want to exit)
```

## Creating a model class
https://docs.djangoproject.com/en/3.1/topics/migrations/
models.py
```python
from django.db import models  
  
  
class Meeting(models.Model):  
    title = models.CharField(max_length=200)  
    date = models.DateField()
```
Make migrations
```
python manage.py makemigrations
```
```
python manage.py sqlmigrate meetings 0001
BEGIN;
--
-- Create model Meeting
--
CREATE TABLE "meetings_meeting" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "title" varchar(200) NOT NULL, "date" date NOT NULL)
;
COMMIT;
python manage.py migrate
```


## The Admin Interface
admin.py
```python
from django.contrib import admin  
  
from .models import Meeting  
  
admin.site.register(Meeting)
```
Add superuser to login to admin interface
```
python manage.py createsuperuser
Username (leave blank to use 'joshua'):
Email address: info@example.com
Password:
Password (again):
This password is too common.
Bypass password validation and create user anyway? [y/N]: y
Superuser created successfully.
```
More information about django model fields: https://docs.djangoproject.com/en/3.1/ref/models/fields/

## Migration workflow
```python
# Step 1: Change model code
# Step 2: Generate migration script (check it!)
python manage.py makemigrations
# Show migrations
python manage.py showmigrations
# Step 3: Run migrations
python manage.py migrate
```
```python
# admin.py
from django.contrib import admin
from .models import Meeting
admin.site.register(Meeting)

# Don't forget to create a superuser
python manage.py createsuperuser
```

# Combining Model, View, and Template
> 02/13/2021

Now I'm going to create a template to render HTML for the website @welcome.html
```html
<!DOCTYPE html\>  
<html lang\="en"\>  
<head>  
 <meta charset\="UTF-8"\>  
 <title>Welcome</title>  
</head>  
<body>  
 <h1>Welcome to the Meeting Planner!</h1>  
 <p> This is my first every website built using django!  
        <em>Getting Started with Django</em>:  
        <a href\="https://bit.ly/JoshEom"\>My repository</a>  
 </p> <p> {{message}} <!-- This is use to create dynamic webpages. Check out views.py and see what the value of message is!"-->  
 </p>  
</body>  
</html>
```
views.py
```
...
def welcome(request):  
    return render(request, "website/welcome.html", {"message": "This data was sent from the view to the template."})
...
```

### Django Templates
```html
<html><head><title>{{name}}'s Page</title></head>
<body>
	<h1>Hi I'm {{name}}!</h1>
		I'm {{age}} years old.
</body></html>
```
- {{ var }} looks up var in the template context
- Other text is copied to HTML output, creating a dynamic HTML page
Calling a template
```python
def home(request):
	return render(request, "website/welcome.html",
		{ 'name':"Bob", 'age': 35 })
```
- render: pass request and name of template file
- Third argument: dict with data passed to the template
- Templates should be in folder /templates inside app
- Don't forget the return keyword

## 404 Error Page
Add get_object_or_404
@meetings/views.py
```python
from django.shortcuts import render, get\_object\_or\_404  
  
from .models import Meeting  
  
  
def detail(request, id):  
    meeting = get\_object\_or\_404(Meeting, pk\=id) \# Returns a 404 error page if it doesn't exist  
 return render(request, "meetings/detail.html", {"meeting": meeting})
```