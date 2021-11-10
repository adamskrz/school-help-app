# School Help App

A Python app built with Kivy and KivyMD to assist with organisation for school. This is an old project from 2019, which I've just pushed to GitHub.

## Functions

### Bus Times

The main functionality of the app is the Bus Times viewer, which stemmed from my frustrastion with availabele apps for my area. Most apps used one data provider which only provided live (GPS assisted) bus times for one of three operators in the area, or if it had more than one, it showed them as separate bus stops. My app takes times from three different sources, and matches their scheduled times to remove duplicate data and get a best effor live time for every bus operator for a stop.

### Homework organiser

The app also features a basic database driven task list, allowing you to input tasks for different subjects, setting due dates and more. This is based around an SQLite3 database.

## Running the app

### Preparing your environment

To run this app, you need to have Python3 installed. Make sure `pip` is up to date and that you have virtualenv installed by running

```bash
python -m pip install --upgrade pip setuptools virtualenv
```

Clone the repo to your system and enter the folder, then create a virtual environment for all the dependencies with

```bash
python -m virtualenv env
```

and activate the env (command depends on system).

### Installing dependencies and launching

Install all the python dependencies for the project with

```bash
python -m pip install -r requirements.txt
```

and you should be able to launch the app with

```bash
python main.py
```

In order to get the bus time functionality to work, you may need to setup your own API credentials. There is a template file at `lib/bus/helper/api_secrets.py.template`, just fill this out and rename the file to remove `.template`.