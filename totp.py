from signal import signal, setitimer as alarm, pause, SIGINT, SIGALRM, ITIMER_REAL as ALARM
from os import path
from time import time
from base64 import b32decode
from struct import pack, unpack
from hmac import HMAC as hmac
from hashlib import sha1
from yaml import safe_load as load, dump

def catch (sig, frame):
  raise Exception
signal(SIGINT, catch)
signal(SIGALRM, catch)

def setCatch(timer):
  alarm(ALARM, timer)

class Config:
  def __init__ (self, confFile):
    setCatch(5)
    confFile = path.expanduser(confFile)
    self.file = confFile
    with open(confFile) as handle:
      self.options = load(handle)
    
    if not 'secret' in self.options:
      raise Exception
    if 'ratelimit' in self.options:
      self.options['ratelimit'].setdefault('limit', 3)
      self.options['ratelimit'].setdefault('window', 0)
      self.options['ratelimit'].setdefault('counter', 0)
    self.options.setdefault('window', 1)
    self.options.setdefault('timer', 30)

    self.time = int(time() /30)
    Secret = b32decode(self.options['secret'].encode('ascii'))
    Drift = int(self.options['window'])
    self.keys = []

    for SkewedTime in range(self.time-Drift,self.time+Drift+1):
      ByteTime = pack(">q", SkewedTime)
      Hash = hmac(Secret, ByteTime, sha1).digest()
      Offset = Hash[-1] & 0x0F
      ShortHash = Hash[Offset:Offset+4]
      Code = unpack('>L', ShortHash)[0]
      Code &= 0x7FFFFFFF
      Code %= 1000000
      Code = '{0:06d}'.format(Code)
      self.keys.append(Code)

  def authenticate(self, Code):
    authed = False
    if 'ratelimit' in self.options:
      if self.options['ratelimit']['window'] == self.time:
        if self.options['ratelimit']['counter'] >= self.options['ratelimit']['limit']:
          raise Exception
        else:
          writeConf = True
          self.options['ratelimit']['counter'] += 1
      else:
        writeConf = True
        self.options['ratelimit']['window'] = self.time
        self.options['ratelimit']['counter'] = 0

    if 'last' in self.options and Code == self.options['last']:
      raise Exception

    if Code in self.keys:
      authed = True
    elif 'scratch' in self.options and Code in self.options['scratch']:
      authed = True
      writeConf = True
      self.options['scratch'].remove(Code)

    if authed and 'last' in self.options:
      writeConf = True
      self.options['last'] = Code

    if writeConf:
      with open(self.file, 'w') as handle:
        dump(self.options, handle)

    return authed


