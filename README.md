# **Full Stack Test - Backend**

## A project repository for applications of Take home project.

### Table of Contents
- Installation
- Usage
- Features
- Configuration
- License
- Contact

### Python Version
- 3.10.11

### Database 
- We are using MongoDB Atlas for connection.
    - go to `https://cloud.mongodb.com/` and login with credential.
    - Create Atlas link to connect with database.
    - One can refer .env.sample for any variable help.

## Migrations
- To apply migrations:
    - write `python manage.py migrate` in same directory where your `manage.py` is located.  
    
### Installation
Follow these steps to set up the project:
1. ### Clone the repository
-   
-   cd Backend
2. ### Create a virtual environment
    1. ### Using Pipenv
        -   #### First create pipenv by:
            - pip install pipenv
        -   #### Then activate virtual environment by:
            - pipenv shell

    2. ### Alternatively you can opt for venv also, To Do:   
        -   #### Create Virtual Environment:
            - python -m venv venv
        -   #### Activate the virtual environment
            -   cd venv
            -   cd Scripts
            -   activate
            -   cd ../..    
3. ### Install all dependencies
    -   pip install -r requirements.txt


## Usage
To start the project
- go to root folder
- write python manage.py runserver this will run project in default port.


## Features
-    Backend operation of Take home project
-    MongoDB database for all backend data handling
-    Pre-configured environment for quick setup


## Configuration
Ensure that your environment is properly set up by following the installation steps. Configuration details and additional settings can be managed in the configuration files included in the repository.


## Contact
For any inquiries or issues, please contact:

- Email : 
- GitHub:
