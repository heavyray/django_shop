### Installation
**1. Create a Folder where you want to save the project**

**2. Create a Virtual Environment and Activate**

Install Virtual Environment First
```
$  pip install virtualenv
```

Create Virtual Environment

For Windows
```
$  python -m venv venv
```
For Mac
```
$  python3 -m venv venv
```
For Linux
```
$  virtualenv .
```

Activate Virtual Environment

For Windows
```
$  source venv/scripts/activate
```

For Linux
```
$  source bin/activate
```

**3. Clone this project**
```
$  git clone https://github.com/heavyray/django_shop.git
```

Then, Enter the project
```
$  cd django_shop
```

**4. Install Requirements from 'requirements.txt'**
```python
$  pip3 install -r requirements.txt
```

**5. Create migrations files**

Command for Windows:
```python
$ python manage.py makemigrations
```

Command for Linux:
```python
$ python3 manage.py makemigrations
```

**6. Create database tables**

Command for Windows:
```python
$ python manage.py migrate
```

Command for Linux:
```python
$ python3 manage.py migrate
```

**7. Run the project**

Command for Windows:
```python
$ python manage.py runserver
```

Command for Linux:
```python
$ python3 manage.py runserver
```