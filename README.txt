README    Improved hashing for VISTA sign-on, XUSHSH: 

Rapid recipe for the already-believer. 
For long-winded (and perhaps to be finished) cookbook see xushsh_pbkdf2.pdf.
(Or look in Appendix README for this file in full color... copy/past the green stuff.)

We will replace XUSHSH with a new version and create a global node,
 ^VA(200,"VWHSH"), that controls its behavior. 
    After a demonstration of pbkdf2,
    we will set it to return the old hash unchanged while moving to convert New Person ACCESS/VERIFY CODEs.
 The ultimate goal is the Conversion to pbkdf2 which is posssible from either "LEGACY"(WorldVistA) or "NONE"(openVistA).
  

GT.M host, this example was run on a dEWDrop virtual machine:

Python will be already installed and in the PATH.

vista@dEWDrop:~$ mkdir git   <<<--- or somewhere of <your> choice.
             :~$ cd git
         :~/git$ git clone git://github.com/grapaZ/xushsh.git   <<<---- or download a zip from https://github.com/grapaZ/xushsh
         :~/git$ cd xushsh
  :~/git/xushsh$ cp xushsh.py ~/bin     <<<--- or some other location; but be prepared to alter ^VA(200,"VWHSH") in a later step.  
  :~/git/xushsh$ python ~/bin/xushsh.py  <<<-- testing w defaults in xushsh.py
f4ca507c07d0bd31bc779a08756826a6fd9dd97d43ac25e4   <<<---- this is the pbkdf2 hash of "password" with no salt, 
                                                           10000iterations, internal function sha512, keylength 24(hex digits).
                                                           This is a good time to add a salt which can be generated thusly:
             :~$ python ~/bin/xushsh.py -h random   
3731f02531b2157558140f0c222ac4aedfa9486bd8889aca    <<<--- for example

             :~$ python ~/bin/xushsh.py --salt="3731f02531b2157558140f0c222ac4aedfa9486bd8889aca" 
f6534f8db4d7f8f3808d0735da1f38c487f539d801ce7dfd

Further, ~/bin/xushsh.py can (and should) be edited now to lock-in your salt as a permanent default (not subject to casual change). 

___________________________________________________manual labor option ____________________________
             :~$ cp ~/git/xushsh/*.m ~/p/

Now we can go into MUMPS:
             :~$ mumps -dir

        MU-beta> zlink "VWHSH8.m","VWHSH0.m","VWHSHLEG.m"
___________________________________________________or we can do: __________________________________

        MU-beta> d ^%RI

                 Formfeed delimited <No>?
                 Input device: <terminal>: /home/vista/git/xushsh/vwhshGTM.ro 
                 VWHSH* for GT.M                          NOTE--->^<-- for Cache' use vwhshCACHE.ro                             
                 GT.M 19-OCT-2012 12:32:40


                 Output directory : /home/vista/p/

                 VWHSH0    VWHSH8    VWHSHLEG


                 Restored 226 lines in 3 routines.
_____________________________________________________continue _____________________________________

        MU-beta> W $$EN^XUSHSH("test")   <<<------------LEGACY hash 
115116101116
        MU-beta> W $$EN^VWHSHLEG("test") 
115116101116

^VWHSH8 will be able to replace ^XUSHSH once global node ^VA(200,"VWHSH") is properly configured by the following call to ^VWHSH0:

       MU-beta> DO BUILD^VWHSH0()    <<<--------configuration will default to “LEGACY”
       MU-beta> w $$EN^VWHSH8("test")
115116101116                       <<<----------and NOW that is what ^VWHSH8 will return.

       MU-beta> DO SET^VWHSH0("PBKDF2") <<<-----LEGACY, NONE, and PBKDF2 are supplied by BUILD()
       MU-beta> W $$EN^VWHSH8("test") 
f054d357dfc8464f110cd32b36423acead8e1bcbf1bd8197  <<<--- If you have not set a default salt.

Lots of other stuff could be done with ^VA(200,"VWHSH"), but KeepItSimple for now.
I recommend looking at ^("VWHSH") with VPE. Some VISTA configurations may require editing the location of xushsh.py

       MU-beta> DO SET^VWHSH0("LEGACY")   <<<---- We are now ready to replace the old XUSHSH.
       MU-beta> zsy "cp ~/p/VWHSH8.m ~/p/XUSHSH.m"  <<<----overwrite ^XUSHSH with ^VWHSH8
       MU-beta> zlink "XUSHSH.m" 

We now have the new XUSHSH replacing the legacy version. 
Nothing else has changed.

   <<<NOW>>> we are ready to switch to PBKDF2...
                                        

       MU-beta> DO CONVERT^VWHSH0("PBKDF2")    <<<--------more or less irreversible step
( or   MU-beta> DO CONVERT^VWHSH0("NONE")     <<<---- less irreversible option :-)

 
CONVERT^VWHSH0()  is going to change fields #2 and #11

^VA(200,D0,0)=  ^ ^ (#2) ACCESS CODE [3F] ^
^VA(200,D0,.1)= ^ (#11) VERIFY CODE [2F] ^ 

And Cross-References:

     "A"    MUMPS
            Field:  ACCESS CODE  (200,2)
                    1)= S ^VA(200,"A",X,DA)=+$H
                    2)= K ^VA(200,"A",X,DA)
                    3)= ACCESS CODE lookup

  "AOLD"    MUMPS
            Field:  ACCESS CODE  (200,2)
      Description:  This is a list of used ACCESS CODES that may not be used
                    again untill the OLD ACCESS CODE PURGE option is run.
                    1)= Q
                    2)= S ^VA(200,"AOLD",X,DA)=+$H
                    3)= OLD ACCESS CODES

  "VOLD"    MUMPS
            Field:  VERIFY CODE  (200,11)
      Description:  This builds a list of old VERIFY CODEs that this user has
                    had in the past.  It is cleaned  out with the same option
                    the purges the old access code X-ref.
                    1)= Q
                    2)= S ^VA(200,DA,"VOLD",X)=+$H

BUT the conversion is NOT going to reset any cross reference $H, etc. 
The goal is to simply rehash ALL of these global nodes without changing anything else.

