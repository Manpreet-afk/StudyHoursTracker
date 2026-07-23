# Python & SQL Study Hours Tracker

## Overview
This is a web-application built with Python and PostgreSQL. It allows users to track their daily study progress by logging the subject and duration of each session into a secure relational database.

## Features
* **📈 Live Dashboard:** Instantly calculates all-time study hours and dynamically tracks your consecutive daily study streak (🔥).
* **📊 Interactive Visualizations:** render color-coded horizontal bar charts that break down total time spent per subject.
* **📋 Complete CRUD Functionality:** 
  * **Create:** Log new subjects and study durations through a clean web form.
  * **Read:** View a formatted, real-time log of all past study sessions.
  * **Update:** Quickly correct or adjust the study duration of existing session IDs.
  * **Delete:** Permanently remove incorrect or unwanted records directly from the interface.
* **🗄️ Robust Backend:** Parameterized SQL queries ensure data integrity and prevent SQL injection using `psycopg2`.

## Tech Stack
- Python
- postgreSQl
- streamlit
