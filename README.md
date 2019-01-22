#Sama Schools API

This application exposes the Sama schools API.

##For developer setup

Please follow the instructions below

`git clone https://github.com/xkmato/sama`

`cd sama` 

**Create Database**

`psql -U postgres -c "CREATE USER sama WITH PASSWORD 'sama';"`

`psql -U postgres -c "ALTER ROLE sama WITH SUPERUSER;"`

`psql -U sama postgres -c "CREATE DATABASE sama;"`

**Run Test**

`./manage.py test`

**Setup Application**

`./manage.py migrate`
`./manage.py runserver`

*Setup Test data(optional)*

`./manage.py load_schools_from_csv test_files/test_csv_data.csv`

##To deploy


