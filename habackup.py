import appdaemon.appapi as appapi
import datetime
import subprocess
from utils import *
             
class habackup(appapi.AppDaemon):

  def initialize(self):
    # self.LOGLEVEL="DEBUG"
    self.log("habackup App")
    runtime = datetime.time(0,1,0)
    tomorrow= datetime.date.today() + datetime.timedelta(days=1)
    event=datetime.datetime.combine(tomorrow,runtime)
    handle=self.run_daily(self.timer_h,runtime)
    #self.perform_backup()   # warning this kicks off in the initialization thread which backs up other apps running in that thread.


  def timer_h(selfi,kwargs):
    self.perform_backup()

  def perform_backup(self):
    self.log("in timer handler")
    cmdline="sudo /home/homeassistant/habackup"
    self.log("running {}".format(cmdline))
    output=subprocess.check_output(cmdline,stderr=subprocess.STDOUT,shell=True)
    self.log("backup returned {}".format(output))

  def log(self,msg,level="INFO"):
    obj,fname, line, func, context, index=inspect.getouterframes(inspect.currentframe())[1]
    super(habackup,self).log("{} - ({}) {}".format(func,str(line),msg),level)

