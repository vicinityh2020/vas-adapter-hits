# VAS Adapter HITS

Adapter used to connect the Value-Added Services and expose them to the VICINITY neighborhood.

## Prerequisites

Before running this adapter, ensure that you have the following in place:

- Python 3.6.5+ 
    ###### Ubuntu 14.04 and 16.04: <br>
    `$ sudo add-apt-repository ppa:deadsnakes/ppa`<br>
    `$ sudo apt-get update`<br>
    `$ sudo apt-get install python3.6`<br> 
    ###### Ubuntu 17.10
    comes with a pre-installed 3.6, use `python3` to invoke it
    ###### Windows 10
    Download binary from: https://www.python.org/downloads/ <br>
    Make sure to update your Environment Variables

- PostgreSQL 9.6+
    ###### Ubuntu 17.04 - 17.10
    `$ sudo apt-get install postgresql-9.6` <br>
    
- RabbitMQ server for message passing between the worker and the adapter
    ###### Ubuntu 14.04+
    `$ sudo apt-get install rabbitmq-server`
    

- Configured and working [VICINITY Client Node](https://github.com/vicinityh2020/vicinity-agent#vicinity-client-node)

## Installation
1. Clone this repository using `git clone` <br>

2. Inside the project directory run `pip install -r requirements.txt` to install the necessary requirements

3. Update your database connection settings in `vas-adapter-hits/vas_adapter/settings.py`

```djangotemplate
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': '',
        'USER': '',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

```

Inside the project directory run <br>
`$ python manage.py makemigrations`<br>
`$ python manage.py migrate`<br>

## Run

Run the adapter on a port of your choice 

`$ python manage.py runserver <your_host>:<your_port>`

Example:

`$ python manage.py runserver 127.0.0.1:9000`

## Celery worker

Celery worker (make sure rabbit-mq server is up and running on your machine)<br>
    `$ celery -A proj worker` to execute tasks<br>
    `$ celery -A proj beat` to schedule tasks
    
## Admin Page
In order to access the admin page, you must first create an admin user by `python manage.py createsuperuser`, then fill out the username and password (feel free to leave other fields blank).

You may then access the page at `http://<your_host>:<your_port>/admin`

## Database data

1. Log in to your admin page

###### Adding a parking lot

1. Under the **API** table, click **Add** next to "Parking Lots"
2. Fill out the parking lot information

###### Adding a parking space

1. Under the **API** table, click **Add** next to "Parking Spaces"
2. Fill out the sensor information. Make sure that the sensor is

###### Adding a parking reservation

1. Under the **API** table, click **Add** next to "Parking Reservations"
2. Fill out the reservation information



