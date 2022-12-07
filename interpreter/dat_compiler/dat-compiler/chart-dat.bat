set knitoutName=%1
set datname= %knitoutName:~0,-2%.dat
node .\knitout-backend-swg-master\knitout-to-dat.js %knitoutName% %datname%
