# AI Usage Report

**Course:** COP4751 - Advanced Database Management
**Project:** Job Application Tracker
**Student:** Giovanna M. Curry PID - 6483095
*** AI Software used:*** Claude and Gemini

## 1. How AI Was Used
I used an AI assistant as a debugging and troubleshooting partner to resolve local environment issues and database connection errors. 


## 2. Specific Problems Solved with AI

* **Database Connection Issues:** 
Solved a persistent `1045 (28000): Access denied for user 'root'@'localhost'` error. 
The AI helped me identify that Windows file permissions were preventing my password updates from saving in `database.py`.

* **Python Connector Syntax:** 
Solved a dictionary mapping error where my configuration was using `'hostname'` and `'username'` instead of the library's required `'host'` and `'user'` keys.

* **Environment Setup:** 
Received guidance on starting the MySQL background service via Windows Services (`services.msc`) when the server tab was not visible in MySQL Workbench.


## 3. Code Attribution
All core application logic, HTML templates, and the database schema were provided by the course materials or authored by me. 
AI was used strictly for debugging terminal/web server execution errors and adjusting the `DB_CONFIG` dictionary to match my local machine's environment.
