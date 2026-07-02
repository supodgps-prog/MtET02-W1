@echo off
title Running Python Calculator
echo Launching Your Python Script...
echo.

:: ย้ายไดเรกทอรีไปยังโฟลเดอร์ของโค้ดที่ถูกต้อง
cd /d "D:\Work3\Kmutnb\2526\IoT\Code\Week1_2"

:: รันไฟล์ Python
python cal.py

:: ปิดหน้าต่าง Command Prompt ทันทีหลังจากปิดโปรแกรมเครื่องคิดเลข
exit
