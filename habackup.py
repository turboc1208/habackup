import appdaemon.appapi as appapi
import os
import datetime
import time
import subprocess
from utils import *
             
class habackup(appapi.AppDaemon):

  def initialize(self):
    # self.LOGLEVEL="DEBUG"
    self.log("habackup App")
    self.backup_dir=self.args["backup_dir"]
    self.retention=int(self.args["days_to_keep"])
    runtime = datetime.time(0,1,0)
    tomorrow= datetime.date.today() + datetime.timedelta(days=1)
    event=datetime.datetime.combine(tomorrow,runtime)
    handle=self.run_daily(self.timer_h,runtime)
    #self.perform_backup()   # warning this kicks off in the initialization thread which backs up other apps running in that thread.

  def timer_h(self,kwargs):
    self.perform_backup()

  def perform_backup(self):
    self.log("in timer handler")
    cmdline="sudo /home/homeassistant/habackup"
    self.log("running {}".format(cmdline))
    output=0
    output=subprocess.check_output(cmdline,stderr=subprocess.STDOUT,shell=True)
    self.log("backup returned {}".format(output))
    self.cleanup_backup()

  def cleanup_backup(self):
    for f in os.listdir(self.backup_dir):
      fcheck=os.path.join(self.backup_dir,f)
      if os.stat(fcheck).st_mtime < (time.time() - (self.retention * 86400)):
        if os.path.isfile(fcheck):
          self.log("removing file {}".format(fcheck))
          os.remove(fcheck)

  def log(self,msg,level="INFO"):
    try:
      obj,fname, line, func, context, index=inspect.getouterframes(inspect.currentframe())[1]
    except IndexError:
      self.log("Unknown - (xxx) {}".format(msg),level)
    
    super(habackup,self).log("{} - ({}) {}".format(func,str(line),msg),level)

