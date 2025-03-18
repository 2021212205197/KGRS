@echo off
start "前端服务" cmd /k "cd /d my-website && npm run serve"
start "后端服务" cmd /k "cd /d kg_system && myenv\Scripts\activate && python manage.py runserver"
exit