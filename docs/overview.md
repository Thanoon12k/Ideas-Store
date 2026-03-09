# Project Overview — فِكْرة (Fikra) Ideas Store

## Purpose
Fikra is a personal web application for capturing and organizing future ideas. It supports voice recordings, multiple images, and rich text with auto-detected clickable links.

## Architecture
- **Framework**: Django 4.2 with Django REST Framework
- **Frontend**: Server-rendered templates with Tailwind CSS (CDN) and vanilla JavaScript
- **Database**: SQLite (single-user personal app)
- **Authentication**: Django's built-in auth (superuser only)
- **i18n**: Arabic (RTL) and English with auto-detection

## Design Philosophy
- Ultra-minimalist, beige color palette
- Centered single-column layout
- Distraction-free idea capture
- Main page = New Idea form (instant capture)

## Key Components
1. **Ideas App** — Core CRUD functionality for ideas and images
2. **REST API** — Full RESTful API for future mobile integration
3. **Voice Recorder** — Browser-based audio recording using MediaRecorder API
4. **i18n** — Complete Arabic/English translation with RTL support

## Security
- Login required for all pages
- CSRF protection on all forms
- XSS prevention via HTML escaping and `linkify` filter
- Content-type nosniff, X-Frame-Options, HSTS in production
- File size limits on uploads (10MB voice, 5MB images)

## Data Models

### Idea
| Field | Type | Notes |
|-------|------|-------|
| title | CharField(200) | Required |
| description | TextField | Optional, URLs auto-linked |
| voice_note | FileField | Optional, WebM/WAV |
| created_at | DateTimeField | Auto |
| updated_at | DateTimeField | Auto |

### IdeaImage
| Field | Type | Notes |
|-------|------|-------|
| idea | ForeignKey(Idea) | Cascade delete |
| image | ImageField | Required |
| caption | CharField(200) | Optional |
| uploaded_at | DateTimeField | Auto |

## URL Patterns

### Web Views
| URL | View | Description |
|-----|------|-------------|
| `/` | idea_create | Main page — new idea form |
| `/ideas/` | idea_list | Browse all ideas |
| `/ideas/<pk>/` | idea_detail | View single idea |
| `/ideas/<pk>/edit/` | idea_edit | Edit idea |
| `/ideas/<pk>/delete/` | idea_delete | Delete confirmation |
| `/login/` | LoginView | Authentication |

### API Endpoints
| Method | URL | Description |
|--------|-----|-------------|
| GET/POST | `/api/ideas/` | List/Create ideas |
| GET/PUT/PATCH/DELETE | `/api/ideas/<pk>/` | Idea detail operations |
| POST | `/api/ideas/<pk>/upload-image/` | Upload image |
| GET/POST/DELETE | `/api/images/` | Image operations |
