README    Improved hashing for VISTA sign-on, XUSHSH: 

Rapid recipe for the already-believer. 
For long-winded (and unfinished) cookbook see xushsh_pbkdf2.pdf.

We will replace XUSHSH with a new version and create a global node,
 ^VA(200,"VWHSH"), that controls its behavior. 
 After a demonstration of pbkdf2,
 we will set it to return the old hash unchanged.

GT.M host, this example was run on dEWDrop virtual machine:

Python is already installed and in the PATH

vista@dEWDrop:~$ mkdir git
             :~$ cd git
         :~/git$ git clone git://github.com/grapaZ/xushsh.git
         :~/git$ cd xushsh
  :~/git/xushsh$ cp xushsh.py ~/bin
  :~/git/xushsh$ python ~/bin/xushsh.py  <<<-- testing w defaults in xushsh.py
f4ca507c07d0bd31bc779a08756826a6fd9dd97d43ac25e4

  :~/git/xushsh$ 
  :~/git/xushsh$ cp *.m ~/p/

Now go into MUMPS:
  :~/git/xushsh$ mumps -dir

       MU-beta3>zlink "VWHSH8.m","VWHSH0.m","VWHSHLEG.m"
       MU-beta3>W $$EN^XUSHSH("test")   <<<------------LEGACY hash 
115116101116
       MU-beta3>W $$EN^VWHSHLEG("test") 
115116101116

^VWHSH8 will be able to replace ^XUSHSH once global node ^VA(200,"VWHSH") is properly configured by the following call to ^VWHSH0:

       MU-beta3>DO BUILD^VWHSH0()    <<<--------configuration will default to “LEGACY”
115116101116                       <<<----------and that is what ^VWHSH8 will return.

       MU-beta3>DO SET^VWHSH0("PBKDF2") <<<-----LEGACY, NONE, and PBKDF2 are supplied by BUILD()
       MU-beta3>W $$EN^VWHSH8("test") 
f054d357dfc8464f110cd32b36423acead8e1bcbf1bd8197

Lots of other stuff could be done with ^VA(200,"VWHSH"), but KeepItSimple for now.
I recommend looking at ^("VWHSH") with VPE. Some VISTA configurations may require
Put LEGACY (or NONE if you are using, for example, openvista.)

       MU-beta3>DO SET^VWHSH0("LEGACY")   <<<---- We are now ready to replace the old XUSHSH.
       MU-beta3>zsy "cp ~/p/VWHSH8.m ~/p/XUSHSH.m"  <<<----overwrite ^XUSHSH with ^VWHSH8
       MU-beta3>zlink "XUSHSH.m" 

We now have the new XUSHSH replacing the legacy version and capable of switching to PBKDF2 as soon as the NEW PERSON file is converted. 


