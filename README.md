Django project for news site backend
======================
name = "news-site-backend"\
version = "0.1.0"\
authors = ["Anastasia Sypkova <a.sypkova@tg.dunice.net>"]\
\
python = "^3.12"\
django = "^5.0.6"\
djangorestframework = "^3.15.1"

Setup instractions
=======================
Prerequisits\
```pip install poetry```

Install dependences from poetry.lock:\
```make install```

Run server\
```make run-server```

Create migration\
```make migrate```

Apply migrations\
```make makemigrations```

Start application\
```make startapp name="application_name" ```
