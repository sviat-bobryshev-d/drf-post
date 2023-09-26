APP=
ENV=test
lint:
	black ./
	ruff --fix ./

use_secrets:
	cp ./secrets/$(ENV)/.env ./.

up: use_secrets
	docker compose up -d

down:
	docker compose down

migrations:
	python manage.py makemigrations $(APP)
	python manage.py migrate $(APP)
