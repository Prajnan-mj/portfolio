# prajnan.dev — portfolio

Personal portfolio of **Prajnan MJ** — applied AI & full-stack engineering.
Django 5 · editorial "neural mesh" design · parallax artwork · admin-driven content.

## Stack

- **Backend:** Django 5, SQLite locally / PostgreSQL on Render
- **Frontend:** hand-rolled CSS + vanilla JS (parallax, scroll reveals, cursor previews)
- **Fonts:** Fraunces · Inter · JetBrains Mono
- **Deploy:** Render (gunicorn + WhiteNoise), one-click via `render.yaml`

## Run locally

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows  (source .venv/bin/activate on mac/linux)
pip install -r requirements.txt
python manage.py migrate
python manage.py seed            # loads profile, projects, skills, timeline, sample post
python manage.py createsuperuser
python manage.py runserver
```

Open http://127.0.0.1:8000 — admin at http://127.0.0.1:8000/admin/.

## Editing content

Everything on the site lives in the database and is edited from the Django admin:

| Model | What it controls |
|---|---|
| **Site profile** | Name, hero text, about, email, socials, resume, background theme (3 mesh variants) |
| **Projects** | Work section rows — tag, description, stack pills, links, hover preview image |
| **Skills** | Toolkit section + the scrolling marquee |
| **Timeline entries** | "Path so far" section |
| **Blog posts** | `/writing/` — publish toggle, auto slug, reading time |
| **Contact messages** | Submissions from the contact form (read-only) |

The seed command is **non-destructive** — it only creates rows that don't
exist yet, so redeploys never overwrite admin edits.

## Deploy to Render

1. Push this folder to a GitHub repository.
2. In Render: **New → Blueprint**, pick the repo — `render.yaml` provisions
   the web service + free PostgreSQL automatically.
3. In the service's **Environment** tab set `DJANGO_SUPERUSER_USERNAME` and
   `DJANGO_SUPERUSER_PASSWORD` — the build creates your admin login.
4. Done. Every push redeploys.

### Notes

- **Uploaded files** (resume PDF, project images) live on an ephemeral disk on
  Render's free tier and reset on redeploy. Durable options: use the
  `resume_url` field (Google Drive/GitHub link) and `image_static` paths
  (files committed under `static/img/`), which both survive deploys.
- **Contact form email:** messages are always saved to the database. To also
  receive email, set `EMAIL_HOST`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`
  (e.g. a Gmail app password with `EMAIL_HOST=smtp.gmail.com`).

## Design

Based on the "neural mesh" concept — ink-on-paper constellation artwork
(2560×8000) that parallax-scrolls behind the content, with three switchable
variants (Breathing / Drift / Journey) selectable from the admin.
