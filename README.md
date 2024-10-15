"# microservice" 

pip install -r .\req.txt

pip-compile req.in

# миграции
alembic revision --autogenerate -m "Создание новой миграции" 

alembic upgrade head
