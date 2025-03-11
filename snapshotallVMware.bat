@echo off
setlocal

set Path=C:\Program Files (x86)\VMware\VMware Workstation
set snapname=

set /p snapname=Enter the name for the snapshot:
for /F "skip=1 delims=," %%i in ('vmrun list') do (
    echo Creating Snapshot for %%i and naming it %snapname%
    vmrun -T ws snapshot "%%i" %snapname%
)

endlocal
set /p any=press any key ....
