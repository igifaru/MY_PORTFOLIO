# NDUNGUTSE David — Portfolio Website

A personal portfolio site built with Django. All content — hero section, bio, skills,
services, projects, and social links — is editable through the Django admin, so the
site can be updated without touching any code.

## Features

- **Home** — animated hero section with a typewriter effect over a comma-separated list
  of roles, social links, CV download button, and a grid of latest projects.
- **About** — bio text plus a technical skills section grouped by category, each skill
  rendered as a proficiency progress bar.
- **Services** — an ordered list of offered services, each linking to the contact page.
- **Portfolio** — full project grid with a dedicated detail page per project
  (image, technology badge, long description, live link).
- **Contact** — a form that stores submissions in the database (`ContactMessage`), emails
  them to your inbox via Gmail SMTP, and shows a success message on submit.
- **Admin (CMS)** — every piece of content above (`Bio`, `Project`, `Category`/`Skill`,
  `Service`, `ContactMessage`) is managed from `/admin`, including inline skill editing
  under each category and image previews for projects.
- Dark/light theme toggle (persisted in `localStorage`) and a responsive mobile nav.

## Tech stack

- **Backend**: Django 6.0
- **Database**: PostgreSQL (via `psycopg2-binary`)
- **Images/CV**: Pillow, Django's `ImageField`/`FileField` with local media storage
- **Frontend**: server-rendered Django templates, vanilla CSS/JS (no build step),
  Font Awesome icons, Google Fonts (Inter)

## Project structure

```
Django/
├── manage.py
├── requirements.txt
├── myportfolio/                # Project config
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── myportfolio_App/            # Main (and only) app
│   ├── models.py               # Bio, Project, Category, Skill, Service, ContactMessage
│   ├── views.py
│   ├── urls.py
│   ├── admin.py                # Custom admin/CMS configuration
│   ├── migrations/
│   ├── static/myportfolio_App/css/
│   └── templates/              # base.html + one template per page
└── media/                      # Uploaded images/CV (created at runtime, gitignored)
```

## Getting started

### Prerequisites

- Python 3.13+
- PostgreSQL (running locally, or update the connection settings to point elsewhere)

### 1. Clone and create a virtual environment

```bash
git clone <repo-url>
cd Django
python -m venv myport_env
```

Activate it:

```bash
# Windows
myport_env\Scripts\activate

# macOS/Linux
source myport_env/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure the database

Create a Postgres database matching `myportfolio/settings.py` (`DATABASES`), or edit
that block to match your own local setup:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'portifolio',
        'USER': 'postgres',
        'PASSWORD': 'newsecurepassword123',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}
```

```bash
# with psql or any Postgres client
createdb portifolio
```

### 4. Configure contact-form email (Gmail SMTP)

Copy `.env.example` to `.env` and fill in your real Gmail address and an
[App Password](https://myaccount.google.com/apppasswords) (requires 2-Step Verification
on the Google account — a regular Gmail password will not work here):

```bash
cp .env.example .env
```

```
EMAIL_HOST_USER=your.email@gmail.com
EMAIL_HOST_PASSWORD=your16digitapppassword
CONTACT_RECIPIENT_EMAIL=ndungutsedavid12@gmail.com
```

`.env` is gitignored — never commit real credentials. Without it, the contact form
still saves messages to the database, it just won't be able to send the email.

### 5. Run migrations

```bash
python manage.py migrate
```

### 5. Create an admin user

```bash
python manage.py createsuperuser
```

### 6. Run the server

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` for the site and `http://127.0.0.1:8000/admin/` to add
your Bio, Projects, Skills, Services, etc.

## Content management

Nothing on the site is hardcoded in templates — populate it all from `/admin`:

1. **Bio** — one row only (admin enforces a singleton); fills in the hero, about, and
   footer sections plus social links and CV.
2. **Category** + **Skill** — add categories (e.g. "Backend"), then skills under each
   with a proficiency percentage.
3. **Service** — one row per service offered, with a FontAwesome icon class (e.g.
   `fas fa-code`) and a display order.
4. **Project** — title, short/long description, technology tag, image, and optional
   live link.
5. **Contact Messages** are read-only in the admin — they're created automatically
   from the contact form.

## Known limitations

- `SECRET_KEY` and the database password are hardcoded in `settings.py` and `DEBUG=True`
  — fine for local development, but both should move to environment variables
  (e.g. via `django-environ` or `os.environ`) before any real deployment, along with
  setting `ALLOWED_HOSTS` and `DEBUG=False`.
- The contact form has no server-side validation beyond HTML `required` attributes,
  and submissions aren't emailed anywhere — they're only stored in the database.
- No automated tests yet (`myportfolio_App/tests.py` is empty).
