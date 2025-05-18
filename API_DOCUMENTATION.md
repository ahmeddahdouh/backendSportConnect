# SportConnect API Documentation

This document provides a comprehensive overview of all available API endpoints in the SportConnect backend.

## Base URL

All API endpoints are prefixed with the base URL of the server.

## Authentication

Most endpoints require JWT authentication. Include the JWT token in the Authorization header:
```
Authorization: Bearer <your_token>
```

## API Endpoints

### Authentication Routes (`/auth`)

#### User Registration
- **POST** `/auth/register`
  - Register a new user
  - Required fields: username, email, password, confirmPassword, firstname, familyname, city, phone, date_of_birth
  - Request Body:
    ```json
    {
      "username": "string",
      "email": "string",
      "password": "string",
      "confirmPassword": "string",
      "firstname": "string",
      "familyname": "string",
      "city": "string",
      "phone": "string",
      "date_of_birth": "YYYY-MM-DD"
    }
    ```
  - Response (201 Created):
    ```json
    {
      "message": "User registered successfully"
    }
    ```

#### User Login
- **POST** `/auth/login`
  - Authenticate a user
  - Required fields: username, password
  - Request Body:
    ```json
    {
      "username": "string",
      "password": "string"
    }
    ```
  - Response (200 OK):
    ```json
    {
      "access_token": "jwt_token_string"
    }
    ```

#### User Profile
- **GET** `/auth/users/<user_id>`
  - Get user information including their events
  - Response (200 OK):
    ```json
    {
      "id": "integer",
      "username": "string",
      "email": "string",
      "firstname": "string",
      "familyname": "string",
      "city": "string",
      "phone": "string",
      "date_of_birth": "YYYY-MM-DD",
      "profileImage": "string",
      "events": [
        {
          "id": "integer",
          "event_name": "string",
          "event_description": "string",
          "event_ville": "string",
          "event_date": "datetime",
          "event_max_utilisateur": "integer",
          "is_private": "boolean",
          "is_team_vs_team": "boolean",
          "event_age_min": "integer",
          "event_age_max": "integer",
          "nombre_utilisateur_min": "integer"
        }
      ]
    }
    ```

- **PUT** `/auth/users/<user_id>`
  - Update user information
  - Request Body:
    ```json
    {
      "username": "string",
      "email": "string",
      "firstname": "string",
      "familyname": "string",
      "city": "string",
      "phone": "string",
      "date_of_birth": "YYYY-MM-DD",
      "password": "string"
    }
    ```
  - Response (200 OK):
    ```json
    {
      "message": "User updated successfully"
    }
    ```

- **PUT** `/auth/users/profile`
  - Update user profile image
  - Request: multipart/form-data with file field
  - Response (201 Created):
    ```json
    {
      "image": "filename.jpg"
    }
    ```

### Event Routes (`/event`)

#### Event Management
- **GET** `/event/booking`
  - Get all events except those created by the current user
  - Requires authentication
  - Response (200 OK):
    ```json
    [
      {
        "id": "integer",
        "event_name": "string",
        "event_description": "string",
        "event_ville": "string",
        "event_date": "datetime",
        "event_max_utilisateur": "integer",
        "is_private": "boolean",
        "is_team_vs_team": "boolean",
        "event_age_min": "integer",
        "event_age_max": "integer",
        "nombre_utilisateur_min": "integer",
        "id_gestionnaire": "integer"
      }
    ]
    ```

- **GET** `/event/curentEvents`
  - Get events created by the current user
  - Requires authentication
  - Response: Same format as `/event/booking`

- **GET** `/event/<event_id>`
  - Get specific event details
  - Requires authentication
  - Response (200 OK):
    ```json
    {
      "id": "integer",
      "event_name": "string",
      "event_description": "string",
      "event_ville": "string",
      "event_date": "datetime",
      "event_max_utilisateur": "integer",
      "is_private": "boolean",
      "is_team_vs_team": "boolean",
      "event_age_min": "integer",
      "event_age_max": "integer",
      "nombre_utilisateur_min": "integer",
      "id_gestionnaire": "integer",
      "users": [
        {
          "id": "integer",
          "username": "string",
          "firstname": "string",
          "familyname": "string"
        }
      ]
    }
    ```

#### Event Participation
- **POST** `/event/participate`
  - Participate in an event
  - Request Body:
    ```json
    {
      "user_id": "integer",
      "event_id": "integer"
    }
    ```
  - Response (201 Created):
    ```json
    {
      "message": "Successfully joined the event"
    }
    ```

- **DELETE** `/event/unparticipate/<event_id>`
  - Unparticipate from an event
  - Requires authentication
  - Response (200 OK):
    ```json
    {
      "message": "Successfully left the event"
    }
    ```

### Team Routes (`/team`)

#### Team Management
- **POST** `/team/`
  - Create a new team
  - Request Body:
    ```json
    {
      "name": "string",
      "description": "string",
      "profile_picture": "string"
    }
    ```
  - Response (201 Created):
    ```json
    {
      "id": "integer",
      "name": "string",
      "description": "string",
      "profile_picture": "string",
      "manager_id": "integer"
    }
    ```

