Capstone Social Media Api

Instructions:

This project is a Django-based backend API for a social media platform. It includes user management, posts, likes, and comments functionality.

I created directory to contain the project on my local machine
Github repository was created
I enabled and activated virtual environment
Pip3 install django
I initialize git in the empty directory.
I creeated the project: python3 django startproject <projectname>.
Initial accounts app was created: python3 manage.py startapp accounts
Migrations were made to get the database, __pychache__, and __init__.py
which were later added to gitignore.
 

 # Capstone Social Media API

This is a RESTful API for a social media platform, allowing users to create posts, interact with other users' content, and perform advanced social media features such as likes, comments, tagging, hashtags, notifications, direct messaging, and trending post.


Core Features
User Authentication and Authorization**:
  JSON Web Token (JWT) for authentication.
  APIView for registring, login, logout, and profile adjustment endpoit.
CRUD Operations for Posts**:
  - Users can create, read, update, and delete their posts.
User Profiles**:
  - Users can customize their profile with fields such as bio, location, profile picture, and cover photo.
Followers and Following:
  - Users can follow and unfollow others.

 Advanced Features
1.Likes and Comments**:
   - Users can like and comment on posts.
   - Endpoints to manage likes and comments.
2.Notifications**:
   - Users receive notifications when someone follows them, likes their post, or comments on it.
3.Direct Messaging**:
   - Allows private messaging between users.
4.Post Sharing and Reposts**:
   - Users can share/repost content from other users to their own feed, with an option to add content to the shared post.
5.Hashtags and Tagging**:
   - Users can tag other users in posts or add hashtags.
   - Endpoints to retrieve posts by specific hashtags or mentions.
6.Trending Posts:
   - Displays trending posts based on likes and reposts in the last 24 hours.



 Installation

Prerequisites
- Python 3.9+
- Django 4.0+
- PostgreSQL
- DRF 

Steps
1. Clone the repository:


2. Install dependencies:
   bash
   pip install -r requirements.txt
   

3. Configure the `.env` file:
   - Add your database credentials, secret key, and JWT settings.

4. Apply migrations:
   python manage.py migrate


5. Start the development server:
   python3 manage.py runserver


---

API Endpoints

Authentication
Login: `POST /auth/login/`
Register: `POST /auth/register/`
Refresh Token: `POST /auth/token/refresh/`

Posts
- Create Post: `POST /posts/`
- Retrieve All Posts: `GET /posts/`
- Retrieve Single Post: `GET /posts/{id}/`
- Update Post: `PUT /posts/{id}/`
- Delete Post: `DELETE /posts/{id}/`

 Likes and Comments
- Like a Post: `POST /posts/{id}/like/`
- Comment on a Post: `POST /posts/{id}/comment/`

Notifications
- Retrieve Notifications: `GET /notifications/`

Direct Messaging
- Send Message: `POST /messages/`
- Retrieve Conversations: `GET /messages/conversations/`

Hashtags and Tagging
- Retrieve Posts by Hashtag: `GET /posts/hashtags/{hashtag}/`
- Retrieve Posts by Mentions: `GET /posts/mentions/{username}/`

Trending Posts
- Retrieve Trending Posts: `GET /posts/trending/`

---

Models Overview

User Model
Custom User model with the following fields:
- `username` (unique)
- `email` (unique)
- `password`
- `bio`, `location`, `profile_picture`, `cover_photo` (optional fields)

Post Model
- `author`: ForeignKey to User.
- `content`: Text field for post content.
- `created_at`: Timestamp for post creation.
- `likes`: ManyToMany field to User.
- `shared_posts`: Related to reposts.
- `hashtags` and `tagged_users`: For tagging and hashtags.

Comment Model
- `post`: ForeignKey to Post.
- `author`: ForeignKey to User.
- `content`: Text field for the comment.

Notification Model
- `recipient`: ForeignKey to User.
- `type`: Notification type (like, comment, follow).
- `post`: ForeignKey (optional).
- `created_at`: Timestamp.

---

Testing

Testing with Postman
1. Import the provided Postman collection (`postman_collection.json`) into Postman.
2. Set up the environment with variables for:
   - `base_url`: The API base URL (e.g., `http://127.0.0.1:8000`).
   - `token`: Your JWT access token.

3. Test endpoints for creating posts, liking, commenting, tagging, and trending posts.

Future Improvements
- Enhance direct messaging with real-time WebSocket support.
- Improve hashtag suggestions based on trending tags.
- Add analytics for post engagements.



