# CoupleCal Backend API Specification

## Overview

This document outlines the backend API requirements for the CoupleCal mobile application. The backend should be built as a RESTful API with JSON responses and JWT-based authentication.

---

## Technology Stack Recommendations

- **Runtime**: Node.js (v20+) with Express.js or NestJS
- **Database**: PostgreSQL or MongoDB
- **Authentication**: JWT (Access + Refresh Tokens)
- **File Storage**: AWS S3 or similar (for image uploads in Week 11-12)
- **Email Service**: SendGrid, AWS SES, or similar
- **Deployment**: AWS, Google Cloud, or similar container service

---

## Base Configuration

### Base URL
```
Development: http://localhost:3000/api
Staging: https://api-staging.couplecal.com/api
Production: https://api.couplecal.com/api
```

### Common Headers
```
Content-Type: application/json
Authorization: Bearer {access_token}
```

### Standard Response Format

#### Success Response
```json
{
  "success": true,
  "data": { ... },
  "message": "Operation successful"
}
```

#### Error Response
```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "Human readable error message",
    "details": { ... }  // Optional additional details
  }
}
```

### Standard Error Codes
- `VALIDATION_ERROR` - Input validation failed
- `UNAUTHORIZED` - Authentication required
- `FORBIDDEN` - Insufficient permissions
- `NOT_FOUND` - Resource not found
- `CONFLICT` - Resource already exists
- `INTERNAL_ERROR` - Server error
- `RATE_LIMIT_EXCEEDED` - Too many requests

---

## Week 1-2: Authentication Endpoints (Priority 1)

### 1. User Signup (Email/Password)

**POST** `/auth/signup`

