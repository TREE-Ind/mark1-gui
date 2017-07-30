from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort
import os
import json
from time import sleep
import platform
import subprocess
from datetime import datetime

with open('config.json') as json_data_file:
    data = json.load(json_data_file)

login = (data['login'])


app = Flask(__name__)

@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        sys_data = {"current_time": '',"machine_name": ''}
        try:
            sys_data['current_time'] = subprocess.check_output(['date'], shell=True)
            sys_data['machine_name'] = platform.node()
            sys_data['mycroft_version'] = subprocess.check_output(['dpkg -s mycroft-core | grep Version'], shell=True)
            sys_data['installed_skills'] = os.listdir('/opt/mycroft/skills')
            disk_usage_info = disk_usage_list()
        except Exception as ex:
            print(ex)
        finally:
            return render_template("index.html", title='Mark 1 - System Information',
                                    sys_data = sys_data,
                                    name=login['username'])


@app.route('/login', methods=['POST'])
def do_admin_login():
    if request.form['password'] == login['password'] and request.form['username'] == login['username']:
        session['logged_in'] = True
    else:
        flash('wrong password!')
    return home()

@app.route("/logout")
def logout():
    session['logged_in'] = False
    return home()

def disk_usage_list():
     try:
         items = [s.split() for s in subprocess.check_output(['df', '-h'], universal_newlines=True).splitlines()]
     except Exception as ex:
         print ex
     finally:
         return items[1:]




if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True,host='0.0.0.0', port=8080)
