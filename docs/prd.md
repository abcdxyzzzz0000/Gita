# Bhagavad Gita Learning Application Product Requirements Document (PRD)

<!-- Powered by BMAD™ Core -->

## Goals and Background Context

### Goals

- Enable students and children to learn the Bhagavad Gita chapter-by-chapter and shloka-by-shloka in a simple, accessible format
- Provide student-friendly explanations grounded strictly in the Gita text to ensure correctness
- Offer practical life guidance using relevant Gita verses for real-world problems
- Create a calm, distraction-free learning experience that feels like a mentor, not a religious textbook
- Build a future-ready platform using entirely open-source technologies for scalability and low-cost operation
- Support offline-friendly access and maintain privacy-respecting practices

### Background Context

The Bhagavad Gita contains timeless wisdom that can guide students and young people through life's challenges, but traditional presentations often feel inaccessible or overly religious. This application aims to bridge that gap by presenting Gita teachings in a modern, attractive, and practical format specifically designed for students aged 12-22 and beginners interested in Gita philosophy.

The platform will use RAG (Retrieval-Augmented Generation) technology to provide AI-powered explanations that are strictly grounded in the actual Gita text, preventing hallucinations and ensuring authenticity. By focusing on simplicity, correctness, and practical application, we create a foundation for future enhancements like gamification and animated stories while maintaining the core value of accessible wisdom.

### Change Log

| Date | Version | Description | Author |
|------|---------|-------------|--------|
| 2026-01-17 | 1.0 | Initial PRD creation from source document | BMad Team |


## Requirements

### Functional

- **FR1**: User authentication via email or Google OAuth with optional anonymous read-only access
- **FR2**: Display a browsable list of all 18 chapters of the Bhagavad Gita
- **FR3**: Display a list of shlokas for each selected chapter
- **FR4**: Provide detailed shloka view showing Sanskrit text, transliteration, meaning, and AI-powered simple explanation
- **FR5**: Enable audio playback of shloka chanting (pre-recorded files)
- **FR6**: Allow users to bookmark shlokas for later reference
- **FR7**: Deliver one "Daily Gita Wisdom" shloka per day with short explanation
- **FR8**: Send optional daily notifications for the wisdom shloka
- **FR9**: Provide "Life Guidance" feature where users select a problem (stress, fear, confusion, etc.) and receive relevant shlokas with AI-generated practical explanations
- **FR10**: Enable keyword search across chapters, themes, and verses
- **FR11**: Display user profile with bookmarked shlokas and reading progress
- **FR12**: Allow users to manage notification settings
- **FR13**: Generate AI explanations using RAG strictly constrained to retrieved Gita context to prevent hallucinations
- **FR14**: Support local caching of content for offline access

### Non Functional

- **NFR1**: Entire technology stack must use open-source components only
- **NFR2**: RAG-based AI responses must return within 2 seconds for optimal user experience
- **NFR3**: UI must be mobile-first and responsive across all device sizes
- **NFR4**: System must be scalable to support millions of users
- **NFR5**: Application must respect user privacy and implement secure authentication practices
- **NFR6**: Infrastructure costs must remain low through use of open-source models and efficient resource usage
- **NFR7**: All AI-generated content must be grounded in actual Gita text with no hallucinated information
- **NFR8**: Application must maintain religious authenticity and avoid dark patterns or addictive mechanics
- **NFR9**: System must be deployable using Docker for consistent environments
- **NFR10**: Application should support future multilingual expansion


## User Interface Design Goals

### Overall UX Vision

The application should feel like a calm, wise mentor guiding students through ancient wisdom. The interface must be clean, distraction-free, and modern - avoiding traditional religious aesthetics that might feel intimidating. Focus on readability, simplicity, and creating moments of reflection. The experience should encourage daily engagement without being addictive or gamified in Phase 1.

### Key Interaction Paradigms

- **Progressive Disclosure**: Start with chapter overview, drill down to shlokas, then to detailed explanations
- **Contextual Help**: Life Guidance feature provides problem-based navigation rather than linear reading
- **Passive Learning**: Daily Wisdom delivers bite-sized content without requiring user action
- **Personal Library**: Bookmarks create a personalized collection of meaningful verses
- **Audio-First Option**: Support audio playback for users who prefer listening over reading

