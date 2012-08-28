#!/usr/bin/env python

from os import environ, setresuid
from pwd import getpwnam as getuid
from sys import argv, exit
from termios import tcgetattr, tcsetattr, ECHO, TCSADRAIN as DRAIN

import totp

try:
  setresuid(getuid(environ['PAM_USER'])[2], getuid(environ['PAM_USER'])[2], 0)

  if len(argv) > 1:
    myFile = argv[1]
  else:
    myFile = '~/.2fa'

  myConf = totp.Config(myFile)
  myTTY = '/dev/' + environ['PAM_TTY']

  setresuid(0,0,0)

  totp.setCatch(myConf.options['timer'])

  with open(myTTY, 'w') as handle:
    handle.write('Challenge: ')
  with open(myTTY) as handle:
    old = tcgetattr(handle.fileno())
    new = tcgetattr(handle.fileno())
    new[3] = new[3] & ~ECHO
    try:
      tcsetattr(handle.fileno(), DRAIN, new)
      while True:
        myCode = handle.readline().rstrip()
        if len(myCode):
          break
    finally:
      tcsetattr(handle.fileno(), DRAIN, old)

  with open(myTTY, 'w') as handle:
    handle.write('\n')

  if myConf.authenticate(myCode):
    exit(0)

except Exception:
  exit(1)

exit(1)

