uvicorn main:app --host 0.0.0.0 --port 8001 --reload

uvicorn main:app --host 192.168.10.253 --port 8000 --reload

gunicorn -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000 main:app

ssh root@167.99.64.58

pip install -r requirements.txt