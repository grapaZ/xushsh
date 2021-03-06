XUSHSH  ;IA/GpZ-ROBUST(PBKDF2)HASHING UTILITY v1.0; 10/11/2012;
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
        ;SET VWCALL="python /home/vista/bin/xushsh.py --data="_X
        ; hardcoded option.
        QUIT:$L($G(VWCALL))=0 X  ;Short circuit to support LEGACY or NULL hash.
        QUIT $$OS(VWCALL)
        ;
        ; -----------GT.M-PIPE-Magic----------------
OS(CALL) ;
        New X
        Open "PIPE":(command=CALL:READONLY)::"PIPE"
        Use "PIPE" READ X
        Close "PIPE"
        Use 0
        QUIT X