**Request Body:**
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "SecurePass123!"
}
```

**Success Response (201):**
```json
{
  "success": true,
  "data": {
    "user": {
      "id": "uuid",
      "name": "John Doe",
      "email": "john@example.com",
      "emailVerified": false,
      "createdAt": "2025-01-01T00:00:00Z"
    },
    "tokens": {
      "accessToken": "jwt_access_token",
      "refreshToken": "jwt_refresh_token",
      "expiresIn": 3600
    }
  },
  "message": "Account created successfully"
}
```

**Validation Rules:**
- Name: Required, 2-50 characters
- Email: Required, valid email format, unique
- Password: Required, minimum 8 characters, must contain uppercase, lowercase, number

---

### 2. User Login (Email/Password)

**POST** `/auth/login`

**Request Body:**
```json
{
  "email": "john@example.com",
  "password": "SecurePass123!"
}
```

**Success Response (200):**
```json
{
  "success": true,
  "data": {
    "user": {
      "id": "uuid",
      "name": "John Doe",
      "email": "john@example.com",
      "emailVerified": true,
      "createdAt": "2025-01-01T00:00:00Z"
    },
    "tokens": {
      "accessToken": "jwt_access_token",
      "refreshToken": "jwt_refresh_token",
      "expiresIn": 3600
    }
  },
  "message": "Login successful"
}
```

**Error Response (401):**
```json
{
  "success": false,
  "error": {
    "code": "INVALID_CREDENTIALS",
    "message": "Invalid email or password"
  }
}
```

---

### 3. Refresh Access Token

**POST** `/auth/refresh`

**Request Body:**
```json
{
  "refreshToken": "jwt_refresh_token"
}
```

**Success Response (200):**
```json
{
  "success": true,
  "data": {
    "accessToken": "new_jwt_access_token",
    "expiresIn": 3600
  }
}
```

---

### 4. Logout

**POST** `/auth/logout`

**Headers:**
```
Authorization: Bearer {access_token}
```

**Success Response (200):**
```json
{
  "success": true,
  "message": "Logged out successfully"
}
```

---

### 5. Forgot Password

**POST** `/auth/forgot-password`

**Request Body:**
```json
{
  "email": "john@example.com"
}
```

**Success Response (200):**
```json
{
  "success": true,
  "message": "Password reset email sent"
}
```

**Note:** Always return success even if email doesn't exist (security best practice)

---

### 6. Reset Password

**POST** `/auth/reset-password`

**Request Body:**
```json
{
  "token": "reset_token_from_email",
  "newPassword": "NewSecurePass123!"
}
```

**Success Response (200):**
```json
{
  "success": true,
  "message": "Password reset successful"
}
```

---

### 7. Verify Email

**POST** `/auth/verify-email`

**Request Body:**
```json
{
  "token": "verification_token_from_email"
}
```

**Success Response (200):**
```json
{
  "success": true,
  "message": "Email verified successfully"
}
```

---

## Week 3-4: User Profile Endpoints (Priority 2)

### 8. Get User Profile

**GET** `/user/profile`

**Headers:**
```
Authorization: Bearer {access_token}
```

**Success Response (200):**
```json
{
  "success": true,
  "data": {
    "user": {
      "id": "uuid",
      "name": "John Doe",
      "email": "john@example.com",
      "emailVerified": true,
      "phone": "+1234567890",
      "avatar": "https://cdn.couplecal.com/avatars/user123.jpg",
      "timezone": "America/New_York",
      "createdAt": "2025-01-01T00:00:00Z",
      "updatedAt": "2025-01-15T00:00:00Z"
    }
  }
}
```

---

### 9. Update User Profile

**PUT** `/user/profile`

**Headers:**
```
Authorization: Bearer {access_token}
```

**Request Body:**
```json
{
  "name": "John Updated",
  "phone": "+1234567890",
  "timezone": "America/Los_Angeles"
}
```

**Success Response (200):**
```json
{
  "success": true,
  "data": {
    "user": { ... }
  },
  "message": "Profile updated successfully"
}
```

---

### 10. Change Password

**POST** `/user/change-password`

**Headers:**
```
Authorization: Bearer {access_token}
```

**Request Body:**
```json
{
  "currentPassword": "OldPass123!",
  "newPassword": "NewPass123!"
}
```

**Success Response (200):**
```json
{
  "success": true,
  "message": "Password changed successfully"
}
```

---

## Week 4: Family Group Endpoints (Priority 3)

### 11. Create Family Group

**POST** `/family/groups`

**Headers:**
```
Authorization: Bearer {access_token}
```

**Request Body:**
```json
{
  "name": "Smith Family",
  "description": "Our family calendar"
}
```

**Success Response (201):**
```json
{
  "success": true,
  "data": {
    "group": {
      "id": "uuid",
      "name": "Smith Family",
      "description": "Our family calendar",
      "ownerId": "user_uuid",
      "members": [
        {
          "userId": "user_uuid",
          "name": "John Doe",
          "email": "john@example.com",
          "role": "owner",
          "joinedAt": "2025-01-01T00:00:00Z"
        }
      ],
      "createdAt": "2025-01-01T00:00:00Z"
    }
  }
}
```

---

### 12. Invite Family Member

**POST** `/family/groups/{groupId}/invite`

**Headers:**
```
Authorization: Bearer {access_token}
```

**Request Body:**
```json
{
  "email": "jane@example.com",
  "role": "member"  // "owner", "admin", "member"
}
```

**Success Response (200):**
```json
{
  "success": true,
  "data": {
    "invitation": {
      "id": "uuid",
      "groupId": "group_uuid",
      "email": "jane@example.com",
      "role": "member",
      "status": "pending",
      "expiresAt": "2025-01-08T00:00:00Z"
    }
  },
  "message": "Invitation sent successfully"
}
```

---

## Week 5-6: Calendar Event Endpoints (Priority 4)

### 13. Create Event

**POST** `/events`

**Headers:**
```
Authorization: Bearer {access_token}
```

**Request Body:**
```json
{
  "title": "Doctor Appointment",
  "description": "Annual checkup",
  "startTime": "2025-01-15T14:00:00Z",
  "endTime": "2025-01-15T15:00:00Z",
  "location": "123 Main St, City, State",
  "attendees": ["user_uuid_1", "user_uuid_2"],
  "recurrence": {
    "frequency": "weekly",  // "daily", "weekly", "monthly", "yearly", "none"
    "interval": 1,
    "endDate": "2025-12-31T00:00:00Z"
  },
  "reminders": [
    {
      "type": "notification",  // "notification", "email"
      "minutesBefore": 30
    }
  ],
  "color": "#FF5733",
  "familyGroupId": "group_uuid"
}
```

**Success Response (201):**
```json
{
  "success": true,
  "data": {
    "event": {
      "id": "uuid",
      "title": "Doctor Appointment",
      "description": "Annual checkup",
      "startTime": "2025-01-15T14:00:00Z",
      "endTime": "2025-01-15T15:00:00Z",
      "location": "123 Main St, City, State",
      "attendees": [...],
      "recurrence": {...},
      "reminders": [...],
      "color": "#FF5733",
      "createdBy": "user_uuid",
      "createdAt": "2025-01-01T00:00:00Z"
    }
  }
}
```

---

### 14. Get Events

**GET** `/events?startDate=2025-01-01&endDate=2025-01-31&familyGroupId=group_uuid`

**Query Parameters:**
- `startDate` (required): ISO 8601 date
- `endDate` (required): ISO 8601 date
- `familyGroupId` (optional): Filter by family group

**Success Response (200):**
```json
{
  "success": true,
  "data": {
    "events": [
      { ... }
    ],
    "pagination": {
      "total": 45,
      "page": 1,
      "pageSize": 20
    }
  }
}
```

---

## Week 7-8: Task Endpoints (Priority 5)

### 15. Create Task

**POST** `/tasks`

**Request Body:**
```json
{
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "dueDate": "2025-01-15T18:00:00Z",
  "priority": "high",  // "low", "medium", "high"
  "assignedTo": "user_uuid",
  "linkedEventId": "event_uuid",  // Optional
  "familyGroupId": "group_uuid"
}
```

**Success Response (201):**
```json
{
  "success": true,
  "data": {
    "task": {
      "id": "uuid",
      "title": "Buy groceries",
      "description": "Milk, eggs, bread",
      "dueDate": "2025-01-15T18:00:00Z",
      "priority": "high",
      "status": "pending",
      "assignedTo": "user_uuid",
      "createdBy": "user_uuid",
      "createdAt": "2025-01-01T00:00:00Z"
    }
  }
}
```

---

### 16. Update Task Status

**PATCH** `/tasks/{taskId}/status`

**Request Body:**
```json
{
  "status": "completed"  // "pending", "in_progress", "completed", "cancelled"
}
```

**Success Response (200):**
```json
{
  "success": true,
  "data": {
    "task": { ... }
  }
}
```

---

## Week 9-10: Voice Command Processing (Priority 6)

### 17. Process Voice Command

**POST** `/ai/voice-command`

**Request Body:**
```json
{
  "transcription": "Add dentist appointment tomorrow at 3pm",
  "context": {
    "userId": "user_uuid",
    "familyGroupId": "group_uuid",
    "timezone": "America/New_York"
  }
}
```

**Success Response (200):**
```json
{
  "success": true,
  "data": {
    "intent": "create_event",
    "confidence": 0.95,
    "extractedData": {
      "title": "Dentist Appointment",
      "startTime": "2025-01-16T15:00:00Z",
      "endTime": "2025-01-16T16:00:00Z"
    },
    "preview": "I'll add 'Dentist Appointment' for tomorrow at 3:00 PM. Should I proceed?"
  }
}
```

---

## Week 11-12: Image Processing Endpoints (Priority 7)

### 18. Upload Schedule Image

**POST** `/ai/upload-schedule`

**Headers:**
```
Authorization: Bearer {access_token}
Content-Type: multipart/form-data
```

**Request Body:**
```
file: [image file]
familyGroupId: group_uuid
```

**Success Response (200):**
```json
{
  "success": true,
  "data": {
    "uploadId": "uuid",
    "imageUrl": "https://cdn.couplecal.com/uploads/schedule123.jpg",
    "status": "processing"
  }
}
```

---

### 19. Get Extracted Events from Image

**GET** `/ai/schedule-extraction/{uploadId}`

**Success Response (200):**
```json
{
  "success": true,
  "data": {
    "status": "completed",
    "events": [
      {
        "title": "Soccer Practice",
        "startTime": "2025-01-15T16:00:00Z",
        "endTime": "2025-01-15T17:30:00Z",
        "location": "Community Field",
        "confidence": 0.92
      }
    ]
  }
}
```

---

## Week 13: Google Calendar Integration (Priority 8)

### 20. Connect Google Calendar

**POST** `/integrations/google/connect`

**Request Body:**
```json
{
  "authCode": "google_auth_code_from_oauth"
}
```

**Success Response (200):**
```json
{
  "success": true,
  "data": {
    "integration": {
      "id": "uuid",
      "provider": "google",
      "status": "connected",
      "calendars": [...]
    }
  }
}
```

---

### 21. Sync Events with Google Calendar

**POST** `/integrations/google/sync`

**Success Response (200):**
```json
{
  "success": true,
  "data": {
    "syncedEvents": 25,
    "conflictsDetected": 2,
    "lastSyncAt": "2025-01-15T12:00:00Z"
  }
}
```

---

## Database Schema Recommendations

### Users Table
```sql
CREATE TABLE users (
  id UUID PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  email VARCHAR(255) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  email_verified BOOLEAN DEFAULT false,
  phone VARCHAR(50),
  avatar_url TEXT,
  timezone VARCHAR(100) DEFAULT 'UTC',
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);
```

### Family Groups Table
```sql
CREATE TABLE family_groups (
  id UUID PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  description TEXT,
  owner_id UUID REFERENCES users(id),
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);
```

### Events Table
```sql
CREATE TABLE events (
  id UUID PRIMARY KEY,
  title VARCHAR(255) NOT NULL,
  description TEXT,
  start_time TIMESTAMP NOT NULL,
  end_time TIMESTAMP NOT NULL,
  location TEXT,
  color VARCHAR(7),
  recurrence JSONB,
  reminders JSONB,
  family_group_id UUID REFERENCES family_groups(id),
  created_by UUID REFERENCES users(id),
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);
```

### Tasks Table
```sql
CREATE TABLE tasks (
  id UUID PRIMARY KEY,
  title VARCHAR(255) NOT NULL,
  description TEXT,
  due_date TIMESTAMP,
  priority VARCHAR(20) DEFAULT 'medium',
  status VARCHAR(20) DEFAULT 'pending',
  assigned_to UUID REFERENCES users(id),
  linked_event_id UUID REFERENCES events(id),
  family_group_id UUID REFERENCES family_groups(id),
  created_by UUID REFERENCES users(id),
  completed_at TIMESTAMP,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);
