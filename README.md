# Greenthreads Thrift Shop

A Django-based thrift shop website with MongoDB Atlas integration.

## Features

- User authentication with Google OAuth
- Item listing with MongoDB Atlas backend
- Search functionality
- CRUD operations for items
- Responsive UI

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set up MongoDB Atlas

1. Create a [MongoDB Atlas](https://www.mongodb.com/cloud/atlas) account
2. Create a new cluster
3. Get your connection string (Click "Connect" > "Connect your application")
4. Create a `.env` file in the project root with:

```
# Django settings
SECRET_KEY=your_secret_key
DEBUG=True

# MongoDB Atlas Settings
MONGODB_URI=your_mongodb_atlas_uri
MONGODB_DB=items_db

# Google OAuth
OAUTH_GOOGLE_CLIENT_ID=your_google_client_id
OAUTH_GOOGLE_SECRET=your_google_client_secret
```

### 3. Run Migrations

```bash
python manage.py migrate
```

### 4. Run the Development Server

```bash
python manage.py runserver
```

## Usage

1. Visit `http://localhost:8000/` in your browser
2. Sign up or login
3. Browse items or add your own items for sale
4. Use the search bar to find specific items

## Project Structure

- `project/` - Main Django project settings
- `users/` - User authentication app
- `items/` - Item management app with MongoDB Atlas integration
- `templates/` - HTML templates for the application

## MongoDB Atlas Integration

This project uses MongoDB Atlas for storing item data. The connection is handled by the `pymongo` library. See `items/db.py` for connection details. 