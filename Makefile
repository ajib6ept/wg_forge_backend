cat_colors_stat:
	@docker-compose -f docker-compose.yml exec web python manage.py cat_colors_stat

cat_stats:
	@docker-compose -f docker-compose.yml exec web python manage.py cat_stats

install:
	poetry install

lint:
	poetry run flake8 WGForge --exclude=migrations,WGForge/settings.py

start_server:
	poetry run python manage.py runserver 127.0.0.1:8080

test:
	poetry run python manage.py test

test_coverage:
	poetry run coverage run --source='WGForge' manage.py test
	poetry run coverage xml
	poetry run coverage report