- **GET** `/team/<team_id>`
  - Get team information
  - Response (200 OK):
    ```json
    {
      "id": "integer",
      "name": "string",
      "description": "string",
      "profile_picture": "string",
      "manager_id": "integer",
      "members": [
        {
          "id": "integer",
          "username": "string",
          "firstname": "string",
          "familyname": "string"
        }
      ]
    }
    ```

- **PUT** `/team/<team_id>`
  - Update team information
  - Request Body:
    ```json
    {
      "name": "string",
      "description": "string",
      "profile_picture": "string"
    }
    ```
  - Response (200 OK):
    ```json
    {
      "message": "Team updated successfully"
    }
    ```

#### Team Members
- **POST** `/team/<team_id>/members`
  - Add a member to the team
  - Request Body:
    ```json
    {
      "user_id": "integer"
    }
    ```
  - Response (201 Created):
    ```json
    {
      "message": "Member added successfully"
    }
    ```

### Sport Routes (`/sport`)

- **GET** `/sport/`
  - Get all available sports
  - Response (200 OK):
    ```json
    [
      {
        "id": "integer",
        "name": "string",
        "description": "string"
      }
    ]
    ```

- **PUT** `/sport/<sport_id>`
  - Update sport statistics for a user
  - Request Body:
    ```json
    {
      "sport_stat": {
        "level": "string",
        "experience": "integer",
        "preferred_position": "string"
      }
    }
    ```
  - Response (200 OK):
    ```json
    {
      "message": "Sport stats updated successfully"
    }
    ```

### Notification Routes (`/notification`)

- **GET** `/notification/`
  - Get all notifications for current user
  - Query params: unread_only (boolean)
  - Response (200 OK):
    ```json
    [
      {
        "id": "integer",
        "message": "string",
        "type": "string",
        "is_read": "boolean",
        "created_at": "datetime"
      }
    ]
    ```

- **PUT** `/notification/<notification_id>/read`
  - Mark a notification as read
  - Response (200 OK):
    ```json
    {
      "id": "integer",
      "message": "string",
      "type": "string",
      "is_read": "boolean",
      "created_at": "datetime"
    }
    ```

### Event Invitation Routes (`/event-invitation`)

- **POST** `/event-invitation/event/<event_id>/invite/<user_id>`
  - Invite a user to a private event
  - Response (201 Created):
    ```json
    {
      "id": "integer",
      "event_id": "integer",
      "user_id": "integer",
      "status": "pending",
      "created_at": "datetime"
    }
    ```

- **GET** `/event-invitation/event/<event_id>/invitations`
  - Get all invitations for an event
  - Requires authentication
  - Returns: List of invitations

- **GET** `/event-invitation/user/invitations`
  - Get all invitations for current user
  - Query params: status
  - Requires authentication
  - Returns: List of invitations

- **GET** `/event-invitation/user/sent-invitations`
  - Get all invitations sent by current user
  - Query params: status
  - Requires authentication
  - Returns: List of invitations

- **POST** `/event-invitation/invitation/<invitation_id>/respond`
  - Respond to an invitation
  - Request Body:
    ```json
    {
      "response": "accepted" | "rejected"
    }
    ```
  - Response (200 OK):
    ```json
    {
      "id": "integer",
      "event_id": "integer",
      "user_id": "integer",
      "status": "accepted" | "rejected",
      "created_at": "datetime"
    }
    ```

### Admin Routes

#### Admin Management (`/api/admins`)
- **GET** `/api/admins`
  - Get all admins
  - Returns: List of admins

- **POST** `/api/admins`
  - Create a new admin
  - Request Body:
    ```json
    {
      "username": "string",
      "email": "string",
      "password": "string",
      "firstname": "string",
      "familyname": "string",
      "city": "string",
      "phone": "string",
      "age": "integer"
    }
    ```
  - Response (201 Created):
    ```json
    {
      "message": "Admin created successfully"
    }
    ```

- **DELETE** `/api/admins/<id>`
  - Delete an admin
  - Returns: Success message

#### Admin Event Management
- **GET** `/api/events`
  - Get all events (admin view)
  - Returns: List of events with member details

#### Admin User Management
- **DELETE** `/api/users/<user_id>`
  - Delete a user and their associated events
  - Returns: Success message

## Error Responses

The API uses standard HTTP status codes:
- 200: Success
- 201: Created
- 400: Bad Request
- 401: Unauthorized
- 404: Not Found
- 409: Conflict
- 500: Internal Server Error

Error responses include a JSON object with an "error" field containing the error message:
```json
{
  "error": "Error message description"
}
```

## File Upload

For file uploads (profile pictures, team photos), the API accepts the following file types:
- PNG
- JPG/JPEG
- GIF

Files are stored in the server's upload directory and served through dedicated endpoints.

## CORS Configuration

The API supports CORS for the following origins:
- http://localhost:3000
- https://sportconnect-front-e283.vercel.app

Allowed methods: GET, POST, PUT, DELETE, OPTIONS
Allowed headers: Content-Type, Authorization 