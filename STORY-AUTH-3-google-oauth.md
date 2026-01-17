# Story AUTH-3: Google OAuth Authentication

**Priority:** High  
**Dependencies:** AUTH-1 (User Registration), OAuth configuration

**User Story:**  
As a user, I want to login using my Google account, so that I can access the app without creating a new password.

**Acceptance Criteria:**
- OAuth flow initiated via `/api/auth/google` endpoint
- User redirected to Google consent screen
- Authorization code exchanged for access token
- User profile retrieved from Google API
- New user created if email doesn't exist
- Existing user matched by email or oauth_id
- JWT token generated and returned to client
- OAuth provider and oauth_id stored in user record

**Definition of Done:**
- All stories follow the format: "As a [user type], I want [goal], so that [benefit]"
- Acceptance criteria are clear, testable, and specific
- Dependencies are explicitly stated to guide sprint planning
- Priorities align with MVP requirements and user value
- Stories are sized to be completable within a sprint
- Technical debt and infrastructure setup are considered in dependencies
