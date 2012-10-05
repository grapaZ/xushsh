#!/usr/bin/python

import getopt
import sys
import hashlib
import binascii
from pbkdf2 import pbkdf2_hex

"""defaults:
"""
hsh="pbkdf2u"
input="password"
salt=""
cycles=10000
keylen=24
func="sha512"

u="$"
flag=0

options, remainder = getopt.gnu_getopt(sys.argv[1:], 'h:p:s:i:k:f:c:', ['hash=','password=','input=','salt=','iterations=','cycles','keylen=','function=',] )

for opt, arg in options:
    if opt in ('-h', '--hash'):
        hsh = str(arg)
    if opt in ('-i', '-p', '--password', '--input'):
        input = str(arg)
    if opt in ('-s', '--salt'):
        salt = str(arg)
    if opt in ('-c', '--cycles', '--iterations'):
        cycles = int(arg)
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

""" "naked" hash without detail:
"""
if (hsh=="pbkdf2u"):
    print pbkdf2_hex(input, salt, cycles, keylen, hashfunc)
    exit()

""" output returned in "$" delimited string:
    pbkdf2$sha1$<salt>$<cycles>$<hash>
"""
if (hsh=="pbkdf2"):
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

if (hsh=="null"):
     print input
     exit()

print "error: << " + hsh + " >> is not supported."
exit()

"""
    :copyright: (c) Copyright 2012 by John Leo Zimmer. 
                     johnleozim@gmail.com
    :license: GNU Affero General Public License version 3, 
        details in file LICENSES or at <http://fsf.org/>

"""

