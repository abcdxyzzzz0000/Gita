# Bhagavad Gita Learning Application - Fullstack Architecture Document

<!-- Powered by BMAD™ Core -->

## Introduction

This document outlines the complete fullstack architecture for the Bhagavad Gita Learning Application, including backend systems, frontend implementation, RAG pipeline, and their integration. It serves as the single source of truth for AI-driven development, ensuring consistency across the entire technology stack.

This architecture is designed to deliver a calm, mentor-like learning experience for students aged 12-22, using entirely open-source technologies to provide AI-powered Gita wisdom grounded strictly in authentic text.

### Starter Template or Existing Project

**Status**: N/A - Greenfield project

This is a new application built from scratch with no existing codebase or starter template dependencies.

### Change Log

| Date | Version | Description | Author |
|------|---------|-------------|--------|
| 2026-01-17 | 1.0 | Initial architecture document | BMad Team |

---

## High Level Architecture

### Technical Summary

The Bhagavad Gita Learning Application follows a **monolithic architecture with modular design**, deployed as Docker containers for consistent environments. The frontend uses **React Native with Expo** for cross-platform mobile (iOS/Android) and web support, while the backend leverages **Python FastAPI** for high-performance async API services. The core intelligence comes from a **RAG (Retrieval-Augmented Generation) pipeline** using FAISS vector store and Ollama-hosted LLM (Mistral 7B) to provide hallucination-free explanations grounded in actual Gita text. Data persistence uses **PostgreSQL** for user data and bookmarks, with **Redis** for caching and task scheduling via Celery. The architecture prioritizes low infrastructure costs, offline-first mobile experience, and sub-2-second RAG response times while maintaining strict religious authenticity.

### Platform and Infrastructure Choice

**Platform**: Self-hosted / Cloud-agnostic (Docker-based)

**Rationale**: Given the open-source constraint (NFR1) and cost-consciousness (NFR6), we avoid vendor lock-in by using containerized deployment that can run on any cloud provider (AWS, GCP, Azure, DigitalOcean) or on-premises infrastructure. This approach:
- Eliminates proprietary service dependencies
- Keeps costs predictable and low
- Enables easy migration between providers
- Supports local development with identical environments

**Key Services**:
- **Compute**: Docker containers (FastAPI backend, Ollama LLM)
- **Database**: PostgreSQL (managed or self-hosted)
- **Cache/Queue**: Redis (for caching and Celery task queue)
- **Storage**: Local file system (mounted volumes for audio files)
- **CDN** (Future): CloudFlare or similar for static asset delivery

**Deployment Host and Regions**: 
- Initial: Single region deployment (recommend US-East or Asia-Pacific based on target audience)
- Future: Multi-region for global scale


### Repository Structure

**Structure**: Monorepo

**Monorepo Tool**: npm workspaces (lightweight, no additional dependencies)

**Package Organization**:
```
bhagavad-gita-app/
├── frontend/          # React Native mobile app
├── backend/           # FastAPI backend
├── shared/            # Shared types and constants
└── infrastructure/    # Docker configs and deployment scripts
```

**Rationale**: Monorepo simplifies dependency management, enables code sharing (TypeScript types, constants), and coordinates versioning between frontend and backend. npm workspaces provides sufficient functionality without additional tooling overhead.

### High Level Architecture Diagram

```mermaid
graph TB
    subgraph "Client Layer"
        Mobile[Mobile App<br/>React Native + Expo]
        Web[Web App<br/>React Native Web]
    end
    
    subgraph "API Gateway"
        FastAPI[FastAPI Backend<br/>Uvicorn Server]
    end
    
    subgraph "Application Services"
        Auth[Auth Service<br/>JWT + OAuth]
        Content[Content Service<br/>Chapters/Shlokas]
        RAG[RAG Service<br/>AI Explanations]
        Notif[Notification Service<br/>Celery Tasks]
    end
    
    subgraph "Data Layer"
        PG[(PostgreSQL<br/>User Data)]
        FAISS[(FAISS<br/>Vector Store)]
        Redis[(Redis<br/>Cache + Queue)]
        Files[File Storage<br/>Audio Files]
    end
    
    subgraph "AI Layer"
        Ollama[Ollama<br/>Mistral 7B LLM]
        Embeddings[Sentence-Transformers<br/>Embeddings Model]
    end
    
    Mobile --> FastAPI
    Web --> FastAPI
    FastAPI --> Auth
    FastAPI --> Content
    FastAPI --> RAG
    FastAPI --> Notif
    
    Auth --> PG
    Content --> PG
    Content --> Redis
    Content --> Files
    
    RAG --> FAISS
    RAG --> Ollama
    RAG --> Redis
    
    Notif --> Redis
    Notif --> PG
    
    FAISS --> Embeddings
```

### Architectural Patterns

- **Monolithic Modular Architecture**: Single deployable unit with clear module boundaries (auth, content, RAG, notifications) - _Rationale:_ Simplifies deployment and reduces operational complexity for Phase 1 while maintaining code organization for future service extraction

- **Repository Pattern**: Abstract data access logic behind repository interfaces - _Rationale:_ Enables testing with mock repositories and provides flexibility for future database changes

- **RAG (Retrieval-Augmented Generation)**: Combine vector similarity search with LLM generation constrained to retrieved context - _Rationale:_ Prevents hallucinations by grounding AI responses strictly in actual Gita text (NFR7)

- **Offline-First Mobile**: Cache content locally with background sync - _Rationale:_ Ensures usability without constant connectivity, critical for mobile learning experience (FR14)

- **Component-Based UI**: Reusable React Native components with TypeScript - _Rationale:_ Maintainability, type safety, and cross-platform code sharing

- **API-First Design**: Well-defined REST API contracts between frontend and backend - _Rationale:_ Enables independent development and testing of frontend/backend

- **Async Task Queue**: Celery with Redis for scheduled tasks (daily wisdom, notifications) - _Rationale:_ Decouples long-running tasks from API request/response cycle

---

## Tech Stack

### Technology Stack Table

| Category | Technology | Version | Purpose | Rationale |
|----------|-----------|---------|---------|-----------|
| Frontend Language | TypeScript | 5.3+ | Type-safe frontend development | Catches errors at compile time, improves maintainability |
| Frontend Framework | React Native | 0.73+ | Cross-platform mobile app | Single codebase for iOS, Android, and web |
| Frontend Runtime | Expo | SDK 50+ | React Native tooling and services | Simplifies build process, provides useful APIs |
| UI Component Library | React Native Paper | 5.11+ | Material Design components | Consistent, accessible UI components |
| State Management | Zustand | 4.4+ | Lightweight state management | Simple API, minimal boilerplate, TypeScript support |
| Navigation | React Navigation | 6.1+ | Mobile navigation | De facto standard for React Native navigation |
| Backend Language | Python | 3.11+ | Backend development | Excellent ML/AI library ecosystem |
| Backend Framework | FastAPI | 0.109+ | High-performance async API | Fast, automatic OpenAPI docs, async support |
| API Server | Uvicorn | 0.27+ | ASGI server for FastAPI | High-performance async server |
| API Style | REST | - | HTTP API design | Simple, well-understood, cacheable |
| Database | PostgreSQL | 15+ | Relational data storage | Robust, open-source, excellent for user data |
| ORM | SQLAlchemy | 2.0+ | Database abstraction | Mature ORM with async support |
| Cache | Redis | 7.2+ | Caching and task queue | Fast in-memory storage, Celery backend |
| Task Queue | Celery | 5.3+ | Async task scheduling | Reliable task scheduling for notifications |
| File Storage | Local File System | - | Audio file storage | Simple, no external dependencies for Phase 1 |
| Vector Store | FAISS | 1.7+ | Similarity search | Fast, open-source, CPU-optimized |
| Embeddings | Sentence-Transformers | 2.3+ | Text embeddings | Open-source, all-MiniLM-L6-v2 model |
| LLM Runtime | Ollama | 0.1+ | Local LLM hosting | Run open-source LLMs locally, no API costs |
| LLM Model | Mistral 7B | 0.2 | Text generation | Better instruction following than LLaMA, faster |
| PDF Processing | pdfplumber | 0.10+ | Extract text from PDF | Reliable PDF text extraction |
| Authentication | JWT + OAuth2 | - | User authentication | Stateless auth, Google OAuth support |
| Password Hashing | bcrypt | 4.1+ | Secure password storage | Industry standard password hashing |
| Frontend Testing | Jest + React Native Testing Library | 29+ / 12+ | Unit and component tests | Standard React Native testing tools |
| Backend Testing | pytest | 7.4+ | Backend unit/integration tests | Powerful Python testing framework |
| E2E Testing | Manual | - | End-to-end testing | Manual testing for Phase 1, automated later |
| Build Tool | npm | 10+ | Package management | Standard Node.js package manager |
| Bundler | Metro | 0.80+ | React Native bundler | Built into React Native/Expo |
| Containerization | Docker | 24+ | Consistent environments | Reproducible deployments |
| Container Orchestration | Docker Compose | 2.24+ | Local multi-container setup | Simple orchestration for development |
| CI/CD | GitHub Actions | - | Automated testing and deployment | Free for public repos, integrated with GitHub |
| Monitoring | Prometheus + Grafana | Latest | Metrics and dashboards | Open-source monitoring stack |
| Logging | Python logging + Loki | - | Centralized logging | Structured logging with aggregation |
| CSS Framework | StyleSheet API | - | React Native styling | Built-in styling system |
| HTTP Client | Axios | 1.6+ | API requests | Robust HTTP client with interceptors |

---


## Data Models

### User

**Purpose**: Represents authenticated users of the application, supporting both email/password and Google OAuth authentication.

**Key Attributes**:
- `id`: UUID - Unique user identifier
- `email`: string - User's email address (unique)
- `hashed_password`: string (nullable) - Bcrypt hashed password (null for OAuth users)
- `oauth_provider`: string (nullable) - OAuth provider name ("google" or null)
- `oauth_id`: string (nullable) - Provider's user ID
- `created_at`: timestamp - Account creation time
- `last_login`: timestamp - Last login time
- `notification_enabled`: boolean - Daily notification preference
- `notification_time`: time - Preferred notification time (default 08:00)

#### TypeScript Interface

```typescript
interface User {
  id: string;
  email: string;
  oauthProvider?: 'google' | null;
  createdAt: Date;
  lastLogin: Date;
  notificationEnabled: boolean;
  notificationTime: string; // HH:MM format
}
```

#### Relationships
- One-to-many with Bookmark
- One-to-many with ReadingProgress

### Bookmark

**Purpose**: Tracks user-saved shlokas for quick access and personal collection building.

**Key Attributes**:
- `id`: UUID - Unique bookmark identifier
- `user_id`: UUID - Foreign key to User
- `chapter`: integer - Chapter number (1-18)
- `shloka_number`: integer - Shloka number within chapter
- `created_at`: timestamp - When bookmark was created

#### TypeScript Interface

```typescript
interface Bookmark {
  id: string;
  userId: string;
  chapter: number;
  shlokaNumber: number;
  createdAt: Date;
}
```

#### Relationships
- Many-to-one with User
- References Shloka (conceptual, not FK)

### ReadingProgress

**Purpose**: Tracks which shlokas users have viewed to show progress and enable "continue reading" feature.

**Key Attributes**:
- `id`: UUID - Unique progress record identifier
- `user_id`: UUID - Foreign key to User
- `chapter`: integer - Chapter number
- `shloka_number`: integer - Shloka number
- `last_read_at`: timestamp - When shloka was last viewed

#### TypeScript Interface

```typescript
interface ReadingProgress {
  id: string;
  userId: string;
  chapter: number;
  shlokaNumber: number;
  lastReadAt: Date;
}
```

#### Relationships
- Many-to-one with User
- References Shloka (conceptual, not FK)

### Shloka

**Purpose**: Represents a single verse from the Bhagavad Gita with all associated content.

**Key Attributes**:
- `id`: UUID - Unique shloka identifier
- `chapter`: integer - Chapter number (1-18)
- `shloka_number`: integer - Verse number within chapter
- `sanskrit_text`: string - Original Sanskrit verse
- `transliteration`: string - Romanized Sanskrit
- `meaning`: string - English translation
- `audio_file_path`: string (nullable) - Path to audio file
- `themes`: string[] - Associated themes/keywords for search
- `embedding_index`: integer - Index in FAISS vector store

#### TypeScript Interface

```typescript
interface Shloka {
  id: string;
  chapter: number;
  shlokaNumber: number;
  sanskritText: string;
  transliteration: string;
  meaning: string;
  audioFilePath?: string;
  themes: string[];
  // Note: embedding_index is backend-only, not exposed to frontend
}
```

#### Relationships
- Referenced by Bookmark (conceptual)
- Referenced by ReadingProgress (conceptual)
- Has one embedding in FAISS vector store

### Chapter

**Purpose**: Represents one of the 18 chapters of the Bhagavad Gita with metadata.

**Key Attributes**:
- `id`: integer - Chapter number (1-18)
- `title`: string - English chapter title
- `sanskrit_name`: string - Sanskrit chapter name
- `description`: string - Brief chapter description
- `shloka_count`: integer - Number of shlokas in chapter

#### TypeScript Interface

```typescript
interface Chapter {
  id: number;
  title: string;
  sanskritName: string;
  description: string;
  shlokaCount: number;
}
```

#### Relationships
- Has many Shlokas (conceptual)

### DailyWisdom

**Purpose**: Tracks which shloka is selected as daily wisdom for each date.

**Key Attributes**:
- `id`: UUID - Unique record identifier
- `date`: date - Date for this wisdom (unique)
- `chapter`: integer - Selected chapter
- `shloka_number`: integer - Selected shloka
- `explanation`: string - Pre-generated AI explanation
- `created_at`: timestamp - When record was created

#### TypeScript Interface

```typescript
interface DailyWisdom {
  id: string;
  date: string; // YYYY-MM-DD format
  chapter: number;
  shlokaNumber: number;
  explanation: string;
  shloka?: Shloka; // Populated by join
}
```

#### Relationships
- References Shloka (conceptual)

### LifeGuidanceProblem

**Purpose**: Defines problem categories for the Life Guidance feature.

**Key Attributes**:
- `id`: string - Problem identifier (slug)
- `title`: string - Display title
- `description`: string - Brief description
- `icon`: string - Icon identifier
- `query_keywords`: string[] - Keywords for RAG retrieval

#### TypeScript Interface

```typescript
interface LifeGuidanceProblem {
  id: string;
  title: string;
  description: string;
  icon: string;
  queryKeywords: string[];
}
```

#### Relationships
- None (static configuration data)

---


## API Specification

### REST API Specification

