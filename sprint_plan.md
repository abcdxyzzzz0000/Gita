# Sprint Plan - Bhagavad Gita Learning App
## 5-Sprint Locked Scope Plan

**Planning Date:** January 17, 2026  
**Total Stories:** 33  
**Sprint Duration:** 2 weeks each  
**Total Timeline:** 10 weeks

---

## Sprint 1: Foundation & Authentication
**Duration:** 2 weeks  
**Sprint Goal:** Establish core infrastructure, authentication system, and basic content browsing capabilities to enable user registration and chapter/shloka viewing.

### Stories Included
- **AUTH-1:** User Registration with Email/Password
- **AUTH-2:** User Login with Email/Password
- **AUTH-5:** Token Validation Middleware
- **CONTENT-1:** Browse Chapter List
- **CONTENT-2:** Browse Shloka List

### Dependencies Resolved
- Database setup and schema (prerequisite)
- User table schema (prerequisite)
- Chapter and shloka data loaded (prerequisite)
- PostgreSQL configuration complete

### Story Points: 21
- AUTH-1: 5 points
- AUTH-2: 3 points
- AUTH-5: 5 points
- CONTENT-1: 3 points
- CONTENT-2: 5 points

### Definition of Done
- [ ] All acceptance criteria met for each story
- [ ] Unit tests written and passing (>80% coverage)
- [ ] API endpoints documented in Swagger/OpenAPI
- [ ] Database migrations created and tested
- [ ] Code reviewed and merged to main branch
- [ ] Manual testing completed on staging environment
- [ ] No critical or high-severity bugs
- [ ] User can register, login, and browse chapters/shlokas

---

## Sprint 2: RAG Engine & Content Detail
**Duration:** 2 weeks  
**Sprint Goal:** Implement RAG engine with AI-powered explanations and complete shloka detail viewing, enabling users to understand verses with AI-generated insights.

### Stories Included
- **RAG-2:** Retrieve Relevant Shlokas
- **RAG-1:** Generate Shloka Explanation
- **CONTENT-3:** View Shloka Detail with AI Explanation
- **AUTH-3:** Google OAuth Authentication

### Dependencies Resolved
- FAISS index setup and configuration (prerequisite)
- Ollama installation and model setup (prerequisite)
- Embedding model configured (prerequisite)
- OAuth configuration with Google Cloud Console (prerequisite)
- Dependencies: AUTH-1, AUTH-2, CONTENT-2

### Story Points: 21
- RAG-2: 8 points
- RAG-1: 8 points
- CONTENT-3: 3 points
- AUTH-3: 5 points

### Definition of Done
- [ ] All acceptance criteria met for each story
- [ ] RAG pipeline tested with sample queries
- [ ] AI explanations generated within 2-second SLA
- [ ] FAISS retrieval completes within 500ms
- [ ] OAuth flow tested end-to-end
- [ ] Unit and integration tests passing
- [ ] Performance benchmarks documented
- [ ] Code reviewed and merged
- [ ] Users can view complete shloka details with AI explanations
- [ ] Users can authenticate via Google OAuth

---

## Sprint 3: Personalization & Bookmarks
**Duration:** 2 weeks  
**Sprint Goal:** Enable personalized user experience through bookmarking, profile management, and keyword search functionality.

### Stories Included
- **CONTENT-5:** Bookmark Shlokas
- **CONTENT-6:** View Bookmarked Shlokas
- **PROFILE-1:** View Profile
- **PROFILE-2:** View Bookmarks in Profile
- **SEARCH-1:** Keyword Search

### Dependencies Resolved
- Dependencies: AUTH-5, CONTENT-3
- PostgreSQL full-text search configured

### Story Points: 20
- CONTENT-5: 5 points
- CONTENT-6: 3 points
- PROFILE-1: 3 points
- PROFILE-2: 3 points
- SEARCH-1: 6 points

### Definition of Done
- [ ] All acceptance criteria met for each story
- [ ] Bookmark sync tested across devices
- [ ] Search performance tested with large datasets
- [ ] Optimistic UI updates working correctly
- [ ] Profile statistics calculated accurately
- [ ] Unit and integration tests passing
- [ ] UI/UX reviewed and approved
- [ ] Code reviewed and merged
- [ ] Users can bookmark shlokas and view them in profile
- [ ] Users can search for shlokas by keyword