### Core Screens and Views

- **Home/Dashboard**: Entry point showing Daily Wisdom, quick access to chapters, and Life Guidance
- **Chapter List**: Browse all 18 chapters with brief descriptions
- **Shloka List**: View all shlokas within a selected chapter
- **Shloka Detail**: Full view with Sanskrit, transliteration, meaning, explanation, audio, and bookmark option
- **Life Guidance**: Problem selection interface leading to relevant shloka recommendations
- **Search Results**: Keyword search results with context snippets
- **Profile/Bookmarks**: User's saved shlokas and reading progress
- **Settings**: Notification preferences and account management

### Accessibility

WCAG AA compliance for text contrast, font sizing, and screen reader support

### Branding

- Clean, modern aesthetic with calming colors (soft blues, warm neutrals)
- Typography that balances readability with a sense of wisdom (consider serif for Sanskrit, sans-serif for explanations)
- Minimal use of religious iconography - focus on text and content
- Smooth, gentle transitions that encourage reflection rather than rapid interaction

### Target Device and Platforms

Web Responsive and all mobile platforms (iOS and Android via React Native)


## Technical Assumptions

### Repository Structure

**Monorepo** - Single repository containing both frontend (React Native) and backend (FastAPI) for simplified development and deployment coordination

### Service Architecture

**Monolith with Modular Design** - Single FastAPI backend application with clear module separation (auth, content, RAG, notifications). This approach keeps infrastructure simple and cost-effective while maintaining code organization. The RAG engine operates as an integrated module within the backend rather than a separate microservice.

**Rationale**: For Phase 1 with focused scope, a well-structured monolith provides faster development, easier debugging, and lower operational complexity. The modular design allows future extraction of services if needed.

### Testing Requirements

**Unit + Integration Testing** - Comprehensive unit tests for business logic and RAG components, integration tests for API endpoints and database interactions. Manual testing for UI/UX flows in Phase 1.

**Specific Requirements**:
- Unit tests for RAG retrieval accuracy and prompt construction
- Integration tests for authentication flows
- API endpoint testing with test database
- Manual testing for mobile UI across devices
- Performance testing for RAG response times (<2s requirement)

### Additional Technical Assumptions and Requests

- **Frontend**: React Native with Expo for cross-platform mobile development (iOS/Android) and web support
- **Backend API**: Python FastAPI with Uvicorn for high-performance async API
- **RAG Pipeline Components**:
  - PDF ingestion: `pdfplumber` for extracting Gita text from source PDF
  - Text chunking: One shloka per chunk with metadata (chapter, verse number, themes)
  - Embeddings: Sentence-Transformers (open-source) for vector generation
  - Vector Store: FAISS for efficient similarity search
  - LLM: Ollama running LLaMA or Mistral models locally for cost-free inference
- **Database**: PostgreSQL for user data, bookmarks, and reading progress
- **Static Content**: Local file system or MinIO for audio files and cached content
- **Audio**: Pre-recorded MP3 files of shloka chanting, linked via metadata
- **Notifications**: Celery with Redis for scheduled tasks, optional Firebase for push notifications
- **Deployment**: Docker containers for consistent environments, Docker Compose for local development
- **CI/CD**: GitHub Actions for automated testing and deployment
- **Security**: JWT tokens for authentication, bcrypt for password hashing, HTTPS enforcement
- **Content Source**: Bhagavad Gita PDF as authoritative source text for RAG ingestion
- **Prompt Engineering**: RAG prompts must explicitly constrain LLM to only use retrieved context, with instructions for student-friendly language
- **Caching Strategy**: Frontend caching of chapter/shloka content for offline access, backend caching of embeddings


## Epic List

