@echo off
FOR /F "tokens=2 delims= " %%P IN ('tasklist /FO Table /M /NH ^| Find /i "Py"') DO (TASKKILL /PID %%P /F)