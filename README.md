# Flask REST API template
## What Is This Template?
This template is the base configuration of the RESTful Flask services we deploy as part of the Asgard System Stack.

The API itself is written in Python (V3), using the Flask web microframework and its RESTful extension. The service was designed as a scalable microservice, providing reusable functionality within the system stack.

<br>

---

## Repository Structure
UNDER CONSTRUCTION

<br>

---

## Dependencies
The template uses the pip3 package manager and is written using Python3.

The following packages are used in the project:

### API - Flask - 1.0.3
Flask is the web microframework the application was developed to use as its core. It supplies all the main functionality and networking.

### API - Flask-RESTful - 0.3.7
Flask-RESTful is an extension to the Flask framework allowing for the easy configuration of REST architecture APIs. This handles our endpoint definition and opening the application up to the different query verb types.

### API - mysqlclient - 1.4.6
MySQL client is required for SQLAlchemy to interact with MySQL databases.

### API - Flask-SQLAlchemy - 2.4.0
Flask-SQLAlchemy is a Flask wrapper for the Object-Relational Mapper, SQLAlchemy. SQLAlchemy provides the toolset we use to interact with the MySQL database used by the API and provide a layer of security between the API and the raw data itself.

### API - Flask-Jsonpify - 1.5.0
Jsonify is our json parser, this package is what converts our result data from the database into the JSON responses we reply to our connected clients.

### API - Flask-Cors - 3.0.8
Flask-Cors is an extension package for routing and managing Cross-Origin Resource Sharing (CORS) across the application, and is mainly used to allow our web client to interact with the API itself.

### API - Webargs - 5.3.2
Webargs handles the parameter parsing from the endpoint URLs to usable data within our Flask resource objects, this library replaces the now depreciated "reqparse" from Flask-RESTful.

### API - Marshmellow - 3.0.1
Marshmellow is a dependency of Webargs, we had to freeze this at this version due to something on their end stopping working correctly.

### API - Nose2 - 0.9.1
Nose2 is an extension of the Python Unittest module, we use this as part of our unit, feature and integration testing. The project is set to export the results of these tests as JUnit XML files.

<br>

---

## Commands
### Pip3
Batch Install the Pip3 modules at their frozen version by the following commands whilst in the projects root directory.
```pip3
pip3 install -r api/requirements.txt
```
