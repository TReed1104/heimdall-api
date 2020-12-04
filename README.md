# Heimdall
## What is Heimdall?
Heimdall is a remote monitoring application used for monitoring the School of Computer Science's computing labs at The University of Lincoln. Heimdall's back-end is written in Python (version 3), using the Flask web microframework and its RESTful extension.

The application was designed as a scalable microservice, providing reusable functionality within our internal system stack - Asgard.

Heimdall takes its name from Norse mythology, where Heimdall is the watchmen of the gods watching over the realm of Asgard.

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
Nose2 is an extension of the Python Unit-test module, we use this as part of our unit, feature and integration testing. The project is set to export the results of these tests as JUnit XML files.

<br>

---

## Commands
### Pip3
Batch Install the Pip3 modules at their frozen version by the following commands whilst in the projects root directory.
```pip3
pip3 install -r api/requirements.txt
```

<br>

---

## Testing
Under Construction

<br>

---

## Installation
Under Construction

<br>

---

## Usage Guide - API Interactions and Endpoints
### Exposed Endpoints
Valid Endpoints
```
<server_address>/heimdall-api/computers
<server_address>/heimdall-api/desks
<server_address>/heimdall-api/rooms
<server_address>/heimdall-api/availability
<server_address>/heimdall-api/computer_handler
<server_address>/heimdall-api/desk_handler
<server_address>/heimdall-api/room_handler
```

Example Endpoints
```
10.5.11.173/heimdall-api/computers
10.5.11.173/heimdall-api/desks
10.5.11.173/heimdall-api/rooms
10.5.11.173/heimdall-api/availability
10.5.11.173/heimdall-api/computer_handler
10.5.11.173/heimdall-api/desk_handler
10.5.11.173/heimdall-api/room_handler
```

### Endpoint - Computer List
Usage:
```
<server_address>/heimdall-api/computers

Supported HTTP Methods
* GET
```

params:
```
room - String name of the room to list the computers from
```

#### GET method
The GET method for the Computer list endpoint returns a JSON array listing the computers registered with Heimdall.

Usage:
```
GET -> <server_address>/heimdall-api/computers
GET -> <server_address>/heimdall-api/computers?room=Lab_A
```

Example Response:
```JSON
{
    "meta":{},
    "links":{
        "self": "http://heimdall-api/computers"
    },
    "data": {
        "computers":[
            {
                "id": 1,
                "desk": "A1",
                "mac_address": "A1:B2:C3:D4:E5:F6",
                "machine_name": "Computer Name",
                "os_name": "Windows",
                "room": "Lab_A",
                "status": "On",
                "updated_at": "Wed, 18 Dec 2019 00:57:14 GMT"
            }
        ]
    }
}
```

### Endpoint - Desk List
Usage:
```
<server_address>/heimdall-api/desks

Supported HTTP Methods
* GET
```

params:
```
room_id - The Integer ID of the room to list the desks from
room_name - String name of the room to list the desks from (room_id takes priority if supplied)
```

#### GET method
The GET method for the Desk list endpoint returns a JSON array, listing the desks within a given room.

Usage:
```
GET -> <server_address>/heimdall-api/desks
GET -> <server_address>/heimdall-api/desks?room_name=Lab_A
GET -> <server_address>/heimdall-api/desks?room_id=1
```

Example Response:
```JSON
{
    "meta": {},
    "links": {
        "self": "http://heimdall-api/desks?room_id=1"
    },
    "data": {
        "desks": [
            {
                "id": 1,
                "desk_id": "A1",
                "number_of_computers": 0,
                "room": "Lab_A",
                "computers":[]
            },
            {
                "id": 2,
                "desk_id": "A2",
                "number_of_computers": 1,
                "room": "Lab_A",
                "computers":[
                    {
                        "id": 1,
                        "mac_address": "A1:B2:C3:D4:E5:F6",
                        "machine_name": "Computer Name",
                        "os_name": "Linux",
                        "room": "Lab_A",
                        "desk": "A2",
                        "status": "On",
                        "updated_at": "Wed, 16 Dec 2019 01:57:14 GMT"
                    }
                ]
            }
        ]
    }
}
```