---

## Sprint 4: Daily Wisdom & Notifications
**Duration:** 2 weeks  
**Sprint Goal:** Implement daily wisdom feature with push notifications to drive daily user engagement and retention.

### Stories Included
- **RAG-4:** Daily Wisdom Explanation Generation
- **DAILY-1:** View Daily Wisdom
- **DAILY-2:** Enable/Disable Notifications
- **DAILY-3:** Set Notification Time
- **DAILY-4:** Receive Daily Notification
- **CONTENT-4:** Play Shloka Audio

### Dependencies Resolved
- Celery setup for scheduled tasks (prerequisite)
- Push notification service configured (Firebase/OneSignal) (prerequisite)
- Audio file storage setup (prerequisite)
- Dependencies: RAG-1, DAILY-1, DAILY-2, DAILY-3, CONTENT-3

### Story Points: 22
- RAG-4: 5 points
- DAILY-1: 3 points
- DAILY-2: 3 points
- DAILY-3: 3 points
- DAILY-4: 5 points
- CONTENT-4: 3 points

### Definition of Done
- [ ] All acceptance criteria met for each story
- [ ] Celery tasks scheduled and tested
- [ ] Notification delivery tested on iOS and Android
- [ ] Timezone handling verified for global users
- [ ] Audio playback tested on multiple devices
- [ ] Daily wisdom changes at midnight UTC
- [ ] Unit and integration tests passing
- [ ] Code reviewed and merged
- [ ] Users receive daily notifications at preferred time
- [ ] Users can play audio for shlokas

---

## Sprint 5: Enhancement & Polish
**Duration:** 2 weeks  
**Sprint Goal:** Complete remaining features, enhance user experience with semantic search and life guidance, and ensure production readiness.

### Stories Included
- **SEARCH-2:** Semantic Search
- **RAG-3:** Life Guidance Recommendations
- **PROFILE-3:** View Reading Progress
- **PROFILE-4:** Manage Account Settings
- **AUTH-4:** Anonymous Read-Only Access
- **DAILY-5:** Access Historical Daily Wisdom

### Dependencies Resolved
- Dependencies: SEARCH-1, RAG-2, RAG-1, PROFILE-1, DAILY-1
- Progress tracking implementation (prerequisite)

### Story Points: 19
- SEARCH-2: 5 points
- RAG-3: 5 points
- PROFILE-3: 3 points
- PROFILE-4: 3 points
- AUTH-4: 2 points
- DAILY-5: 1 point

### Definition of Done
- [ ] All acceptance criteria met for each story
- [ ] Semantic search accuracy validated
- [ ] Life guidance recommendations tested with real scenarios
- [ ] Reading progress tracking accurate
- [ ] Account deletion flow tested
- [ ] Anonymous access properly restricted
- [ ] All unit and integration tests passing
- [ ] End-to-end testing completed
- [ ] Performance testing completed
- [ ] Security audit completed
- [ ] Code reviewed and merged
- [ ] Production deployment checklist completed
- [ ] User documentation updated

---

## Sprint Summary

| Sprint | Stories | Story Points | Focus Area |
|--------|---------|--------------|------------|
| Sprint 1 | 5 | 21 | Foundation & Auth |
| Sprint 2 | 4 | 21 | RAG & Content Detail |
| Sprint 3 | 5 | 20 | Personalization |
| Sprint 4 | 6 | 22 | Engagement |
| Sprint 5 | 6 | 19 | Enhancement |
| **Total** | **26** | **103** | **Full MVP** |

**Note:** 7 stories not included in sprints (considered post-MVP or merged into other stories)

---

## Dependency Chain Validation

### Sprint 1 → Sprint 2
✅ AUTH-1, AUTH-2 completed → enables AUTH-3  
✅ CONTENT-2 completed → enables CONTENT-3  
✅ Database setup → enables RAG setup

### Sprint 2 → Sprint 3
✅ AUTH-5 completed → enables CONTENT-5, PROFILE-1  
✅ CONTENT-3 completed → enables CONTENT-5  
✅ RAG-1, RAG-2 completed → enables advanced features

