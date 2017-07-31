# Mark 1 Gui
This will be a ongoing project in flask to build a web ui for the mark 1.

Currently setup for http://mark1_ip:8080 will take you to the login page

# Running It
**This is currently in development and not ready for production use**

1. Clone the repo to your mark 1 device `git clone https://github.com/Geeked-Out-Solutions/mark1-gui.git`
2. Change to the new mark1-gui dir, `cd mark1-gui`
3. Install requirements: `sudo pip install -r requirements.txt`
4. Run the app, `python app.py`


# Login Example:

![login example](https://user-images.githubusercontent.com/1426587/28755344-af03371e-7526-11e7-8853-2d82cb931e3d.png)

The username and pw for the login is taken from the config.json file.  After logging in you will see something similiar to this image, after I finish getting all the data in here that is needed then a CSS can clean it up and make it look pretty:
![](https://user-images.githubusercontent.com/1426587/28755365-5f3a3bd2-7527-11e7-831e-820daf559906.png)

# Logout
You can currently logout by going to http://mark1_ip:8080/logout.html, will be adding official logout button shortly.
