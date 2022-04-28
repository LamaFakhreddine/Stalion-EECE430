# Stalion-EECE430
This project is the website developed for Stallion Sports Club. 

Note that for this project, we are using Django 4.0 and pyhton versions 3.6 and later. 

--How to Run--

1- Create a virtual python environment for this project, within the project directory, by executing the
following terminal command while within the project directory:

Unix:
python3 -m venv venv

Windows:
py -3 -m venv venv

2- Activate the newly created python environment within your terminal. Upon doing so, the terminal
should indicate that you are running within the specified virtual environment:

  Unix:
  . venv/bin/activate
  
  Windows:
  venv\Scripts\activate
 
3- After activating the virutual environment, install the project dependencies using the following command: 

pip install -r requirements.txt

4- navigate to stallion_app via:

cd stallion_app

5- Create a django admin account (with username=admin and passsword=admin) :

python manage.py createsuperuser

6. Make migrations and run the app 

python manage.py makemigrations --> to make model migrations (if necessary) 
python manage.py migrate        --> to apply migrations
python manage.py runserver      --> to run the server on localhost:8000



