# Python & SQL Study Hours Tracker

## Overview
This is a Command Line Interface (CLI) application built with Python and PostgreSQL. It allows users to track their daily study hours by logging the subject and duration of each session into a secure relational database.

## Features
- **Add a Session:** Dynamically log a study subject and the amount of time spent studying.
- **View History:** Retrieve and display a formatted list of all past study sessions.
- **Secure Architecture:** Uses `python-dotenv` to keep database credentials hidden and secure.
- **Auto-Initialization:** Automatically creates the necessary database tables upon the first run.

## Tech Stack
- **Backend:** Python 3
- **Database:** PostgreSQL
- **Driver:** psycopg2
