req:
	pip install -r requirements.txt
migrate:
	alembic upgrade head
start:
	cd src && uvicorn main:create_app --reload
cw:
	cd src && celery -A tasks.tasks:celery worker -l info
cf:
	cd src && celery -A tasks.tasks:celery flower