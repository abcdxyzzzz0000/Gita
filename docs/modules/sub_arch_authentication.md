# Authentication Module - Sub-Architecture

## Module-Level Architecture Overview

The Authentication Module implements a stateless JWT-based authentication system with support for email/password and Google OAuth flows. It follows a layered architecture with clear separation between API endpoints, business logic, and data access layers.

```
┌─────────────────────────────────────────────────────────┐
│                    API Layer                            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │   Register   │  │    Login     │  │ Google OAuth │ │
│  │   Endpoint   │  │   Endpoint   │  │   Endpoints  │ │
│  └──────────────┘  └──────────────┘  └──────────────┘ │
└─────────────────────────────────────────────────────────┘
                          │
┌─────────────────────────────────────────────────────────┐
│                  Business Logic Layer                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │   Password   │  │     JWT      │  │    OAuth     │ │
│  │   Hashing    │  │   Manager    │  │   Handler    │ │
│  └──────────────┘  └──────────────┘  └──────────────┘ │
└─────────────────────────────────────────────────────────┘
                          │
┌─────────────────────────────────────────────────────────┐
│                  Data Access Layer                      │
│  ┌──────────────┐  ┌──────────────┐                    │
│  │     User     │  │  PostgreSQL  │                    │
│  │  Repository  │  │   Database   │                    │
│  └──────────────┘  └──────────────┘                    │
└─────────────────────────────────────────────────────────┘
```

## Internal Components & Responsibilities

### 1. Auth Router (`auth_router.py`)
**Responsibility**: Define API endpoints and handle HTTP request/response

**Functions**:
- `POST /api/auth/register` - User registration endpoint
- `POST /api/auth/login` - User login endpoint
- `GET /api/auth/google` - Initiate OAuth flow
- `GET /api/auth/google/callback` - Handle OAuth callback

**Dependencies**: AuthService, UserRepository

### 2. Auth Service (`auth_service.py`)
**Responsibility**: Business logic for authentication operations

**Functions**:
- `register_user(email, password)` - Create new user account
- `authenticate_user(email, password)` - Validate credentials
- `create_access_token(user_id, email)` - Generate JWT token
- `verify_access_token(token)` - Validate JWT token
- `handle_google_oauth(code)` - Process OAuth callback

**Dependencies**: PasswordHasher, JWTManager, UserRepository, GoogleOAuthClient

### 3. Password Hasher (`password_hasher.py`)
**Responsibility**: Secure password hashing and verification

**Functions**:
- `hash_password(plain_password)` - Hash password with bcrypt
- `verify_password(plain_password, hashed_password)` - Verify password

**Dependencies**: bcrypt library

### 4. JWT Manager (`jwt_manager.py`)
**Responsibility**: JWT token generation and validation

**Functions**:
- `create_token(payload, expires_delta)` - Generate signed JWT
- `decode_token(token)` - Validate and decode JWT
- `get_current_user(token)` - Extract user from token

**Dependencies**: python-jose library, Config

### 5. Google OAuth Client (`google_oauth_client.py`)
**Responsibility**: Handle Google OAuth flow

**Functions**:
- `get_authorization_url(redirect_uri, state)` - Generate OAuth URL
- `exchange_code_for_token(code)` - Exchange auth code for access token
- `get_user_info(access_token)` - Retrieve user profile from Google

**Dependencies**: httpx library, Config

### 6. User Repository (`user_repository.py`)
**Responsibility**: Database operations for User entity

**Functions**:
- `create_user(email, hashed_password, oauth_provider, oauth_id)` - Insert user
- `get_user_by_email(email)` - Find user by email
- `get_user_by_oauth(provider, oauth_id)` - Find user by OAuth ID
- `update_last_login(user_id)` - Update login timestamp

**Dependencies**: SQLAlchemy, PostgreSQL

### 7. Auth Middleware (`auth_middleware.py`)
**Responsibility**: Protect endpoints requiring authentication

**Functions**:
- `require_auth(request)` - Dependency for protected routes
- `optional_auth(request)` - Dependency for optional auth

**Dependencies**: JWTManager

## Data Flow

### Registration Flow (Email/Password)

```
1. Client → POST /api/auth/register {email, password}
2. AuthRouter → validate request body
3. AuthRouter → AuthService.register_user(email, password)
4. AuthService → UserRepository.get_user_by_email(email)
5. UserRepository → PostgreSQL SELECT query
6. PostgreSQL → return null (user doesn't exist)
7. AuthService → PasswordHasher.hash_password(password)
8. PasswordHasher → bcrypt.hashpw() → return hashed_password
9. AuthService → UserRepository.create_user(email, hashed_password)
10. UserRepository → PostgreSQL INSERT query
11. PostgreSQL → return user record
12. AuthService → JWTManager.create_token(user.id, user.email)
13. JWTManager → jwt.encode() → return access_token
14. AuthService → return {user, access_token}
15. AuthRouter → return 201 Created response
16. Client ← {user, accessToken}
```

