import os

print("현재 작업 경로:", os.getcwd())
print("app 폴더 존재 여부:", os.path.isdir("app"))
print("app/__init__.py 존재 여부:", os.path.isfile("app/__init__.py"))
print("app/daily_worker_eligibility.py 존재 여부:", os.path.isfile("app/daily_worker_eligibility.py"))
