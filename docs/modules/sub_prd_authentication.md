# Authentication Module - Sub-PRD

## Module Overview & Purpose

The Authentication Module provides secure user registration, login, and session management for the Bhagavad Gita Learning Application. It supports both email/password authentication and Google OAuth, enabling users to access personalized features like bookmarks and reading progress while maintaining optional anonymous read-only access.

## Functional Requirements

### User Stories & Acceptance Criteria

#### US-AUTH-1: User Registration with Email/Password
**As a** new user  
**I want** to register using my email and password  
**So that** I can create a personalized account

**Acceptance Criteria:**
- Email validation enforces valid email format
- Password must be minimum 8 characters
- Password is hashed using bcrypt before storage
- Duplicate email registration returns appropriate error
- Successful registration returns user object and JWT access token
- User record created in PostgreSQL with timestamp
- Token expiration set to 7 days by default

#### US-AUTH-2: User Login with Email/Password
**As a** registered user  
**I want** to login with my email and password  
**So that** I can access my personalized content

**Acceptance Criteria:**
- Email and password validated against database
- Invalid credentials return 401 Unauthorized error
- Successful login returns user object and JWT access token
- Last login timestamp updated in database
- Token includes user ID and email in payload
- Token can be validated on subsequent requests

#### US-AUTH-3: Google OAuth Authentication
**As a** user  
**I want** to login using my Google account  
**So that** I can access the app without creating a new password

**Acceptance Criteria:**
- OAuth flow initiated via `/api/auth/google` endpoint
- User redirected to Google consent screen
- Authorization code exchanged for access token
- User profile retrieved from Google API
- New user created if email doesn't exist
- Existing user matched by email or oauth_id
- JWT token generated and returned to client
- OAuth provider and oauth_id stored in user record

#### US-AUTH-4: Anonymous Read-Only Access
**As a** visitor  
**I want** to browse content without authentication  
**So that** I can explore the app before registering

**Acceptance Criteria:**
- Chapter and shloka endpoints accessible without token
- Bookmark and profile endpoints require authentication
- Anonymous users see "Sign in to bookmark" prompts
- No user-specific data returned for anonymous requests

#### US-AUTH-5: Token Validation
**As a** system  
**I want** to validate JWT tokens on protected endpoints  
**So that** only authenticated users access personalized features

**Acceptance Criteria:**
- Protected endpoints check for Authorization header
- Token signature validated using secret key
- Expired tokens return 401 Unauthorized
- Invalid tokens return 401 Unauthorized
- Valid tokens extract user ID for request context
- Token validation middleware reusable across endpoints

## Non-Functional Requirements

### Performance
- Token generation: < 100ms
- Token validation: < 50ms
- Password hashing: < 200ms (bcrypt with appropriate cost factor)
- OAuth flow completion: < 3 seconds total

### Security
- Passwords hashed with bcrypt (cost factor 12)
- JWT tokens signed with HS256 algorithm
- Secret keys stored in environment variables
- HTTPS enforced for all authentication endpoints
- OAuth state parameter prevents CSRF attacks
- Rate limiting on login endpoint (5 attempts per minute per IP)

### Scalability
- Stateless JWT authentication enables horizontal scaling
- No session storage required
- Token validation doesn't require database lookup

### Reliability
- OAuth failures gracefully handled with user-friendly errors
- Database connection errors return 503 Service Unavailable
- Token expiration handled with clear error messages

## API Contracts

### POST /api/auth/register

