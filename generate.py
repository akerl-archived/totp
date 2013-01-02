#!/usr/bin/env python

import os
import sys
import yaml
import base64

def feedback(message = None, validate = None, default = None, inputMsg = '? [{0}] '):
  if message is not None:
    print(message)
  while True:
    tmp = input(inputMsg.format(default))
    if tmp == '' and default is not None:
      tmp = default
    tmp = tmp.lower()
    if validate is bool:
      if tmp in ['y','yes']:
        return True
      elif tmp in ['n','no']:
        return False
    elif validate is int:
      if tmp.isdigit():
        return int(tmp)
    elif type(validate) is list:
      if type(validate[0]) is tuple:
        for item in validate:
          if tmp in item:
            return item[0]
      elif tmp in validate:
        return tmp
    elif hasattr(validate, '__call__'):
      if validate(tmp):
        return tmp

if len(sys.argv) > 1:
  myFile = sys.argv[1]
else:
  myFile = input('File to use (blank for stdout): ')
if not len(myFile):
  myFile = None

myConf = {}
myConf['secret'] = str(base64.b32encode(os.urandom(10)),'ascii')

myConf['window'] = feedback('How many codes before or after $now should be valid? (1 allows $now +/- 1)', int, '1')
myConf['timer'] = feedback('After how many seconds should the challenge prompt time out?', int, '30')
if feedback('Should code reuse be prevented? [Y/n]', bool, 'yes', '? '):
  myConf['last'] = "0"
if feedback('Should attempts be ratelimited? [Y/n]', bool, 'yes', '? '):
  myConf['ratelimit'] = {
    'window' : 1,
    'counter' : 0,
    'limit' : feedback('How many attempts should be allowed per 30 seconds?', int, '3')
  }
doScratch = feedback('How many scratch codes should be created? (0 for none)', int, '2')
if doScratch:
  myConf['scratch'] = []
  for x in range(0,doScratch):
    myConf['scratch'].append(str(base64.b32encode(os.urandom(6))[0:10], 'ascii'))
myConf['url'] = "https://www.google.com/chart?chs=200x200&chld=M|0&cht=qr&chl=otpauth://totp/{0}@{1}%3Fsecret%3D{2}".format(os.environ['USER'], os.uname()[1], myConf['secret'])

if myFile is not None:
  if not os.path.exists(os.path.expanduser(myFile)):
    os.mknod(os.path.expanduser(myFile), 0o600)
  elif os.stat(os.path.expanduser(myFile))[0] != 0o100600:
    print('Warning: The permissions on {0} appear to be overly permissive'.format(myFile))
  handle = open(os.path.expanduser(myFile), 'w')
  yaml.dump(myConf, handle)
  print(myConf['url'])
  if 'scratch' in myConf:
    print(myConf['scratch'])
else:
  print(yaml.dump(myConf))

