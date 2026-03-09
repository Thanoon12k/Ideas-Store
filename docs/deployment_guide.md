# Deployment Guide — PythonAnywhere

## Prerequisites
- PythonAnywhere account (free or paid)
- Git installed on PythonAnywhere

## Step 1: Upload Code

### Option A: Git (Recommended)
```bash
# In PythonAnywhere Bash console
cd ~
git clone <your-repo-url>
cd ideas_store
```

### Option B: Manual Upload
Upload via PythonAnywhere Files tab or ZIP upload.

## Step 2: Create Virtual Environment
```bash
mkvirtualenv --python=/usr/bin/python3.10 fikra-env
pip install -r requirements.txt
```

## Step 3: Configure Settings

Create a `.env` file in the project root:
```bash
cd ~/ideas_store
cat > .env << 'EOF'
DJANGO_SECRET_KEY=generate-a-long-random-secret-key-here
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=yourusername.pythonanywhere.com
CORS_ALLOWED_ORIGINS=https://yourusername.pythonanywhere.com
SECURE_SSL_REDIRECT=True
EOF
```

Generate a secret key:
```python
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

## Step 4: Initialize Database
```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py compilemessages
python manage.py collectstatic --noinput
```

## Step 5: Configure Web App

Go to **Web** tab on PythonAnywhere:

### Source Code
```
/home/yourusername/ideas_store
```

### WSGI Configuration File
Edit the WSGI file to contain:
```python
import os
import sys

path = '/home/yourusername/ideas_store'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

### Virtualenv
```
/home/yourusername/.virtualenvs/fikra-env
```

## Step 6: Configure Static & Media Files

In PythonAnywhere **Web** tab → **Static files**:

| URL | Directory |
|-----|-----------|
| `/static/` | `/home/yourusername/ideas_store/staticfiles` |
| `/media/` | `/home/yourusername/ideas_store/media` |

## Step 7: Reload

Click **Reload** on the Web tab.

## Updating

```bash
cd ~/ideas_store
git pull
workon fikra-env
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
# Reload via Web tab
```

## Troubleshooting

1. **500 Error**: Check error log in Web tab
2. **Static files not loading**: Ensure `collectstatic` ran and paths are correct
3. **Media uploads fail**: Ensure `media/` directory exists and has write permissions
4. **HTTPS issues**: Set `SECURE_SSL_REDIRECT=False` temporarily to debug
