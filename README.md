# <p align="center">ARMDET </p>



<p align="center">
  <img width="400" src="https://github.com/shireenchand/ARMDET/blob/main/ARMDET.png" alt="ARMDET logo">
</p>

<p align="center">
  Demo - https://bit.ly/armdet_demo
</p>

Currently, the world stands in a place where one small conflict can lead to a very dangerous environment. Generally, these situations are dangerous due to the use of weapons. All sorts of weapons can be used to scare or hurt individuals,communities and organizations.

To avert such incidents, the use of a Weapon Detection System comes to play. An automatic weapon detection system can provide the early detection of potentially violent situations that is of paramount importance for citizens security. One way to prevent these situations is by detecting the presence of dangerous objects such as handguns,knives and other objects in surveillance videos.

## What is it?
ARMDET is a Weapon Detection System with not only detection but also a necessary alert system. This type of system is very useful in public places like malls, airports, offices etc.

## How to use it?
- There are 2 parts to this system 
  - Flask Server
  - Main Streamlit App
- First the Server needs to be turned on and then the app

- Navigate to the folder which consists of all the files and type the following command to install all dependencies
```
pip install -r requirements.txt
```
- Then turn on the server by using the following commands
  - For MacOS/LINUX
    ```
    export FLASK_APP=api.py
    flask run
    ```
  - For Windows
    ```
    set FLASK_APP=api.py
    flask run
    ```
- Once the server is on, open another terminal or command prompt and navigate to the project folder
  ```
  streamlit run app.py
  ```
  Note: Streamlit might ask you to login, so it's handy to keep a streamlit account ready.
  
  
## Changes we are looking forward to doing in the future
1. We plan on increasing our model's accuracy by experimenting more.
2. The system will also be hosted once we get the required resources.
3. Make the system more flexible.

