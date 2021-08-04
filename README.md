# COVID TRACKER
#### Video Demo:  https://www.youtube.com/channel/UC_c2eMREqXYhiACQr8Tkisg
#### Description:
Covid Tracker is a web app which keep track of Covid-19 data in the world and the data about vaccination against Corona Virus. The app is structured in two part: pubblic areas provides global data and data by Country, meanwhile the private ones it is a space where every user can follow their favorite Countries.

#### Architecture:
Covid Tracker follow the MVC model and it is based on Flask.
In the home directory it has the following files:

* .gitignore: Contain files not shared in git.
* app.py: it is the app's controller. It contain route, configuration and back end's logic.
* covid_cache.sqlite: It is a database where the app caches data obtain from API.
* covidtracker.db: It is the database where app store users and Covid datas stored from users.
* form.py: In this file there are all form in use.
* helpers.py: In this file there are a collection of funcions: decorate routes, a Jinja custom filter, the management and caching of request to API, and the management of data for database.   
* models.py: This file includes database models.
* LICENSE: Include terms of GNU GPL 3.0 license.
* Pipfile and Pipfile.lock: Those two file contains information for virtual enviroment.
* README.md: It is the documentation file.
* requirements.txt: It contains all dependences for Flask.

In the /static directory are stored all static files:
* /static/css/styles.css: This is the stylesheet for the entire app
* /static/favicon/virus-solid.png and /static/favicon/virus-solid.svg: Those two files are the favicon.
* /static/js/navbar.js: This file contain a front end feature of navbar: changing navigation menu between desktop and mobile.
* /static/js/tables.js: This file contain the sort algorithm for tables

In the /templates folders are stored HTML views:
* /templates/add_country_cases.html: HTML page for searching and adding to dashboard a specific Country data about Covid-19 cases.
* /templates/add_country_vaccination.html: HTML page for searching and adding to dashboard a specific Country data about vaccinations against Covid-19.
* /templates/by_country.html: HTML page for render a table of all Covid-19 cases data by Country.
* /templates/dashboard.html: HTML page where user can access its favorite datas.
* /templates/index.html: HTML page for homepage where Global data are shown.
* /templates/layout.html: Boilerplate HTML.
* /templates/login.html: HTML page for login.
* /templates/register.html: HTML page for registration.
* /templates/vaccination.html: HTML page for render data about vaccination against Covid-19 divided by Country. 
* /templates/includes/_formrender.html: Macro for render forms.
* /templates/includes/_messages.html: Render flash message.
* /templates/includes/_navbar.html: This (partial) HTML file include navigation bar's rendering. 

#### Design:
For back end, the idea is to create a secure, mainteinable and scalable application. About security we rely on some Flask library to manage and process users input and on built-in feature on Flask and Jinja. In the database users password are encrypted.
For back end the app is built with the following technologies: 

* Python.
* Flask - web framework.
* SQLite - database.
* Jinja2 - template. 
* Flask WTF form - Form handler / Form validation.
* flask-sqlalchemy - ORM.
* Flask-Session - manage session.
* requests - manage http requests.
* requests_cache - cache requests for 10 minutes.

For front end, the idea is to focus on a responsive and accessible application. Font and color palette choises are based on readability and many app feature are about responsivness. 

For front end the app is built with the following technologies: 
* HTML 
* CSS 
* JavaScript
* Font Awesome Icon
##### API:
Data are retrived from Covid-19 API.
API base:
https://covid-api.mmediagroup.fr/v1