```yaml
openapi: 3.0.0
info:
  title: Bhagavad Gita Learning API
  version: 1.0.0
  description: REST API for Bhagavad Gita learning application with RAG-powered explanations

servers:
  - url: http://localhost:8000/api
    description: Local development
  - url: https://api.bhagavadgita.app/api
    description: Production

components:
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
  
  schemas:
    User:
      type: object
      properties:
        id: { type: string, format: uuid }
        email: { type: string, format: email }
        oauthProvider: { type: string, nullable: true }
        createdAt: { type: string, format: date-time }
        notificationEnabled: { type: boolean }
        notificationTime: { type: string, pattern: '^([01]?[0-9]|2[0-3]):[0-5][0-9]$' }
    
    Chapter:
      type: object
      properties:
        id: { type: integer, minimum: 1, maximum: 18 }
        title: { type: string }
        sanskritName: { type: string }
        description: { type: string }
        shlokaCount: { type: integer }
    
    Shloka:
      type: object
      properties:
        id: { type: string, format: uuid }
        chapter: { type: integer }
        shlokaNumber: { type: integer }
        sanskritText: { type: string }
        transliteration: { type: string }
        meaning: { type: string }
        audioFilePath: { type: string, nullable: true }
        themes: { type: array, items: { type: string } }
        isBookmarked: { type: boolean }
    
    Bookmark:
      type: object
      properties:
        id: { type: string, format: uuid }
        userId: { type: string, format: uuid }
        chapter: { type: integer }
        shlokaNumber: { type: integer }
        createdAt: { type: string, format: date-time }
        shloka: { $ref: '#/components/schemas/Shloka' }
    
    Error:
      type: object
      properties:
        detail: { type: string }

paths:
  /health:
    get:
      summary: Health check endpoint
      tags: [System]
      responses:
        '200':
          description: Service is healthy
          content:
            application/json:
              schema:
                type: object
                properties:
                  status: { type: string, example: 'healthy' }
                  database: { type: string, example: 'connected' }
                  timestamp: { type: string, format: date-time }

  /auth/register:
    post:
      summary: Register new user with email/password
      tags: [Authentication]
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required: [email, password]
              properties:
                email: { type: string, format: email }
                password: { type: string, minLength: 8 }
      responses:
        '201':
          description: User created successfully
          content:
            application/json:
              schema:
                type: object
                properties:
                  user: { $ref: '#/components/schemas/User' }
                  accessToken: { type: string }
        '400':
          description: Invalid input or email already exists
          content:
            application/json:
              schema: { $ref: '#/components/schemas/Error' }

  /auth/login:
    post:
      summary: Login with email/password
      tags: [Authentication]
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required: [email, password]
              properties:
                email: { type: string, format: email }
                password: { type: string }
      responses:
        '200':
          description: Login successful
          content:
            application/json:
              schema:
                type: object
                properties:
                  user: { $ref: '#/components/schemas/User' }
                  accessToken: { type: string }
        '401':
          description: Invalid credentials
          content:
            application/json:
              schema: { $ref: '#/components/schemas/Error' }

  /auth/google:
    get:
      summary: Initiate Google OAuth flow
      tags: [Authentication]
      responses:
        '302':
          description: Redirect to Google OAuth consent screen

  /auth/google/callback:
    get:
      summary: Google OAuth callback
      tags: [Authentication]
      parameters:
        - name: code
          in: query
          required: true
          schema: { type: string }
      responses:
        '200':
          description: OAuth successful
          content:
            application/json:
              schema:
                type: object
                properties:
                  user: { $ref: '#/components/schemas/User' }
                  accessToken: { type: string }

  /chapters:
    get:
      summary: Get all chapters
      tags: [Content]
      responses:
        '200':
          description: List of all chapters
          content:
            application/json:
              schema:
                type: array
                items: { $ref: '#/components/schemas/Chapter' }

  /chapters/{chapterId}/shlokas:
    get:
      summary: Get all shlokas in a chapter
      tags: [Content]
      security:
        - BearerAuth: []
        - {} # Allow anonymous
      parameters:
        - name: chapterId
          in: path
          required: true
          schema: { type: integer, minimum: 1, maximum: 18 }
      responses:
        '200':
          description: List of shlokas
          content:
            application/json:
              schema:
                type: array
                items: { $ref: '#/components/schemas/Shloka' }

  /shlokas/{shlokaId}:
    get:
      summary: Get detailed shloka with AI explanation
      tags: [Content]
      security:
        - BearerAuth: []
        - {} # Allow anonymous
      parameters:
        - name: shlokaId
          in: path
          required: true
          schema: { type: string, format: uuid }
      responses:
        '200':
          description: Shloka details with explanation
          content:
            application/json:
              schema:
                allOf:
                  - $ref: '#/components/schemas/Shloka'
                  - type: object
                    properties:
                      explanation: { type: string }

  /shlokas/{shlokaId}/audio:
    get:
      summary: Stream shloka audio
      tags: [Content]
      parameters:
        - name: shlokaId
          in: path
          required: true
          schema: { type: string, format: uuid }
      responses:
        '200':
          description: Audio file stream
          content:
            audio/mpeg:
              schema:
                type: string
                format: binary
        '404':
          description: Audio file not found

  /bookmarks:
    get:
      summary: Get user's bookmarks
      tags: [Bookmarks]
      security:
        - BearerAuth: []
      responses:
        '200':
          description: List of bookmarks
          content:
            application/json:
              schema:
                type: array
                items: { $ref: '#/components/schemas/Bookmark' }
    
    post:
      summary: Create bookmark
      tags: [Bookmarks]
      security:
        - BearerAuth: []
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required: [chapter, shlokaNumber]
              properties:
                chapter: { type: integer }
                shlokaNumber: { type: integer }
      responses:
        '201':
          description: Bookmark created
          content:
            application/json:
              schema: { $ref: '#/components/schemas/Bookmark' }

  /bookmarks/{bookmarkId}:
    delete:
      summary: Delete bookmark
      tags: [Bookmarks]
      security:
        - BearerAuth: []
      parameters:
        - name: bookmarkId
          in: path
          required: true
          schema: { type: string, format: uuid }
      responses:
        '204':
          description: Bookmark deleted

  /daily-wisdom:
    get:
      summary: Get daily wisdom shloka
      tags: [Daily Wisdom]
      parameters:
        - name: date
          in: query
          required: false
          schema: { type: string, format: date }
          description: Date in YYYY-MM-DD format (defaults to today)
      responses:
        '200':
          description: Daily wisdom shloka
          content:
            application/json:
              schema:
                type: object
                properties:
                  date: { type: string, format: date }
                  shloka: { $ref: '#/components/schemas/Shloka' }
                  explanation: { type: string }

  /life-guidance/problems:
    get:
      summary: Get list of life guidance problem categories
      tags: [Life Guidance]
      responses:
        '200':
          description: List of problem categories
          content:
            application/json:
              schema:
                type: array
                items:
                  type: object
                  properties:
                    id: { type: string }
                    title: { type: string }
                    description: { type: string }
                    icon: { type: string }

  /life-guidance/recommendations:
    get:
      summary: Get shloka recommendations for a problem
      tags: [Life Guidance]
      parameters:
        - name: problem
          in: query
          required: true
          schema: { type: string }
          description: Problem category ID
      responses:
        '200':
          description: Recommended shlokas
          content:
            application/json:
              schema:
                type: array
                items:
                  type: object
                  properties:
                    shloka: { $ref: '#/components/schemas/Shloka' }
                    explanation: { type: string }
                    relevanceScore: { type: number, minimum: 0, maximum: 1 }

  /search:
    get:
      summary: Search shlokas by keyword
      tags: [Search]
      parameters:
        - name: q
          in: query
          required: true
          schema: { type: string, minLength: 3 }
          description: Search query
      responses:
        '200':
          description: Search results
          content:
            application/json:
              schema:
                type: array
                items:
                  type: object
                  properties:
                    shloka: { $ref: '#/components/schemas/Shloka' }
                    matchedText: { type: string }
                    relevanceScore: { type: number }

  /profile:
    get:
      summary: Get user profile with statistics
      tags: [Profile]
      security:
        - BearerAuth: []
      responses:
        '200':
          description: User profile
          content:
            application/json:
              schema:
                type: object
                properties:
                  user: { $ref: '#/components/schemas/User' }
                  stats:
                    type: object
                    properties:
                      bookmarkCount: { type: integer }
                      shlokasRead: { type: integer }
                      chaptersCompleted: { type: integer }
                      daysActive: { type: integer }

  /settings:
    get:
      summary: Get user settings
      tags: [Settings]
      security:
        - BearerAuth: []
      responses:
        '200':
          description: User settings
          content:
            application/json:
              schema:
                type: object
                properties:
                  notificationEnabled: { type: boolean }
                  notificationTime: { type: string }
    
    put:
      summary: Update user settings
      tags: [Settings]
      security:
        - BearerAuth: []
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                notificationEnabled: { type: boolean }
                notificationTime: { type: string }
      responses:
        '200':
          description: Settings updated
          content:
            application/json:
              schema:
                type: object
                properties:
                  notificationEnabled: { type: boolean }
                  notificationTime: { type: string }

  /progress:
    post:
      summary: Record reading progress
      tags: [Progress]
      security:
        - BearerAuth: []
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required: [chapter, shlokaNumber]
              properties:
                chapter: { type: integer }
                shlokaNumber: { type: integer }
      responses:
        '201':
          description: Progress recorded
```

---


## Components

### Backend API Service

**Responsibility**: Central FastAPI application serving all REST endpoints, coordinating between modules, handling authentication, and managing request/response lifecycle.

**Key Interfaces**:
- REST API endpoints (see API Specification)
- WebSocket connections (future for real-time features)
- Health check and metrics endpoints

**Dependencies**: 
- Auth Module
- Content Module
- RAG Module
- Notification Module
- PostgreSQL database
- Redis cache

**Technology Stack**: Python 3.11+, FastAPI 0.109+, Uvicorn, SQLAlchemy 2.0+

### Auth Module

**Responsibility**: Handle user authentication (email/password and Google OAuth), JWT token generation/validation, password hashing, and session management.

**Key Interfaces**:
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - Email/password login
- `GET /api/auth/google` - OAuth initiation
- `GET /api/auth/google/callback` - OAuth callback
- `verify_token()` - Internal JWT validation function

**Dependencies**:
- PostgreSQL (User table)
- bcrypt for password hashing
- OAuth2 library for Google integration

**Technology Stack**: FastAPI OAuth2, python-jose (JWT), bcrypt, httpx (OAuth requests)

### Content Module

**Responsibility**: Serve Bhagavad Gita content (chapters, shlokas), manage bookmarks, track reading progress, and stream audio files.

**Key Interfaces**:
- `GET /api/chapters` - List chapters
- `GET /api/chapters/{id}/shlokas` - List shlokas
- `GET /api/shlokas/{id}` - Get shloka details
- `GET /api/shlokas/{id}/audio` - Stream audio
- `GET /api/bookmarks` - User bookmarks
- `POST /api/bookmarks` - Create bookmark
- `DELETE /api/bookmarks/{id}` - Remove bookmark
- `POST /api/progress` - Record progress

**Dependencies**:
- PostgreSQL (Chapter, Shloka, Bookmark, ReadingProgress tables)
- Redis (content caching)
- File system (audio files)
- RAG Module (for shloka explanations)

**Technology Stack**: FastAPI, SQLAlchemy, Redis, FileResponse for audio streaming

### RAG Module

**Responsibility**: Provide AI-powered explanations for shlokas using Retrieval-Augmented Generation, ensuring responses are grounded in actual Gita text to prevent hallucinations.

**Key Interfaces**:
- `generate_explanation(shloka_id: str, context: str) -> str` - Generate explanation for specific shloka
- `retrieve_relevant_shlokas(query: str, top_k: int) -> List[Shloka]` - Semantic search
- `search_by_problem(problem_id: str) -> List[Shloka]` - Life guidance recommendations

**Dependencies**:
- FAISS vector store (shloka embeddings)
- Ollama (Mistral 7B LLM)
- Sentence-Transformers (embedding model)
- Redis (explanation caching)
- Content Module (shloka data)

**Technology Stack**: FAISS, Sentence-Transformers (all-MiniLM-L6-v2), Ollama Python client, Redis

**Performance Target**: <2 seconds total (retrieval + generation)

### Notification Module

**Responsibility**: Schedule and send daily wisdom notifications, manage user notification preferences, and handle background task execution.

**Key Interfaces**:
- `schedule_daily_wisdom()` - Celery task to select and send daily wisdom
- `send_notification(user_id: str, shloka_id: str)` - Send push notification
- `update_notification_settings(user_id: str, settings: dict)` - Update preferences

**Dependencies**:
- Celery (task scheduling)
- Redis (Celery broker and result backend)
- PostgreSQL (User, DailyWisdom tables)
- Content Module (shloka data)
- RAG Module (explanation generation)
- Firebase Cloud Messaging (future, for push notifications)

**Technology Stack**: Celery 5.3+, Redis, Python logging

### Ingestion Pipeline (One-time Setup)

**Responsibility**: Extract Bhagavad Gita content from PDF source, parse into structured data, generate embeddings, and populate FAISS vector store.

**Key Interfaces**:
- `ingest_pdf(pdf_path: str) -> List[Shloka]` - Extract and parse PDF
- `generate_embeddings(shlokas: List[Shloka]) -> np.ndarray` - Create embeddings
- `build_faiss_index(embeddings: np.ndarray) -> faiss.Index` - Build vector store
- `seed_database(shlokas: List[Shloka])` - Populate PostgreSQL

**Dependencies**:
- pdfplumber (PDF extraction)
- Sentence-Transformers (embedding generation)
- FAISS (index creation)
- PostgreSQL (data storage)

**Technology Stack**: Python scripts, pdfplumber, Sentence-Transformers, FAISS, SQLAlchemy

**Note**: This is a one-time setup process, not part of the runtime application.

### Frontend Mobile App

**Responsibility**: Provide cross-platform mobile interface for iOS, Android, and web, handle offline caching, manage local state, and communicate with backend API.

**Key Interfaces**:
- React Native screens and components
- API client service layer
- Local storage (AsyncStorage)
- Navigation system

**Dependencies**:
- Backend API Service (all endpoints)
- AsyncStorage (offline caching)
- React Navigation (routing)
- Zustand (state management)

**Technology Stack**: React Native 0.73+, Expo SDK 50+, TypeScript 5.3+, Zustand, React Navigation, Axios

---

## Component Interaction Diagram

