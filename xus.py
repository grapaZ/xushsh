#!/usr/bin/python

import os 
import getopt 
import sys 
import binascii 
import imp 
import string 
from ctypes import (cdll, POINTER, pointer, c_char_p, c_size_t, c_double, c_int, c_uint64, c_uint32, create_string_buffer)
import hmac 
import hashlib 
from operator import xor 
from itertools import izip, starmap 
import getopt
import subprocess

from struct import Struct 
_pack_int = Struct('>I').pack

def pbkdf2_hex(data, salt, iterations=1000, keylen=24, hashfunc=None):
    return pbkdf2_bin(data, salt, iterations, keylen, hashfunc).encode('hex') 

def pbkdf2_bin(data, salt, iterations=1000, keylen=24, hashfunc=None):
    """Returns a binary digest for the PBKDF2 hash algorithm of `data`
    with the given `salt`.  It iterates `iterations` time and produces a
    key of `keylen` bytes.  By default SHA-1 is used as hash function,
    a different hashlib `hashfunc` can be provided.
    """
    hashfunc = hashfunc or hashlib.sha1
    mac = hmac.new(data, None, hashfunc)
    def _pseudorandom(x, mac=mac):
        h = mac.copy()
        h.update(x)
        return map(ord, h.digest())
    buf = []
    for block in xrange(1, -(-keylen // mac.digest_size) + 1):
        rv = u = _pseudorandom(salt + _pack_int(block))
        for i in xrange(iterations - 1):
            u = _pseudorandom(''.join(map(chr, u)))
            rv = starmap(xor, izip(rv, u))
        buf.extend(rv)
    return ''.join(map(chr, buf))[:keylen]
    raise SystemExit(bool(failed))

_scrypt = cdll.LoadLibrary(imp.find_module('_scrypt')[1]) 
_crypto_scrypt = _scrypt.exp_crypto_scrypt 
_crypto_scrypt.argtypes = [c_char_p, # const uint8_t *passwd
                           c_size_t, # size_t passwdlen
                           c_char_p, # const uint8_t *salt
                           c_size_t, # size_t saltlen
                           c_uint64, # uint64_t N
                           c_uint32, # uint32_t r
                           c_uint32, # uint32_t p
                           c_char_p, # uint8_t *buf
                           c_size_t, # size_t buflen
                           ] 
_crypto_scrypt.restype = c_int 

def scrypt(data, salt, N=1 << 14, r=8, p=1, buflen=64):
    return _crypto_scrypt(data, len(data), salt, len(salt), N, r, p, outbuf, buflen)

""" defaults: 
""" 

hsh="sha256" 
input="password" 
salt="Salty"  #for example: salt="bfe102f3b4877733e8dfe2877a860606f69f900d865b3df3" 
salt = "1340f327dc01a6cb7bc8d5446149e614ba62c79d20a6b8cd"
func="sha1"
N=1
r=1
p=1
keylen=24 
u="$" 
flag=0 

options, remainder = getopt.gnu_getopt(sys.argv[1:], 'h:d:s:i:n:k:f:m:z:', ['hash=','data=','salt=','iterations=','keylen=','function=','mods=','Z='] ) 

for opt, arg in options:
    if opt in ('-h', '--hash'):
        hsh = str(arg)
    if opt in ('-d', '--data'):
        input = str(arg)
    if opt in ('-s', '--salt'):
        salt = str(arg)
    if opt in ('-i', '-n', '--iterations'):
        N = int(arg)
    if opt in ('-s', '--salt'):
        salt = str(arg)
    if opt in ('-k', '--keylen'):
        keylen = int(arg)
    if opt in ('-f', '--function'):
        func = str(arg) 
    if opt in ('-m', '--mods'):
        modifiers = str(arg) 
    if opt in ('-z', '--Z'):
        Z=str(arg).split('$')
        hsh=str(Z[0])
        mod=str(Z[1]).split()
        if (hsh=='pbkdf2'):
            N=int(mod[0])
            func=str(mod[1])
            keylen=int(mod[2])
            salt=str(Z[2])
        if (hsh=='scrypt'):
            N=int(mod[0])
            p=int(mod[1]) 
            r=int(mod[2])
            keylen=int(mod[3])
            salt=str(Z[2])

""" options for internal hash used by pbkdf2: 
""" 

if (func=="sha1"):
    hashfunc=hashlib.sha1 
if (func=="sha256"):
    hashfunc=hashlib.sha256 
if (func=="sha512"):
    hashfunc=hashlib.sha512

""" output returned in "$" delimited string:
    pbkdf2$<salt>$<N>$<keylength>$<function>$$<hash> 
"""
 
if (hsh=="pbkdf2u"):
    if (salt=="random"):
        salt=binascii.hexlify(os.urandom(keylen))
    print "pbkdf2"+u+str(N)+" "+str(func)+" "+str(keylen)+u+salt+u+pbkdf2_hex(input, salt, N, keylen, hashfunc)
    exit() 

if (hsh=="pbkdf2"):
    if (salt=="random"):
        salt=binascii.hexlify(os.urandom(keylen))
    print "pbkdf2"+u+str(N)+u+salt+u+pbkdf2_hex(input, salt, N, keylen, hashfunc)
    exit() 

if (hsh=="scrypt"):
    outbuf = create_string_buffer(keylen)
    if (salt=="random"):
        salt=binascii.hexlify(os.urandom(keylen))
    
    result = scrypt(input, salt, N, r, p, keylen)
    if result:
        print "error in scrypt"
        print result
        exit()
    if (N==1):
        print "scrypt"+u+str(N)+u+binascii.hexlify(outbuf.raw)
        exit()
    print "scrypt"+u+str(N)+" "+str(r)+" "+str(p)+" "+str(keylen)+u+salt+u+binascii.hexlify(outbuf.raw)
    exit()

""" older hashes: md5, sha1, sha256, sha512, null 
"""

if (hsh=="md5"):
     hash=hashlib.md5
     flag=1 
if (hsh=="sha1"):
     hash=hashlib.sha1
     flag=1 
if (hsh=="sha256"):
     hash=hashlib.sha256
     flag=1 
if (hsh=="sha512"):
     hash=hashlib.sha512
     flag=1 

if (flag==1):
     print hsh+"$"+hash(input + salt).hexdigest()
     exit() 
if (hsh=="crc32"):
     print binascii.crc32(input) & 0xffffffff
     exit() 
if (hsh=="random"):
    hash = os.urandom(keylen).encode('hex')
    print hash
    exit() 
if (hsh=="null"):
     print input
     exit() 

print "error: << " + hsh + " >> is not supported." 
exit() 

"""
    :license: BSD, see LICENSE for more details. copyright: (c) 
    :Copyright 2012 by John Leo Zimmer.
                     johnleozim@gmail.com 
 pbkdf2
 Module from https://github.com/mitsuhiko/python-pbkdf2 implements PBKDF2 hash.
 :copyright: (c) Copyright 2011 by Armin Ronacher. license: BSD
 Cut and pasted here from his pbkdf2.py to simplify distribution.

  Scrypt was created by Colin Percival and is licensed as 2-clause BSDscrypt.py
  Author: Magnus Hallin
  Home Page: http://bitbucket.org/mhallin/py-scrypt
  License: 2-clause BSD
  wget https://pypi.python.org/packages/source/s/scrypt/scrypt-0.6.1.tar.gz
  tar zxvf scrypt-0.6.1.tar.gz

	$ cd py-scrypt
	$ python setup.py build

	Become superuser (or use virtualenv):
	$ sudo python setup.py install

	Run tests after install:
	$ python setup.py test
  
"""