```

---

## Security Requirements

1. **Authentication**
   - Use bcrypt or argon2 for password hashing
   - JWT tokens with 1-hour expiry for access tokens
   - Refresh tokens valid for 7 days
   - Implement rate limiting on auth endpoints

2. **Authorization**
   - Validate user permissions for family group operations
   - Ensure users can only access their own data
   - Implement role-based access control (owner, admin, member)

3. **Data Validation**
   - Validate all input on the server side
   - Sanitize user input to prevent XSS
   - Use parameterized queries to prevent SQL injection

4. **HTTPS Only**
   - All API endpoints must use HTTPS in production
   - Implement CORS properly
   - Set secure HTTP headers

---

## Performance Requirements

- API response time: < 200ms for 95% of requests
- Support 1000+ concurrent users
- Implement database indexing on frequently queried fields
- Use caching (Redis) for frequently accessed data
- Implement pagination for list endpoints

---

## Monitoring and Analytics

- Log all API requests with timestamps
- Track error rates and response times
- Monitor database performance
- Set up alerts for critical failures
- Implement health check endpoint: `GET /health`

---

## Development Timeline

- **Week 1-2**: Auth endpoints (Priority 1) ✅ Required for frontend
- **Week 3-4**: User profile + Family groups (Priority 2-3)
- **Week 5-6**: Calendar events (Priority 4)
- **Week 7-8**: Tasks (Priority 5)
- **Week 9-10**: Voice AI integration (Priority 6)
- **Week 11-12**: Image OCR + AI (Priority 7)
- **Week 13**: Google Calendar sync (Priority 8)

---

## Contact and Support

For questions or clarifications regarding this API specification, please contact the backend development team.

**Note**: This specification covers the MVP (Phase 1) requirements. Additional features and endpoints will be defined in Phase 2.