```mermaid
graph TB
    subgraph "Frontend"
        UI[React Native UI]
        State[Zustand State]
        APIClient[API Client]
        Cache[AsyncStorage Cache]
    end
    
    subgraph "Backend API"
        FastAPI[FastAPI Router]
        AuthMod[Auth Module]
        ContentMod[Content Module]
        RAGMod[RAG Module]
        NotifMod[Notification Module]
    end
    
    subgraph "Data & AI"
        PG[(PostgreSQL)]
        Redis[(Redis)]
        FAISS[(FAISS)]
        Ollama[Ollama LLM]
        Files[Audio Files]
    end
    
    subgraph "Background Tasks"
        Celery[Celery Worker]
    end
    
    UI --> State
    State --> APIClient
    APIClient --> Cache
    APIClient --> FastAPI
    
    FastAPI --> AuthMod
    FastAPI --> ContentMod
    FastAPI --> RAGMod
    FastAPI --> NotifMod
    
    AuthMod --> PG
    ContentMod --> PG
    ContentMod --> Redis
    ContentMod --> Files
    ContentMod --> RAGMod
    
    RAGMod --> FAISS
    RAGMod --> Ollama
    RAGMod --> Redis
    
    NotifMod --> Celery
    Celery --> Redis
    Celery --> PG
    Celery --> RAGMod
```

---


## External APIs

### Google OAuth 2.0 API

- **Purpose**: Enable users to authenticate using their Google accounts
- **Documentation**: https://developers.google.com/identity/protocols/oauth2
- **Base URL(s)**: 
  - Authorization: `https://accounts.google.com/o/oauth2/v2/auth`
  - Token Exchange: `https://oauth2.googleapis.com/token`
  - User Info: `https://www.googleapis.com/oauth2/v2/userinfo`
- **Authentication**: OAuth 2.0 Authorization Code Flow with PKCE
- **Rate Limits**: 10,000 requests per day (free tier)

**Key Endpoints Used**:
- `GET /o/oauth2/v2/auth` - Initiate OAuth flow
- `POST /token` - Exchange authorization code for access token
- `GET /oauth2/v2/userinfo` - Retrieve user profile information

**Integration Notes**: 
- Store client ID and secret in environment variables
- Implement state parameter for CSRF protection
- Handle token refresh for long-lived sessions
- Gracefully handle OAuth errors and user cancellations

### Firebase Cloud Messaging (Future Phase)

- **Purpose**: Send push notifications for daily wisdom reminders
- **Documentation**: https://firebase.google.com/docs/cloud-messaging
- **Base URL(s)**: `https://fcm.googleapis.com/v1/projects/{project-id}/messages:send`
- **Authentication**: Service account JSON key
- **Rate Limits**: No hard limit, but throttling may occur with excessive usage

**Key Endpoints Used**:
- `POST /v1/projects/{project-id}/messages:send` - Send notification to device

**Integration Notes**:
- Phase 1 uses local notifications only
- FCM integration planned for Phase 2
- Requires user permission on mobile devices
- Store FCM tokens in User table when implemented

---

## Core Workflows

### User Authentication Flow (Email/Password)

```mermaid
sequenceDiagram
    actor User
    participant App as Mobile App
    participant API as FastAPI
    participant Auth as Auth Module
    participant DB as PostgreSQL
    
    User->>App: Enter email/password
    App->>API: POST /api/auth/login
    API->>Auth: validate_credentials()
    Auth->>DB: SELECT user WHERE email=?
    DB-->>Auth: User record
    Auth->>Auth: bcrypt.verify(password)
    alt Valid credentials
        Auth->>Auth: generate_jwt_token()
        Auth-->>API: {user, accessToken}
        API-->>App: 200 OK {user, accessToken}
        App->>App: Store token in AsyncStorage
        App->>App: Navigate to Home
        App-->>User: Show home screen
    else Invalid credentials
        Auth-->>API: 401 Unauthorized
        API-->>App: 401 {detail: "Invalid credentials"}
        App-->>User: Show error message
    end
```

### RAG Explanation Generation Flow

```mermaid
sequenceDiagram
    actor User
    participant App as Mobile App
    participant API as FastAPI
    participant Content as Content Module
    participant RAG as RAG Module
    participant Cache as Redis
    participant FAISS as FAISS Store
    participant LLM as Ollama (Mistral)
    participant DB as PostgreSQL
    
    User->>App: View shloka detail
    App->>API: GET /api/shlokas/{id}
    API->>Content: get_shloka_with_explanation(id)
    Content->>DB: SELECT shloka WHERE id=?
    DB-->>Content: Shloka data
    
    Content->>RAG: generate_explanation(shloka)
    RAG->>Cache: GET explanation:{shloka_id}
    
    alt Cache hit
        Cache-->>RAG: Cached explanation
    else Cache miss
        RAG->>FAISS: similarity_search(shloka_embedding)
        FAISS-->>RAG: Top 3 related shlokas
        RAG->>RAG: build_prompt(shloka, context)
        Note over RAG: Prompt includes:<br/>- Target shloka<br/>- Related shlokas<br/>- Constraints against hallucination<br/>- Student-friendly language instruction
        RAG->>LLM: generate(prompt)
        LLM-->>RAG: AI explanation
        RAG->>Cache: SET explanation:{shloka_id}
    end
    
    RAG-->>Content: Explanation text
    Content-->>API: {shloka, explanation}
    API-->>App: 200 OK {shloka, explanation}
    App-->>User: Display shloka with explanation
```

### Life Guidance Recommendation Flow

```mermaid
sequenceDiagram
    actor User
    participant App as Mobile App
    participant API as FastAPI
    participant RAG as RAG Module
    participant FAISS as FAISS Store
    participant LLM as Ollama
    participant DB as PostgreSQL
    
    User->>App: Select problem (e.g., "Stress")
    App->>API: GET /api/life-guidance/recommendations?problem=stress
    API->>RAG: get_recommendations_for_problem("stress")
    RAG->>RAG: Map problem to query keywords
    Note over RAG: "stress" → ["peace", "calm", "equanimity", "tranquility"]
    
    RAG->>FAISS: similarity_search(query_embedding, top_k=5)
    FAISS-->>RAG: Top 5 relevant shlokas
    
    loop For each shloka
        RAG->>DB: Get full shloka details
        DB-->>RAG: Shloka data
        RAG->>RAG: build_practical_prompt(shloka, problem)
        RAG->>LLM: generate(prompt)
        LLM-->>RAG: Practical explanation
    end
    
    RAG-->>API: [{shloka, explanation, relevanceScore}]
    API-->>App: 200 OK [recommendations]
    App-->>User: Display recommended shlokas
```

### Daily Wisdom Notification Flow

```mermaid
sequenceDiagram
    participant Scheduler as Celery Beat
    participant Worker as Celery Worker
    participant DB as PostgreSQL
    participant RAG as RAG Module
    participant Notif as Notification Service
    participant FCM as Firebase (Future)
    participant User as User Device
    
    Note over Scheduler: Daily at 8:00 AM
    Scheduler->>Worker: schedule_daily_wisdom()
    Worker->>DB: SELECT daily_wisdom WHERE date=today
    
    alt Wisdom already selected
        DB-->>Worker: DailyWisdom record
    else No wisdom for today
        Worker->>Worker: Select next shloka (sequential)
        Worker->>RAG: generate_explanation(shloka)
        RAG-->>Worker: Explanation
        Worker->>DB: INSERT daily_wisdom
    end
    
    Worker->>DB: SELECT users WHERE notification_enabled=true
    DB-->>Worker: List of users
    
    loop For each user
        Worker->>Notif: send_notification(user, shloka)
        alt Phase 2 (FCM)
            Notif->>FCM: Send push notification
            FCM-->>User: Push notification
        else Phase 1 (Local)
            Note over Notif: Local notification scheduled<br/>when app is active
        end
    end
```

### Offline Content Access Flow

```mermaid
sequenceDiagram
    actor User
    participant App as Mobile App
    participant Cache as AsyncStorage
    participant API as FastAPI
    
    User->>App: Open app / View content
    App->>App: Check network connectivity
    
    alt Online
        App->>API: GET /api/chapters
        API-->>App: Chapters data
        App->>Cache: STORE chapters
        App-->>User: Display chapters
    else Offline
        App->>Cache: GET chapters
        alt Cache exists
            Cache-->>App: Cached chapters
            App-->>User: Display chapters (offline mode indicator)
        else No cache
            App-->>User: Show "No offline content" message
        end
    end
    
    Note over App,Cache: Similar flow for shlokas,<br/>bookmarks, and progress
```

---


## Database Schema

### PostgreSQL Schema Definition

```sql
-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Users table
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255), -- Nullable for OAuth users
    oauth_provider VARCHAR(50), -- 'google' or NULL
    oauth_id VARCHAR(255), -- Provider's user ID
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    notification_enabled BOOLEAN DEFAULT true,
    notification_time TIME DEFAULT '08:00:00',
    CONSTRAINT unique_oauth UNIQUE (oauth_provider, oauth_id)
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_oauth ON users(oauth_provider, oauth_id);

-- Chapters table (static reference data)
CREATE TABLE chapters (
    id INTEGER PRIMARY KEY CHECK (id BETWEEN 1 AND 18),
    title VARCHAR(255) NOT NULL,
    sanskrit_name VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    shloka_count INTEGER NOT NULL
);

-- Shlokas table
CREATE TABLE shlokas (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    chapter INTEGER NOT NULL REFERENCES chapters(id),
    shloka_number INTEGER NOT NULL,
    sanskrit_text TEXT NOT NULL,
    transliteration TEXT NOT NULL,
    meaning TEXT NOT NULL,
    audio_file_path VARCHAR(500),
    themes TEXT[], -- Array of theme keywords
    embedding_index INTEGER NOT NULL, -- Index in FAISS vector store
    CONSTRAINT unique_shloka UNIQUE (chapter, shloka_number)
);

CREATE INDEX idx_shlokas_chapter ON shlokas(chapter);
CREATE INDEX idx_shlokas_themes ON shlokas USING GIN(themes);
CREATE INDEX idx_shlokas_embedding ON shlokas(embedding_index);

-- Bookmarks table
CREATE TABLE bookmarks (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    chapter INTEGER NOT NULL,
    shloka_number INTEGER NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT unique_user_bookmark UNIQUE (user_id, chapter, shloka_number)
);

CREATE INDEX idx_bookmarks_user ON bookmarks(user_id);
CREATE INDEX idx_bookmarks_created ON bookmarks(created_at DESC);

-- Reading progress table
CREATE TABLE reading_progress (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    chapter INTEGER NOT NULL,
    shloka_number INTEGER NOT NULL,
    last_read_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT unique_user_progress UNIQUE (user_id, chapter, shloka_number)
);

CREATE INDEX idx_progress_user ON reading_progress(user_id);
CREATE INDEX idx_progress_last_read ON reading_progress(last_read_at DESC);

-- Daily wisdom table
CREATE TABLE daily_wisdom (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    date DATE UNIQUE NOT NULL,
    chapter INTEGER NOT NULL,
    shloka_number INTEGER NOT NULL,
    explanation TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_daily_wisdom_date ON daily_wisdom(date DESC);

-- Life guidance problems (static configuration, could be JSON file instead)
CREATE TABLE life_guidance_problems (
    id VARCHAR(50) PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    icon VARCHAR(50) NOT NULL,
    query_keywords TEXT[] NOT NULL
);
```

### Entity Relationship Diagram

```mermaid
erDiagram
    USERS ||--o{ BOOKMARKS : "has many"
    USERS ||--o{ READING_PROGRESS : "tracks"
    CHAPTERS ||--o{ SHLOKAS : "contains"
    SHLOKAS ||--o{ BOOKMARKS : "bookmarked in"
    SHLOKAS ||--o{ READING_PROGRESS : "read in"
    DAILY_WISDOM }o--|| SHLOKAS : "references"
    
    USERS {
        uuid id PK
        string email UK
        string hashed_password
        string oauth_provider
        string oauth_id
        timestamp created_at
        timestamp last_login
        boolean notification_enabled
        time notification_time
    }
    
    CHAPTERS {
        int id PK
        string title
        string sanskrit_name
        text description
        int shloka_count
    }
    
    SHLOKAS {
        uuid id PK
        int chapter FK
        int shloka_number
        text sanskrit_text
        text transliteration
        text meaning
        string audio_file_path
        array themes
        int embedding_index
    }
    
    BOOKMARKS {
        uuid id PK
        uuid user_id FK
        int chapter
        int shloka_number
        timestamp created_at
    }
    
    READING_PROGRESS {
        uuid id PK
        uuid user_id FK
        int chapter
        int shloka_number
        timestamp last_read_at
    }
    
    DAILY_WISDOM {
        uuid id PK
        date date UK
        int chapter
        int shloka_number
        text explanation
        timestamp created_at
    }
    
    LIFE_GUIDANCE_PROBLEMS {
        string id PK
        string title
        text description
        string icon
        array query_keywords
    }
```

### Database Indexing Strategy

**Performance Considerations**:

1. **User Lookups**: Index on `email` for login, composite index on `(oauth_provider, oauth_id)` for OAuth
2. **Content Retrieval**: Index on `chapter` for shloka lists, GIN index on `themes` array for keyword search
3. **Bookmark Queries**: Index on `user_id` for user's bookmarks, composite unique index prevents duplicates
4. **Progress Tracking**: Index on `user_id` and `last_read_at` for recent activity queries
5. **Daily Wisdom**: Index on `date` for quick daily lookup

**Scalability Notes**:
- Chapters and Shlokas tables are relatively static (~700 shlokas total)
- User-generated data (bookmarks, progress) will grow linearly with users
- Consider partitioning reading_progress by date if table grows very large
- FAISS vector store is separate from PostgreSQL for performance

---


## Frontend Architecture

### Component Architecture

#### Component Organization

```
frontend/src/
├── components/              # Reusable UI components
│   ├── common/             # Generic components
│   │   ├── Button.tsx
│   │   ├── Card.tsx
│   │   ├── LoadingSpinner.tsx
│   │   └── ErrorBoundary.tsx
│   ├── shloka/             # Shloka-specific components
│   │   ├── ShlokaCard.tsx
│   │   ├── ShlokaDetail.tsx
│   │   ├── AudioPlayer.tsx
│   │   └── BookmarkButton.tsx
│   └── navigation/         # Navigation components
│       ├── TabBar.tsx
│       └── Header.tsx
├── screens/                # Screen components (pages)
│   ├── HomeScreen.tsx
│   ├── ChapterListScreen.tsx
│   ├── ShlokaListScreen.tsx
│   ├── ShlokaDetailScreen.tsx
│   ├── LifeGuidanceScreen.tsx
│   ├── SearchScreen.tsx
│   ├── ProfileScreen.tsx
│   ├── SettingsScreen.tsx
│   └── auth/
│       ├── LoginScreen.tsx
│       └── RegisterScreen.tsx
├── hooks/                  # Custom React hooks
│   ├── useAuth.ts
│   ├── useBookmarks.ts
│   ├── useOfflineSync.ts
│   └── useAudio.ts
├── services/               # API client services
│   ├── api.ts             # Axios instance configuration
│   ├── authService.ts
│   ├── contentService.ts
│   ├── ragService.ts
│   └── storageService.ts
├── stores/                 # Zustand state stores
│   ├── authStore.ts
│   ├── contentStore.ts
│   └── settingsStore.ts
├── types/                  # TypeScript type definitions
│   ├── models.ts
│   └── api.ts
├── utils/                  # Utility functions
│   ├── formatting.ts
│   ├── validation.ts
│   └── constants.ts
├── styles/                 # Global styles and theme
│   ├── theme.ts
│   └── globalStyles.ts
└── App.tsx                 # Root component
```

