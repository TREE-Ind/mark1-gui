from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort, url_for
import os
import json
from time import sleep
import platform
import subprocess
from subprocess import call
from datetime import datetime
import shutil
import stat

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
        mycroft_skills = ""
        try:
            sys_data['current_time'] = subprocess.check_output(['date'], shell=True)
            sys_data['machine_name'] = platform.node()
            sys_data['mycroft_version'] = subprocess.check_output(['dpkg -s mycroft-core | grep Version'], shell=True)
            mycroft_skills = sorted(os.listdir('/opt/mycroft/skills'))
            sys_data['skills_log'] = subprocess.check_output(['tail -n 10 /var/log/mycroft-skills.log'], shell=True)
            print(type(sys_data['skills_log']))
            disk_usage_info = disk_usage_list()
        except Exception as ex:
            print(ex)
        finally:
            return render_template("index.html", title='Mark 1 - System Information',
                                    sys_data = sys_data,
                                    name=login['username'], mycroft_skills=mycroft_skills)


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

@app.route('/delete', methods=['POST'])
def delete_skill():
    skill_delete = request.form['skill_to_delete']
    #print("This is the request form: {}".format(request.form))
    print("This is the skill to delete: {}".format(skill_delete))
    call("sudo rm -rf /opt/mycroft/skills/" + skill_delete, shell=True)
    print("Successfully removed folder: {}".format('/opt/mycroft-skills/' + skill_delete))
    return redirect(url_for('home'))

@app.context_processor
def boot_info():
    item = {'start_time': 'Na','running_since':'Na'}
    try:
        item['running_duration'] = subprocess.check_output(['uptime -p'], shell=True)
        item['start_time'] = subprocess.check_output(['uptime -s'], shell=True)
    except Exception as ex:
        print ex
    finally:
        return dict(boot_info = item)

def del_rw(action, name, exc):
    os.chmod(name, stat.S_IWRITE)
    os.remove(name)

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
