SERVICE=bot

build:
	docker-compose up --build -d

logs_bot:
	docker-compose logs -f bot

restart_bot:
	docker-compose restart bot

shell_plus:
	docker-compose exec ${SERVICE} python manage.py shell_plus

quintoandar:
	docker-compose exec ${SERVICE} python quintoandar.py

vivareal:
	docker-compose exec ${SERVICE} python vivareal.py