#### Component Template

```typescript
// Example: ShlokaCard.tsx
import React from 'react';
import { View, Text, StyleSheet, TouchableOpacity } from 'react-native';
import { Card } from 'react-native-paper';
import { Shloka } from '../types/models';
import { useNavigation } from '@react-navigation/native';

interface ShlokaCardProps {
  shloka: Shloka;
  isBookmarked?: boolean;
  showChapter?: boolean;
}

export const ShlokaCard: React.FC<ShlokaCardProps> = ({
  shloka,
  isBookmarked = false,
  showChapter = false,
}) => {
  const navigation = useNavigation();

  const handlePress = () => {
    navigation.navigate('ShlokaDetail', { shlokaId: shloka.id });
  };

  return (
    <Card style={styles.card} onPress={handlePress}>
      <Card.Content>
        <View style={styles.header}>
          <Text style={styles.reference}>
            {showChapter && `Chapter ${shloka.chapter}, `}
            Verse {shloka.shlokaNumber}
          </Text>
          {isBookmarked && <Text style={styles.bookmark}>🔖</Text>}
        </View>
        <Text style={styles.sanskrit} numberOfLines={2}>
          {shloka.sanskritText}
        </Text>
        <Text style={styles.transliteration} numberOfLines={1}>
          {shloka.transliteration}
        </Text>
      </Card.Content>
    </Card>
  );
};

const styles = StyleSheet.create({
  card: {
    marginVertical: 8,
    marginHorizontal: 16,
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: 8,
  },
  reference: {
    fontSize: 12,
    color: '#666',
    fontWeight: '600',
  },
  bookmark: {
    fontSize: 16,
  },
  sanskrit: {
    fontSize: 16,
    fontFamily: 'serif',
    marginBottom: 4,
  },
  transliteration: {
    fontSize: 14,
    color: '#888',
    fontStyle: 'italic',
  },
});
```

### State Management Architecture

#### State Structure

```typescript
// stores/authStore.ts
import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { User } from '../types/models';

interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  
  // Actions
  setUser: (user: User, token: string) => void;
  logout: () => void;
  updateUser: (user: Partial<User>) => void;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      user: null,
      token: null,
      isAuthenticated: false,
      isLoading: false,
      
      setUser: (user, token) => set({
        user,
        token,
        isAuthenticated: true,
      }),
      
      logout: () => set({
        user: null,
        token: null,
        isAuthenticated: false,
      }),
      
      updateUser: (updates) => set((state) => ({
        user: state.user ? { ...state.user, ...updates } : null,
      })),
    }),
    {
      name: 'auth-storage',
      storage: createJSONStorage(() => AsyncStorage),
    }
  )
);

// stores/contentStore.ts
import { create } from 'zustand';
import { Chapter, Shloka, Bookmark } from '../types/models';

interface ContentState {
  chapters: Chapter[];
  shlokas: Record<number, Shloka[]>; // Keyed by chapter ID
  bookmarks: Bookmark[];
  dailyWisdom: { shloka: Shloka; explanation: string } | null;
  
  // Actions
  setChapters: (chapters: Chapter[]) => void;
  setShlokas: (chapterId: number, shlokas: Shloka[]) => void;
  setBookmarks: (bookmarks: Bookmark[]) => void;
  addBookmark: (bookmark: Bookmark) => void;
  removeBookmark: (bookmarkId: string) => void;
  setDailyWisdom: (wisdom: { shloka: Shloka; explanation: string }) => void;
}

export const useContentStore = create<ContentState>((set) => ({
  chapters: [],
  shlokas: {},
  bookmarks: [],
  dailyWisdom: null,
  
  setChapters: (chapters) => set({ chapters }),
  
  setShlokas: (chapterId, shlokas) => set((state) => ({
    shlokas: { ...state.shlokas, [chapterId]: shlokas },
  })),
  
  setBookmarks: (bookmarks) => set({ bookmarks }),
  
  addBookmark: (bookmark) => set((state) => ({
    bookmarks: [...state.bookmarks, bookmark],
  })),
  
  removeBookmark: (bookmarkId) => set((state) => ({
    bookmarks: state.bookmarks.filter((b) => b.id !== bookmarkId),
  })),
  
  setDailyWisdom: (wisdom) => set({ dailyWisdom: wisdom }),
}));
```

#### State Management Patterns

- **Zustand for Global State**: Lightweight, minimal boilerplate, excellent TypeScript support
- **Persist Middleware**: Automatically sync auth state to AsyncStorage for offline access
- **Selective Subscriptions**: Components subscribe only to needed state slices for performance
- **Optimistic Updates**: Update UI immediately, rollback on API failure
- **Normalized Data**: Store shlokas keyed by chapter to avoid duplication

### Routing Architecture

#### Route Organization

```typescript
// navigation/AppNavigator.tsx
import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { useAuthStore } from '../stores/authStore';

// Stack navigators
const AuthStack = createNativeStackNavigator();
const HomeStack = createNativeStackNavigator();
const ExploreStack = createNativeStackNavigator();
const ProfileStack = createNativeStackNavigator();

// Tab navigator
const Tab = createBottomTabNavigator();

// Auth flow
function AuthNavigator() {
  return (
    <AuthStack.Navigator screenOptions={{ headerShown: false }}>
      <AuthStack.Screen name="Login" component={LoginScreen} />
      <AuthStack.Screen name="Register" component={RegisterScreen} />
    </AuthStack.Navigator>
  );
}

// Home flow
function HomeNavigator() {
  return (
    <HomeStack.Navigator>
      <HomeStack.Screen name="Home" component={HomeScreen} />
      <HomeStack.Screen name="ShlokaDetail" component={ShlokaDetailScreen} />
      <HomeStack.Screen name="LifeGuidance" component={LifeGuidanceScreen} />
    </HomeStack.Navigator>
  );
}

// Explore flow
function ExploreNavigator() {
  return (
    <ExploreStack.Navigator>
      <ExploreStack.Screen name="ChapterList" component={ChapterListScreen} />
      <ExploreStack.Screen name="ShlokaList" component={ShlokaListScreen} />
      <ExploreStack.Screen name="ShlokaDetail" component={ShlokaDetailScreen} />
      <ExploreStack.Screen name="Search" component={SearchScreen} />
    </ExploreStack.Navigator>
  );
}

// Profile flow
function ProfileNavigator() {
  return (
    <ProfileStack.Navigator>
      <ProfileStack.Screen name="Profile" component={ProfileScreen} />
      <ProfileStack.Screen name="Settings" component={SettingsScreen} />
      <ProfileStack.Screen name="Bookmarks" component={BookmarksScreen} />
    </ProfileStack.Navigator>
  );
}

// Main tab navigator
function MainTabs() {
  return (
    <Tab.Navigator>
      <Tab.Screen name="HomeTab" component={HomeNavigator} />
      <Tab.Screen name="ExploreTab" component={ExploreNavigator} />
      <Tab.Screen name="ProfileTab" component={ProfileNavigator} />
    </Tab.Navigator>
  );
}

// Root navigator
export function AppNavigator() {
  const isAuthenticated = useAuthStore((state) => state.isAuthenticated);
  
  return (
    <NavigationContainer>
      {isAuthenticated ? <MainTabs /> : <AuthNavigator />}
    </NavigationContainer>
  );
}
```

#### Protected Route Pattern

```typescript
// components/navigation/ProtectedRoute.tsx
import React from 'react';
import { useAuthStore } from '../../stores/authStore';
import { useNavigation } from '@react-navigation/native';

interface ProtectedRouteProps {
  children: React.ReactNode;
  fallback?: React.ReactNode;
}

export const ProtectedRoute: React.FC<ProtectedRouteProps> = ({
  children,
  fallback,
}) => {
  const isAuthenticated = useAuthStore((state) => state.isAuthenticated);
  const navigation = useNavigation();
  
  React.useEffect(() => {
    if (!isAuthenticated) {
      navigation.navigate('Login');
    }
  }, [isAuthenticated, navigation]);
  
  if (!isAuthenticated) {
    return fallback || null;
  }
  
  return <>{children}</>;
};
```

### Frontend Services Layer

#### API Client Setup

```typescript
// services/api.ts
import axios, { AxiosInstance, AxiosError } from 'axios';
import { useAuthStore } from '../stores/authStore';
import AsyncStorage from '@react-native-async-storage/async-storage';

const API_BASE_URL = process.env.EXPO_PUBLIC_API_URL || 'http://localhost:8000/api';

// Create axios instance
export const apiClient: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor: Add auth token
apiClient.interceptors.request.use(
  async (config) => {
    const token = useAuthStore.getState().token;
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor: Handle errors
apiClient.interceptors.response.use(
  (response) => response,
  async (error: AxiosError) => {
    if (error.response?.status === 401) {
      // Token expired or invalid
      useAuthStore.getState().logout();
      await AsyncStorage.clear();
    }
    return Promise.reject(error);
  }
);

// Offline detection
export const isOnline = async (): Promise<boolean> => {
  try {
    const response = await fetch(API_BASE_URL + '/health', {
      method: 'HEAD',
      cache: 'no-cache',
    });
    return response.ok;
  } catch {
    return false;
  }
};
```

#### Service Example

```typescript
// services/contentService.ts
import { apiClient } from './api';
import { storageService } from './storageService';
import { Chapter, Shloka } from '../types/models';

export const contentService = {
  // Get all chapters
  async getChapters(): Promise<Chapter[]> {
    try {
      const response = await apiClient.get<Chapter[]>('/chapters');
      // Cache for offline access
      await storageService.setItem('chapters', response.data);
      return response.data;
    } catch (error) {
      // Fallback to cached data if offline
      const cached = await storageService.getItem<Chapter[]>('chapters');
      if (cached) return cached;
      throw error;
    }
  },

  // Get shlokas for a chapter
  async getShlokas(chapterId: number): Promise<Shloka[]> {
    try {
      const response = await apiClient.get<Shloka[]>(`/chapters/${chapterId}/shlokas`);
      await storageService.setItem(`shlokas_${chapterId}`, response.data);
      return response.data;
    } catch (error) {
      const cached = await storageService.getItem<Shloka[]>(`shlokas_${chapterId}`);
      if (cached) return cached;
      throw error;
    }
  },

  // Get shloka detail with explanation
  async getShlokaDetail(shlokaId: string): Promise<Shloka & { explanation: string }> {
    const response = await apiClient.get(`/shlokas/${shlokaId}`);
    return response.data;
  },

  // Get audio URL
  getAudioUrl(shlokaId: string): string {
    return `${apiClient.defaults.baseURL}/shlokas/${shlokaId}/audio`;
  },
};

// services/storageService.ts
import AsyncStorage from '@react-native-async-storage/async-storage';

export const storageService = {
  async setItem<T>(key: string, value: T): Promise<void> {
    try {
      await AsyncStorage.setItem(key, JSON.stringify(value));
    } catch (error) {
      console.error('Storage set error:', error);
    }
  },

  async getItem<T>(key: string): Promise<T | null> {
    try {
      const value = await AsyncStorage.getItem(key);
      return value ? JSON.parse(value) : null;
    } catch (error) {
      console.error('Storage get error:', error);
      return null;
    }
  },

  async removeItem(key: string): Promise<void> {
    try {
      await AsyncStorage.removeItem(key);
    } catch (error) {
      console.error('Storage remove error:', error);
    }
  },

  async clear(): Promise<void> {
    try {
      await AsyncStorage.clear();
    } catch (error) {
      console.error('Storage clear error:', error);
    }
  },
};
```

---


## Backend Architecture

### Service Architecture

#### Controller/Route Organization

```
backend/src/
├── main.py                 # FastAPI application entry point
├── config.py               # Configuration and environment variables
├── database.py             # Database connection and session management
├── dependencies.py         # Shared dependencies (auth, db session)
├── routes/                 # API route handlers
│   ├── __init__.py
│   ├── auth.py            # Authentication endpoints
│   ├── content.py         # Content browsing endpoints
│   ├── bookmarks.py       # Bookmark management
│   ├── search.py          # Search endpoints
│   ├── profile.py         # User profile and settings
│   └── health.py          # Health check
├── services/              # Business logic layer
│   ├── __init__.py
│   ├── auth_service.py    # Authentication logic
│   ├── content_service.py # Content retrieval logic
│   ├── rag_service.py     # RAG pipeline
│   ├── notification_service.py # Notification scheduling
│   └── ingestion_service.py # PDF ingestion (one-time)
├── models/                # SQLAlchemy ORM models
│   ├── __init__.py
│   ├── user.py
│   ├── shloka.py
│   ├── bookmark.py
│   ├── progress.py
│   └── daily_wisdom.py
├── schemas/               # Pydantic schemas for validation
│   ├── __init__.py
│   ├── user.py
│   ├── shloka.py
│   ├── auth.py
│   └── responses.py
├── middleware/            # Custom middleware
│   ├── __init__.py
│   ├── cors.py
│   ├── error_handler.py
│   └── logging.py
├── utils/                 # Utility functions
│   ├── __init__.py
│   ├── jwt.py            # JWT token utilities
│   ├── password.py       # Password hashing
│   └── validators.py     # Input validation
├── tasks/                 # Celery tasks
│   ├── __init__.py
│   ├── celery_app.py     # Celery configuration
│   └── daily_wisdom.py   # Daily wisdom task
└── tests/                 # Backend tests
    ├── unit/
    ├── integration/
    └── conftest.py
```

#### Controller Template

