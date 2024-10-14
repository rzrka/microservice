"# microservice" 

pip install -r .\req.txt

pip-compile req.in

# миграции

alembic upgrade head