### Endpoint - Room List
Usage:
```
<server_address>/heimdall-api/rooms

Supported HTTP Methods
* GET
```

#### GET method
The GET method for the Room list endpoint returns a JSON array, listing each room registered with the system.

Usage:
```
GET -> <server_address>/heimdall-api/rooms
```

Example Response:
```JSON
{
    "meta": {},
    "links": {
        "self": "http://heimdall-api/rooms"
    },
    "data":{
        "rooms":[
            {
                "id": 1,
                "has_availability_map": true,
                "capacity": 15,
                "number_of_computers": 2,
                "number_of_desks": 10,
                "name": "Lab_A",
                "subnets": "192.168.0"
            }
        ]
    }
}
```

### Endpoint - Availability List
Usage:
```
<server_address>/heimdall-api/availability

Supported HTTP Methods
* GET
```

params:
```
room - The string name of the room to filter the results for
```

#### GET method
The GET method for the Availability list endpoint returns a JSON array listing the current availability status of the computers registered with Heimdall.

Usage:
```
GET -> <server_address>/heimdall-api/availability?room=Lab_A
```

Example Response:
```JSON
{
    "meta":{},
    "links":{
        "self": "http://heimdall-api/availability?room=Lab_A"
    },
    "data": {
        "availability": [
            {
                "availability_status": "Available",
                "desk": "A2",
                "id": 1,
                "mac_address": "A1:B2:C3:D4:E5:F6",
                "machine_name": "Computer Name",
            }
        ]
    }
}
```

### Endpoint - Room Handler
Usage:
```
<server_address>/heimdall-api/room_handler

Supported HTTP Methods
* GET
* POST
* PUT
* DELETE
```

params:

GET
```
id - The integer id of the room to get
```

POST
```
room - The string name of the room to create
subnets - The CSV string of the subnets the room contains
capacity - The integer value of the teaching capacity of the room
has_availability_map - A boolean storing if the room has enabled for the availability system
```

PUT
```
id - The integer id of the room to update
subnets - The new subnets CSV string to write to the room instance (optional)
capacity - The new capacity integer to write to the room instance (optional)
has_availability_map - The new state of the rooms compatitibility with the availability system (optional)
```

DELETE
```
id - The integer id of the room to delete
```

#### GET method
The GET method for the room_handler endpoint returns a JSON object representing a serialised version of the room.

Usage:
```
GET -> <server_address>/heimdall-api/room_handler?id=1
```

Response Codes:
```
200 - Ok
404 - Room not found
422 - Invalid Parameters
```

Example Response:
```JSON
{
    "meta":{},
    "links":{
        "self": "http://heimdall-api:5000/room_handler?id=1"
    },
    "data":{
        "room":{
            "id": 1,
            "has_availability_map": true,
            "capacity": 15,
            "number_of_computers": 2,
            "number_of_desks": 10,
            "name": "Lab_A",
            "subnets": "192.168.0"
        }
    }
}
```

#### POST method
The POST method for the room_handler endpoint allows the creation of a new room.

Usage:
```
POST -> <server_address>/heimdall-api/room_handler
```

Response Codes:
```
201 - Created
405 - A Room already exists with the supplied name
422 - Invalid Parameters
422 - Invalid Subnets
```

Example Request Body:
```JSON
{
    "name": "Lab_A",
    "capacity": 15,
    "subnets": "192.168.0",
    "has_availability_map": true
}
```

#### PUT method
The PUT method for the room_handler endpoint allows for changes to be made to a room's data.

Usage:
```
PUT -> <server_address>/heimdall-api/room_handler
```

Response Codes:
```
202 - Accepteds
405 - Room does not exist
422 - Invalid Parameters
```

