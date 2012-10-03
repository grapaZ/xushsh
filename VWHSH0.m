VWHSH0  ;IOWA/GpZ- IMPROVED HASHING UTILITY v0.9 MAIN INSTALL MODULE; 10/2/12 10:42am
V       ;;8.0;KERNEL;;Jul 10, 1995
        ;;
        ; -------------------------------------
        ; TEST : Check current installation.
        ; SAVEOLD : Move XUSHSH --> VWHSHLEG
        ; BUILD() : Write ^VA(200,"VWHSH"),^%ZOSF("VWHSH") array (duplicate)
        ; MOVEIN : Install VWXHSH --> XUSHSH
        ; BUILD("PBKPLUS") : post conversion adjustment
        ;
        ; -------------------------------------
TEST    ; What hash is installed?
        ;New I,X,%S,%D,%ZR,HSH,HASH,HASHLIST,MUMPS,OS,PATH,SCR,ZTOS
        ;
        ; What is currently installed on this host?
        Set HASH=$$EN^XUSHSH("test") Do
        . SET HASH=$Select(HASH="test":"NONE",HASH="115116101116":"LEGACY",HASH["pbkdf2":"PBKDF2",1:"OOPS!")
        . Write !!,"HASH is "_HASH,!
        . Quit
        If HASH="OOPS!" Do  QUIT
        . Write ?20,"Old ^XUSHSH may not be compatable.",!!
        . Write "This system is already running a modified hashing algorithm.",!
        . Write "HALTING INSTALL",!!
        . Quit
        If HASH="PBKDF2" Do  Quit
        . Write "We may not want to install PBKDF2 on top of itself.",!
        . Write "Proceed only if you know what you want to accomplish.",!
        . Quit
        ;
        Write !,"OK, current HASH is identified as ",HASH,".",!
        Quit
        ; -------------------------------------
SAVEOLD ; Archive current version of XUSHSH to VWHSHLEG
        If $L($Text(^VWHSHLEG)) Do  Quit
        . Write "Archive routine ^VWHSHLEG already exists.",!
        . Write "Must be deleted or renamed before this installation can continue.",!
        . Quit
        Set U="^",SCR="I 1",MUMPS=^%ZOSF("OS"),ZTOS=$S(MUMPS["GT.M":8,MUMPS["OpenM":3)
        Set %S="XUSHSH",%D="VWHSHLEG"
        Do MOVE^ZTMGRSET
        Quit
        ;
        ; -------------------------------------
BUILD(DEFAULT)  ; Set up defaults for LEGACY, NONE/NULL, PBKDF2 hashes
        New X,I
        Set:'$L($G(DEFAULT)) DEFAULT="LEGACY"
        For I=4:1:8 Set X=$P($Text(BUILD+I),"; ",2,99) Set HASH($P(X," ",1))=$P(X," ",2,99)
        ; LINUX SET VWCALL="python /home/vista/bin/xushsh.py --input="_X XECUTE ^VA(200,"VWHSH","LEGACY")
        ; WINDOWS Set VWCALL="C:\Python27\python C:\Python27\xushsh.py --input="_X XECUTE ^VA(200,"VWHSH","LEGACY")
        ; LEGACY KILL VWCALL SET X=$$EN^VWHSHLEG(X)
        ; NONE KILL VWCALL
        ; PBKDF2 SET VWCALL=VWCALL_" --hash=pbkdf2" XECUTE ^VA(200,"VWHSH","SALT")
        ;
        Set HASH=$Select($ZV["Linux":HASH("LINUX"),1:HASH("WINDOWS"))
        Kill HASH("LINUX"),HASH("WINDOWS")
        Set HASH(0)=HASH(DEFAULT)
        ;;Kill ^%ZOSF("VWHSH") Merge ^%ZOSF("VWHSH")=HASH
        Kill ^VA(200,"VWHSH") Merge ^VA(200,"VWHSH")=HASH
        QUIT
        ;
RESET(DEFAULT) ; Change only top node
        Set ^VA(200,"VWHSH",0)=^VA(200,"VWHSH",DEFAULT)
        QUIT
        ; -------------------------------------
MOVEIN  ;
        NEW %D,%S,MUMPS,SCR,ZTOS
        Set U="^",SCR="I 1",MUMPS=^%ZOSF("OS"),ZTOS=$S(MUMPS["GT.M":8,MUMPS["OpenM":3)
        Set %S="VWHSH"_ZTOS,%D="XUSHSH"
        Do MOVE^ZTMGRSET
        Quit
        ;
        ; -------------------------------------
REVERT  ;
        New X,Y
        Set X="VWH VA(200) "
        F  Set X=$Order(^XTMP(X)) Quit:X'["VWH VA"  Do
        . Set Y=X
        . Write Y,!
        . Quit
        If $Get(Y)'["VWH VA" Write "Nothing stored yet." Quit
        Write "Returning to Latest entry: ",!
        Write "^XTMP("_Y_"0) = ",!,?10,^XTMP(Y,0),!
        Write !!,"Do you wish to proceed now? //Yes/No "
        Read OK Quit:OK'="Yes"
        Kill ^VA(200) Merge ^VA(200)=^XTMP(Y,200)
        Quit
        ;
KILL    ;
        ; PLEASE do not run this by accident.
        ; REMOVES ^XTMP BACKUP NODE(S).
        ;
        Set X="VWH VA(200) "
        For  Set X=$Order(^XTMP(X)) w X,!! Quit:X'["VWH VA(200)"  Do
        . Write ^XTMP(X,0),!
        . Write "Are we certain we want to kill this backup? //Yes/No "
        . Read OK Quit:OK'="Yes"
        . Kill ^XTMP(X) 
        . Quit
        Quit
        ;
CONVERT ; Allows "NONE" or "PBKDF2"
        ;New %H,X,Y,Z,HSH,ACODE,AOLD,FROM,VCODE,VOLD,D0,NODE,NOW,XT
        Do TEST^VWHSH0
        Set FROMHASH=HASH
        Set TOHASH="NONE"
        ;;Set X="test"
        X ^VA(200,"HASH")
        X ^VA(200,"HASH",TOHASH)
        quit     ;;;;;;;;;;;;;;;;;;;;;;;;;;;
        Set U="^"
        ; ---------------------------------------------------------
        ; Copy/Backup ^VA(200) before modifying default HASH
        Set NOW=$$NOW^XLFDT,NODE="^XTMP(""VWH VA(200) "_NOW_""","
        Set @(NODE_"0)")=$$FMADD^XLFDT($$DT^XLFDT,2,0,0,0)_U_NOW_U_FROMHASH
        Merge @(NODE_"200)")=^VA(200)
        ; ---------------------------------------------------------
        ;
        ; Access Code and "A" cross reference:
        Kill ^VA(200,"A") ;;                                                                      < KILLING "A" >
        Set D0=.99
        For  Set D0=$Order(^VA(200,D0)) Quit:D0<1  Do  ;; $Order down NEW PERSON list
        . Set ACODE=$P(^VA(200,D0,0),U,3) Do:ACODE]""
        . . Set %H=$Select($D(@(NODE_"200,""A"",ACODE,D0)")):^(D0),1:+$H) ;; If "A" index incomplete set to today.
        . . Set ACODE=$$MK(ACODE)
        . . Write D0,"  ",$E("************",0,$Length(ACODE)),!
        . . Set $P(^VA(200,D0,0),U,3)=ACODE Quit:ACODE=""  ;;                         < SET Access Code >
        . . Set ^VA(200,"A",ACODE,D0)=%H
        . . Quit
        . ;
        . ; Verify Code
        . If $Length($Get(^VA(200,D0,.1))) Do
        . . Set VCODE=$Piece(^VA(200,D0,.1),U,2)
        . . If VCODE]"" Set $Piece(^VA(200,D0,.1),U,2)=$$MK(VCODE)  ;;               < SET Verify Code >
        . . Quit
        . ;
        . Quit
VOLD    ;
        W "VOLD",!
        ; "VOLD" cross reference
        S D0=.99 F  Set D0=$Order(^VA(200,D0)) Quit:D0<1  Do:$D(^VA(200,D0,"VOLD"))>9
        . Kill ^VA(200,D0,"VOLD") ;;                                                   < KILL D0,"VOLD" >
        . Set VOLD="" For  Set VOLD=$Order(@(NODE_"200,"_D0_",""VOLD"",VOLD)")) Quit:VOLD=""  Do
        . . Set XT=$$MK(VOLD) Quit:XT=""
        . . Set ^VA(200,D0,"VOLD",XT)=@(NODE_"200,"_D0_",""VOLD"",VOLD)")
        . . Quit
        . Quit
        ;
AOLD    ; "AOLD" cross reference
        Kill ^VA(200,"AOLD") ;;                                                         < KILL "AOLD" >
        Set AOLD=""
        For  Set AOLD=$Order(@(NODE_"200,""AOLD"",AOLD)")) Quit:AOLD=""  Do
        . Set D0=.99 F  Set D0=$Order(@(NODE_"200,""AOLD"",AOLD,D0)")) Quit:+D0=0  Do
        . . Set XT=$$MK(AOLD) Quit:XT=""
        . . Set ^VA(200,"AOLD",XT,D0)=@(NODE_"200,""AOLD"",AOLD,D0)")
        . Quit
        ;;Set $Piece($Piece(^VA(200,"HASH"),""")"),",""",2)=TOHASH
        Set $Piece(^VA(200,"HASH")," X ",2)="^(""""HASH"""","""""_TOHASH_""""")"
        Quit
        ;
MK(X)   ;
        IF FROMHASH="LEGACY" W !,X S X=$$UN(X) W "   "_X QUIT:TOHASH="NONE" X
        Set X=$$CMD^XUSHSH(PYTHON,PARAMS,X)
         W "  "_X
        Q X
        ;
        ;------------Unhash Legacy-------------------
UN(X)   ;TMG/kst - UNHASH, reverses FOIA ASCII encoding
        New %HASH Set %HASH=""
        New %TMP Set %TMP=""
        New %DIGIT Set %DIGIT=""
        New I
        For I=1:1:$L(X) Do
        . Set %DIGIT=%DIGIT_$E(X,I)
        . If (+%DIGIT>31) Do
        . . Set %TMP=%TMP_$char(%DIGIT)
        . . Set %DIGIT=""
        For I=$L(%TMP):-1:1 Do
        . If I#2 Do
        . . Set %HASH=$E(%TMP,1)_%HASH          ;"get 1st char
        . . Set %TMP=$E(%TMP,2,$L(%TMP))        ;"trim off 1st char
        . else  Do
        . . Set %HASH=$E(%TMP,$L(%TMP))_%HASH   ;"get last char
        . . Set %TMP=$E(%TMP,1,$L(%TMP)-1)      ;"trim last char
        Quit %HASH
        ;;
        ;; GNU Affero General Public License, see ^VWHSH
        ;;
       
