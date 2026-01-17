# Story AUTH-5: Token Validation Middleware

**Priority:** High  
**Dependencies:** AUTH-1, AUTH-2, AUTH-3

**User Story:**  
As a system, I want to validate JWT tokens on protected endpoints, so that only authenticated users access personalized features.

**Acceptance Criteria:**
- Protected endpoints check for Authorization header
- Token signature validated using secret key
- Expired tokens return 401 Unauthorized
- Invalid tokens return 401 Unauthorized
- Valid tokens extract user ID for request context
- Token validation middleware reusable across endpoints

**Definition of Done:**
- All stories follow the format: "As a [user type], I want [goal], so that [benefit]"
- Acceptance criteria are clear, testable, and specific
- Dependencies are explicitly stated to guide sprint planning
- Priorities align with MVP requirements and user value
- Stories are sized to be completable within a sprint
- Technical debt and infrastructure setup are considered in dependencies
