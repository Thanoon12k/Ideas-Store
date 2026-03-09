# فِكْرة (Fikra) — Ideas Store

A minimalist Django web application for capturing and organizing future ideas with voice notes, images, and rich descriptions.

## ✨ Features

- **Voice Recording** — Record voice notes directly in the browser
- **Multiple Images** — Attach images to each idea
- **Auto-linkification** — URLs in descriptions become clickable
- **Bilingual** — Full Arabic (RTL) and English support
- **REST API** — Ready for mobile app integration
- **Minimalist Design** — Beige, centered, distraction-free UI

## 🛠 Tech Stack

- **Backend**: Django 4.2, Django REST Framework
- **Frontend**: Tailwind CSS (CDN), Vanilla JavaScript
- **Database**: SQLite
- **Fonts**: Inter, Noto Sans Arabic

## 🚀 Quick Start

### 1. Clone and setup
```bash
git clone <your-repo-url>
cd ideas_store
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Linux/Mac
pip install -r requirements.txt
```

### 2. Configure environment
```bash
# Create .env file (optional for development)
echo DJANGO_SECRET_KEY=your-secret-key-here > .env
echo DJANGO_DEBUG=True >> .env
```

### 3. Initialize database
```bash
python manage.py migrate
python manage.py createsuperuser
```

### 4. Compile translations
```bash
python manage.py compilemessages
```

### 5. Run
```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` — the new idea form loads as the main page.

## 🧪 Run Tests
```bash
python manage.py test tests --verbosity=2
```

## 📁 Project Structure
```
ideas_store/
├── config/          # Django settings, URLs, WSGI
├── ideas/           # Main app (models, views, API, forms)
├── templates/       # HTML templates
├── static/          # CSS, JS, images
├── locale/          # Arabic/English translations
├── tests/           # Separated test files
├── docs/            # Full documentation
└── media/           # User uploads (git-ignored)
```

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/ideas/` | List all ideas |
| POST | `/api/ideas/` | Create an idea |
| GET | `/api/ideas/{id}/` | Get idea details |
| PUT | `/api/ideas/{id}/` | Update idea |
| DELETE | `/api/ideas/{id}/` | Delete idea |
| POST | `/api/ideas/{id}/upload-image/` | Upload image to idea |

## 📄 License

MIT
