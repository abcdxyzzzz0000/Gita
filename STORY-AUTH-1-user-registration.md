# Story AUTH-1: User Registration with Email/Password

**Priority:** High  
**Dependencies:** Database setup, User table schema

**User Story:**  
As a new user, I want to register using my email and password, so that I can create a personalized account.

**Acceptance Criteria:**
- Email validation enforces valid email format
- Password must be minimum 8 characters
- Password is hashed using bcrypt before storage
- Duplicate email registration returns appropriate error
- Successful registration returns user object and JWT access token
- User record created in PostgreSQL with timestamp
- Token expiration set to 7 days by default

**Definition of Done:**
- All stories follow the format: "As a [user type], I want [goal], so that [benefit]"
- Acceptance criteria are clear, testable, and specific
- Dependencies are explicitly stated to guide sprint planning
- Priorities align with MVP requirements and user value
- Stories are sized to be completable within a sprint
- Technical debt and infrastructure setup are considered in dependencies
