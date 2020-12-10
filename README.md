# Hospital Automation Project

TABLE OF CONTENTS
-------------------
* Introduction
* Requirements
* Installation
* Deployment
* Configuration


INTRODUCTION
--------------
This project aims to cut the paperwork in hospitals and bring fluidity to hospital workflows.  
The scope of this project covers 4 user groups: _Doctor_, _Receptionist_, _Dispensary_ and _Test_. What all these four user groups will be dealing with is _patient_ data. Hence the object of our workflow are _patients_.

As a _receptionist_ I shall be able to:  
* Add new patient record.
* Send patient details to respective doctor(s).
* View all patient records.

As a _doctor_ I shall be able to:  
* Receive incoming patient details in realtime.
* Select a patient from the incoming list and open a descriptive view.
* Note diagnosis report for the patient.
* Prescribe medications to the respective patient(s).
* Send prescription of respective patient to the dispensary.

As a _dispensary_ clerk I shall be able to:  
* Receive incoming prescriptions for respective patient(s) in realtime.

As a _test_ incharge I shall be able to:  
* Receive incoming patient details in realtime.



REQUIREMENTS
-------------
Basic requirements to run this app are as follows:
* Python 3.6.6
* Django 2.1.1
* Django REST Framework 3.8.2
* Redis 2.10.6
* MySQL 14.14
* django-redis 4.9.0
* mysqlclient 1.3.13


INSTALLATION
-------------
The installation of this piece of software requires setting up a virtual environment, setting up a database, installing requirements and starting the server.

### Setting up virtual environment
1.  Install pip.
    ```bash
    sudo apt install python3-pip
    ```
2.  Install virtualenv using pip3.
    ```bash
    pip3 install virtualenv
    ```
3.  Create virtual environment.
    ```bash
    virtualenv -p python3 myvenv
    ```
4.  Activate your virtual environment.
    ```bash
    source myvenv/bin/activate
    ```
5.  To deactivate.
    ```bash
    deactivate
    ```

### Setting up database
1.  Create database while creating database select Collation as `utf8_unicode_ci`.
    ```sql
    mysql> CREATE DATABASE hospital_db;
    ```
2.  Create an account and grant it access to specific database.
    ```sql
    mysql> CREATE USER 'custom'@'localhost' IDENTIFIED BY 'password';
    mysql> GRANT SELECT, INSERT, UPDATE, DELETE, CREATE, DROP
        ->      ON hospital_db.*
        ->      TO 'custom'@'localhost';
    ```

### Clone project
```bash
git clone https://github.com/mayank2k16/hospital-automation.git
```

### Install requirements
1.  Activate virtual environment.
    ```bash
    source myvenv/bin/activate
    ```
2.  Change working directory to project directory.
    ```bash
    cd hospital-automation
    ```
3.  Install everything in requirements.txt using pip.
    ```bash
    pip install -r requirements.txt
    ```

Now before we start the server and start automating everything in the hospital we need to setup database_conf.py file in the project.
1.  Navigate to `major_project` directory.
    ```bash
    cd hospital-automation/major_project
    ```
2.  Create `database_conf.py` and enter database details.
    ```bash
    vim database_conf.py
    ```
    ```python
    DBNAME = 'hospital_db'
    DBUSER = 'custom'
    DBPASS = 'password'
    ```
3.  Save the file.



DEPLOYMENT
-----------
To start the server we just need to execute the following in a virtual environment:
```bash
$ python manage.py migrate
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, hospital_automation, sessions
Running migrations:
...
$ python manage.py runserver
Performing system checks...

System check identified no issues (0 silenced).
Django version 2.1.1, using settings 'major_project.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server using CONTROL-C.
```


CONFIGURATION
--------------
After successful deployment of server, you must create a superuser and add user groups to the database using the admin panel.
1.  ```bash
    $ python manage.py createsuperuser
    Username:
    Email address:
    Password:
    Password (again):   
    Super user created.
    ```
2.  Add 4 groups using the `Add Group` option under Groups table in the admin panel.
    ![Add Group](https://i.imgur.com/rlipW3N.png)
    ![User Groups](https://i.imgur.com/KebUT2j.png)
3.  Similarly, add users (receptionist/doctor/dispensary/test) using the same procedure but under Users table in the admin panel.