Example Request Body:
```JSON
{
    "id": "1",
    "capacity": 25,
    "subnets": "192.168.1",
    "has_availability_map": false
}
```

#### DELETE method
The DELETE method for the room_handler endpoint allows for the deletion of a specified Room.

Usage:
```
DELETE -> <server_address>/heimdall-api/room_handler?id=1
```

Response Codes:
```
202 - Success
404 - Room not found
422 - Invalid Parameters
```

### Endpoint - Desk Handler
Usage:
```
<server_address>/heimdall-api/desk_handler

Supported HTTP Methods
* GET
* POST
* PUT
* DELETE
```

params:

GET
```
id - The integer id of the desk to get the details of
```

POST
```
desk - The string name of the desk to create, this needs to be unique
room - The string name of the room to attach the new desk to
```

PUT
```
id - The integer id of the desk to Update
new_room - The string name of the new room to attach the specified desk to
```

DELETE
```
id - The integer id of the desk to delete
```

#### GET method
The GET method for the desk_handler endpoint returns a JSON object representing a serialised version of the requested desk.

Usage:
```
GET -> <server_address>/heimdall-api/desk_handler?id=1
```

Response Codes:
```
200 - Ok
404 - Desk not found
422 - Invalid Parameters
```

Example Response:
```JSON
{
    "meta": {},
    "links": {
        "self": "http://heimdall-api:5000/desk_handler?id=1"
    },
    "data": {
        "desk": {
            "computers":[],
            "id": 1,
            "name": "A1",
            "number_of_computers": 0,
            "room": "Lab_A"
        }
    }
}
```

#### POST method
The POST method for the desk_handler endpoint allows the creation of a new desk.

Usage:
```
POST -> <server_address>/heimdall-api/desk_handler
```

Response Codes:
```
201 - Created
405 - A Desk already exists with the supplied name
422 - Invalid Parameters
404 - Room not found
```

Example Request Body:
```JSON
{
    "desk": "1B",
    "room": "Lab_A"
}
```

#### PUT method
The PUT method for the desk_handler endpoint allows for changes to be made to a desk's data.

Usage:
```
PUT -> <server_address>/heimdall-api/desk_handler
```

Response Codes:
```
202 - Success
422 - Invalid Parameters
422 - The new room already contains a desk of that name
405 - A Desk already exists with the supplied name
404 - Desk does not exist
404 - New Room does not exist
```

Example Request Body:
```JSON
{
    "id": 2,
    "new_room": "Lab_B"
}
```

#### DELETE method
The DELETE method for the desk_handler endpoint allows for the deletion of a desk.

Usage:
```
DELETE -> <server_address>/heimdall-api/desk_handler?id=1
```

Response Codes:
```
202 - Success
404 - Desk not found
422 - Invalid Parameters
```

### Endpoint - Computer Handler
Usage:
```
<server_address>/heimdall-api/computer_handler

Supported HTTP Methods
* GET
* POST
* PUT
* DELETE
```

params:

GET
```
id - The integer id of the computer to get the details of
```

POST
```
mac_address - The string value of the unique MAC address of the machine to be created
machine_name - The hostname of the machine
ip_address - The IP address of the machine
os_name - The name of the operating system of the machine
os_release - The version of the Operating system the machine is running
os_build - The build number of the version of the Operating system the machine is running
room - The string name of the room the machine is located in (optional, but MUST be used with the desk parameter)
desk - The string name of the desk the machine is assigned to (optional, but MUST be used with the room parameter)
```

PUT
```
mac_address - The string value of the unique MAC address of the machine to be created
machine_name - The hostname of the machine (optional)
ip_address - The IP address of the machine (optional)
os_name - The name of the operating system of the machine (optional)
os_release - The version of the Operating system the machine is running (optional)
os_build - The build number of the version of the Operating system the machine is running (optional)
room - The string name of the room the machine is located in (optional, but MUST be used with the desk parameter)
desk - The string name of the desk the machine is assigned to (optional, but MUST be used with the room parameter)
```

