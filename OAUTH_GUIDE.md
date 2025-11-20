# OAuth Integration Guide (Google & Apple Sign-In)

This guide explains how to integrate Google and Apple Sign-In with your CoupleCal backend.

## Overview

The backend now supports three authentication methods:

1. **Email/Password** - Traditional authentication
2. **Google Sign-In** - OAuth 2.0 with Google
3. **Apple Sign-In** - OAuth 2.0 with Apple

## API Endpoints

### OAuth Login

```
POST /api/auth/oauth/login
```

**Request Body:**

```json
{
  "provider": "google", // or "apple"
  "idToken": "eyJhbGciOiJSUzI1NiIsImtpZCI..."
}
```

**Response:**

```json
{
  "success": true,
  "data": {
    "user": {
      "id": "uuid",
      "name": "John Doe",
      "email": "john@example.com",
      "emailVerified": true,
      "authProvider": "google",
      "avatar": "https://...",
      "timezone": "UTC",
      "createdAt": "2025-11-20T...",
      "updatedAt": "2025-11-20T..."
    },
    "tokens": {
      "accessToken": "eyJhbGciOiJIUzI1NiIs...",
      "refreshToken": "eyJhbGciOiJIUzI1NiIs...",
      "expiresIn": 3600
    }
  },
  "message": "Login successful"
}
```

### OAuth Signup

```
POST /api/auth/oauth/signup
```

**Request Body:**

```json
{
  "provider": "google", // or "apple"
  "idToken": "eyJhbGciOiJSUzI1NiIsImtpZCI...",
  "name": "John Doe", // Optional, for Apple first-time signup
  "timezone": "America/New_York" // Optional
}
```

**Response:** Same as OAuth login

## Setup Instructions

### 1. Google Sign-In Setup

#### Step 1: Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the **Google+ API** or **Google Identity Services**

#### Step 2: Create OAuth 2.0 Credentials

1. Navigate to **APIs & Services** > **Credentials**
2. Click **Create Credentials** > **OAuth 2.0 Client ID**
3. Configure the OAuth consent screen if prompted
4. Select **Web application** as the application type
5. Add authorized redirect URIs (if needed for web)
6. For mobile apps, select appropriate platform (iOS/Android)
7. Copy the **Client ID**

#### Step 3: Configure Backend

Add to your `.env` file:

```env
GOOGLE_CLIENT_ID=your-client-id.apps.googleusercontent.com
```

#### Step 4: Client-Side Implementation

**Web (React/Next.js):**

```javascript
import { GoogleOAuthProvider, GoogleLogin } from "@react-oauth/google";

function App() {
  const handleGoogleSuccess = async (credentialResponse) => {
    const response = await fetch("http://your-backend/api/auth/oauth/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        provider: "google",
        idToken: credentialResponse.credential,
      }),
    });
    const data = await response.json();
    // Store tokens and redirect
  };

  return (
    <GoogleOAuthProvider clientId="your-client-id">
      <GoogleLogin
        onSuccess={handleGoogleSuccess}
        onError={() => console.log("Login Failed")}
      />
    </GoogleOAuthProvider>
  );
}
```

**React Native:**

```javascript
import { GoogleSignin } from "@react-native-google-signin/google-signin";

// Configure
GoogleSignin.configure({
  webClientId: "your-client-id.apps.googleusercontent.com",
  offlineAccess: true,
});

// Sign in
const signInWithGoogle = async () => {
  try {
    await GoogleSignin.hasPlayServices();
    const userInfo = await GoogleSignin.signIn();
    const idToken = userInfo.idToken;

    // Send to backend
    const response = await fetch("http://your-backend/api/auth/oauth/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        provider: "google",
        idToken: idToken,
      }),
    });
  } catch (error) {
    console.error(error);
  }
};
```

### 2. Apple Sign-In Setup

#### Step 1: Apple Developer Account Setup

