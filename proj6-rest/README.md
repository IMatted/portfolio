# Project 6: Brevet Calculator, Powered by MongoDB With a RestAPI
Author: Danish Singh

Contact: danishs@uoregon.edu

Course: CS 322

## Project Description:
This project is designed to calculate the opening and closing times for a Brevet race based on distinct control points entered by the user.
It makes use of a Flask frontend and an AJAX backend to dynamically update the web-app. On the web app, a submit button allows you to submit control points, opening times, and closing times to a database powered by MongoDB, beside the submit button is the display button which fetches the submitted entries to the database and displays them in a separate webpage. Once data is stored in the database, it is retrieved to be used on the consumer service side, which makes use of a RestAPI for a consumer service, allowing the user to view open and close times in the form of a webpage, json, and csv format.

---

## The Algorithm:
[Project 4]: To understand the algorithm, an essential to understand the concept of control points. 
Control points are points that split up a race, (i.e., A 200km race could be split into controls of 50km, 100km, 150km, 200km) a participant must pass through these points to obtain proof of passage. 
Building off of this, control times are the minimum and maximum times by which the rider must arrive at the location. 

The algorithm for calculating the control times is based from the offical RUSA website (https://rusa.org/pages/acp-brevet-control-times-calculator)
> The opening time calculation is done by first finding the total distance of one control point to another, for example 125km to 200km would be 75km, we call this a "section"
>
> Next, it takes the section and divides it by the max speed to get its final result. (The maximum speed is obtained through the offical RUSA website)

> The closing time calculation is done by finding the total distance of one control point to another, just like the opening function, we call this a "section"
>
> Next, it takes the section and divides it by the minimum speed to get its final result. (The minimum speed is obtained through the offical RUSA website)

How this translates on the web-app:
> First the user selects the length of the Brevet race. (200km, 400km, 600km, 800km, 1000km)
>
> Next the user inputs the length of each control point into a cell.
>
> The Flask frontend receives this data and performs the algorithmic calculations, and subsequently the AJAX backend serves the live calculation to the user. 

[Project 5]: Once the algorithmic calculations are made:
> The user can click the submit button, which sends the control point distance, opening time, and closing time distance into an entry in the MongoDB database
>
> Hitting display button renders and redirects the user to the display page in which uses the AJAX backend to retrieve the data and html to display the entries currently in the database in a neat organized fashion.

[Project 6]: After the data is stored in the database:
> The open and close times, given from the MongoDB database entries, will be displayed on the consumer web-service page, which allows a user to view all open and closing times for a submitted Brevet race from the Brevet calculator
>
> On the webpage lies various hyperlinks which makes use of RestAPI principles, specifically the principle of a resource, and in this case the resource allows users to view open and close times in a JSON or CSV format, with the user also having the power to filter data by modifying the resource link (i.e., listAll/json or listCloseOnly/csv) and lastly, allows the user to list the top "k" opening/closing times with k being any positive integer (i.e., listOpenOnly/csv?top=3 will list the top 3 opening times, in csv)
>
> *note that JSON will be the default output if not specified in the resource link.

---

# Running the Application
To run the application follow these steps:

>  Navigate to the project directory and run in terminal:
>
> **cd DockerRestAPI**
>
> **docker compose up -d** 
>
> Upon execution, 4 images will be built, and subsequently, 4 containers will be ran in parallel. One for the Brevets Race Calculator, one for MongoDB, one for PHP server, and one for the consumer web-service.
>
> To view the Brevets Calculator, go to a browser of choice and type in the search bar:
>
> **http://localhost:5002/**
>
> To view the Consumer Web-Service, go to the browser of choice and type in the search bar:
>
> **http://localhost:5000/**
>
> The app is deployed and ready! (Note localhost:5001 is used to display the data via JSON or CSV format)

To stop the application follow these steps:

> Run in terminal:
>
> **docker-compose down**
>
> The application and containers have now stopped running, you can now safely delete the images from docker.

# Entering the Database Through Command Line

To enter the database from the terminal follow these steps:

> Make sure you are in the "DockerRestAPI" directory, if not, navigate to the project directory and type in terminal:
>
> **cd DockerRestAPI**
>
> Execute in terminal:
>
> **docker compose exec db mongo**
>
> **use brevetsdb**
>
> You are now in the database!
>
> To see all entries in the database through the terminal execute:
>
> **db.brevets_list.find().pretty()**
>
> To delete all entries you can execute in the terminal:
>
> **db.brevets_list.drop()**
>
> To exit the database, simply type in terminal:
>
> **exit**

---

# Running Tests

**This Assumes the Application is Running**

To run tests regarding the database follow these steps:

> Make sure you are in the "DockerRestAPI" directory, if not, navigate to the project directory and type in terminal:
>
> **cd DockerRestAPI**
>
> Next to run the tests, execute in the terminal:
>
> **docker compose exec web pytest test_database.py**

To run tests regarding the algorithmic calculation logic follow these steps:

> Make sure you are in the "DockerRestAPI" directory, if not, navigate to the project directory and type in terminal:
>
> **cd DockerRestAPI**
>
> Next to run the tests, execute in the terminal:
>
> **docker compose exec web pytest test_acp_times.py**

To run tests regarding the RestAPI follow these steps:

> Make sure you are in the "DockerRestAPI" directory, if not, navigate to the project directory and type in terminal:
>
> **cd DockerRestAPI**
>
> Next to run the tests, execute in the terminal:
>
> **./testapi.sh**

---

The list of dependencies is as follows:

> Docker
>
> Git Bash [Windows Only]
>
> Python version 3.14
>

Libraries (detailed from requirements.txt):

- arrow

- flask

- nose

- pep8

- autopep8

- pytest

- pymongo

- flask-restful

Set-up Instructions:

> Place directory containing the app in a directory of choice
>
> Follow instructions on how to run the app

--- 

Maintainer: Danish Singh

Contact: danishs@uoregon.edu