# cash-management-system-django
A personal cash management web application built with Django for tracking income, expenses, and current balance.

Django Deployment Guide (PythonAnywhere & python-decouple)

A step-by-step production deployment guide tailored for **PythonAnywhere** using **`python-decouple`** for environment variables and **Whitenoise** for static files.

## Phase 1: Local Project Preparation

Before zipping your files, you need to configure your Django project locally to use `python-decouple` and update your settings for PythonAnywhere's environment.

### 1. Install Required Packages

Ensure `python-decouple` and `whitenoise` are installed in your local environment:

```bash
pip install python-decouple whitenoise gunicorn pillow django-cleanup crispy-bootstrap5

```

### 2. Configure Environment Variables (`settings.py`)

Open your `settings.py` file and update it to look like this:

```python
import os
from pathlib import Path
from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent

# Use decouple to read variables
SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)

# Change this to your specific pythonanywhere domain
ALLOWED_HOSTS = ['aatansen.pythonanywhere.com'] 

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # Must be placed here
    'django.middleware.common.CommonMiddleware',
    # ... rest of your middleware
]

# Static files configuration
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles/'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Media files configuration
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media/'

```
Environment variable
For this we can use python-dotenv or python-decouple

python-dotenv

Install it pip install python-dotenv

##Create a .env
```python
SECRET_KEY='write the key here'
DEBUG=False
```
### 3. Configure Routing for Media (`urls.py`)

Ensure your main project `urls.py` is explicitly routing media files using `re_path`:

```python
from django.contrib import admin
from django.conf import settings
from django.views.static import serve
from django.urls import path, include, re_path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('imageApp.urls')), # Your app routes

    # Media file serving path for production
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT})
]

```

### 4. Update and Freeze Requirements

Because PythonAnywhere's latest stable Python version is currently **3.10.x**, it does not support Django 6.0+. **You must explicitly target Django 5.2.x.** Manually create or edit your `requirements.txt` file to match this configuration:

```text
Django==5.2.14
gunicorn==26.0.0
pillow==12.2.0
whitenoise==6.12.0
django-cleanup==9.0.0
crispy-bootstrap5==2026.3
python-decouple==3.8

```

### 5. Generate Static Files and Package Project

Run the compilation command locally since free hosting layers restrict running command executions during deployment:

```bash
python manage.py collectstatic

```

Compress your entire project folder (including the newly generated `staticfiles` folder) into a single file named `imageProject.zip`.

---

## Phase 2: PythonAnywhere Environment Cleanup

> ⚠️ **Warning:** The following step completely wipes existing default configuration files in your PythonAnywhere directory to ensure a clean slate. Do not run this on other servers.

1. Log into your **PythonAnywhere** account.
2. Go to the **Consoles** tab and open a new **Bash** console.
3. Run the following commands to clear the workspace:

```bash
rm -rf ~/*
rm -rf ~/.??*

```

---

## Phase 3: Upload and Unzip Project Files

1. Navigate to the **Files** tab on PythonAnywhere.
2. Upload your `imageProject.zip` file directly to the `/home/aatansen/` root directory.
3. Return to your **Bash console** and extract the file into its own dedicated directory:

```bash
unzip imageProject.zip -d imageProject

```

---

## Phase 4: Create and Setup Virtual Environment

In your active **Bash console**, run these commands sequentially to build your virtual environment and install dependencies:

```bash
# Verify you are running python 3.10
python --version

# Create the virtual environment named .venv inside your project root
cd ~/imageProject
python -m venv .venv

# Activate the virtual environment
source .venv/bin/activate

# Install your specified requirements
pip install -r requirements.txt

```

---

## Phase 5: Setting Up the `.env` File

While still inside your project directory (`/home/aatansen/imageProject`) in the **Bash console**, create your production `.env` configuration file:

```bash
nano .env

```

Paste your production environment variables into the editor (replace with your actual secret key):

```text
SECRET_KEY='your-production-secret-key-here'
DEBUG=False

```

*Press `Ctrl + O` then `Enter` to save, and `Ctrl + X` to exit the nano text editor.*

---

## Phase 6: Web App & WSGI Configuration

1. Navigate to the **Web** tab on the PythonAnywhere dashboard.
2. Click **Add a new web app**.
3. Select **Manual configuration (including virtualenvs)** and choose **Python 3.10**.
4. Set up your system paths under the **Web** tab sections:
* **Source code:** `/home/aatansen/imageProject`
* **Working directory:** `/home/aatansen/imageProject`
* **Virtualenv path:** `/home/aatansen/imageProject/.venv`


5. Find the **Code** section and click the link next to **WSGI configuration file**.
6. Erase all default placeholder code inside the file completely, replace it with the configuration below, and click **Save**:

```python
import sys
sys.path.append('/home/aatansen/imageProject') # path of the project

from imageProject.wsgi import application
```

---

## Phase 7: Finalize Static/Media Slugs & Launch

1. Go back to the **Web** tab.
2. Scroll down to the **Static files** routing table section and map your directories directly so PythonAnywhere can catch assets before hitting Django routing:

| URL | Path |
| --- | --- |
| `/static/` | `/home/aatansen/imageProject/staticfiles/` |
| `/media/` | `/home/aatansen/imageProject/media/` |

3. Scroll back up to the top of the **Web** tab and click the green **Reload** button.

Your application is now live at `https://aatansen.pythonanywhere.com/`.