- **Epic 1: Foundation & Core Infrastructure** - Establish project setup, repository structure, Docker configuration, database schema, authentication system, and basic health check API endpoint
- **Epic 2: Content Ingestion & RAG Pipeline** - Build PDF ingestion system, implement text chunking and embedding generation, set up FAISS vector store, and create RAG retrieval and generation pipeline
- **Epic 3: Core Content Browsing** - Implement chapter list, shloka list, and detailed shloka view with Sanskrit text, transliteration, meaning, AI explanation, and bookmark functionality
- **Epic 4: Daily Wisdom & Life Guidance** - Create daily wisdom feature with scheduling, notification system, and life guidance problem-based shloka recommendation engine
- **Epic 5: Search & User Profile** - Implement keyword search across content, user profile with bookmarks and reading progress, and settings management


## Epic 1: Foundation & Core Infrastructure

**Goal**: Establish the foundational project structure, development environment, database schema, authentication system, and a deployable health check endpoint. This epic delivers a working, testable application skeleton that can be deployed and verified, setting the stage for all subsequent feature development.

### Story 1.1: Project Setup & Repository Structure

As a **developer**,
I want **a properly initialized monorepo with frontend and backend folders, dependency management, and Docker configuration**,
so that **the team has a consistent development environment and deployment foundation**.

#### Acceptance Criteria

1. Monorepo created with `/frontend` (React Native/Expo) and `/backend` (FastAPI) directories
2. Python virtual environment and `requirements.txt` configured for backend with FastAPI, Uvicorn, SQLAlchemy, and testing dependencies
3. React Native project initialized with Expo and essential dependencies (navigation, async storage)
4. Docker Compose configuration created for local development with backend, database, and Redis services
5. `.gitignore` configured to exclude virtual environments, node_modules, and sensitive files
6. README.md created with setup instructions and architecture overview
7. GitHub Actions workflow file created for CI (placeholder for future test automation)

### Story 1.2: Database Schema & Models

As a **developer**,
I want **PostgreSQL database schema and SQLAlchemy models for users, bookmarks, and reading progress**,
so that **the application can persist user data and track engagement**.

#### Acceptance Criteria

1. PostgreSQL database container configured in Docker Compose
2. SQLAlchemy models created for User (id, email, hashed_password, oauth_provider, created_at, last_login)
3. SQLAlchemy model created for Bookmark (id, user_id, chapter, shloka_number, created_at)
4. SQLAlchemy model created for ReadingProgress (id, user_id, chapter, shloka_number, last_read_at)
5. Alembic migrations configured for database schema versioning
6. Initial migration created and tested with `alembic upgrade head`
7. Database connection utility created with connection pooling and error handling

### Story 1.3: Authentication System

As a **user**,
I want **to register and log in using email/password or Google OAuth**,
so that **I can access personalized features like bookmarks and reading progress**.

#### Acceptance Criteria

1. FastAPI endpoints created for user registration (`POST /api/auth/register`) with email validation and password hashing using bcrypt
2. FastAPI endpoint created for email/password login (`POST /api/auth/login`) returning JWT access token
3. JWT token generation and validation utilities implemented with configurable expiration
4. Google OAuth integration implemented using OAuth2 flow (`GET /api/auth/google`, `GET /api/auth/google/callback`)
5. Protected route decorator created to validate JWT tokens on authenticated endpoints
6. Anonymous access flag supported (read-only mode without authentication)
7. Unit tests created for authentication utilities (token generation, password hashing)
8. Integration tests created for registration and login endpoints

### Story 1.4: Health Check & Basic API

As a **developer**,
I want **a health check endpoint and basic API structure**,
so that **I can verify the application is running and monitor service health**.

#### Acceptance Criteria

1. FastAPI application structure created with router organization (auth, content, health)
2. Health check endpoint implemented (`GET /api/health`) returning status, database connectivity, and timestamp
3. CORS middleware configured to allow frontend origin
4. API documentation automatically generated via FastAPI's built-in Swagger UI (`/docs`)
5. Environment variable configuration implemented using python-dotenv for secrets and settings
6. Docker container for backend builds and runs successfully
7. Integration test created verifying health endpoint returns 200 status
8. Application deployable and accessible via `docker-compose up`


## Epic 2: Content Ingestion & RAG Pipeline

**Goal**: Build the complete RAG (Retrieval-Augmented Generation) pipeline that ingests Bhagavad Gita content from PDF, generates embeddings, stores them in FAISS vector database, and provides accurate, context-grounded AI explanations. This epic delivers the core intelligence of the application.

