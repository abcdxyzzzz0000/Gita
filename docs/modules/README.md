# Bhagavad Gita Learning Application - Module Decomposition

## Overview

This directory contains module-wise execution-ready artifacts decomposed from the master PRD and Architecture documents. Each module is independently implementable with clear boundaries, dependencies, and success criteria.

## Module Structure

Each module consists of two documents:
1. **Sub-PRD** (`sub_prd_<module_name>.md`) - Product requirements, user stories, API contracts, and success metrics
2. **Sub-Architecture** (`sub_arch_<module_name>.md`) - Technical architecture, components, data flows, and deployment considerations

## Modules

### 1. Authentication Module
**Purpose**: User registration, login, and session management with email/password and Google OAuth support

**Files**:
- `sub_prd_authentication.md`
- `sub_arch_authentication.md`

**Key Features**:
- Email/password registration and login
- Google OAuth integration
- JWT token-based authentication
- Anonymous read-only access
- Password hashing with bcrypt

**Dependencies**: PostgreSQL, bcrypt, python-jose, Google OAuth API

**Traceability**: FR1, NFR5, Epic 1 Story 1.3

---

### 2. Content Browsing Module
**Purpose**: Browse and consume Bhagavad Gita content through chapters, shlokas, audio, and bookmarks

**Files**:
- `sub_prd_content_browsing.md`
- `sub_arch_content_browsing.md`

**Key Features**:
- Chapter list (18 chapters)
- Shloka list per chapter
- Shloka detail view with AI explanation
- Audio playback
- Bookmark management
- Offline content caching

**Dependencies**: PostgreSQL, Redis, RAG Module, File System (audio), React Native

**Traceability**: FR2, FR3, FR4, FR5, FR6, FR14, NFR2, NFR3, Epic 3

---

### 3. RAG Engine Module
**Purpose**: AI-powered explanations using Retrieval-Augmented Generation strictly grounded in Gita text

**Files**:
- `sub_prd_rag_engine.md`
- `sub_arch_rag_engine.md`

**Key Features**:
- Semantic search using FAISS vector store
- LLM-based explanation generation (Ollama + Mistral 7B)
- Student-friendly language (age 12-22)
- Life guidance recommendations
- Daily wisdom explanations
- Hallucination prevention through context grounding

**Dependencies**: FAISS, Sentence-Transformers, Ollama, PostgreSQL, Redis

**Traceability**: FR4, FR9, FR13, NFR2, NFR6, NFR7, Epic 2, Epic 4

---

### 4. Daily Wisdom & Notifications Module
**Purpose**: Deliver daily wisdom shlokas with notifications to build learning habits

**Files**:
- `sub_prd_daily_wisdom_notifications.md`
- `sub_arch_daily_wisdom_notifications.md`

**Key Features**:
- Daily shloka selection (sequential rotation)
- Daily wisdom API endpoint
- Notification scheduling (Celery + Redis)
- User notification preferences
- Timezone-aware notification delivery
- Historical daily wisdom access

**Dependencies**: Celery, Redis, PostgreSQL, RAG Module, Firebase Cloud Messaging (Phase 2)

**Traceability**: FR7, FR8, FR12, Epic 4 Stories 4.1, 4.2

---

### 5. Search & Profile Module
**Purpose**: Find content through search and manage personalized learning journey

**Files**:
- `sub_prd_search_profile.md`
- `sub_arch_search_profile.md`

**Key Features**:
- Keyword search (PostgreSQL full-text search)
- Semantic search (RAG embeddings)
- Combined search ranking
- User profile with statistics
- Bookmarks management
- Reading progress tracking
- Account settings
- Password change and account deletion

**Dependencies**: PostgreSQL (FTS), RAG Module, Redis, Authentication Module

**Traceability**: FR10, FR11, FR12, Epic 5

---

## Module Dependencies