### Login Flow (Email/Password)

```
1. Client → POST /api/auth/login {email, password}
2. AuthRouter → validate request body
3. AuthRouter → AuthService.authenticate_user(email, password)
4. AuthService → UserRepository.get_user_by_email(email)
5. UserRepository → PostgreSQL SELECT query
6. PostgreSQL → return user record
7. AuthService → PasswordHasher.verify_password(password, user.hashed_password)
8. PasswordHasher → bcrypt.checkpw() → return True/False
9. If False → raise 401 Unauthorized
10. AuthService → UserRepository.update_last_login(user.id)
11. UserRepository → PostgreSQL UPDATE query
12. AuthService → JWTManager.create_token(user.id, user.email)
13. JWTManager → jwt.encode() → return access_token
14. AuthService → return {user, access_token}
15. AuthRouter → return 200 OK response
16. Client ← {user, accessToken}
```

### Google OAuth Flow

```
1. Client → GET /api/auth/google
2. AuthRouter → GoogleOAuthClient.get_authorization_url()
3. GoogleOAuthClient → generate OAuth URL with state
4. AuthRouter → return 302 Redirect to Google
5. User → completes Google consent
6. Google → redirect to /api/auth/google/callback?code=xxx&state=yyy
7. AuthRouter → validate state parameter
8. AuthRouter → GoogleOAuthClient.exchange_code_for_token(code)
9. GoogleOAuthClient → POST to Google token endpoint
10. Google → return access_token
11. GoogleOAuthClient → get_user_info(access_token)
12. GoogleOAuthClient → GET Google userinfo endpoint
13. Google → return {email, name, id}
14. AuthService → UserRepository.get_user_by_oauth('google', google_id)
15. UserRepository → PostgreSQL SELECT query
16. If not found → UserRepository.create_user(email, oauth_provider='google')
17. AuthService → JWTManager.create_token(user.id, user.email)
18. AuthService → return {user, access_token}
19. AuthRouter → return 200 OK response
20. Client ← {user, accessToken}
```

### Token Validation Flow (Protected Endpoint)

```
1. Client → GET /api/bookmarks (with Authorization: Bearer <token>)
2. AuthMiddleware → extract token from header
3. AuthMiddleware → JWTManager.decode_token(token)
4. JWTManager → jwt.decode() with secret key
5. If expired or invalid → raise 401 Unauthorized
6. JWTManager → return decoded payload {user_id, email, exp}
7. AuthMiddleware → inject user_id into request context
8. BookmarksRouter → access user_id from context
9. BookmarksRouter → process request with authenticated user
```

## Database Schema / Tables Involved

### Users Table

```sql
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
```

**Columns Used by Auth Module**:
- `id`: Primary key, included in JWT payload
- `email`: Unique identifier for login, included in JWT payload
- `hashed_password`: Bcrypt hashed password (null for OAuth users)
- `oauth_provider`: 'google' for OAuth users, null for email/password
- `oauth_id`: Google user ID for OAuth users
- `created_at`: Account creation timestamp
- `last_login`: Updated on each successful login

**Indexes**:
- `idx_users_email`: Fast lookup during login
- `idx_users_oauth`: Fast lookup during OAuth callback

## External Services Used

### Google OAuth 2.0 API

**Purpose**: Authenticate users via Google accounts

**Endpoints Used**:
1. **Authorization Endpoint**
   - URL: `https://accounts.google.com/o/oauth2/v2/auth`
   - Method: GET (redirect)
   - Parameters: client_id, redirect_uri, response_type=code, scope, state
   - Response: Redirect to callback with authorization code

2. **Token Exchange Endpoint**
   - URL: `https://oauth2.googleapis.com/token`
   - Method: POST
   - Body: code, client_id, client_secret, redirect_uri, grant_type
   - Response: `{access_token, token_type, expires_in}`

3. **User Info Endpoint**
   - URL: `https://www.googleapis.com/oauth2/v2/userinfo`
   - Method: GET
   - Headers: `Authorization: Bearer <access_token>`
   - Response: `{id, email, name, picture}`

**Configuration Required**:
- `GOOGLE_CLIENT_ID`: OAuth client ID from Google Console
- `GOOGLE_CLIENT_SECRET`: OAuth client secret
- `GOOGLE_REDIRECT_URI`: Callback URL registered in Google Console

**Error Handling**:
- Network errors: Retry with exponential backoff
- Invalid code: Return 400 Bad Request to client
- Expired token: Prompt user to retry OAuth flow

