SERVICE=bot

shell_plus:
	docker-compose exec ${SERVICE} python manage.py shell_plus