**Request:**
```json
{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

**Response (201 Created):**
```json
{
  "user": {
    "id": "uuid",
    "email": "user@example.com",
    "oauthProvider": null,
    "createdAt": "2026-01-17T10:00:00Z",
    "notificationEnabled": true,
    "notificationTime": "08:00"
  },
  "accessToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Error Response (400 Bad Request):**
```json
{
  "detail": "Email already registered"
}
```

### POST /api/auth/login

**Request:**
```json
{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

**Response (200 OK):**
```json
{
  "user": {
    "id": "uuid",
    "email": "user@example.com",
    "oauthProvider": null,
    "createdAt": "2026-01-17T10:00:00Z",
    "lastLogin": "2026-01-17T15:30:00Z",
    "notificationEnabled": true,
    "notificationTime": "08:00"
  },
  "accessToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Error Response (401 Unauthorized):**
```json
{
  "detail": "Invalid credentials"
}
```

### GET /api/auth/google

**Response:** 302 Redirect to Google OAuth consent screen

**Query Parameters:**
- `redirect_uri`: Callback URL after OAuth completion
- `state`: CSRF protection token

### GET /api/auth/google/callback

**Query Parameters:**
- `code`: Authorization code from Google
- `state`: CSRF protection token

**Response (200 OK):**
```json
{
  "user": {
    "id": "uuid",
    "email": "user@gmail.com",
    "oauthProvider": "google",
    "createdAt": "2026-01-17T10:00:00Z",
    "lastLogin": "2026-01-17T15:30:00Z",
    "notificationEnabled": true,
    "notificationTime": "08:00"
  },
  "accessToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

## Error Handling & Edge Cases

### Error Scenarios

1. **Duplicate Email Registration**
   - Error: 400 Bad Request
   - Message: "Email already registered"
   - Action: Prompt user to login instead

2. **Invalid Email Format**
   - Error: 400 Bad Request
   - Message: "Invalid email format"
   - Action: Client-side validation before submission

3. **Weak Password**
   - Error: 400 Bad Request
   - Message: "Password must be at least 8 characters"
   - Action: Client-side validation with strength indicator

4. **Invalid Login Credentials**
   - Error: 401 Unauthorized
   - Message: "Invalid credentials"
   - Action: Generic message to prevent email enumeration

5. **Expired Token**
   - Error: 401 Unauthorized
   - Message: "Token expired"
   - Action: Redirect to login, clear local storage

6. **OAuth Failure**
   - Error: 400 Bad Request
   - Message: "OAuth authentication failed"
   - Action: Retry option or fallback to email/password

7. **Database Connection Error**
   - Error: 503 Service Unavailable
   - Message: "Service temporarily unavailable"
   - Action: Retry after delay

### Edge Cases

- User cancels OAuth consent: Return to login with message
- OAuth email doesn't match existing account: Create new account or link
- Token validation during database downtime: Fail gracefully
- Concurrent registration with same email: Database unique constraint prevents
- Password change for OAuth users: Not applicable, show appropriate message

## Dependencies on Other Modules

### Internal Dependencies
- **Database Module**: User table for storing credentials and profile
- **Configuration Module**: Environment variables for JWT secret, OAuth credentials

### External Dependencies
- **Google OAuth API**: User authentication and profile retrieval
- **PostgreSQL**: User data persistence
- **bcrypt Library**: Password hashing
- **python-jose Library**: JWT token generation and validation

## Assumptions & Constraints

### Assumptions
- Users have valid email addresses
- Google OAuth is available and operational
- HTTPS is enforced in production
- Frontend handles token storage securely
- Token refresh not required in Phase 1 (7-day expiration sufficient)

### Constraints
- JWT tokens are stateless (cannot be revoked before expiration)
- OAuth limited to Google provider in Phase 1
- No multi-factor authentication in Phase 1
- No password reset functionality in Phase 1
- Rate limiting requires reverse proxy or API gateway

## Success Metrics

### Functional Metrics
- Registration success rate > 95%
- Login success rate > 98%
- OAuth completion rate > 90%
- Token validation accuracy: 100%

### Performance Metrics
- Average registration time < 500ms
- Average login time < 300ms
- Token validation time < 50ms
- OAuth flow completion < 3 seconds

### Security Metrics
- Zero plaintext passwords in database
- Zero successful brute force attacks
- 100% HTTPS coverage for auth endpoints
- Token expiration enforced correctly

## Traceability to Master PRD

- **FR1**: User authentication via email or Google OAuth with optional anonymous read-only access
- **NFR5**: Application must respect user privacy and implement secure authentication practices
- **Epic 1, Story 1.3**: Authentication System implementation
