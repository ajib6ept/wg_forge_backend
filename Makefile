cat_colors_stat:
	poetry run python manage.py cat_colors_stat

cat_stats:
	poetry run python manage.py cat_stats

install:
	poetry install

lint:
	poetry run flake8 WGForge --exclude=WGForge/settings.py

start_server:
	poetry run python manage.py runserver 127.0.0.1:8080

test:
	poetry run python manage.py test
