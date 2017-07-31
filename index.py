from flask import Flask, render_template
from datetime import datetime
import platform
import subprocess

app = Flask(__name__)

@app.route('/')
@app.route('/home')
def index():
 sys_data = {"current_time": '',"machine_name": ''}
 try:
     sys_data['current_time'] = datetime.now().strftime("%d-%b-%Y , %I : %M : %S %p")
     sys_data['machine_name'] =  platform.node()
     cpu_genric_info = cpu_generic_details()
     disk_usage_info = disk_usage_list()
     running_process_info = running_process_list()
 except Exception as ex:
     print ex
 finally:
     return render_template("index.html", title='Mark 1 - System Information',
                            sys_data = sys_data,
                            cpu_genric_info = cpu_genric_info,
                            disk_usage_info= disk_usage_info,
                            running_process_info = running_process_info)


def cpu_generic_details():
 try:
     items = [s.split('\t: ') for s in subprocess.check_output(["cat /proc/cpuinfo  | grep 'model name\|Hardware\|Serial' | uniq "], shell=True).splitlines()]
 except Exception as ex:
     print ex
 finally:
     return items

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


@app.context_processor
def memory_usage_info():
 try:
     item = {'total': 0,'used': 0,'available': 0 }
     item['total']=  subprocess.check_output(["free -m -t | awk 'NR==2' | awk '{print $2'}"], shell=True)
     item['used']=  subprocess.check_output(["free -m -t | awk 'NR==3' | awk '{print $3'}"], shell=True)
     item['available']= int(item['total'])- int(item['used'])
 except Exception as ex:
     print ex
 finally:
     return dict(memory_usage_info = item)


@app.context_processor
def os_name():
 os_info = subprocess.check_output("cat /etc/*-release | grep PRETTY_NAME | cut -d= -f2", shell=True).replace('\"', '')
 return dict(os_name=os_info)


@app.context_processor
def cpu_usage_info():
 item = {'in_use': 0}
 try:
     item['in_use'] = subprocess.check_output("top -b -n2 | grep 'Cpu(s)'|tail -n 1 | awk '{print $2 + $4 }'", shell=True)
 except Exception as ex:
     print ex
 finally:
     return dict(cpu_usage_info = item)


@app.context_processor
def cpu_processor_count():
 proc_info = subprocess.check_output("nproc", shell=True).replace('\"', '')
 return dict(cpu_processor_count=proc_info)


@app.context_processor
def cpu_core_frequency():
 core_frequency = subprocess.check_output("vcgencmd get_config arm_freq | cut -d= -f2", shell=True).replace('\"', '')
 return dict(cpu_core_frequency=core_frequency)


@app.context_processor
def cpu_core_volt():
 core_volt = subprocess.check_output("vcgencmd measure_volts| cut -d= -f2", shell=True).replace('\"', '')
 return dict(cpu_core_volt=core_volt)


@app.context_processor
def cpu_temperature():
 cpuInfo = {'temperature': 0, 'color': 'white'}
 try:
     cpuTemp = float(subprocess.check_output(["vcgencmd measure_temp"], shell=True).split('=')[1].split('\'')[0])
     cpuInfo['temperature']=cpuTemp
     if cpuTemp > 40 and cpuTemp < 50:
         cpuInfo['color'] = 'orange'
     elif cpuTemp > 50:
         cpuInfo['color'] = 'red'
     return cpuInfo
 except Exception as ex:
     print ex
 finally:
     return dict(cpu_temperature=cpuInfo)

def disk_usage_list():
 try:
     items = [s.split() for s in subprocess.check_output(['df', '-h'], universal_newlines=True).splitlines()]
 except Exception as ex:
     print ex
 finally:
     return items[1:]

def running_process_list():
 try:
     items = [s.split() for s in subprocess.check_output(["ps -Ao user,pid,pcpu,pmem,comm,lstart --sort=-pcpu"], shell=True).splitlines()]
 except Exception as ex:
     print ex
 finally:
     return items[1:]


@app.context_processor
def utility_processor():
 def short_date(a,b,c):
     return u'{0}{1}, {2}'.format(a, b,c)
 return dict(short_date=short_date)


if __name__ == "__main__":
 app.run(host='0.0.0.0',debug=True)