1. Go to [Apple Developer](https://developer.apple.com/)
2. Navigate to **Certificates, Identifiers & Profiles**
3. Register an **App ID** (if not already done)
4. Enable **Sign in with Apple** capability

#### Step 2: Create Service ID

1. Go to **Identifiers** > **Services IDs**
2. Click **+** to create a new Service ID
3. Enter a description and identifier (e.g., `com.yourcompany.yourapp.signin`)
4. Enable **Sign in with Apple**
5. Configure domains and return URLs
6. Save the Service ID (this is your `APPLE_CLIENT_ID`)

#### Step 3: Create Key for Apple Sign-In

1. Go to **Keys** section
2. Click **+** to create a new key
3. Enter a name and enable **Sign in with Apple**
4. Configure the key with your App ID
5. Download the `.p8` key file (save it securely!)
6. Note the **Key ID**

#### Step 4: Configure Backend

Add to your `.env` file:

```env
APPLE_CLIENT_ID=com.yourcompany.yourapp.signin
APPLE_TEAM_ID=ABC123DEFG
APPLE_KEY_ID=XYZ123WXYZ
APPLE_PRIVATE_KEY=/path/to/AuthKey_XYZ123WXYZ.p8
```

#### Step 5: Client-Side Implementation

**Web:**

```javascript
// Load Apple Sign-In JS SDK
<script src="https://appleid.cdn-apple.com/appleauth/static/jsapi/appleid/1/en_US/appleid.auth.js"></script>;

// Initialize
window.AppleID.auth.init({
  clientId: "com.yourcompany.yourapp.signin",
  scope: "name email",
  redirectURI: "https://your-app.com/auth/callback",
  usePopup: true,
});

// Sign in
async function signInWithApple() {
  try {
    const data = await window.AppleID.auth.signIn();
    const response = await fetch("http://your-backend/api/auth/oauth/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        provider: "apple",
        idToken: data.authorization.id_token,
        name: data.user?.name
          ? `${data.user.name.firstName} ${data.user.name.lastName}`
          : null,
      }),
    });
  } catch (error) {
    console.error(error);
  }
}
```

**React Native:**

```javascript
import appleAuth from "@invertase/react-native-apple-authentication";

const signInWithApple = async () => {
  try {
    const appleAuthRequestResponse = await appleAuth.performRequest({
      requestedOperation: appleAuth.Operation.LOGIN,
      requestedScopes: [appleAuth.Scope.EMAIL, appleAuth.Scope.FULL_NAME],
    });

    const { identityToken, fullName } = appleAuthRequestResponse;

    // Send to backend
    const response = await fetch("http://your-backend/api/auth/oauth/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        provider: "apple",
        idToken: identityToken,
        name: fullName ? `${fullName.givenName} ${fullName.familyName}` : null,
      }),
    });
  } catch (error) {
    console.error(error);
  }
};
```

## Database Changes

The `users` table has been updated with the following fields:

- `password_hash` - Now nullable (for OAuth-only users)
- `auth_provider` - VARCHAR(50), defaults to 'email' (values: 'email', 'google', 'apple')
- `oauth_provider_id` - VARCHAR(255), nullable, indexed - Unique ID from OAuth provider

### Running Migration

To apply the database migration:

```bash
# Using the migration script
./migrate.sh

# Or manually with alembic
alembic upgrade head
```

## Security Considerations

1. **Token Verification**: The backend verifies ID tokens with Google/Apple servers to ensure authenticity
2. **Email Uniqueness**: Users cannot create multiple accounts with the same email using different providers
3. **Provider Locking**: Once an email is registered with a provider, users must use that same provider to login
4. **HTTPS Required**: OAuth flows should only be used over HTTPS in production

## Error Handling

### Common Error Responses

**Invalid Token:**

```json
{
  "success": false,
  "error": {
    "code": "UNAUTHORIZED",
    "message": "Invalid Google ID token"
  }
}
```

**Email Already Exists:**

```json
{
  "success": false,
  "error": {
    "code": "CONFLICT",
    "message": "An account with email user@example.com already exists. Please login with email."
  }
}
```

## Testing

### Testing Google Sign-In

1. Use Google's OAuth 2.0 Playground to get test tokens
2. Or use the official Google Sign-In button in your test app
3. The backend will verify tokens against Google's servers

### Testing Apple Sign-In

1. Apple Sign-In requires a real device or simulator for iOS
2. For web testing, use Apple's provided test accounts
3. The backend validates JWT signatures using Apple's public keys

## Environment Variables Summary

Required environment variables:

```env
# Google OAuth
GOOGLE_CLIENT_ID=your-google-client-id.apps.googleusercontent.com

# Apple OAuth
APPLE_CLIENT_ID=com.yourcompany.yourapp.signin
APPLE_TEAM_ID=ABC123DEFG
APPLE_KEY_ID=XYZ123WXYZ
APPLE_PRIVATE_KEY=/path/to/AuthKey_XYZ123WXYZ.p8
```

## Additional Notes

### Apple Sign-In Specifics

- **Name Availability**: Apple only provides the user's name on the **first** sign-in. Subsequent sign-ins will not include the name.
- **Email Privacy**: Users can choose to hide their email, in which case Apple provides a proxy email (e.g., `abc123@privaterelay.appleid.com`)
- **Token Expiration**: Apple ID tokens expire after 10 minutes

### Google Sign-In Specifics

- **Profile Picture**: Google provides a profile picture URL that can be stored
- **Email Verification**: Google-verified emails are automatically marked as verified
- **Token Expiration**: Google ID tokens are short-lived (typically 1 hour)

## Migration from Email to OAuth

If a user already has an email/password account and wants to link OAuth:

1. Currently, the system prevents duplicate emails across auth providers
2. To implement account linking, you would need to:
   - Add a linking endpoint
   - Verify the user is authenticated
   - Update their `auth_provider` and `oauth_provider_id`
   - Handle password field appropriately

## Support

For issues or questions:

- Check the backend logs for detailed error messages
- Verify your OAuth credentials are correctly configured
- Ensure ID tokens are not expired
- Test with the provider's official testing tools first