## Security Considerations

### Password Security
- Bcrypt hashing with cost factor 12 (adjustable via config)
- Passwords never logged or exposed in responses
- Minimum password length enforced (8 characters)
- Password strength validation on client side

### JWT Security
- Tokens signed with HS256 algorithm
- Secret key stored in environment variable (min 32 characters)
- Token expiration set to 7 days
- No sensitive data in JWT payload (only user_id and email)
- Tokens validated on every protected request

### OAuth Security
- State parameter prevents CSRF attacks
- Authorization code used only once
- HTTPS enforced for all OAuth redirects
- Client secret never exposed to frontend

### API Security
- Rate limiting on login endpoint (5 attempts/minute per IP)
- HTTPS enforced in production
- CORS configured to allow only trusted origins
- SQL injection prevented by parameterized queries

### Data Protection
- User emails treated as PII
- Database connections encrypted (SSL/TLS)
- Audit logging for authentication events
- Failed login attempts logged for monitoring

## Scalability & Failure Handling

### Scalability Strategies

**Horizontal Scaling**:
- Stateless JWT authentication enables multiple API instances
- No session storage required
- Database connection pooling (10 connections per instance)
- Read replicas for user lookups (future optimization)

**Performance Optimization**:
- Password hashing offloaded to background thread (async)
- JWT validation cached for 1 minute per token
- Database indexes on email and oauth fields
- Connection pooling prevents connection exhaustion

**Load Handling**:
- Expected load: 1000 logins/hour
- Token validation: 10,000 requests/hour
- Database capacity: 1 million users
- OAuth rate limits: 10,000 requests/day (Google free tier)

### Failure Handling

**Database Failures**:
- Connection timeout: 5 seconds
- Retry logic: 3 attempts with exponential backoff
- Circuit breaker: Stop retries after 5 consecutive failures
- Fallback: Return 503 Service Unavailable

**OAuth Failures**:
- Google API timeout: 10 seconds
- Network errors: Retry once, then fail gracefully
- Invalid response: Log error, return user-friendly message
- Rate limit exceeded: Queue requests or show maintenance message

**Token Validation Failures**:
- Expired token: Return 401 with clear error message
- Invalid signature: Return 401, log potential security issue
- Malformed token: Return 400 Bad Request
- Missing token: Return 401 for protected routes, allow for public routes

**Monitoring & Alerts**:
- Failed login rate > 10% triggers alert
- OAuth failure rate > 5% triggers alert
- Database connection errors logged and alerted
- Token validation errors tracked for anomaly detection

## Deployment Considerations

### Environment Variables

```bash
# JWT Configuration
JWT_SECRET_KEY=<32+ character random string>
JWT_ALGORITHM=HS256
JWT_EXPIRATION_DAYS=7

# Google OAuth Configuration
GOOGLE_CLIENT_ID=<from Google Console>
GOOGLE_CLIENT_SECRET=<from Google Console>
GOOGLE_REDIRECT_URI=https://api.bhagavadgita.app/api/auth/google/callback

# Database Configuration
DATABASE_URL=postgresql://user:password@localhost:5432/bhagavad_gita

# Security
BCRYPT_COST_FACTOR=12
RATE_LIMIT_LOGIN=5/minute
```

### Docker Configuration

```dockerfile
# Dockerfile for auth module (part of backend)
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy auth module
COPY backend/auth ./auth
COPY backend/main.py .

# Run FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Health Checks

```python
# Health check endpoint
@router.get("/health")
async def health_check():
    try:
        # Check database connection
        await user_repository.health_check()
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}, 503
```

### Logging Configuration

```python
# Structured logging for auth events
logger.info("user_registered", extra={
    "user_id": user.id,
    "email": user.email,
    "oauth_provider": user.oauth_provider
})

logger.warning("login_failed", extra={
    "email": email,
    "ip_address": request.client.host,
    "reason": "invalid_credentials"
})

logger.error("oauth_error", extra={
    "provider": "google",
    "error": str(e),
    "code": code
})
```

### Migration Strategy

```bash
# Alembic migration for users table
alembic revision --autogenerate -m "create_users_table"
alembic upgrade head
```

### Testing Strategy

**Unit Tests**:
- Password hashing and verification
- JWT token generation and validation
- OAuth URL generation
- User repository CRUD operations

**Integration Tests**:
- Registration endpoint with database
- Login endpoint with database
- OAuth callback flow (mocked Google API)
- Token validation middleware

**Security Tests**:
- SQL injection attempts
- JWT tampering detection
- Expired token rejection
- Rate limiting enforcement

**Performance Tests**:
- 1000 concurrent logins
- Token validation under load
- Database connection pool exhaustion
