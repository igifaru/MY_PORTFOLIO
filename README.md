# NDUNGUTSE David — Portfolio Website

A personal portfolio site built with Django. All content — hero section, bio, skills,
projects, certificates, and social links — is editable through the Django admin, so the
site can be updated without touching any code.

## Features

- **One-page scrolling site** — Home, About, Projects, and Contact are stacked as
  sections on a single page (nav links smooth-scroll between them), with a scroll-spy
  that highlights the active section. Each section also has its own standalone URL
  (`/about/`, `/project/`, `/contact/`) as a fallback.
- **Home** — animated hero section with a typewriter effect over a comma-separated list
  of roles.
- **About** — bio text, a "My CV" button (in-page PDF preview with a download button),
  a "Certificates" button (modal listing uploaded certificates with view links), and a
  "Technical Arsenal" section showing skills as tags grouped by category (no fabricated
  proficiency percentages — just an honest list of what you actually know).
- **Projects** — grid of project cards (2–3 columns depending on screen size), each with
  a detail page (image, technology badge, description, and "View Live"/"View on GitHub"
  buttons when those links are set).
- **Contact** — a form that stores submissions in the database (`ContactMessage`), emails
  them to your inbox via Gmail SMTP, and shows a success message on submit.
- **Admin (CMS)** — every piece of content above (`Bio`, `Project`, `Category`/`Skill`,
  `Certificate`, `ContactMessage`) is managed from `/admin`.
- Dark/light theme toggle (persisted in `localStorage`, light by default) and a
  responsive mobile nav.

## Tech stack

- **Backend**: Django 6.0
- **Database**: SQLite (chosen for zero-setup free hosting — see Deployment below)
- **Email**: Gmail SMTP via `django.core.mail`, credentials from `.env`
- **Images/CV/Certificates**: Pillow, Django's `ImageField`/`FileField` with local media storage
- **Frontend**: server-rendered Django templates, vanilla CSS/JS (no build step),
  Font Awesome icons, Google Fonts (Inter)

## Project structure

```
Django/
├── manage.py
├── requirements.txt
├── .env.example                 # Template for required environment variables
├── myportfolio/                 # Project config
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── myportfolio_App/             # Main (and only) app
│   ├── models.py                # Bio, Project, Category, Skill, Certificate, ContactMessage
│   ├── views.py
│   ├── urls.py
│   ├── admin.py                 # Custom admin/CMS configuration
│   ├── migrations/
│   ├── static/myportfolio_App/css/
│   └── templates/
│       ├── base.html            # Shared layout, nav, footer
│       ├── home.html            # The merged one-page experience
│       └── partials/            # Shared section content (About/Projects/Contact)
└── media/                       # Uploaded images/CV/certificates (gitignored)
```

## Getting started (local development)

### Prerequisites

- Python 3.13+

### 1. Clone and create a virtual environment

```bash
git clone <repo-url>
cd Django
python -m venv env
```

Activate it:

```bash
# Windows
env\Scripts\activate

# macOS/Linux
source env/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure contact-form email (Gmail SMTP)

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
`SECRET_KEY`/`DEBUG`/`ALLOWED_HOSTS` in `.env.example` are production-only — leave them
unset locally.

### 4. Run migrations

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
your Bio, Projects, Skills, and Certificates.

## Content management

Nothing on the site is hardcoded in templates — populate it all from `/admin`:

1. **Bio** — one row only (admin enforces a singleton); fills in the hero, about, and
   footer sections, social links, and CV (PDF only, enforced).
2. **Category** + **Skill** — add categories (e.g. "Backend Development"), then skills
   under each. Categories have a display `order` field; skills just need a name (typed
   with correct casing, e.g. "PostgreSQL", not lowercase).
3. **Certificate** — title, institution, and a PDF file; shown in the "Certificates"
   modal on the About section.
4. **Project** — title, short/long description, technology tag, image, and optional
   `github_link`/`live_link` (either, both, or neither).
5. **Contact Messages** are read-only in the admin — they're created automatically
   from the contact form (and emailed to `CONTACT_RECIPIENT_EMAIL`).

## Deployment (PythonAnywhere free tier)

This project targets PythonAnywhere's free tier specifically because it's genuinely
always-on (no cold-start/sleep like Render or Railway's free tiers) at no cost. That
tier only supports MySQL or SQLite (no PostgreSQL), which is why the project uses
SQLite — it needs no separate database server at all.

1. **Push your latest code to GitHub** (PythonAnywhere clones from there):
   ```bash
   git add -A && git commit -m "Deploy prep" && git push
   ```

2. **Create a free account** at [pythonanywhere.com](https://www.pythonanywhere.com).

3. **Open a Bash console** (from the PythonAnywhere dashboard) and clone your repo:
   ```bash
   git clone https://github.com/<you>/MY_PORTFOLIO.git
   cd MY_PORTFOLIO
   ```

4. **Create a virtualenv and install dependencies:**
   ```bash
   mkvirtualenv --python=/usr/bin/python3.13 myportfolio-env
   pip install -r requirements.txt
   ```
   (If 3.13 isn't available on their image, use the closest available 3.x — check with
   `python3.X` in the console — and adjust the Web tab's Python version to match.)

5. **Create `.env`** in the project root (same keys as `.env.example`), and additionally
   set for production:
   ```
   SECRET_KEY=<generate with: python -c "import secrets; print(secrets.token_urlsafe(50))">
   DEBUG=False
   ALLOWED_HOSTS=<yourusername>.pythonanywhere.com
   ```

6. **Run migrations and collect static files:**
   ```bash
   python manage.py migrate
   python manage.py collectstatic
   python manage.py createsuperuser
   ```

7. **Create a new Web App** on the **Web** tab: choose "Manual configuration", the
   Python version matching your virtualenv, and set the virtualenv path to the one
   created in step 4.

8. **Edit the WSGI configuration file** (linked from the Web tab) — replace its
   contents with something like:
   ```python
   import sys
   path = '/home/<yourusername>/MY_PORTFOLIO'
   if path not in sys.path:
       sys.path.append(path)

   os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myportfolio.settings')
   from django.core.wsgi import get_wsgi_application
   application = get_wsgi_application()
   ```

9. **Set static/media file mappings** on the **Web** tab:
   - URL `/static/` → `/home/<yourusername>/MY_PORTFOLIO/staticfiles`
   - URL `/media/` → `/home/<yourusername>/MY_PORTFOLIO/media`

10. **Reload the web app** (green button on the Web tab) and visit
    `https://<yourusername>.pythonanywhere.com`.

**Known risk to check first**: PythonAnywhere's free tier restricts outbound network
access to a whitelist of external hosts for some protocols. If the contact form's Gmail
SMTP send fails silently in production (check the error log on the Web tab), it's likely
this restriction — the message will still be saved to the database either way, since
email sending is wrapped in a try/except that never blocks the form submission.

## Known limitations

- The contact form has no server-side validation beyond HTML `required` attributes.
- No automated tests yet (`myportfolio_App/tests.py` is empty).
- SQLite is fine for a low-traffic personal site but isn't built for concurrent writes
  at scale — reasonable for this use case, worth revisiting if traffic ever grows a lot.
