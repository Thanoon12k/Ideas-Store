# Models Reference — Fikra Ideas Store

## Entity Relationship

```
┌──────────────┐       ┌──────────────────┐
│     Idea     │       │    IdeaImage      │
├──────────────┤       ├──────────────────┤
│ id (PK)      │  1──M │ id (PK)          │
│ title        │       │ idea_id (FK)     │
│ description  │       │ image            │
│ voice_note   │       │ caption          │
│ created_at   │       │ uploaded_at      │
│ updated_at   │       └──────────────────┘
└──────────────┘
```

## Idea

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | BigAutoField | PK, auto | Primary key |
| title | CharField | max_length=200, required | Idea title |
| description | TextField | blank=True | Full description, URLs auto-linked |
| voice_note | FileField | blank=True, null=True, upload_to='voices/%Y/%m/' | Audio recording |
| created_at | DateTimeField | auto_now_add=True | Creation timestamp |
| updated_at | DateTimeField | auto_now=True | Last update timestamp |

**Ordering**: `-created_at` (newest first)

## IdeaImage

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | BigAutoField | PK, auto | Primary key |
| idea | ForeignKey | on_delete=CASCADE, related_name='images' | Parent idea |
| image | ImageField | upload_to='idea_images/%Y/%m/' | Image file |
| caption | CharField | max_length=200, blank=True | Optional caption |
| uploaded_at | DateTimeField | auto_now_add=True | Upload timestamp |

**Ordering**: `uploaded_at` (oldest first)
**Cascade**: Deleting an Idea deletes all associated IdeaImages.

## File Storage
- Voice notes: `media/voices/YYYY/MM/`
- Images: `media/idea_images/YYYY/MM/`
- Organized by year/month for efficient storage