```python
# routes/content.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from ..dependencies import get_db, get_current_user
from ..services.content_service import ContentService
from ..schemas.shloka import ShlokaResponse, ShlokaDetailResponse
from ..schemas.user import User

router = APIRouter(prefix="/content", tags=["content"])

@router.get("/chapters/{chapter_id}/shlokas", response_model=List[ShlokaResponse])
async def get_shlokas(
    chapter_id: int,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user)
):
    """
    Get all shlokas for a specific chapter.
    Includes bookmark status if user is authenticated.
    """
    if chapter_id < 1 or chapter_id > 18:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Chapter ID must be between 1 and 18"
        )
    
    service = ContentService(db)
    shlokas = await service.get_shlokas_by_chapter(
        chapter_id=chapter_id,
        user_id=current_user.id if current_user else None
    )
    
    return shlokas

@router.get("/shlokas/{shloka_id}", response_model=ShlokaDetailResponse)
async def get_shloka_detail(
    shloka_id: str,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user)
):
    """
    Get detailed shloka information with AI-generated explanation.
    """
    service = ContentService(db)
    shloka = await service.get_shloka_with_explanation(
        shloka_id=shloka_id,
        user_id=current_user.id if current_user else None
    )
    
    if not shloka:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Shloka not found"
        )
    
    return shloka
```

### Database Architecture

#### Schema Design

See "Database Schema" section above for complete SQL schema.

#### Data Access Layer (Repository Pattern)

```python
# services/content_service.py
from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import List, Optional
from uuid import UUID

from ..models.shloka import Shloka
from ..models.bookmark import Bookmark
from ..models.progress import ReadingProgress
from ..schemas.shloka import ShlokaResponse, ShlokaDetailResponse
from .rag_service import RAGService
from .cache_service import CacheService

class ContentService:
    def __init__(self, db: Session):
        self.db = db
        self.rag_service = RAGService()
        self.cache = CacheService()
    
    async def get_shlokas_by_chapter(
        self,
        chapter_id: int,
        user_id: Optional[UUID] = None
    ) -> List[ShlokaResponse]:
        """Get all shlokas for a chapter with bookmark status."""
        # Query shlokas
        shlokas = self.db.query(Shloka).filter(
            Shloka.chapter == chapter_id
        ).order_by(Shloka.shloka_number).all()
        
        # Get user's bookmarks if authenticated
        bookmarked_ids = set()
        if user_id:
            bookmarks = self.db.query(Bookmark).filter(
                and_(
                    Bookmark.user_id == user_id,
                    Bookmark.chapter == chapter_id
                )
            ).all()
            bookmarked_ids = {
                (b.chapter, b.shloka_number) for b in bookmarks
            }
        
        # Build response
        return [
            ShlokaResponse(
                **shloka.__dict__,
                isBookmarked=(shloka.chapter, shloka.shloka_number) in bookmarked_ids
            )
            for shloka in shlokas
        ]
    
    async def get_shloka_with_explanation(
        self,
        shloka_id: str,
        user_id: Optional[UUID] = None
    ) -> Optional[ShlokaDetailResponse]:
        """Get shloka with AI-generated explanation."""
        # Get shloka from database
        shloka = self.db.query(Shloka).filter(
            Shloka.id == shloka_id
        ).first()
        
        if not shloka:
            return None
        
        # Check cache for explanation
        cache_key = f"explanation:{shloka_id}"
        explanation = await self.cache.get(cache_key)
        
        if not explanation:
            # Generate explanation using RAG
            explanation = await self.rag_service.generate_explanation(shloka)
            # Cache for 24 hours
            await self.cache.set(cache_key, explanation, ttl=86400)
        
        # Check if bookmarked
        is_bookmarked = False
        if user_id:
            bookmark = self.db.query(Bookmark).filter(
                and_(
                    Bookmark.user_id == user_id,
                    Bookmark.chapter == shloka.chapter,
                    Bookmark.shloka_number == shloka.shloka_number
                )
            ).first()
            is_bookmarked = bookmark is not None
        
        # Record reading progress
        if user_id:
            await self._record_progress(user_id, shloka.chapter, shloka.shloka_number)
        
        return ShlokaDetailResponse(
            **shloka.__dict__,
            explanation=explanation,
            isBookmarked=is_bookmarked
        )
    
    async def _record_progress(
        self,
        user_id: UUID,
        chapter: int,
        shloka_number: int
    ):
        """Record or update reading progress."""
        progress = self.db.query(ReadingProgress).filter(
            and_(
                ReadingProgress.user_id == user_id,
                ReadingProgress.chapter == chapter,
                ReadingProgress.shloka_number == shloka_number
            )
        ).first()
        
        if progress:
            progress.last_read_at = datetime.utcnow()
        else:
            progress = ReadingProgress(
                user_id=user_id,
                chapter=chapter,
                shloka_number=shloka_number
            )
            self.db.add(progress)
        
        self.db.commit()
```

### Authentication and Authorization

#### Auth Flow

```mermaid
sequenceDiagram
    participant Client
    participant API as FastAPI
    participant Auth as Auth Service
    participant DB as PostgreSQL
    participant Google as Google OAuth
    
    alt Email/Password Login
        Client->>API: POST /auth/login {email, password}
        API->>Auth: validate_credentials()
        Auth->>DB: Query user by email
        DB-->>Auth: User record
        Auth->>Auth: bcrypt.verify(password, hashed_password)
        Auth->>Auth: create_access_token(user_id)
        Auth-->>API: {user, access_token}
        API-->>Client: 200 OK {user, accessToken}
    else Google OAuth
        Client->>API: GET /auth/google
        API-->>Client: 302 Redirect to Google
        Client->>Google: OAuth consent
        Google-->>Client: Redirect with code
        Client->>API: GET /auth/google/callback?code=...
        API->>Google: Exchange code for token
        Google-->>API: Access token
        API->>Google: GET user info
        Google-->>API: User profile
        API->>Auth: find_or_create_oauth_user()
        Auth->>DB: Query or insert user
        DB-->>Auth: User record
        Auth->>Auth: create_access_token(user_id)
        Auth-->>API: {user, access_token}
        API-->>Client: 200 OK {user, accessToken}
    end
```

#### Auth Middleware

```python
# dependencies.py
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import Optional

from .database import get_db
from .utils.jwt import decode_access_token
from .models.user import User

security = HTTPBearer(auto_error=False)

async def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    db: Session = Depends(get_db)
) -> Optional[User]:
    """
    Get current authenticated user from JWT token.
    Returns None if no token or invalid token (for optional auth).
    """
    if not credentials:
        return None
    
    try:
        payload = decode_access_token(credentials.credentials)
        user_id = payload.get("sub")
        
        if not user_id:
            return None
        
        user = db.query(User).filter(User.id == user_id).first()
        return user
    except Exception:
        return None

async def require_auth(
    current_user: Optional[User] = Depends(get_current_user)
) -> User:
    """
    Require authentication. Raises 401 if not authenticated.
    """
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return current_user

# utils/jwt.py
from datetime import datetime, timedelta
from typing import Dict, Any
from jose import JWTError, jwt
from ..config import settings

def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """Create JWT access token."""
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=7)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )
    return encoded_jwt

def decode_access_token(token: str) -> Dict[str, Any]:
    """Decode and validate JWT token."""
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )

# utils/password.py
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Hash password using bcrypt."""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password against hash."""
    return pwd_context.verify(plain_password, hashed_password)
```

---


## RAG Pipeline Architecture

### RAG Service Implementation

```python
# services/rag_service.py
from typing import List, Dict, Any
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss
import ollama

from ..models.shloka import Shloka
from ..config import settings

class RAGService:
    def __init__(self):
        # Load embedding model
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Load FAISS index
        self.index = faiss.read_index(settings.FAISS_INDEX_PATH)
        
        # Load shloka metadata (mapping index to shloka_id)
        self.index_to_shloka = self._load_index_mapping()
        
        # Ollama client
        self.llm_model = settings.OLLAMA_MODEL  # "mistral:7b"
    
    async def generate_explanation(
        self,
        shloka: Shloka,
        context_size: int = 3
    ) -> str:
        """
        Generate AI explanation for a shloka using RAG.
        
        Args:
            shloka: The shloka to explain
            context_size: Number of related shlokas to retrieve for context
        
        Returns:
            AI-generated explanation grounded in Gita text
        """
        # Retrieve related shlokas for context
        related_shlokas = await self.retrieve_similar_shlokas(
            query=f"{shloka.sanskrit_text} {shloka.meaning}",
            top_k=context_size,
            exclude_id=shloka.id
        )
        
        # Build prompt with constraints
        prompt = self._build_explanation_prompt(shloka, related_shlokas)
        
        # Generate explanation using Ollama
        try:
            response = ollama.generate(
                model=self.llm_model,
                prompt=prompt,
                options={
                    'temperature': 0.7,
                    'top_p': 0.9,
                    'max_tokens': 500,
                }
            )
            explanation = response['response'].strip()
            return explanation
        except Exception as e:
            # Fallback to basic explanation if LLM fails
            return self._fallback_explanation(shloka)
    
    async def retrieve_similar_shlokas(
        self,
        query: str,
        top_k: int = 5,
        exclude_id: str = None
    ) -> List[Shloka]:
        """
        Retrieve semantically similar shlokas using FAISS.
        
        Args:
            query: Search query text
            top_k: Number of results to return
            exclude_id: Shloka ID to exclude from results
        
        Returns:
            List of similar shlokas with relevance scores
        """
        # Generate query embedding
        query_embedding = self.embedding_model.encode([query])[0]
        query_embedding = np.array([query_embedding]).astype('float32')
        
        # Search FAISS index
        distances, indices = self.index.search(query_embedding, top_k + 1)
        
        # Convert to shloka IDs and fetch from database
        similar_shlokas = []
        for idx, distance in zip(indices[0], distances[0]):
            shloka_id = self.index_to_shloka.get(int(idx))
            if shloka_id and shloka_id != exclude_id:
                # Fetch shloka from database
                shloka = self._get_shloka_by_id(shloka_id)
                if shloka:
                    similar_shlokas.append({
                        'shloka': shloka,
                        'relevance_score': float(1 / (1 + distance))  # Convert distance to similarity
                    })
        
        return similar_shlokas[:top_k]
    
    async def search_by_problem(
        self,
        problem_id: str,
        top_k: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Find relevant shlokas for a life guidance problem.
        
        Args:
            problem_id: Problem category identifier
            top_k: Number of recommendations
        
        Returns:
            List of shlokas with practical explanations
        """
        # Get problem keywords from configuration
        problem_keywords = self._get_problem_keywords(problem_id)
        query = " ".join(problem_keywords)
        
        # Retrieve relevant shlokas
        similar_shlokas = await self.retrieve_similar_shlokas(query, top_k)
        
        # Generate practical explanations
        recommendations = []
        for item in similar_shlokas:
            shloka = item['shloka']
            explanation = await self._generate_practical_explanation(
                shloka,
                problem_id
            )
            recommendations.append({
                'shloka': shloka,
                'explanation': explanation,
                'relevance_score': item['relevance_score']
            })
        
        return recommendations
    
    def _build_explanation_prompt(
        self,
        shloka: Shloka,
        related_shlokas: List[Dict]
    ) -> str:
        """Build prompt for explanation generation with hallucination constraints."""
        context_text = "\n\n".join([
            f"Related Verse {i+1}:\n"
            f"Sanskrit: {s['shloka'].sanskrit_text}\n"
            f"Meaning: {s['shloka'].meaning}"
            for i, s in enumerate(related_shlokas)
        ])
        
        prompt = f"""You are a wise teacher explaining the Bhagavad Gita to students aged 12-22.

CRITICAL RULES:
1. Base your explanation ONLY on the verse provided and related verses below
2. Do NOT add information not present in these verses
3. Use simple, student-friendly language
4. Keep explanation under 200 words
5. Focus on practical wisdom applicable to daily life

TARGET VERSE:
Chapter {shloka.chapter}, Verse {shloka.shloka_number}
Sanskrit: {shloka.sanskrit_text}
Transliteration: {shloka.transliteration}
Meaning: {shloka.meaning}

RELATED VERSES FOR CONTEXT:
{context_text}

Provide a clear, simple explanation of what this verse teaches, using only the information from the verses above. Make it relatable to a student's life.

Explanation:"""
        
        return prompt
    
    def _build_practical_prompt(
        self,
        shloka: Shloka,
        problem_id: str
    ) -> str:
        """Build prompt for practical life guidance."""
        problem_descriptions = {
            'stress': 'dealing with stress and anxiety',
            'fear': 'overcoming fear and worry',
            'confusion': 'finding clarity in confusion',
            'anger': 'managing anger and frustration',
            'sadness': 'coping with sadness and disappointment',
            'purpose': 'finding life purpose and meaning',
            'relationships': 'navigating relationships',
            'decision-making': 'making difficult decisions',
        }
        
        problem_desc = problem_descriptions.get(problem_id, 'life challenges')
        
        prompt = f"""You are a wise mentor helping a student with {problem_desc}.

VERSE:
Chapter {shloka.chapter}, Verse {shloka.shloka_number}
Sanskrit: {shloka.sanskrit_text}
Meaning: {shloka.meaning}

TASK:
Explain how this verse's wisdom can help with {problem_desc}. 
- Use simple language for students
- Give 1-2 practical examples
- Keep it under 150 words
- Base explanation ONLY on this verse

Practical Guidance:"""
        
        return prompt
    
    async def _generate_practical_explanation(
        self,
        shloka: Shloka,
        problem_id: str
    ) -> str:
        """Generate practical explanation for life guidance."""
        prompt = self._build_practical_prompt(shloka, problem_id)
        
        try:
            response = ollama.generate(
                model=self.llm_model,
                prompt=prompt,
                options={'temperature': 0.7, 'max_tokens': 300}
            )
            return response['response'].strip()
        except Exception:
            return self._fallback_explanation(shloka)
    
    def _fallback_explanation(self, shloka: Shloka) -> str:
        """Fallback explanation if LLM is unavailable."""
        return (
            f"This verse from Chapter {shloka.chapter} teaches: {shloka.meaning}. "
            "For a detailed explanation, please try again when online."
        )
    
    def _get_problem_keywords(self, problem_id: str) -> List[str]:
        """Get search keywords for a problem category."""
        keywords_map = {
            'stress': ['peace', 'calm', 'equanimity', 'tranquility', 'serenity'],
            'fear': ['courage', 'fearlessness', 'strength', 'confidence'],
            'confusion': ['clarity', 'wisdom', 'understanding', 'knowledge'],
            'anger': ['patience', 'forgiveness', 'compassion', 'control'],
            'sadness': ['joy', 'contentment', 'acceptance', 'resilience'],
            'purpose': ['dharma', 'duty', 'purpose', 'meaning', 'path'],
            'relationships': ['love', 'compassion', 'understanding', 'harmony'],
            'decision-making': ['wisdom', 'discernment', 'action', 'choice'],
        }
        return keywords_map.get(problem_id, ['wisdom', 'guidance'])
    
    def _load_index_mapping(self) -> Dict[int, str]:
        """Load mapping from FAISS index position to shloka ID."""
        import json
        with open(settings.FAISS_MAPPING_PATH, 'r') as f:
            return json.load(f)
    
    def _get_shloka_by_id(self, shloka_id: str) -> Shloka:
        """Fetch shloka from database by ID."""
        from ..database import SessionLocal
        db = SessionLocal()
        try:
            return db.query(Shloka).filter(Shloka.id == shloka_id).first()
        finally:
            db.close()
```

