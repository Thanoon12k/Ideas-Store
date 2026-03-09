# API Reference — Fikra Ideas Store

## Base URL
```
http://your-domain.com/api/
```

## Authentication
All API endpoints require authentication. Two methods are supported:

### Session Authentication
Log in via the web interface — cookies are sent automatically.

### Token Authentication
```bash
# Get token (create manually in Django admin or via createsuperuser)
curl -H "Authorization: Token YOUR_TOKEN_HERE" http://localhost:8000/api/ideas/
```

---

## Ideas Endpoints

### List Ideas
```
GET /api/ideas/
```
**Response** (200):
```json
{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "title": "My First Idea",
            "description": "A great idea for the future",
            "voice_note": "/media/voices/2024/01/voice.webm",
            "created_at": "2024-01-15T10:30:00Z",
            "updated_at": "2024-01-15T10:30:00Z",
            "images": [
                {
                    "id": 1,
                    "image": "/media/idea_images/2024/01/photo.png",
                    "caption": "Sketch",
                    "uploaded_at": "2024-01-15T10:30:00Z"
                }
            ]
        }
    ]
}
```

### Create Idea
```
POST /api/ideas/
Content-Type: multipart/form-data
```
**Fields**:
| Field | Required | Type |
|-------|----------|------|
| title | Yes | string (max 200) |
| description | No | string |
| voice_note | No | audio file |

**Response** (201):
```json
{
    "id": 2,
    "title": "New Idea",
    "description": "Description here",
    "voice_note": null
}
```

### Get Idea Details
```
GET /api/ideas/{id}/
```

### Update Idea
```
PUT /api/ideas/{id}/
PATCH /api/ideas/{id}/
```

### Delete Idea
```
DELETE /api/ideas/{id}/
```
**Response** (204): No content

---

## Image Endpoints

### Upload Image to Idea
```
POST /api/ideas/{id}/upload-image/
Content-Type: multipart/form-data
```
**Fields**:
| Field | Required | Type | Limit |
|-------|----------|------|-------|
| image | Yes | image file | 5 MB |
| caption | No | string (max 200) | — |

**Response** (201):
```json
{
    "id": 1,
    "image": "/media/idea_images/2024/01/photo.png",
    "caption": "My sketch",
    "uploaded_at": "2024-01-15T10:30:00Z"
}
```

### List All Images
```
GET /api/images/
```

### Delete Image
```
DELETE /api/images/{id}/
```

---

## Error Responses

### 400 Bad Request
```json
{"title": ["This field is required."]}
```

### 403 Forbidden
```json
{"detail": "Authentication credentials were not provided."}
```

### 404 Not Found
```json
{"detail": "Not found."}
```

## Pagination
All list endpoints use page-based pagination (20 items per page):
```
GET /api/ideas/?page=2
```