### Story 2.1: PDF Ingestion & Text Processing

As a **developer**,
I want **to extract and structure Bhagavad Gita text from PDF source**,
so that **the content is available in a clean, queryable format for the RAG pipeline**.

#### Acceptance Criteria

1. PDF ingestion script created using `pdfplumber` to extract text from Bhagavad Gita PDF
2. Text parsing logic implemented to identify chapter boundaries and individual shlokas
3. Data structure created for each shloka containing: chapter number, shloka number, Sanskrit text, transliteration, and meaning
4. Text cleaning and normalization applied (remove extra whitespace, standardize formatting)
5. Structured content exported to JSON file for downstream processing
6. Metadata extraction implemented for themes/keywords per shloka (manual tagging or rule-based)
7. Unit tests created verifying correct parsing of sample chapters
8. Documentation created explaining the ingestion process and data format

### Story 2.2: Embedding Generation & Vector Store

As a **developer**,
I want **to generate vector embeddings for all shlokas and store them in FAISS**,
so that **the system can perform semantic similarity search for relevant content**.

#### Acceptance Criteria

1. Sentence-Transformers model integrated (e.g., `all-MiniLM-L6-v2` for efficiency)
2. Embedding generation script created that processes all shlokas from JSON
3. Each shloka embedded using combined text (Sanskrit + transliteration + meaning) for richer semantic representation
4. FAISS index created and populated with embeddings
5. Metadata mapping maintained linking FAISS index positions to shloka identifiers
6. FAISS index persisted to disk for loading at application startup
7. Embedding generation performance measured and documented (target: <5 minutes for full Gita)
8. Unit tests created verifying embedding dimensions and FAISS index integrity

### Story 2.3: RAG Retrieval Engine

As a **developer**,
I want **a retrieval engine that finds relevant shlokas based on user queries**,
so that **the system can provide contextually appropriate Gita wisdom**.

#### Acceptance Criteria

1. Query embedding function created using same Sentence-Transformers model
2. FAISS similarity search implemented returning top-k relevant shlokas (configurable k, default 3-5)
3. Retrieval API endpoint created (`POST /api/rag/retrieve`) accepting query text and returning matched shlokas with similarity scores
4. Metadata enrichment implemented to include full shloka details (Sanskrit, transliteration, meaning) in results
5. Filtering options implemented for chapter-specific or theme-specific retrieval
6. Retrieval performance optimized to meet <500ms requirement
7. Unit tests created for query embedding and similarity search
8. Integration tests created verifying retrieval accuracy for sample queries

### Story 2.4: LLM Integration & Explanation Generation

As a **user**,
I want **AI-generated simple explanations for shlokas that are grounded in the actual text**,
so that **I can understand the wisdom in student-friendly language without hallucinations**.

#### Acceptance Criteria

1. Ollama integrated with LLaMA or Mistral model configured for local inference
2. Prompt template created that includes retrieved shloka context and explicit constraints against hallucination
3. Prompt engineering implemented for student-friendly language (12-22 age group)
4. RAG generation endpoint created (`POST /api/rag/explain`) accepting shloka reference and returning AI explanation
5. Response streaming implemented for better user experience with longer explanations
6. Fallback mechanism implemented if LLM is unavailable (return pre-written explanation or error message)
7. Generation performance optimized to meet <2s total response time (retrieval + generation)
8. Unit tests created for prompt construction
9. Integration tests created verifying explanation quality and constraint adherence
10. Manual testing performed to validate explanation appropriateness for target age group


## Epic 3: Core Content Browsing

**Goal**: Implement the primary content browsing experience allowing users to navigate chapters, view shlokas, access AI explanations, play audio, and bookmark verses. This epic delivers the core value proposition of accessible Gita learning.

### Story 3.1: Chapter List API & Frontend

As a **user**,
I want **to see a list of all 18 Bhagavad Gita chapters with brief descriptions**,
so that **I can choose which chapter to explore**.

#### Acceptance Criteria