DELETE
```
id - The integer id of the computer to delete
```

#### GET method
The GET method for the computer_handler endpoint returns a JSON object representing a serialised version of the requested computer registered with Heimdall.

Usage:
```
GET -> <server_address>/heimdall-api/computer_handler?id=1
```

Response Codes:
```
200 - Ok
404 - Computer not found
422 - Invalid Parameters
```

Example Response:
```JSON
{
    "meta": {},
    "links": {
        "self": "http://heimdall-api:5000/computer_handler?id=1"
    },
    "data": {
        "computer": {
            "desk": "A2",
            "id": 1,
            "ip_address": "192.168.1.12",
            "mac_address": "A1:B2:C3:D4:E5:F6",
            "machine_name": "Computer Name",
            "os_build": "#1145 SMP Fri Sep 21 15:38:35 BST 2018",
            "os_name": "Linux",
            "os_release": "4.14.71-v7+",
            "room": "Lab_A",
            "status": "On",
            "updated_at": "Mon, 27 Jan 2020 09:40:03 GMT"
        }
    }
}
```

#### POST method
The POST method for the computer_handler endpoint allows the creation of a new computer.

Usage:
```
POST -> <server_address>/heimdall-api/computer_handler
```

Response Codes:
```
201 - Created
405 - The supplied Computer already exists.
422 - Invalid Parameters
422 - Invalid Parameters, Desk and Room are mutually dependant and cannot be used individually
404 - Room not found
404 - Desk not found
```

Example Request Body (No Room/Desk - Basic Creation):
```JSON
{
    "mac_address": "A1:B2:C3:D4:E5:F6",
    "machine_name": "Computer Name",
    "ip_address": "192.168.1.12",
    "os_name": "Linux",
    "os_release": "4.14.71-v7+",
    "os_build": "#1145 SMP Fri Sep 21 15:38:35 BST 2018",
}
```

Example Request Body (Room & Desk Supplied - Basic Creation And Desk Assignment):
```JSON
{
    "mac_address": "A1:B2:C3:D4:E5:F6",
    "machine_name": "Computer Name",
    "ip_address": "192.168.1.12",
    "os_name": "Linux",
    "os_release": "4.14.71-v7+",
    "os_build": "#1145 SMP Fri Sep 21 15:38:35 BST 2018",
    "room": "Lab_A",
    "desk": "A2"
}
```

#### PUT method
The PUT method for the computer_handler endpoint allows the changes to be made to a computer's data.

Usage:
```
PUT -> <server_address>/heimdall-api/computer_handler
```

Response Codes:
```
202 - Accepted
405 - The supplied Computer does not exist.
422 - Invalid Parameters
422 - Invalid Parameters, Desk and Room are mutually dependant and cannot be used individually
404 - Room not found
404 - Desk not found
```

Example Request Body (No Room/Desk - Basic Creation):
```JSON
{
    "mac_address": "A1:B2:C3:D4:E5:F6",
    "machine_name": "Computer Name",
    "ip_address": "192.168.1.12",
    "os_name": "Linux",
    "os_release": "4.14.71-v7+",
    "os_build": "#1145 SMP Fri Sep 21 15:38:35 BST 2018",
    "room": "Lab_A",
    "desk": "A2"
}
```

Example Request Body (Room & Desk Supplied - Desk Assignment):
```JSON
{
    "mac_address": "A1:B2:C3:D4:E5:F6",
    "room": "Lab_A",
    "desk": "A2"
}
```

#### DELETE method
The DELETE method for the computer_handler endpoint allows for the deletion of a specified Computer registered with the Heimdall.

Usage:
```
DELETE -> <server_address>/heimdall-api/computer_handler?id=1
```

Response Codes:
```
202 - Success
404 - Computer not found
422 - Invalid Parameters
```
