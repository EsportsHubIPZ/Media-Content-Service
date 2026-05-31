# Behaviors of Media/Content Service

The Media/Content Service is responsible for managing all static and dynamic media assets on the Esports Hub Platform. It provides capabilities for secure file uploads, validation, storage (via object storage), and news management.

## 1. File Upload and Management (Screenshots/Avatars)
*   **Behavior:** Users (Players, Captains) can upload images, such as match result screenshots, as proof for dispute resolution.
*   **Validation:** The service enforces strict file type (e.g., JPEG, PNG) and size limits before processing.
*   **Storage:** Accepted files are streamed and saved to an Object Storage system (e.g., AWS S3, MinIO).
*   **Metadata:** Information about the uploaded file (original name, S3 key, MIME type, size, uploaded_by) is persisted in the service's relational database (PostgreSQL).
*   **Retrieval:** The Match Engine Service or Web Application can request metadata or pre-signed URLs to view the uploaded screenshots.

## 2. News and Content Publishing
*   **Behavior:** Platform Administrators can author, publish, edit, and delete news articles or announcements.
*   **News Feed:** Registered users can browse a paginated feed of the latest news and updates.
*   **Event Publishing:** Upon publishing a new article, the Media Service publishes a `NewsPublished` event to the RabbitMQ Message Bus. This triggers the Notification Service to alert users about important updates according to their preferences.

## 3. Asynchronous Communication (RabbitMQ)
*   **Publisher:** The Media Service acts as an event publisher for content-related events (e.g., `NewsPublished`).
*   **Decoupling:** By using events, the Media Service does not need to know about the Notification Service directly, ensuring loose coupling.

## 4. Security and Access Control
*   **Authentication:** All endpoints (except public news reading or public media access) require a valid JWT token validated by the API Gateway.
*   **Authorization:** Administrative endpoints (e.g., creating news) are restricted to users with the 'Admin' role.
