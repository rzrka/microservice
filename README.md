"# microservice" 

pip install -r .\req.txt

pip-compile req.in

# миграции
alembic revision --autogenerate -m "Создание новой миграции" 

alembic upgrade head
alembic downgrade -1
admin = root@example.com
password = root


python -m http.server 9000