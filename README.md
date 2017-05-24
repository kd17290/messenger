Messenger
--------------
Prerequisites 

 1. Python 3.x
 2. Virtualenv

How to setup / run

 1. Create virtualenv : `virtualenv venv -p python3.6`
 2. Install depedencies : `pip install -r requirements.pip`
 3. Create superuser : `python manage.py createsuperuser`
 4. Runserver : `python manage.py runserver`

Usage

 1. For API structures, refer to postman collection : `https://www.getpostman.com/collections/70284787a42f2df57ec6`
 2. Create sample users using Django admin, located at `http://127.0.0.1:8000/admin/`
 3. To view messages for any given user (pushed through websocket) : go to `http://127.0.0.1:8000/updates/<user-id>/` , i.e. on page `http://127.0.0.1:8000/updates/1/`, you'll be able to see messages being sent to user with id 1
