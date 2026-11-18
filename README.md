# GapGo – Account Feature (Phase 1)

Django full-stack app with PostgreSQL (or Supabase).

## Setup
1. `python -m venv venv` then activate it
2. `pip install -r requirements.txt`
3. Create a PostgreSQL database named `gapgo` (or use your Supabase connection details)
4. Set the environment variables from `.env.example`
5. `python manage.py makemigrations accounts`
6. `python manage.py migrate`
7. `python manage.py createsuperuser`  (superusers are Admins automatically)
8. `python manage.py runserver`

## Roles
- Student: created through the public sign-up form
- Admin: created with `createsuperuser` (or change a user's role in /django-admin/)

## Pages
| URL | Who |
|---|---|
| /register/, /login/ | Everyone |
| /dashboard/ | Logged-in users (redirects by role) |
| /dashboard/student/ | Students only |
| /dashboard/admin/ | Admins only |
| /profile/, /profile/edit/ | Logged-in user (own profile only) |