```
┌─────────────────────────────────────────────────────────┐
│                  Frontend (React Native)                │
└─────────────────────────────────────────────────────────┘
                          │
        ┌─────────────────┼─────────────────┐
        │                 │                 │
┌───────▼────────┐ ┌──────▼──────┐ ┌───────▼────────┐
│Authentication  │ │   Content   │ │Search & Profile│
│    Module      │ │   Browsing  │ │     Module     │
└───────┬────────┘ └──────┬──────┘ └───────┬────────┘
        │                 │                 │
        │         ┌───────▼────────┐        │
        │         │   RAG Engine   │        │
        │         │     Module     │        │
        │         └───────┬────────┘        │
        │                 │                 │
        │         ┌───────▼────────┐        │
        │         │ Daily Wisdom & │        │
        │         │ Notifications  │        │
        │         └────────────────┘        │
        │                                   │
        └───────────────┬───────────────────┘
                        │
        ┌───────────────▼───────────────┐
        │     Shared Infrastructure     │
        │  PostgreSQL | Redis | Files   │
        └───────────────────────────────┘
```

## Implementation Order

### Phase 1: Foundation (Weeks 1-2)
1. **Authentication Module** - Core user management
2. **Content Browsing Module** (Basic) - Chapter/shloka display without AI

### Phase 2: Intelligence (Weeks 3-4)
3. **RAG Engine Module** - AI explanations and semantic search
4. **Content Browsing Module** (Complete) - Add AI explanations and audio

### Phase 3: Engagement (Weeks 5-6)
5. **Daily Wisdom & Notifications Module** - Daily content delivery
6. **Search & Profile Module** - Search and user features

## Testing Strategy

Each module includes:
- **Unit Tests**: Component-level testing
- **Integration Tests**: Module integration with dependencies
- **Performance Tests**: Load and response time validation
- **End-to-End Tests**: Complete user journeys

## Deployment

All modules deploy as part of a monolithic backend with modular organization:
- Single FastAPI application
- Shared database (PostgreSQL)
- Shared cache (Redis)
- Docker containerization
- Environment-based configuration

## Success Criteria

Each module defines:
- **Functional Metrics**: Feature completion and correctness
- **Performance Metrics**: Response times and throughput
- **Quality Metrics**: User satisfaction and accuracy
- **Engagement Metrics**: Usage patterns and retention

## Traceability Matrix

| Module | PRD Requirements | Architecture Components | Epics/Stories |
|--------|-----------------|------------------------|---------------|
| Authentication | FR1, NFR5 | Auth Service, JWT Manager, OAuth Client | Epic 1, Story 1.3 |
| Content Browsing | FR2-6, FR14, NFR2-3 | Content Service, Bookmark Service, Audio Service | Epic 3 |
| RAG Engine | FR4, FR9, FR13, NFR2, NFR6-7 | RAG Service, FAISS Index, Ollama Client | Epic 2, Epic 4 |
| Daily Wisdom | FR7-8, FR12 | Daily Wisdom Service, Celery Tasks | Epic 4, Stories 4.1-4.2 |
| Search & Profile | FR10-12 | Search Service, Profile Service, Progress Service | Epic 5 |

## Documentation Standards

Each Sub-PRD includes:
- Module overview and purpose
- Functional requirements (user stories with acceptance criteria)
- Non-functional requirements
- API contracts (request/response schemas)
- Error handling and edge cases
- Dependencies on other modules
- Assumptions and constraints
- Success metrics
- Traceability to master PRD

Each Sub-Architecture includes:
- Module-level architecture diagram
- Internal components and responsibilities
- Data flow (step-by-step)
- Database schema/tables involved
- External services used
- Security considerations
- Scalability and failure handling
- Deployment considerations

## Next Steps

1. Review each module's Sub-PRD for completeness
2. Validate dependencies between modules
3. Prioritize implementation order
4. Assign modules to development teams
5. Set up CI/CD pipelines per module
6. Begin implementation starting with Authentication module

---

**Document Version**: 1.0  
**Last Updated**: 2026-01-17  
**Maintained By**: BMad Team