### Ingestion Pipeline (One-time Setup)

```python
# services/ingestion_service.py
import pdfplumber
import re
from typing import List, Dict
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss
import json

from ..models.shloka import Shloka
from ..models.chapter import Chapter
from ..database import SessionLocal

class IngestionService:
    def __init__(self):
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
    
    def ingest_gita_pdf(self, pdf_path: str) -> List[Dict]:
        """
        Extract Bhagavad Gita content from PDF.
        
        Returns:
            List of shloka dictionaries with all fields
        """
        shlokas = []
        
        with pdfplumber.open(pdf_path) as pdf:
            current_chapter = None
            current_shloka = None
            
            for page in pdf.pages:
                text = page.extract_text()
                
                # Parse text to identify chapters and shlokas
                # This is highly dependent on PDF structure
                # Adjust regex patterns based on actual PDF format
                
                chapter_match = re.search(r'Chapter (\d+)', text)
                if chapter_match:
                    current_chapter = int(chapter_match.group(1))
                
                # Extract shloka blocks (adjust pattern to PDF format)
                shloka_blocks = re.findall(
                    r'(\d+\.\d+)\s+(.*?)\n(.*?)\n(.*?)(?=\n\d+\.\d+|\Z)',
                    text,
                    re.DOTALL
                )
                
                for block in shloka_blocks:
                    verse_num, sanskrit, transliteration, meaning = block
                    chapter, shloka_num = map(int, verse_num.split('.'))
                    
                    shlokas.append({
                        'chapter': chapter,
                        'shloka_number': shloka_num,
                        'sanskrit_text': sanskrit.strip(),
                        'transliteration': transliteration.strip(),
                        'meaning': meaning.strip(),
                        'themes': self._extract_themes(meaning),
                    })
        
        return shlokas
    
    def generate_embeddings(self, shlokas: List[Dict]) -> np.ndarray:
        """Generate embeddings for all shlokas."""
        texts = [
            f"{s['sanskrit_text']} {s['transliteration']} {s['meaning']}"
            for s in shlokas
        ]
        embeddings = self.embedding_model.encode(texts, show_progress_bar=True)
        return embeddings
    
    def build_faiss_index(
        self,
        embeddings: np.ndarray,
        output_path: str
    ) -> faiss.Index:
        """Build and save FAISS index."""
        dimension = embeddings.shape[1]
        
        # Use IndexFlatL2 for exact search (good for <1M vectors)
        index = faiss.IndexFlatL2(dimension)
        index.add(embeddings.astype('float32'))
        
        # Save index
        faiss.write_index(index, output_path)
        
        return index
    
    def seed_database(self, shlokas: List[Dict]):
        """Populate PostgreSQL database with shlokas."""
        db = SessionLocal()
        
        try:
            # Seed chapters first
            self._seed_chapters(db)
            
            # Seed shlokas
            for idx, shloka_data in enumerate(shlokas):
                shloka = Shloka(
                    chapter=shloka_data['chapter'],
                    shloka_number=shloka_data['shloka_number'],
                    sanskrit_text=shloka_data['sanskrit_text'],
                    transliteration=shloka_data['transliteration'],
                    meaning=shloka_data['meaning'],
                    themes=shloka_data['themes'],
                    embedding_index=idx,
                    audio_file_path=self._get_audio_path(
                        shloka_data['chapter'],
                        shloka_data['shloka_number']
                    )
                )
                db.add(shloka)
            
            db.commit()
            print(f"Seeded {len(shlokas)} shlokas")
        
        finally:
            db.close()
    
    def save_index_mapping(
        self,
        shlokas: List[Dict],
        output_path: str
    ):
        """Save mapping from FAISS index to shloka IDs."""
        # After seeding database, fetch shloka IDs
        db = SessionLocal()
        try:
            mapping = {}
            for idx, shloka_data in enumerate(shlokas):
                shloka = db.query(Shloka).filter(
                    Shloka.chapter == shloka_data['chapter'],
                    Shloka.shloka_number == shloka_data['shloka_number']
                ).first()
                if shloka:
                    mapping[idx] = str(shloka.id)
            
            with open(output_path, 'w') as f:
                json.dump(mapping, f)
            
            print(f"Saved index mapping with {len(mapping)} entries")
        finally:
            db.close()
    
    def _extract_themes(self, meaning: str) -> List[str]:
        """Extract theme keywords from meaning text."""
        # Simple keyword extraction (can be enhanced with NLP)
        theme_keywords = [
            'duty', 'action', 'knowledge', 'devotion', 'yoga',
            'peace', 'wisdom', 'self', 'soul', 'karma',
            'dharma', 'meditation', 'detachment', 'surrender'
        ]
        
        meaning_lower = meaning.lower()
        themes = [kw for kw in theme_keywords if kw in meaning_lower]
        return themes or ['general']
    
    def _get_audio_path(self, chapter: int, shloka_number: int) -> str:
        """Generate audio file path."""
        return f"audio/chapter_{chapter:02d}/shloka_{shloka_number:03d}.mp3"
    
    def _seed_chapters(self, db):
        """Seed chapter metadata."""
        chapters_data = [
            {
                'id': 1,
                'title': 'Arjuna's Dilemma',
                'sanskrit_name': 'Arjuna Vishada Yoga',
                'description': 'Arjuna faces moral confusion on the battlefield',
                'shloka_count': 47
            },
            # ... (all 18 chapters)
        ]
        
        for chapter_data in chapters_data:
            chapter = Chapter(**chapter_data)
            db.add(chapter)
        
        db.commit()

# CLI script to run ingestion
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python ingestion_service.py <path_to_gita_pdf>")
        sys.exit(1)
    
    pdf_path = sys.argv[1]
    service = IngestionService()
    
    print("Step 1: Extracting text from PDF...")
    shlokas = service.ingest_gita_pdf(pdf_path)
    print(f"Extracted {len(shlokas)} shlokas")
    
    print("Step 2: Generating embeddings...")
    embeddings = service.generate_embeddings(shlokas)
    print(f"Generated embeddings with shape {embeddings.shape}")
    
    print("Step 3: Building FAISS index...")
    service.build_faiss_index(embeddings, "data/faiss_index.bin")
    print("FAISS index saved")
    
    print("Step 4: Seeding database...")
    service.seed_database(shlokas)
    print("Database seeded")
    
    print("Step 5: Saving index mapping...")
    service.save_index_mapping(shlokas, "data/faiss_mapping.json")
    print("Index mapping saved")
    
    print("Ingestion complete!")
```

---


## Unified Project Structure

```
bhagavad-gita-app/
├── .github/                          # CI/CD workflows
│   └── workflows/
│       ├── ci.yml                    # Run tests on PR
│       ├── deploy-backend.yml        # Deploy backend
│       └── deploy-frontend.yml       # Deploy frontend
├── frontend/                         # React Native mobile app
│   ├── src/
│   │   ├── components/               # Reusable UI components
│   │   │   ├── common/
│   │   │   ├── shloka/
│   │   │   └── navigation/
│   │   ├── screens/                  # Screen components
│   │   │   ├── HomeScreen.tsx
│   │   │   ├── ChapterListScreen.tsx
│   │   │   ├── ShlokaListScreen.tsx
│   │   │   ├── ShlokaDetailScreen.tsx
│   │   │   ├── LifeGuidanceScreen.tsx
│   │   │   ├── SearchScreen.tsx
│   │   │   ├── ProfileScreen.tsx
│   │   │   ├── SettingsScreen.tsx
│   │   │   └── auth/
│   │   ├── hooks/                    # Custom React hooks
│   │   ├── services/                 # API client services
│   │   ├── stores/                   # Zustand state stores
│   │   ├── navigation/               # Navigation configuration
│   │   ├── types/                    # TypeScript types
│   │   ├── utils/                    # Utility functions
│   │   ├── styles/                   # Global styles and theme
│   │   └── App.tsx                   # Root component
│   ├── assets/                       # Static assets
│   │   ├── images/
│   │   └── fonts/
│   ├── __tests__/                    # Frontend tests
│   ├── app.json                      # Expo configuration
│   ├── package.json
│   ├── tsconfig.json
│   └── .env.example
├── backend/                          # FastAPI backend
│   ├── src/
│   │   ├── routes/                   # API route handlers
│   │   │   ├── __init__.py
│   │   │   ├── auth.py
│   │   │   ├── content.py
│   │   │   ├── bookmarks.py
│   │   │   ├── search.py
│   │   │   ├── profile.py
│   │   │   └── health.py
│   │   ├── services/                 # Business logic
│   │   │   ├── __init__.py
│   │   │   ├── auth_service.py
│   │   │   ├── content_service.py
│   │   │   ├── rag_service.py
│   │   │   ├── notification_service.py
│   │   │   ├── cache_service.py
│   │   │   └── ingestion_service.py
│   │   ├── models/                   # SQLAlchemy ORM models
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   ├── shloka.py
│   │   │   ├── chapter.py
│   │   │   ├── bookmark.py
│   │   │   ├── progress.py
│   │   │   └── daily_wisdom.py
│   │   ├── schemas/                  # Pydantic schemas
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   ├── shloka.py
│   │   │   ├── auth.py
│   │   │   └── responses.py
│   │   ├── middleware/               # Custom middleware
│   │   │   ├── __init__.py
│   │   │   ├── cors.py
│   │   │   ├── error_handler.py
│   │   │   └── logging.py
│   │   ├── utils/                    # Utility functions
│   │   │   ├── __init__.py
│   │   │   ├── jwt.py
│   │   │   ├── password.py
│   │   │   └── validators.py
│   │   ├── tasks/                    # Celery tasks
│   │   │   ├── __init__.py
│   │   │   ├── celery_app.py
│   │   │   └── daily_wisdom.py
│   │   ├── main.py                   # FastAPI app entry point
│   │   ├── config.py                 # Configuration
│   │   ├── database.py               # Database connection
│   │   └── dependencies.py           # Shared dependencies
│   ├── tests/                        # Backend tests
│   │   ├── unit/
│   │   ├── integration/
│   │   └── conftest.py
│   ├── alembic/                      # Database migrations
│   │   ├── versions/
│   │   └── env.py
│   ├── data/                         # Data files
│   │   ├── faiss_index.bin           # FAISS vector store
│   │   ├── faiss_mapping.json        # Index to shloka ID mapping
│   │   └── gita_source.pdf           # Source PDF
│   ├── audio/                        # Audio files
│   │   ├── chapter_01/
│   │   ├── chapter_02/
│   │   └── ...
│   ├── requirements.txt              # Python dependencies
│   ├── pyproject.toml                # Python project config
│   ├── alembic.ini                   # Alembic configuration
│   └── .env.example
├── shared/                           # Shared code (future)
│   ├── types/                        # Shared TypeScript types
│   └── constants/                    # Shared constants
├── infrastructure/                   # Infrastructure as Code
│   ├── docker/
│   │   ├── Dockerfile.backend
│   │   ├── Dockerfile.ollama
│   │   └── Dockerfile.frontend
│   ├── docker-compose.yml            # Local development
│   ├── docker-compose.prod.yml       # Production
│   └── nginx/                        # Nginx configuration (if needed)
├── scripts/                          # Build and deployment scripts
│   ├── setup.sh                      # Initial setup
│   ├── seed-data.sh                  # Run ingestion
│   ├── run-tests.sh                  # Run all tests
│   └── deploy.sh                     # Deployment script
├── docs/                             # Documentation
│   ├── prd.md                        # Product Requirements
│   ├── architecture.md               # This document
│   ├── api-docs.md                   # API documentation
│   └── deployment.md                 # Deployment guide
├── .gitignore
├── .env.example                      # Environment template
├── README.md                         # Project overview
└── package.json                      # Root package.json (monorepo)
```

---

## Development Workflow

### Local Development Setup

#### Prerequisites

```bash
# Install Node.js (v18+)
node --version

# Install Python (3.11+)
python --version

# Install Docker and Docker Compose
docker --version
docker-compose --version

# Install Ollama
curl https://ollama.ai/install.sh | sh

# Pull Mistral model
ollama pull mistral:7b
```

#### Initial Setup

```bash
# Clone repository
git clone https://github.com/your-org/bhagavad-gita-app.git
cd bhagavad-gita-app

# Install frontend dependencies
cd frontend
npm install
cd ..

# Install backend dependencies
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cd ..

# Copy environment files
cp frontend/.env.example frontend/.env.local
cp backend/.env.example backend/.env

# Start infrastructure services
docker-compose up -d postgres redis

# Run database migrations
cd backend
alembic upgrade head

# Run ingestion (one-time setup)
python -m src.services.ingestion_service data/gita_source.pdf

# Start Ollama (if not running as service)
ollama serve
```

#### Development Commands

```bash
# Start all services (recommended)
docker-compose up

# Or start services individually:

# Start backend
cd backend
source venv/bin/activate
uvicorn src.main:app --reload --port 8000

# Start Celery worker (separate terminal)
cd backend
celery -A src.tasks.celery_app worker --loglevel=info

# Start Celery beat (separate terminal)
cd backend
celery -A src.tasks.celery_app beat --loglevel=info

# Start frontend
cd frontend
npm start

# Run tests
npm test                    # Frontend tests
cd backend && pytest        # Backend tests
```

### Environment Configuration

#### Required Environment Variables

```bash
# Frontend (.env.local)
EXPO_PUBLIC_API_URL=http://localhost:8000/api
EXPO_PUBLIC_GOOGLE_CLIENT_ID=your_google_client_id

# Backend (.env)
# Database
DATABASE_URL=postgresql://gita_user:password@localhost:5432/gita_db

# Redis
REDIS_URL=redis://localhost:6379/0

# JWT
JWT_SECRET_KEY=your_secret_key_here_change_in_production
JWT_ALGORITHM=HS256

# OAuth
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
GOOGLE_REDIRECT_URI=http://localhost:8000/api/auth/google/callback

# Ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=mistral:7b

# FAISS
FAISS_INDEX_PATH=data/faiss_index.bin
FAISS_MAPPING_PATH=data/faiss_mapping.json

# File Storage
AUDIO_FILES_PATH=audio/

# Celery
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0

# Shared
ENVIRONMENT=development
LOG_LEVEL=INFO
```