1. Backend endpoint created (`GET /api/chapters`) returning all 18 chapters with id, title, Sanskrit name, and brief description
2. Chapter data seeded in database or loaded from static JSON file
3. React Native screen created displaying chapter list with card-based layout
4. Each chapter card shows chapter number, title, and description
5. Navigation implemented to shloka list when chapter is tapped
6. Loading state and error handling implemented in frontend
7. Offline caching implemented using AsyncStorage for chapter data
8. Integration test created verifying chapter list endpoint returns correct data

### Story 3.2: Shloka List API & Frontend

As a **user**,
I want **to see all shlokas within a selected chapter**,
so that **I can browse and select specific verses to study**.

#### Acceptance Criteria

1. Backend endpoint created (`GET /api/chapters/{chapter_id}/shlokas`) returning all shlokas for specified chapter
2. Response includes shloka number, first line of Sanskrit text (preview), and bookmark status for authenticated users
3. React Native screen created displaying shloka list with numbered items
4. Each shloka item shows verse number and preview text
5. Visual indicator displayed for bookmarked shlokas
6. Navigation implemented to shloka detail when item is tapped
7. Pull-to-refresh functionality implemented
8. Offline caching implemented for shloka lists
9. Integration test created verifying shloka list endpoint with authentication

### Story 3.3: Shloka Detail View with AI Explanation

As a **user**,
I want **to view complete shloka details including Sanskrit text, transliteration, meaning, and AI-generated explanation**,
so that **I can deeply understand the verse's wisdom**.

#### Acceptance Criteria

1. Backend endpoint created (`GET /api/shlokas/{shloka_id}`) returning full shloka details
2. RAG explanation integrated into shloka detail endpoint (calls RAG generation service)
3. React Native screen created with scrollable detail view showing all shloka components
4. Sanskrit text displayed in appropriate font with proper rendering
5. Transliteration displayed in readable Latin script
6. Meaning displayed as concise translation
7. AI explanation displayed with clear visual separation and "AI-generated" label
8. Loading state shown while AI explanation generates
9. Error handling implemented if explanation generation fails (show fallback message)
10. Offline mode supported showing cached explanation or "offline" message
11. Integration test created verifying complete shloka detail response

### Story 3.4: Audio Playback

As a **user**,
I want **to listen to audio chanting of shlokas**,
so that **I can experience the verses through sound and aid memorization**.

#### Acceptance Criteria

1. Audio file storage configured (local file system or MinIO) with organized directory structure
2. Audio metadata added to shloka data model linking shloka_id to audio file path
3. Backend endpoint created (`GET /api/shlokas/{shloka_id}/audio`) streaming audio file
4. React Native audio player component integrated (expo-av)
5. Play/pause controls added to shloka detail screen
6. Audio progress indicator displayed
7. Audio continues playing when screen is backgrounded (background audio support)
8. Error handling implemented for missing audio files
9. Audio files preloaded or cached for offline playback
10. Integration test created verifying audio endpoint returns valid audio stream

### Story 3.5: Bookmark Functionality

As a **user**,
I want **to bookmark shlokas for easy access later**,
so that **I can build a personal collection of meaningful verses**.

#### Acceptance Criteria

1. Backend endpoint created (`POST /api/bookmarks`) to add bookmark (requires authentication)
2. Backend endpoint created (`DELETE /api/bookmarks/{bookmark_id}`) to remove bookmark
3. Backend endpoint created (`GET /api/bookmarks`) returning user's bookmarked shlokas
4. Bookmark button added to shloka detail screen with visual toggle state
5. Bookmark action triggers API call and updates local state
6. Optimistic UI update implemented (immediate visual feedback before API response)
7. Bookmark status synchronized across chapter list, shloka list, and detail views
8. Error handling implemented with rollback on failure
9. Unit tests created for bookmark model and database operations
10. Integration tests created for bookmark endpoints with authentication


## Epic 4: Daily Wisdom & Life Guidance

**Goal**: Implement features that deliver proactive value to users through daily wisdom notifications and problem-based shloka recommendations. This epic creates engagement mechanisms that bring Gita wisdom into users' daily lives.

### Story 4.1: Daily Wisdom Selection & API

