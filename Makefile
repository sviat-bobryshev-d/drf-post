APP=

lint:
	black ./
	ruff --fix ./

up:
	python manage.py runserver

migrations:
	python manage.py makemigrations $(APP)
	python manage.py migrate $(APP)
