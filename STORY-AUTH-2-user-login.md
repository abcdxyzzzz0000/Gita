# Story AUTH-2: User Login with Email/Password

**Priority:** High  
**Dependencies:** AUTH-1 (User Registration)

**User Story:**  
As a registered user, I want to login with my email and password, so that I can access my personalized content.

**Acceptance Criteria:**
- Email and password validated against database
- Invalid credentials return 401 Unauthorized error
- Successful login returns user object and JWT access token
- Last login timestamp updated in database
- Token includes user ID and email in payload
- Token can be validated on subsequent requests

**Definition of Done:**
- All stories follow the format: "As a [user type], I want [goal], so that [benefit]"
- Acceptance criteria are clear, testable, and specific
- Dependencies are explicitly stated to guide sprint planning
- Priorities align with MVP requirements and user value
- Stories are sized to be completable within a sprint
- Technical debt and infrastructure setup are considered in dependencies
