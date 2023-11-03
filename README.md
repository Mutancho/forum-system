# Forum System

## Name
Forum System

## Description
Forum System is an intuitive and robust Python-based backend application that powers online forum services. Developed with FastAPI and SQL (MariaDB), it offers a comprehensive suite of features that allows users to create topics, post replies, and engage in dynamic discussions. It also includes advanced administrative capabilities such as locking/unlocking topics, setting the best replies, and managing user roles and categories. Secure user registration and authentication are facilitated through JWT. With its blend of technology and user-centric design, Forum System is equipped to deliver a seamless and engaging online forum experience.

## Installation
List Of Technologies:
Python
FastAPI
SQL (MariaDB)
Pydantic
JWT for authentication

To install required modules use "pip install –r requirements.txt" in ternimal.

## Visuals
MariaDB relational database diagram:
![Alt text](/images/database_diagram.jpg)


## Usage
In terminal use the command "uvicorn main:app --reload" to load up the application.

The HTTP endpoints are listed in http://127.0.0.1:8000/docs 

Refer to docstrings and typehints if you have questions regarding certain functionality.

To run the project first include a .env in config folder with the following parameters:

DATABASE_HOSTNAME
DATABASE_PORT
DATABASE_PASSWORD
DATABASE_NAME
DATABASE_USERNAME 
SECRET_KEY
ALGORITHM= eg. "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES="enter integer for minutes"

Navigate to the root folder and create a file named `mariadb.env`. This file will hold environment variables specific to your MariaDB container setup:
- `MYSQL_ROOT_PASSWORD`: The password for the root user of your MariaDB instance. Ensure this is a strong, unique password.
- `MYSQL_DATABASE`: The name of the database that MariaDB will initially create upon container startup. This should ideally match the `DATABASE_NAME` from the `.env` file in the `backend/config` directory.

When you provide an authorization token go to the authorisation tab in postman and there you should select bearer token, enclosed in quotation marks. 


## Roadmap
If you have ideas for releases in the future, it is a good idea to list them in the README.


## Authors and acknowledgment
We want to thank our lecturers and colleagues at Telerik Academy for the continous support throughtout the integration of the project. 

## License
Telerik Academy

