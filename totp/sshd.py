#!/usr/bin/env python

from os import environ, execl as exec
from sys import argv, exit
from getpass import getpass

import totp

try:
  if len(argv) > 1:
    myFile = argv[1]
  else:
    myFile = '~/.2fa'

  myTOTP = totp.Config(myFile)

  totp.setCatch(myTOTP.options['timer'])

  while True:
    myCode = getpass('Challenge: ')
    if len(myCode):
      break

  if myTOTP.authenticate(myCode):
    myShell = environ['SHELL']
    with open('/etc/shells') as handle:
      goodShell = False
      for line in handle:
        if line.rstrip() == myShell:
          goodShell = True
          break
      if not goodShell:
        exit(1)
      totp.setCatch(0)
      exec(myShell, '-' + myShell.rsplit('/',1)[-1])
except Exception:
  exit(1)
exit(1)

