#!/usr/bin/python
import sys, os, pwd, commands, string
import optparse, shlex, re
import time
from time import gmtime, strftime
import math

def processCmd(cmd, quite = 0):
  #    print cmd
  status, output = commands.getstatusoutput(cmd)
  if (status !=0 and not quite):
    print 'Error in processing command:\n   ['+cmd+']'
    print 'Output:\n   ['+output+'] \n'
  return output

def getSignal(coupling):

  if coupling == "800":
    setup = "V"

  if coupling == "801":
    setup = "A"

  if coupling == "805":
    setup = "S"

  if coupling == "806":
    setup = "P"

  os.system("cp configs/categories_config_signal_monojet_TEMP.py configs/categories_config_signal_monojet_"+coupling+".py")
  os.system("sed -i 's~TEMP~"+coupling+"~g' configs/categories_config_signal_monojet_"+coupling+".py")
  os.system("sed -i 's~SETUP~"+setup+"~g' configs/categories_config_signal_monojet_"+coupling+".py")
  cmd = 'python signal_builModel.py categories_config_signal_monojet_'+coupling
  output = processCmd(cmd)

  os.system("cp configs/categories_config_signal_monojet2_TEMP.py configs/categories_config_signal_monojet2_"+coupling+".py")
  os.system("sed -i 's~TEMP~"+coupling+"~g' configs/categories_config_signal_monojet2_"+coupling+".py")
  os.system("sed -i 's~SETUP~"+setup+"~g' configs/categories_config_signal_monojet2_"+coupling+".py")
  cmd2 = 'python signal_builModel.py categories_config_signal_monojet2_'+coupling
  output = processCmd(cmd2)

if __name__ == "__main__": 
    getSignal("800") 
    getSignal("801") 
    getSignal("805") 
    getSignal("806") 