---


## Deployment Architecture

### Deployment Strategy

**Frontend Deployment:**
- **Platform**: Vercel / Netlify (for web) + Expo EAS (for mobile apps)
- **Build Command**: `npm run build` (web) / `eas build` (mobile)
- **Output Directory**: `dist/` (web)
- **CDN/Edge**: Automatic via Vercel/Netlify edge network

**Backend Deployment:**
- **Platform**: Docker containers on cloud provider (AWS ECS, GCP Cloud Run, or DigitalOcean App Platform)
- **Build Command**: `docker build -f infrastructure/docker/Dockerfile.backend`
- **Deployment Method**: Container registry + orchestration platform

**Database & Services:**
- **PostgreSQL**: Managed database service (AWS RDS, GCP Cloud SQL, or DigitalOcean Managed Database)
- **Redis**: Managed Redis service or containerized
- **Ollama**: Self-hosted container with GPU support (optional)

### CI/CD Pipeline

```yaml
# .github/workflows/ci.yml
name: CI Pipeline

on:
  pull_request:
    branches: [main, develop]
  push:
    branches: [main, develop]

jobs:
  frontend-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '18'
      - name: Install dependencies
        run: cd frontend && npm ci
      - name: Run linter
        run: cd frontend && npm run lint
      - name: Run tests
        run: cd frontend && npm test
      - name: Build
        run: cd frontend && npm run build

  backend-tests:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: test
          POSTGRES_DB: test_db
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
      redis:
        image: redis:7
        options: >-
          --health-cmd "redis-cli ping"
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          cd backend
          pip install -r requirements.txt
      - name: Run linter
        run: cd backend && flake8 src/
      - name: Run type checker
        run: cd backend && mypy src/
      - name: Run tests
        run: cd backend && pytest
        env:
          DATABASE_URL: postgresql://postgres:test@localhost:5432/test_db
          REDIS_URL: redis://localhost:6379/0

# .github/workflows/deploy-backend.yml
name: Deploy Backend

on:
  push:
    branches: [main]
    paths:
      - 'backend/**'
      - 'infrastructure/**'

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v2
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: us-east-1
      
      - name: Login to Amazon ECR
        id: login-ecr
        uses: aws-actions/amazon-ecr-login@v1
      
      - name: Build and push Docker image
        env:
          ECR_REGISTRY: ${{ steps.login-ecr.outputs.registry }}
          ECR_REPOSITORY: gita-backend
          IMAGE_TAG: ${{ github.sha }}
        run: |
          docker build -f infrastructure/docker/Dockerfile.backend -t $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG .
          docker push $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG
      
      - name: Deploy to ECS
        run: |
          # Update ECS service with new image
          aws ecs update-service --cluster gita-cluster --service gita-backend --force-new-deployment
```

### Environments

| Environment | Frontend URL | Backend URL | Purpose |
|-------------|--------------|-------------|---------|
| Development | http://localhost:19006 | http://localhost:8000 | Local development |
| Staging | https://staging.bhagavadgita.app | https://api-staging.bhagavadgita.app | Pre-production testing |
| Production | https://bhagavadgita.app | https://api.bhagavadgita.app | Live environment |

### Docker Configuration

```dockerfile
# infrastructure/docker/Dockerfile.backend
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY backend/src ./src
COPY backend/alembic ./alembic
COPY backend/alembic.ini .
COPY backend/data ./data
COPY backend/audio ./audio

# Expose port
EXPOSE 8000

# Run migrations and start server
CMD alembic upgrade head && \
    uvicorn src.main:app --host 0.0.0.0 --port 8000
```

```dockerfile
# infrastructure/docker/Dockerfile.ollama
FROM ollama/ollama:latest

# Pull Mistral model during build
RUN ollama pull mistral:7b

EXPOSE 11434

CMD ["ollama", "serve"]
```

```yaml
# infrastructure/docker-compose.yml
version: '3.8'

services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_USER: gita_user
      POSTGRES_PASSWORD: gita_password
      POSTGRES_DB: gita_db
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U gita_user"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

  ollama:
    build:
      context: .
      dockerfile: infrastructure/docker/Dockerfile.ollama
    ports:
      - "11434:11434"
    volumes:
      - ollama_data:/root/.ollama
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]  # Optional: GPU acceleration

  backend:
    build:
      context: .
      dockerfile: infrastructure/docker/Dockerfile.backend
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql://gita_user:gita_password@postgres:5432/gita_db
      REDIS_URL: redis://redis:6379/0
      OLLAMA_BASE_URL: http://ollama:11434
      JWT_SECRET_KEY: ${JWT_SECRET_KEY}
      GOOGLE_CLIENT_ID: ${GOOGLE_CLIENT_ID}
      GOOGLE_CLIENT_SECRET: ${GOOGLE_CLIENT_SECRET}
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
      ollama:
        condition: service_started
    volumes:
      - ./backend/audio:/app/audio
      - ./backend/data:/app/data

  celery-worker:
    build:
      context: .
      dockerfile: infrastructure/docker/Dockerfile.backend
    command: celery -A src.tasks.celery_app worker --loglevel=info
    environment:
      DATABASE_URL: postgresql://gita_user:gita_password@postgres:5432/gita_db
      REDIS_URL: redis://redis:6379/0
      CELERY_BROKER_URL: redis://redis:6379/0
      CELERY_RESULT_BACKEND: redis://redis:6379/0
    depends_on:
      - redis
      - postgres

  celery-beat:
    build:
      context: .
      dockerfile: infrastructure/docker/Dockerfile.backend
    command: celery -A src.tasks.celery_app beat --loglevel=info
    environment:
      DATABASE_URL: postgresql://gita_user:gita_password@postgres:5432/gita_db
      REDIS_URL: redis://redis:6379/0
      CELERY_BROKER_URL: redis://redis:6379/0
      CELERY_RESULT_BACKEND: redis://redis:6379/0
    depends_on:
      - redis
      - postgres

volumes:
  postgres_data:
  redis_data:
  ollama_data:
```

---

## Security and Performance

### Security Requirements

**Frontend Security:**
- **CSP Headers**: `default-src 'self'; script-src 'self' 'unsafe-inline'; connect-src 'self' https://api.bhagavadgita.app`
- **XSS Prevention**: React Native's built-in escaping, sanitize user inputs
- **Secure Storage**: Use Expo SecureStore for sensitive data (tokens), AsyncStorage for non-sensitive cache

