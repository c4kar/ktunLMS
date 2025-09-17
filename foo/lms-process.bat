@echo off
rem Bu betik, Python isleme betigini calistirir.
rem Arguman olarak verilen goreceli klasor adini tam yola cevirir.

set "target_dir=%~f1"
python "D:\Diger\code\ktunLMS\foo\process_images.py" "%target_dir%"
