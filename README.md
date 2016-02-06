# MenuMoo
For this project I am using the Flask web framework to build an application
to manage and view the menus of various restaurants. It connects to a database
via SQLAlchemy, and can perform basic CRUD operations using WTForms for users 
to interact with the application.

It will implement basic user authentication utilizing OAuth 2.0 through a
Google+ and Facebook sign-in.

# Usage
If you use vagrant, the pg_config.sh will provision the development environment
for you. See the file for requirements needed to run on a local rather than
virtual machine.

Running `python runserver.py` from within a vagrant virtual environment
will allow you to interface with the application via localhost in your browser.