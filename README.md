[![Build Status](https://travis-ci.org/xkmato/sama.svg?branch=master)](https://travis-ci.org/xkmato/sama)

# Sama Schools API

This application exposes the Sama schools API.

## For developer setup

Please follow the instructions below

```
git clone https://github.com/xkmato/sama
cd sama
mv sama/settings.py.dev sama/settings.py #replace heroku settings
pip install pipenv
pipenv install
```

**Create Database**

```
psql -U postgres -c "CREATE USER sama WITH PASSWORD 'sama';"

psql -U postgres -c "ALTER ROLE sama WITH SUPERUSER;"

psql -U sama postgres -c "CREATE DATABASE sama;"
```

**Run Test**

```
./manage.py test
```

**Setup Application**

```
./manage.py migrate
./manage.py runserver
```

*Setup Test data(optional)*

`./manage.py load_schools_from_csv test_files/test_csv_data.csv`

*Create superuser(optional)*

```
./manage.py createsuperuser
#Signin user at /rest-auth/login
#Access full API documentation at /
```

### Creating the machine

Type this command from the `ansible` directory:

```
vagrant up
```

(To use Docker instead of VirtualBox, add the flag `--provider=docker` to the
command above. Note that extra configuration may be required first on your host
for Docker to run systemd in a container.)

Wait a few minutes for the magic to happen. Access the app by going to this
URL: [https://sama-school-app.local](https://sama-school-app.local)

### Provision Staging server

Type this command from the `ansible` directory:

```
ansible-playbook -i stage site.yml --tags="deploy"
```



