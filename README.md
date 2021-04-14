# resize_app_django

## Installation for Windows cmd
Clone the repository to your directory:
```
git clone https://github.com/cruelflanky/resize_app_django.git
```
Go to the directory and activate virtualenv:
```
cd resize_app_django
.\env\Scripts\activate
```
Then you have to runserver for the first time and migrate all migrations:
```
cd myproject
py manage.py runserver
py manage.py migrate
```
Now u can runserver and use app:
```
py manage.py runserver