As a **user**,
I want **to receive one meaningful shloka each day with a short explanation**,
so that **I can reflect on Gita wisdom as part of my daily routine**.

#### Acceptance Criteria

1. Daily wisdom selection algorithm implemented (sequential through chapters, or curated list, or random with tracking)
2. Backend endpoint created (`GET /api/daily-wisdom`) returning today's shloka with explanation
3. Daily wisdom cached to ensure all users see the same shloka on a given day
4. Explanation generated using RAG with focus on practical daily application
5. Date-based rotation logic implemented to ensure new shloka each day
6. Historical daily wisdom accessible via date parameter (`GET /api/daily-wisdom?date=YYYY-MM-DD`)
7. React Native home screen component created displaying daily wisdom prominently
8. "Read More" navigation implemented to full shloka detail
9. Unit tests created for selection algorithm
10. Integration test created verifying daily wisdom endpoint consistency

### Story 4.2: Notification System

As a **user**,
I want **to receive optional daily notifications reminding me to read the daily wisdom**,
so that **I build a consistent learning habit**.

#### Acceptance Criteria

1. Celery task scheduler configured with Redis backend
2. Daily notification task created scheduled at user-configurable time (default 8 AM local time)
3. Firebase Cloud Messaging (FCM) integrated for push notifications (optional, can use local notifications)
4. User notification preferences stored in database (enabled/disabled, preferred time)
5. Backend endpoint created (`PUT /api/settings/notifications`) to update preferences
6. React Native notification permission request implemented on first app launch
7. Notification payload includes daily wisdom preview and deep link to app
8. Notification scheduling respects user timezone
9. Settings screen created allowing users to toggle notifications and set time
10. Integration test created for notification scheduling logic

### Story 4.3: Life Guidance Problem Selection

As a **user**,
I want **to select a life problem I'm facing and receive relevant Gita shlokas**,
so that **I can find practical wisdom for my current situation**.

#### Acceptance Criteria

1. Problem categories defined (stress, fear, confusion, anger, sadness, purpose, relationships, decision-making)
2. Backend endpoint created (`GET /api/life-guidance/problems`) returning list of problem categories
3. React Native screen created displaying problem categories as selectable cards
4. Each category card includes icon, title, and brief description
5. Navigation implemented to guidance results when category is selected
6. Visual design creates calm, supportive atmosphere
7. Problem categories stored in database or configuration file for easy updates
8. Integration test created verifying problem list endpoint

### Story 4.4: Life Guidance RAG Recommendations

As a **user**,
I want **to see relevant shlokas and practical explanations for my selected problem**,
so that **I receive actionable guidance from the Gita**.

#### Acceptance Criteria

1. Problem-to-query mapping created for each category (e.g., "stress" → "peace, calm, equanimity")
2. Backend endpoint created (`GET /api/life-guidance/recommendations?problem={category}`) using RAG retrieval
3. RAG query enhanced with problem-specific context for better relevance
4. Top 3-5 most relevant shlokas returned with similarity scores
5. AI explanations generated with explicit focus on practical application to the problem
6. React Native results screen created displaying recommended shlokas
7. Each recommendation shows shloka preview, relevance indicator, and practical explanation
8. Navigation implemented to full shloka detail from recommendations
9. "Not helpful" feedback option implemented (stored for future improvement)
10. Integration test created verifying recommendation quality for sample problems
11. Manual testing performed to validate practical applicability of recommendations


## Epic 5: Search & User Profile

**Goal**: Complete the user experience with powerful search functionality and personalized profile features. This epic enables users to find specific content and manage their learning journey.

### Story 5.1: Keyword Search Implementation

As a **user**,
I want **to search for shlokas by keyword, theme, or concept**,
so that **I can quickly find relevant verses without browsing all chapters**.

#### Acceptance Criteria

