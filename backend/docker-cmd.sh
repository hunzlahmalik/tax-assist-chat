#!/bin/sh
# vim:sw=4:ts=4:et

su-exec "$USER" python manage.py collectstatic --noinput

# Creating the first user in the system
USER_EXISTS="from django.contrib.auth import get_user_model; User = get_user_model(); exit(User.objects.exists())"
su-exec "$USER" python manage.py shell -c "$USER_EXISTS" && su-exec "$USER" python manage.py createsuperuser --noinput && su-exec "$USER" python manage.py createsuperuser --email llm@email.com --username llm --no-input

if [ "$1" = "--debug" ]; then
  # Django development server
  exec su-exec "$USER" python manage.py runserver "0.0.0.0:$DJANGO_DEV_SERVER_PORT"
else
  # Gunicorn
  # exec su-exec "$USER" gunicorn "$PROJECT_NAME.wsgi:application" \
  #   --bind "0.0.0.0:$GUNICORN_PORT" \
  #   --workers "$GUNICORN_WORKERS" \
  #   --timeout "$GUNICORN_TIMEOUT" \
  #   --log-level "$GUNICORN_LOG_LEVEL"

  # Start Daphne ASGI server
  exec su-exec "$USER" daphne -b 0.0.0.0 -p $GUNICORN_PORT "backend.asgi:application"
fi
