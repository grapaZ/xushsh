XUSHSH  ;IA/GpZ-ROBUST(PBKDF2)HASHING UTILITY v1.0; 10/1/12 6:26pm
V       ;;8.0;KERNEL;;Jul 10, 1995
        ;
        ;
        ;------------------------------------------------------------------------
        ; Copyright (c) 2012 John Leo Zimmer      Email: johnleozim@gmail.com    ;
        ; All rights reserved.                                  Glenwood, Iowa   ;
        ;                                                                        ;
        ; This program is free software: You can redistribute it and/or modify   ;
        ; it under the terms of the GNU Affero General Public License as         ;
        ; published by the Free Software Foundation, either version 3 of the     ;
        ; License, or (at your option) any later version.                        ;
        ;                                                                        ;
        ; See COPY in distribution package or <http://www.gnu.org/licenses/>.    ;
        ;------------------------------------------------------------------------
        ;
A       SET X=$$EN(X) QUIT
        ;
EN(X)   ;
        NEW VWCALL
        XECUTE ^VA(200,"VWHSH")  
        QUIT:$L($G(VWCALL))=0 X  ;Short circuit to support LEGACY or NULL hash.
        QUIT $$HOSTPIPE(VWCALL)
        ;
        ; -----------Cache-PIPE-WaveWand------------
OS(CALL) ;
        New ZUT,X
        Set ZUT=$ZUTIL(68,40,1)
        Open CALL:"Q"  Use CALL Read X
        Close CALL
        Set ZUT=$ZUTIL(68,40,ZUT)
        Use 0
        Quit X
       