1. Backend search endpoint created (`GET /api/search?q={query}`) supporting keyword search
2. Search implementation uses both full-text search (PostgreSQL) and semantic search (RAG embeddings)
3. Search results ranked by relevance combining text match score and semantic similarity
4. Results include shloka preview, chapter/verse reference, and highlighted matching text
5. Search supports Sanskrit, transliteration, and English meaning fields
6. Minimum query length enforced (3 characters) with validation
7. React Native search screen created with search input and results list
8. Search debouncing implemented (300ms delay) to reduce API calls
9. Recent searches stored locally for quick access
10. Empty state and no-results state designed with helpful suggestions
11. Navigation implemented to shloka detail from search results
12. Integration test created verifying search accuracy for sample queries

### Story 5.2: User Profile & Bookmarks View

As a **user**,
I want **to view my profile with all bookmarked shlokas and reading statistics**,
so that **I can track my learning journey and revisit meaningful verses**.

#### Acceptance Criteria

1. Backend endpoint created (`GET /api/profile`) returning user info, bookmark count, and reading stats
2. Reading statistics calculated: total shlokas read, chapters completed, days active
3. React Native profile screen created displaying user information and statistics
4. Bookmarks section displays all bookmarked shlokas in chronological or chapter order
5. Each bookmark shows shloka preview and chapter reference
6. Swipe-to-delete gesture implemented for removing bookmarks
7. Empty state designed for users with no bookmarks yet
8. Navigation implemented to shloka detail from bookmark list
9. Pull-to-refresh implemented to sync latest data
10. Integration test created verifying profile endpoint with authentication

### Story 5.3: Settings & Account Management

As a **user**,
I want **to manage my notification preferences and account settings**,
so that **I can customize my experience and maintain account security**.

#### Acceptance Criteria

1. Backend endpoint created (`GET /api/settings`) returning current user settings
2. Backend endpoint created (`PUT /api/settings`) to update settings
3. React Native settings screen created with organized sections
4. Notification settings section includes toggle and time picker
5. Account section displays email and account creation date
6. Password change functionality implemented (for email/password users)
7. Logout functionality implemented clearing local tokens and cache
8. Account deletion option implemented with confirmation dialog
9. Settings changes synchronized immediately with backend
10. Visual feedback provided for successful updates
11. Unit tests created for settings update logic
12. Integration tests created for settings endpoints

### Story 5.4: Reading Progress Tracking

As a **user**,
I want **my reading progress automatically tracked**,
so that **I can see which shlokas I've read and resume where I left off**.

#### Acceptance Criteria

1. Backend endpoint created (`POST /api/progress`) to record shloka view
2. Progress automatically recorded when user views shloka detail for >5 seconds
3. Backend endpoint created (`GET /api/progress`) returning reading history
4. Progress indicators added to chapter list showing completion percentage
5. Progress indicators added to shloka list showing read/unread status
6. "Continue Reading" feature added to home screen showing last read shloka
7. Progress data synchronized across devices for authenticated users
8. Offline progress tracked locally and synced when connection restored
9. Unit tests created for progress tracking logic
10. Integration tests created for progress endpoints


## Checklist Results Report

*This section will be populated after running the PM checklist to validate the PRD completeness and quality.*

## Next Steps

### UX Expert Prompt

Please review this PRD and create a detailed Front-End Specification document that expands on the UI/UX Design Goals. Focus on:
- Detailed screen layouts and component hierarchy
- User flow diagrams for key journeys (onboarding, daily wisdom, life guidance)
- Design system specifications (colors, typography, spacing, components)
- Interaction patterns and micro-interactions
- Accessibility implementation details
- Mobile-specific considerations for React Native

Use the front-end-spec template and ensure alignment with the calm, mentor-like experience described in this PRD.

### Architect Prompt

Please review this PRD and create a comprehensive Architecture Document that details:
- System architecture diagram showing all components and data flows
- Backend API design with detailed endpoint specifications
- RAG pipeline architecture with component interactions
- Database schema with relationships and indexes
- Authentication and security architecture
- Deployment architecture using Docker
- Performance optimization strategies to meet NFR requirements
- Error handling and logging strategies
- Testing strategy aligned with the testing requirements

Use the fullstack-architecture template and ensure all technical assumptions from this PRD are addressed in your design.

---

**Document Status**: Draft - Ready for Review
**Next Action**: Run PM Checklist, then proceed to UX Expert and Architect phases
