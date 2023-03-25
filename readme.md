## M56studios BE

## Installation
```
Tested on python 3.7
pip install -r requirements.txt
```

## Environment Variable configuration 
- Django App Setting (Used to add configuration to run django app, filename should be settings.env)
```
ALLOWD_HOST=*(all) or some_ip_address or domain
DEBUG=True/False
```
- MYSQL Database (Used for managing visitors email and generated passcode, filename should be mysqldb.env)
```
NAME=m56studios_db
USER=root
PASSWORD=12345678
HOST=127.0.0.1
PORT=3306
```
- SendGrid (Used for sending mails to visitors, filename should be sendgrid.env)
```
SENDGRID_API_KEY=SG.arQMDPB!@%&_QRCBk0v6.Zg6HCAu-NqeuDlRHSjU7ncohGkw
FROM_EMAIL="hello@maguresoftwares.com"
CC_EMAIL="xyz@maguresoftwares.com"
```
Note - The above mentioned credentials are example, please add actual values in the same way if working on windows operating system(All the env variable should be created inside env dir at root) otherwise use export keyword to set the same environment variables.

## How to run?

- To make database migration use the following command `python manage.py makemigrations`.

- To migrate the database changes use the following command `python manage.py migrate`.

- Navigate to root directory and run `python manage.py runserver`.

## Using background task

- Create a new docker container