**Backend Security:**
- **Input Validation**: Pydantic schemas validate all inputs, reject malformed requests
- **Rate Limiting**: 100 requests/minute per IP for anonymous, 1000/minute for authenticated
- **CORS Policy**: Allow only frontend origins (https://bhagavadgita.app, http://localhost:19006 for dev)

**Authentication Security:**
- **Token Storage**: JWT tokens in SecureStore (mobile), httpOnly cookies (web future)
- **Session Management**: 7-day token expiration, refresh token mechanism (Phase 2)
- **Password Policy**: Minimum 8 characters, bcrypt with cost factor 12

**Additional Security Measures:**
- HTTPS enforcement in production
- SQL injection prevention via SQLAlchemy parameterized queries
- Secrets management via environment variables (never commit to git)
- Regular dependency updates and security scanning

### Performance Optimization

**Frontend Performance:**
- **Bundle Size Target**: <5MB initial bundle, code splitting for screens
- **Loading Strategy**: 
  - Lazy load screens with React.lazy()
  - Prefetch next chapter's shlokas on chapter view
  - Image optimization with WebP format
- **Caching Strategy**: 
  - Cache chapters and shlokas in AsyncStorage (7-day TTL)
  - Cache explanations in memory (session-based)
  - Offline-first architecture with background sync

**Backend Performance:**
- **Response Time Target**: 
  - Content endpoints: <200ms
  - RAG explanation: <2s (NFR2)
  - Search: <500ms
- **Database Optimization**:
  - Indexes on frequently queried columns (see Database Schema section)
  - Connection pooling (max 20 connections)
  - Query optimization with SQLAlchemy eager loading
- **Caching Strategy**:
  - Redis cache for:
    - RAG explanations (24-hour TTL)
    - Chapter/shloka lists (7-day TTL)
    - Daily wisdom (24-hour TTL)
  - FAISS index loaded in memory at startup
  - Embedding model loaded once and reused

**RAG Pipeline Optimization:**
- Pre-compute embeddings during ingestion (not at query time)
- Use FAISS IndexFlatL2 for exact search (fast for <1M vectors)
- Limit context to top 3 related shlokas to reduce LLM input size
- Stream LLM responses for better perceived performance
- Cache generated explanations aggressively

**Scalability Considerations:**
- Horizontal scaling: Backend is stateless, can run multiple instances behind load balancer
- Database read replicas for read-heavy workloads (future)
- CDN for static assets and audio files (future)
- FAISS index can be sharded if vector count grows significantly (not needed for Gita's ~700 shlokas)

---


## Testing Strategy

### Testing Pyramid

```
        E2E Tests (Manual Phase 1)
       /                          \
      /    Integration Tests       \
     /    (API + Database)          \
    /                                \
   /  Frontend Unit    Backend Unit  \
  /   (Components)     (Services)     \
 /____________________________________\
```

### Test Organization

#### Frontend Tests

```
frontend/__tests__/
├── unit/
│   ├── components/
│   │   ├── ShlokaCard.test.tsx
│   │   ├── AudioPlayer.test.tsx
│   │   └── BookmarkButton.test.tsx
│   ├── hooks/
│   │   ├── useAuth.test.ts
│   │   └── useBookmarks.test.ts
│   ├── services/
│   │   ├── contentService.test.ts
│   │   └── authService.test.ts
│   └── utils/
│       ├── formatting.test.ts
│       └── validation.test.ts
├── integration/
│   ├── screens/
│   │   ├── HomeScreen.test.tsx
│   │   ├── ShlokaDetailScreen.test.tsx
│   │   └── LifeGuidanceScreen.test.tsx
│   └── navigation/
│       └── AppNavigator.test.tsx
└── setup.ts
```

#### Backend Tests

```
backend/tests/
├── unit/
│   ├── services/
│   │   ├── test_auth_service.py
│   │   ├── test_content_service.py
│   │   ├── test_rag_service.py
│   │   └── test_notification_service.py
│   ├── utils/
│   │   ├── test_jwt.py
│   │   ├── test_password.py
│   │   └── test_validators.py
│   └── models/
│       └── test_models.py
├── integration/
│   ├── routes/
│   │   ├── test_auth_routes.py
│   │   ├── test_content_routes.py
│   │   ├── test_bookmark_routes.py
│   │   └── test_search_routes.py
│   └── database/
│       └── test_repositories.py
└── conftest.py
```

#### E2E Tests (Manual for Phase 1)

```
Manual test scenarios documented in:
docs/test-scenarios.md

Key flows to test:
1. User registration and login
2. Browse chapters and shlokas
3. View shloka with AI explanation
4. Bookmark and unbookmark shlokas
5. Daily wisdom notification
6. Life guidance recommendations
7. Search functionality
8. Offline mode
```

### Test Examples

#### Frontend Component Test

```typescript
// __tests__/unit/components/ShlokaCard.test.tsx
import React from 'react';
import { render, fireEvent } from '@testing-library/react-native';
import { ShlokaCard } from '../../../src/components/shloka/ShlokaCard';
import { Shloka } from '../../../src/types/models';

const mockShloka: Shloka = {
  id: '123',
  chapter: 2,
  shlokaNumber: 47,
  sanskritText: 'कर्मण्येवाधिकारस्ते मा फलेषु कदाचन',
  transliteration: 'karmaṇy-evādhikāras te mā phaleṣhu kadāchana',
  meaning: 'You have a right to perform your duty, but not to the fruits of action',
  themes: ['karma', 'duty', 'detachment'],
};

describe('ShlokaCard', () => {
  it('renders shloka information correctly', () => {
    const { getByText } = render(<ShlokaCard shloka={mockShloka} />);
    
    expect(getByText('Verse 47')).toBeTruthy();
    expect(getByText(mockShloka.sanskritText)).toBeTruthy();
    expect(getByText(mockShloka.transliteration)).toBeTruthy();
  });

  it('shows bookmark indicator when bookmarked', () => {
    const { getByText } = render(
      <ShlokaCard shloka={mockShloka} isBookmarked={true} />
    );
    
    expect(getByText('🔖')).toBeTruthy();
  });

  it('navigates to detail screen on press', () => {
    const mockNavigate = jest.fn();
    jest.mock('@react-navigation/native', () => ({
      useNavigation: () => ({ navigate: mockNavigate }),
    }));

    const { getByTestId } = render(<ShlokaCard shloka={mockShloka} />);
    const card = getByTestId('shloka-card');
    
    fireEvent.press(card);
    
    expect(mockNavigate).toHaveBeenCalledWith('ShlokaDetail', {
      shlokaId: '123',
    });
  });
});
```

#### Backend API Test

```python
# tests/integration/routes/test_content_routes.py
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from src.main import app
from src.models.shloka import Shloka
from src.models.user import User
from src.utils.jwt import create_access_token

client = TestClient(app)

@pytest.fixture
def test_user(db: Session):
    """Create a test user."""
    user = User(
        email="test@example.com",
        hashed_password="hashed_password"
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@pytest.fixture
def auth_headers(test_user):
    """Create authentication headers."""
    token = create_access_token({"sub": str(test_user.id)})
    return {"Authorization": f"Bearer {token}"}

def test_get_chapters(db: Session):
    """Test getting all chapters."""
    response = client.get("/api/chapters")
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 18
    assert data[0]["id"] == 1
    assert "title" in data[0]
    assert "sanskritName" in data[0]

def test_get_shlokas_by_chapter(db: Session):
    """Test getting shlokas for a chapter."""
    response = client.get("/api/chapters/2/shlokas")
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert all(s["chapter"] == 2 for s in data)

def test_get_shloka_detail(db: Session, test_shloka):
    """Test getting shloka detail with explanation."""
    response = client.get(f"/api/shlokas/{test_shloka.id}")
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == str(test_shloka.id)
    assert "explanation" in data
    assert len(data["explanation"]) > 0

def test_create_bookmark(db: Session, auth_headers, test_shloka):
    """Test creating a bookmark."""
    response = client.post(
        "/api/bookmarks",
        json={
            "chapter": test_shloka.chapter,
            "shlokaNumber": test_shloka.shloka_number
        },
        headers=auth_headers
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["chapter"] == test_shloka.chapter
    assert data["shlokaNumber"] == test_shloka.shloka_number

def test_create_bookmark_requires_auth(db: Session):
    """Test that bookmark creation requires authentication."""
    response = client.post(
        "/api/bookmarks",
        json={"chapter": 1, "shlokaNumber": 1}
    )
    
    assert response.status_code == 401

def test_rag_explanation_performance(db: Session, test_shloka):
    """Test that RAG explanation meets performance requirement."""
    import time
    
    start = time.time()
    response = client.get(f"/api/shlokas/{test_shloka.id}")
    duration = time.time() - start
    
    assert response.status_code == 200
    assert duration < 2.0  # NFR2: <2 seconds
```

#### E2E Test (Manual)

```markdown
# Manual E2E Test: Complete User Journey

## Test Case: New User Onboarding and First Shloka

### Prerequisites
- Fresh app installation
- No existing account

### Steps
1. Launch app
   - Expected: See login/register screen

2. Tap "Register with Email"
   - Enter email: test@example.com
   - Enter password: TestPass123
   - Tap "Register"
   - Expected: Navigate to home screen

3. View Daily Wisdom
   - Expected: See today's shloka with preview
   - Tap "Read More"
   - Expected: Navigate to shloka detail

4. View Shloka Detail
   - Expected: See Sanskrit text, transliteration, meaning
   - Expected: See AI explanation (loads within 2 seconds)
   - Expected: See audio player
   - Tap play button
   - Expected: Audio plays

5. Bookmark Shloka
   - Tap bookmark button
   - Expected: Button changes to bookmarked state
   - Navigate back to home

6. Browse Chapters
   - Tap "Explore" tab
   - Expected: See list of 18 chapters
   - Tap "Chapter 2"
   - Expected: See list of shlokas

7. Test Offline Mode
   - Enable airplane mode
   - Navigate to previously viewed chapter
   - Expected: Content loads from cache
   - Try to view new shloka
   - Expected: See "Offline" indicator

8. Test Life Guidance
   - Disable airplane mode
   - Tap "Life Guidance" from home
   - Select "Stress"
   - Expected: See 3-5 recommended shlokas
   - Tap first recommendation
   - Expected: See practical explanation

### Pass Criteria
- All steps complete without errors
- Performance meets targets (<2s for explanations)
- Offline mode works for cached content
- UI is responsive and intuitive
```

### Testing Tools and Configuration

```json
// frontend/package.json (test scripts)
{
  "scripts": {
    "test": "jest",
    "test:watch": "jest --watch",
    "test:coverage": "jest --coverage",
    "lint": "eslint src/ --ext .ts,.tsx",
    "type-check": "tsc --noEmit"
  },
  "jest": {
    "preset": "jest-expo",
    "transformIgnorePatterns": [
      "node_modules/(?!((jest-)?react-native|@react-native(-community)?)|expo(nent)?|@expo(nent)?/.*|@expo-google-fonts/.*|react-navigation|@react-navigation/.*|@unimodules/.*|unimodules|sentry-expo|native-base|react-native-svg)"
    ],
    "collectCoverageFrom": [
      "src/**/*.{ts,tsx}",
      "!src/**/*.d.ts"
    ],
    "coverageThreshold": {
      "global": {
        "branches": 70,
        "functions": 70,
        "lines": 70,
        "statements": 70
      }
    }
  }
}
```

```ini
# backend/pytest.ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = 
    --verbose
    --cov=src
    --cov-report=html
    --cov-report=term-missing
    --cov-fail-under=80
```

### Coverage Targets

- **Frontend**: 70% code coverage (components, hooks, services)
- **Backend**: 80% code coverage (services, routes, utils)
- **Critical Paths**: 100% coverage for auth, RAG, and payment flows (future)

---


## Coding Standards

### Critical Fullstack Rules

- **Type Safety**: Always use TypeScript in frontend, type hints in Python backend. No `any` types without explicit justification.

- **Error Handling**: All API calls must have try-catch blocks with user-friendly error messages. Backend must return consistent error format: `{"detail": "Error message"}`.

- **Authentication**: Never store passwords in plain text. Always use bcrypt for hashing. JWT tokens must have expiration. Validate tokens on every protected endpoint.

- **RAG Constraints**: All LLM prompts must explicitly instruct the model to use only provided context. Never allow free-form generation without grounding.

- **Database Queries**: Always use SQLAlchemy ORM, never raw SQL. Use parameterized queries to prevent SQL injection. Close database sessions properly.

- **API Responses**: Follow REST conventions. Use appropriate HTTP status codes (200, 201, 400, 401, 404, 500). Include pagination for list endpoints (future).

- **Caching**: Cache expensive operations (RAG explanations, embeddings). Set appropriate TTLs. Invalidate cache on data updates.

- **Logging**: Log all errors with stack traces. Log authentication attempts. Never log sensitive data (passwords, tokens). Use structured logging.

- **Environment Variables**: Never commit secrets to git. Use `.env` files locally, environment variables in production. Validate required env vars at startup.

- **Code Organization**: Follow the project structure strictly. Keep components small (<300 lines). Services should have single responsibility.

- **Testing**: Write tests for all business logic. Mock external dependencies (LLM, database). Test error cases, not just happy paths.

- **Performance**: Avoid N+1 queries. Use eager loading for related data. Implement pagination for large datasets. Profile slow endpoints.

- **Offline Support**: All content endpoints must support offline fallback. Cache data in AsyncStorage. Sync changes when online.

- **Accessibility**: Use semantic HTML/React Native components. Provide alt text for images. Ensure sufficient color contrast. Support screen readers.

- **Mobile Optimization**: Minimize bundle size. Lazy load screens. Optimize images. Test on low-end devices. Handle slow networks gracefully.

### Python Backend Standards

```python
# Good: Type hints, error handling, logging
from typing import Optional
import logging

logger = logging.getLogger(__name__)

async def get_shloka(shloka_id: str, db: Session) -> Optional[Shloka]:
    """
    Retrieve shloka by ID.
    
    Args:
        shloka_id: UUID of the shloka
        db: Database session
    
    Returns:
        Shloka object or None if not found
    """
    try:
        shloka = db.query(Shloka).filter(Shloka.id == shloka_id).first()
        if not shloka:
            logger.warning(f"Shloka not found: {shloka_id}")
        return shloka
    except Exception as e:
        logger.error(f"Error fetching shloka {shloka_id}: {e}", exc_info=True)
        raise

# Bad: No types, no error handling
def get_shloka(id, db):
    return db.query(Shloka).filter(Shloka.id == id).first()
```

### TypeScript Frontend Standards

```typescript
// Good: Proper typing, error handling, user feedback
import { useState } from 'react';
import { contentService } from '../services/contentService';
import { Shloka } from '../types/models';

export const useShlokaDetail = (shlokaId: string) => {
  const [shloka, setShloka] = useState<Shloka | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchShloka = async () => {
    setLoading(true);
    setError(null);
    
    try {
      const data = await contentService.getShlokaDetail(shlokaId);
      setShloka(data);
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Failed to load shloka';
      setError(message);
      console.error('Error fetching shloka:', err);
    } finally {
      setLoading(false);
    }
  };

  return { shloka, loading, error, fetchShloka };
};

// Bad: No types, no error handling
export const useShlokaDetail = (shlokaId) => {
  const [shloka, setShloka] = useState(null);

  const fetchShloka = async () => {
    const data = await contentService.getShlokaDetail(shlokaId);
    setShloka(data);
  };

  return { shloka, fetchShloka };
};
```

### Git Commit Standards

```bash
# Format: <type>(<scope>): <subject>

# Types:
# feat: New feature
# fix: Bug fix
# docs: Documentation changes
# style: Code style changes (formatting, no logic change)
# refactor: Code refactoring
# test: Adding or updating tests
# chore: Build process or auxiliary tool changes

# Examples:
git commit -m "feat(rag): add caching for explanations"
git commit -m "fix(auth): handle expired token gracefully"
git commit -m "docs(api): update OpenAPI spec for bookmarks"
git commit -m "test(content): add integration tests for shloka endpoints"
```

---

## Monitoring and Observability

### Logging Strategy

**Backend Logging:**
```python
# src/middleware/logging.py
import logging
import time
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger(__name__)

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        
        # Log request
        logger.info(f"Request: {request.method} {request.url.path}")
        
        # Process request
        response = await call_next(request)
        
        # Log response
        duration = time.time() - start_time
        logger.info(
            f"Response: {response.status_code} "
            f"Duration: {duration:.3f}s "
            f"Path: {request.url.path}"
        )
        
        return response

# Structured logging format
LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        },
        'json': {
            '()': 'pythonjsonlogger.jsonlogger.JsonFormatter',
            'format': '%(asctime)s %(name)s %(levelname)s %(message)s'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'json',
            'level': 'INFO'
        },
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'logs/app.log',
            'maxBytes': 10485760,  # 10MB
            'backupCount': 5,
            'formatter': 'json',
            'level': 'INFO'
        }
    },
    'root': {
        'level': 'INFO',
        'handlers': ['console', 'file']
    }
}
```

**Frontend Logging:**
```typescript
// src/utils/logger.ts
export const logger = {
  info: (message: string, data?: any) => {
    console.log(`[INFO] ${message}`, data);
    // Send to analytics service (future)
  },
  
  error: (message: string, error?: Error) => {
    console.error(`[ERROR] ${message}`, error);
    // Send to error tracking service (future)
  },
  
  warn: (message: string, data?: any) => {
    console.warn(`[WARN] ${message}`, data);
  }
};
```

### Metrics and Monitoring

**Key Metrics to Track:**

1. **Performance Metrics**:
   - API response times (p50, p95, p99)
   - RAG explanation generation time
   - Database query duration
   - Cache hit rate

2. **Business Metrics**:
   - Daily active users
   - Shlokas viewed per user
   - Bookmarks created
   - Daily wisdom engagement rate
   - Life guidance usage

3. **System Metrics**:
   - CPU and memory usage
   - Database connection pool utilization
   - Redis memory usage
   - Error rate by endpoint

4. **User Experience Metrics**:
   - App crash rate
   - API error rate
   - Offline mode usage
   - Average session duration

**Monitoring Stack:**
- **Prometheus**: Metrics collection
- **Grafana**: Dashboards and visualization
- **Loki**: Log aggregation
- **Sentry** (Future): Error tracking and alerting

```python
# src/middleware/metrics.py
from prometheus_client import Counter, Histogram, Gauge
import time

# Define metrics
request_count = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

request_duration = Histogram(
    'http_request_duration_seconds',
    'HTTP request duration',
    ['method', 'endpoint']
)

rag_generation_duration = Histogram(
    'rag_generation_duration_seconds',
    'RAG explanation generation duration'
)

active_users = Gauge(
    'active_users',
    'Number of active users'
)

# Middleware to track metrics
class MetricsMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        
        response = await call_next(request)
        
        duration = time.time() - start_time
        
        request_count.labels(
            method=request.method,
            endpoint=request.url.path,
            status=response.status_code
        ).inc()
        
        request_duration.labels(
            method=request.method,
            endpoint=request.url.path
        ).observe(duration)
        
        return response
```

### Health Checks

```python
# src/routes/health.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from redis import Redis
import ollama

from ..database import get_db
from ..config import settings

router = APIRouter()

@router.get("/health")
async def health_check(db: Session = Depends(get_db)):
    """
    Comprehensive health check for all system components.
    """
    health_status = {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "components": {}
    }
    
    # Check database
    try:
        db.execute("SELECT 1")
        health_status["components"]["database"] = "healthy"
    except Exception as e:
        health_status["components"]["database"] = f"unhealthy: {str(e)}"
        health_status["status"] = "degraded"
    
    # Check Redis
    try:
        redis_client = Redis.from_url(settings.REDIS_URL)
        redis_client.ping()
        health_status["components"]["redis"] = "healthy"
    except Exception as e:
        health_status["components"]["redis"] = f"unhealthy: {str(e)}"
        health_status["status"] = "degraded"
    
    # Check Ollama
    try:
        ollama.list()
        health_status["components"]["ollama"] = "healthy"
    except Exception as e:
        health_status["components"]["ollama"] = f"unhealthy: {str(e)}"
        health_status["status"] = "degraded"
    
    # Check FAISS index
    try:
        import os
        if os.path.exists(settings.FAISS_INDEX_PATH):
            health_status["components"]["faiss"] = "healthy"
        else:
            health_status["components"]["faiss"] = "unhealthy: index not found"
            health_status["status"] = "degraded"
    except Exception as e:
        health_status["components"]["faiss"] = f"unhealthy: {str(e)}"
        health_status["status"] = "degraded"
    
    return health_status
```

---

## Future Enhancements

### Phase 2 Features (Post-MVP)

1. **Gamification**:
   - Daily streak tracking
   - Achievement badges
   - Progress milestones
   - Leaderboards (optional)

2. **Social Features**:
   - Share shlokas on social media
   - Discussion forums
   - Study groups

3. **Advanced Learning**:
   - Quizzes and assessments
   - Flashcards for memorization
   - Personalized learning paths

4. **Multilingual Support**:
   - Hindi, Sanskrit, and other Indian languages
   - Localized UI

5. **Enhanced RAG**:
   - Fine-tuned LLM on Gita commentary
   - Multi-modal explanations (text + images)
   - Voice-based Q&A

6. **Analytics Dashboard**:
   - Personal learning analytics
   - Reading patterns
   - Favorite themes

### Scalability Roadmap

**Current Architecture Supports**:
- Up to 100K users with single backend instance
- Up to 1M users with horizontal scaling

**Future Scaling Strategies**:
1. **Database**: Read replicas, connection pooling optimization
2. **Backend**: Horizontal scaling behind load balancer
3. **RAG**: Separate RAG service, GPU acceleration for LLM
4. **Caching**: Redis cluster, CDN for static assets
5. **Storage**: Move to S3/CloudFlare R2 for audio files

---

## Conclusion

This architecture document provides a comprehensive blueprint for building the Bhagavad Gita Learning Application. The design prioritizes:

- **Authenticity**: RAG pipeline ensures AI explanations are grounded in actual Gita text
- **Accessibility**: Mobile-first, offline-capable, student-friendly interface
- **Cost-Effectiveness**: Open-source stack, efficient resource usage
- **Scalability**: Modular design allows future growth
- **Developer Experience**: Clear structure, comprehensive testing, good documentation

The architecture is ready for implementation. All technical decisions are locked, ambiguities resolved, and requirements traced to architectural components.

**Next Steps**:
1. Review and approve this architecture document
2. Set up development environment
3. Run ingestion pipeline to populate database
4. Begin Epic 1: Foundation & Core Infrastructure
5. Iterate through epics following the PRD

---

**Document Status**: Complete - Ready for Development  
**Last Updated**: 2026-01-17  
**Version**: 1.0