### Sprint 3 → Sprint 4
✅ CONTENT-5 completed → enables CONTENT-6  
✅ PROFILE-1 completed → enables PROFILE-2  
✅ AUTH-5 completed → enables DAILY-2, DAILY-3

### Sprint 4 → Sprint 5
✅ RAG-1 completed → enables RAG-3  
✅ RAG-2 completed → enables SEARCH-2  
✅ DAILY-1 completed → enables DAILY-5  
✅ PROFILE-1 completed → enables PROFILE-3, PROFILE-4

---

## Risk Mitigation

### Sprint 1 Risks
- **Risk:** Database schema changes during development
- **Mitigation:** Finalize schema in sprint planning, use migrations

### Sprint 2 Risks
- **Risk:** RAG performance not meeting 2-second SLA
- **Mitigation:** Early performance testing, fallback to cached explanations

### Sprint 3 Risks
- **Risk:** Search performance degradation with large datasets
- **Mitigation:** Implement pagination, indexing, and caching early

### Sprint 4 Risks
- **Risk:** Push notification delivery issues across platforms
- **Mitigation:** Use reliable service (Firebase), test early on both platforms

### Sprint 5 Risks
- **Risk:** Scope creep with enhancement features
- **Mitigation:** Strict adherence to acceptance criteria, defer nice-to-haves

---

## Prerequisites & Setup Tasks

### Before Sprint 1
- [ ] PostgreSQL database provisioned
- [ ] Development, staging, production environments ready
- [ ] CI/CD pipeline configured
- [ ] Git repository and branching strategy established
- [ ] Chapter and shloka data imported
- [ ] Team onboarding completed

### Before Sprint 2
- [ ] Ollama installed and configured
- [ ] FAISS library integrated
- [ ] Embedding model selected and tested
- [ ] Google OAuth credentials obtained
- [ ] RAG pipeline architecture reviewed

### Before Sprint 3
- [ ] Full-text search indexes created
- [ ] Profile statistics calculation logic designed
- [ ] Bookmark sync strategy defined

### Before Sprint 4
- [ ] Celery and Redis/RabbitMQ configured
- [ ] Push notification service account created
- [ ] Audio files uploaded to storage
- [ ] Notification templates designed

### Before Sprint 5
- [ ] Progress tracking database schema ready
- [ ] Production monitoring tools configured
- [ ] Security audit scheduled
- [ ] User documentation framework ready

---

## Success Metrics

### Sprint 1 Success Criteria
- 100% of users can register and login
- Chapter and shloka lists load within 1 second
- Zero authentication-related bugs in staging

### Sprint 2 Success Criteria
- 95% of AI explanations generated within 2 seconds
- OAuth success rate > 98%
- User satisfaction with explanations > 4/5

### Sprint 3 Success Criteria
- Bookmark sync success rate > 99%
- Search returns results within 500ms
- Profile page loads within 1 second

### Sprint 4 Success Criteria
- Notification delivery rate > 95%
- Daily wisdom engagement rate > 30%
- Audio playback success rate > 98%

### Sprint 5 Success Criteria
- Semantic search accuracy > 85%
- Life guidance relevance score > 4/5
- Zero critical bugs in production
- App store submission ready

---

## Post-Sprint Activities

### After Each Sprint
- Sprint retrospective meeting
- Demo to stakeholders
- Update product backlog
- Deploy to staging environment
- Collect user feedback (if applicable)

### After Sprint 5
- Production deployment
- App store submission (iOS/Android)
- Marketing launch preparation
- User onboarding flow testing
- Monitor production metrics
- Plan post-MVP enhancements

---

## Notes

- **Story Allocation:** Each story appears in exactly one sprint
- **Dependency Respect:** All dependencies resolved before dependent stories
- **Workload Balance:** Story points range from 19-22 per sprint
- **Flexibility:** 10% buffer time built into each sprint for bug fixes
- **Quality:** Definition of Done enforced strictly for each sprint
- **Communication:** Daily standups, sprint planning, and retrospectives mandatory

---

**Approved By:** Scrum Master (BMAD Control)  
**Date:** January 17, 2026  
**Status:** LOCKED - No changes without change control process
