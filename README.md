# Online Newspaper Web Application

## Overview

This project is a modern online newspaper platform featuring news articles, analytics, thematic categories, and archive access. It supports personalized news feeds, subscriptions, comments, and notifications.

Built with a clean architecture leveraging design patterns (GoF) and best coding practices, it provides extensibility, maintainability, and scalability.

---

## Features

- **News Feed**
  - Homepage displays latest and recommended articles.
  - Thematic categories such as Politics, Economy, Culture, Sports, Technology.
  - Advanced search with filters by keywords, authors, and date.
  
- **User Personalization**
  - Favorite topics and categories settings.
  - Recommendation system based on views and likes.
  
- **User Profiles**
  - Subscription to newsletters and push notifications.
  - Commenting and rating articles.
  - Articles saved for later reading.
  
- **Subscription System**
  - Free access with ads.
  - Paid subscriptions with ad-free experience and exclusive articles.
  - Special packages for students.
  
- **Notification System**
  - Breaking news alerts.
  - Daily news digests.
  - Notifications on new articles by favorite authors.

---

## Technology Stack

- **Frontend:** Svelte 5 + SvelteKit
- **Backend:** Python Flask with Dependency Injection (DI)
- **Database:** SQLite (with potential PostgreSQL support)
- **API:** RESTful endpoints
- **Authentication:** JWT (JSON Web Tokens)
- **Design Patterns:** Singleton, Factory, Observer, Strategy, Facade
  
---

## Architecture

- Separation of concerns with layers:
  - Models (SQLAlchemy ORM)
  - Repository layer for data access abstraction
  - Services encapsulating business logic
  - Controllers / Blueprints handling HTTP requests
- Dependency Injection container for flexible component resolution.
- Background tasks for notification delivery and digest generation.

---

## Setup & Installation

### Backend Setup

1. Clone repository:

```
git clone https://github.com/OleksiuDatsko/news.git
cd backend
```

2. Create and activate virtual environment:

```
python -m venv venv
source venv/bin/activate 
```

3. Install Python dependencies:

```
pip install -r requirements.txt
```

4. Create `.env` file based on `.env.example` and configure environment variables (e.g., `DATABASE_URL`, `JWT_SECRET_KEY`).

5. Start backend server:

```
python app.py
```

#### Admin Login
email: admin@some.com
password: admin

### Frontend Setup

1. Install dependencies:

```
yarn
```

2. Run development server:

```
yarn run dev
```


