# BriteCore-Engineering-Application
This is a feature request web application, A feature request is usually initiated by a customer to add a new feature or fix an issue with an existing piece of software. Assume that the user is an employee at IWS who would be entering this information after having some correspondence with the client that is requesting the feature
# Getting Started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.
# Prerequisites
These are the environmental variables you need to have in order to get this project up and running

    OS: Ubuntu
    Server Side Scripting:Python 3.6+
    Server Framework: Flask
    ORM: Sql-Alchemy
    
#Installing
These are what you need to know to install this project 
 
    set up a virtual environment 
    clone this repository
To install all the dependencies run
 
    pip install -r requirements.txt
Once dependencies are installed migrate database with

    flask db migrate 
    flask db upgrade
    
Then run flask app

    python run.py 
 This gets your project started and you can view it at 
  
     127.0.0.1:5000
  
# Solving the problem
if a staff logs a request with a client priority already existing, i increment every request from that priority number and above so my new request can use the priority logged by the staff. this way there cannot be two request with same priority number.since the priority is directly proportional to number of requests then if a user types in a priority above the current number of request in the system, the request priority will be the number of total requests + 1.

# Running unit tests
run tests by using this command at the projects root directory

    python -m unittest tests/Test_app.py
    
    
# Deployment and Tools
The project was built using 
Aws- Hosting Service
Gunicorn - Python WSGI HTTP Server for UNIX
Nginx - web server
Flask - python web framework 
Vue.js - javascript framework
jquery - javascript framework

# Live demo 

http://52.15.87.199
    
    
    
