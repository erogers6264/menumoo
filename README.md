# MenuMoo
For this project I used the Flask web framework to build an application
to manage and view the menus of various restaurants. It connects to a database
via SQLAlchemy, and can perform CRUD operations using WTForms for users
to interact with the application.

It implements basic user authentication utilizing OAuth 2.0 through a
Google+ and Facebook sign-in. In addition, there is a local permission
system in place to prevent users from editing each others' entries.

## Table of contents
* Usage
* Bugs and feature requests
* Creators
* Copyright & License

## Usage
If you use vagrant, the pg_config.sh will provision the development environment
for you.

```shell
vagrant up && vagrant ssh
cd /vagrant
```

Set up the sqlite database by calling the `create_all()` method from a python
shell in the app root directory.

```python
from menumoo import db
db.create_all()
```

Running `python runserver.py` from within a vagrant virtual environment
will allow you to interface with the application via localhost:5000 in
your browser.

```
python runserver.py
```

Make sure you obtain your own client secret from Google and Facebook if you
are to use the OAuth authentication features. The app will look at the current
working directory for `client_secrets.json` (Google) and `fb_client_secrets.json`
(Facebook).

## Bugs and feature requests
Have a bug or a feature request? Please e-mail me at erogers6264@gmail.com
or fork and implement yourself! Pull requests welcome.

## Creators
Ethan Rogers, Udacity

## Copyright & license
This work is licensed under the Creative Commons Attribution 4.0 International
License. To view a copy of this license, visit http://creativecommons.org/licenses/by/4.0/.
