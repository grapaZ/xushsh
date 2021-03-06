#!/usr/bin/python

import hmac
import hashlib
from struct import Struct
from operator import xor
from itertools import izip, starmap

import getopt
import sys
import binascii
import os

_pack_int = Struct('>I').pack
"""GpaZ knows not what this line does.
"""
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
    """GpaZ: knows not what this line does.
    """

    """
    pbkdf2
    Module from https://github.com/mitsuhiko/python-pbkdf2 implements pbkdf2 for Python.
    :copyright: (c) Copyright 2011 by Armin Ronacher.
    :license: BSD, see LICENSE for more details.
    
    Cut and pasted here from his pbkdf2.py to simplify distribution.
    """

""" defaults:
"""
hsh="pbkdf2"
input="password"
salt=""
"""for example: salt="bfe102f3b4877733e8dfe2877a860606f69f900d865b3df3"
"""
cycles=10000
keylen=24
func="sha512"

u="$"
flag=0

options, remainder = getopt.gnu_getopt(sys.argv[1:], 'h:d:s:i:k:f:', ['hash=','data=','salt=','iterations=','keylen=','function=',] )

for opt, arg in options:
    if opt in ('-h', '--hash'):
        hsh = str(arg)
    if opt in ('-d', '--data'):
        input = str(arg)
    if opt in ('-s', '--salt'):
        salt = str(arg)
    if opt in ('-i', '--iterations'):
        cycles = int(arg)
    if opt in ('-s', '--salt'):
        salt = str(arg)
    if opt in ('-k', '--keylen'):
        keylen = int(arg)
    if opt in ('-f', '--function'):
        func = str(arg)

""" options for internal hash used by pbkdf2:
"""
if (func=="sha1"):
    hashfunc=hashlib.sha1    
if (func=="sha256"):
    hashfunc=hashlib.sha256
if (func=="sha512"):
    hashfunc=hashlib.sha512

""" "naked" pbkdf2 hash without detail:
"""

if (hsh=="pbkdf2"):
    print pbkdf2_hex(input, salt, cycles, keylen, hashfunc)
    exit()

""" output returned in "$" delimited string:
    pbkdf2$<salt>$<cycles>$<keylength>$<function>$$<hash>
"""

if (hsh=="pbkdf2u"):
    print "pbkdf2"+u+salt+u+str(cycles)+u+str(keylen)+u+func+u+u+pbkdf2_hex(input, salt, cycles, keylen, hashfunc)
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

""" $<hsh>$<salt>$<result>
"""
if (flag==1):
     print hash(input + salt).hexdigest()
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
    :license: BSD, see LICENSE for more details.
    :copyright: (c) Copyright 2012 by John Leo Zimmer. 
                     johnleozim@gmail.com
"""

