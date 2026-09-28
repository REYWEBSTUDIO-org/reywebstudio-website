# 🚀 Rey Web Studio — Full-Stack Platform

> **Brand:** Rey Web Studio  
> **Tagline:** Crafting Your Digital Presence  
> **Visual Identity:** Dark charcoal background (`#0B0E12`), sophisticated gold accents (`#C7A04D` / `#E3C069`), editorial typography (*Fraunces* serif & *Poppins* sans-serif), clean layout spacing, and subtle micro-interactions.

---

## 📖 Overview

**Rey Web Studio** is a full-stack digital studio web platform featuring:
- **Public Creative Studio Frontend:** High-converting portfolio showcasing bespoke web builds, services, client testimonials, and an integrated inquiry contact form.
- **Enterprise-Grade FastAPI Backend:** High-performance RESTful API powered by Python 3, SQLAlchemy ORM, Pydantic data validation, bcrypt password hashing, and JWT bearer authentication.
- **Dual-Engine Database Layer:** Native support for **PostgreSQL** in production with automatic fallback to **SQLite** for instant zero-configuration local development.
- **Hybrid Contact & Lead Pipeline:** Public inquiries are validated and permanently archived in the database before triggering client-side notifications via EmailJS.
- **Dynamic Project Portfolio Engine:** Projects are stored, filtered, categorized, and served dynamically via REST APIs without hardcoded limitations.
- **Integrated Admin Management Console (`/admin.html`):** A secure, authenticated dashboard for real-time lead tracking, status lifecycle management, and full project CRUD operations.

---

## 🛠️ Technology Stack

| Layer | Technologies |
| :--- | :--- |
| **Frontend** | HTML5 Semantic Architecture, Vanilla CSS3 (Custom Design System), Vanilla ES6+ JavaScript |
| **Backend Framework**| Python 3.14, [FastAPI](https://fastapi.tiangolo.com/), [Uvicorn](https://www.uvicorn.org/) (ASGI Server) |
| **Database & ORM** | [SQLAlchemy 2.0+](https://www.sqlalchemy.org/) ORM, PostgreSQL (via `psycopg2` / `psycopg3`), SQLite |
| **Data Validation** | [Pydantic v2](https://docs.pydantic.dev/) & `email-validator` |
| **Security & Auth** | JWT (JSON Web Tokens via `PyJWT`), `bcrypt` password hashing, HTTPBearer Auth |
| **Notifications** | EmailJS Client SDK (guarded with graceful network fallback) |

---

## 📐 System Architecture & Data Flow

```text
                                 PUBLIC FRONTEND
               ┌─────────────────────────────────────────────────┐
               │  Inquiry Form: Name, Email, Project Message      │
               └───────────────────────┬─────────────────────────┘
                                       │
                         1. POST /api/leads (JSON)
                                       │
                                       ▼
                             FASTAPI BACKEND
               ┌─────────────────────────────────────────────────┐
               │  • Pydantic Schema Validation                   │
               │  • SQLAlchemy ORM Persistence                   │
               └───────────────────────┬─────────────────────────┘
                                       │
                         2. Persist Lead to Database
                                       │
                                       ▼
                             POSTGRESQL / SQLITE
               ┌─────────────────────────────────────────────────┐
               │  Table: leads (status: 'new', timestamps)       │
               └───────────────────────┬─────────────────────────┘
                                       │
                         3. HTTP 201 Created Response
                                       │
                                       ▼
                              EMAILJS TRIGGER
               ┌─────────────────────────────────────────────────┐
               │  Dispatches instant email alert to studio inbox  │
               └─────────────────────────────────────────────────┘
```

---

## 🗄️ Database Models

### 1. `AdminUser` (`admin_users`)
| Column | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | Integer | Primary Key, Autoincrement | Unique Admin ID |
| `username` | String(50) | Unique, Index, Not Null | Admin handle for authentication |
| `email` | String(100) | Unique, Index, Not Null | Admin email address |
| `password_hash`| String(255)| Not Null | `bcrypt` cryptographic salt & hash |
| `is_active` | Boolean | Default: `True` | Account operational status |
| `created_at` | DateTime | Default: `utcnow` | Account creation timestamp |

### 2. `Lead` (`leads`)
| Column | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | Integer | Primary Key, Autoincrement | Unique Lead ID |
| `name` | String(100)| Not Null | Client full name |
| `email` | String(100)| Index, Not Null | Client email address |
| `message` | Text | Not Null | Project inquiry specifications |
| `status` | String(20) | Default: `'new'`, Index | Lifecycle: `new`, `contacted`, `qualified`, `converted`, `closed` |
| `created_at` | DateTime | Default: `utcnow` | Submission timestamp |
| `updated_at` | DateTime | Auto-updating | Timestamp of last lifecycle update |

### 3. `Project` (`projects`)
| Column | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | Integer | Primary Key, Autoincrement | Unique Project ID |
| `title` | String(150)| Not Null | Project title (e.g. *Gym Website*) |
| `description` | Text | Not Null | Executive summary / scope |
| `image_url` | String(500)| Not Null | Remote or hosted showcase asset URL |
| `live_url` | String(500)| Nullable | Optional live URL / demo endpoint |
| `category` | String(50) | Default: `'Web Design'` | Category (*Business Website*, *Portfolio*, *E-commerce*, etc.) |
| `featured` | Boolean | Default: `False` | Showcase highlight status |
| `created_at` | DateTime | Default: `utcnow` | Project upload timestamp |
| `updated_at` | DateTime | Auto-updating | Timestamp of last modification |

---

## 🌐 API Reference

### 1. Authentication
- `POST /api/auth/login`
  - **Access:** Public
  - **Body:** `{ "username": "admin", "password": "password" }`
  - **Returns:** `{ "access_token": "<jwt>", "token_type": "bearer" }`
- `GET /api/auth/me`
  - **Access:** Admin (Bearer JWT required)
  - **Returns:** Current authenticated admin user details

### 2. Lead Management
- `POST /api/leads`
  - **Access:** Public (Used by frontend contact form)
  - **Body:** `{ "name": "Jane", "email": "jane@example.com", "message": "Website build inquiry" }`
  - **Returns:** HTTP 201 Created with saved Lead record
- `GET /api/leads?search=<query>&status=<status>`
  - **Access:** Admin (Bearer JWT required)
  - **Returns:** Array of matching leads sorted chronologically
- `GET /api/leads/{id}`
  - **Access:** Admin (Bearer JWT required)
  - **Returns:** Single lead details
- `PUT /api/leads/{id}`
  - **Access:** Admin (Bearer JWT required)
  - **Body:** `{ "status": "contacted" | "qualified" | "converted" | "closed" }`
  - **Returns:** Updated lead record
- `DELETE /api/leads/{id}`
  - **Access:** Admin (Bearer JWT required)
  - **Returns:** HTTP 204 No Content

### 3. Dynamic Projects
- `GET /api/projects?category=<category>&featured=<bool>`
  - **Access:** Public
  - **Returns:** Array of project records
- `GET /api/projects/{id}`
  - **Access:** Public
  - **Returns:** Project record details
- `POST /api/projects`
  - **Access:** Admin (Bearer JWT required)
  - **Body:** `{ "title": "...", "description": "...", "image_url": "...", "live_url": "...", "category": "...", "featured": true }`
  - **Returns:** HTTP 201 Created with new Project record
- `PUT /api/projects/{id}`
  - **Access:** Admin (Bearer JWT required)
  - **Returns:** Updated Project record
- `DELETE /api/projects/{id}`
  - **Access:** Admin (Bearer JWT required)
  - **Returns:** HTTP 204 No Content

### 4. Real-Time Analytics
- `GET /api/analytics/overview`
  - **Access:** Admin (Bearer JWT required)
  - **Returns:**
    ```json
    {
      "total_leads": 2,
      "new_leads": 1,
      "contacted_leads": 0,
      "qualified_leads": 1,
      "converted_leads": 0,
      "closed_leads": 0,
      "total_projects": 4
    }
    ```

---

## 🔐 Default Admin Credentials

To access the Admin Management Console (`/admin.html`):

- **URL:** [http://127.0.0.1:8000/admin.html](http://127.0.0.1:8000/admin.html)
- **Username:** `admin`
- **Password:** `password`

*(Default credentials can be configured at any time in the `.env` file).*

---

## ⚡ Quick Start & Running Locally

### Prerequisites
- Python 3.10+ (Tested on Python 3.14)
- (Optional) PostgreSQL server running locally or remotely

### 1. Clone & Navigate
```bash
cd "c:\Users\Fayaz\OneDrive\Desktop\reywebdesign\reywebstudio-website-main"
```

### 2. Activate Virtual Environment
```powershell
.\venv\Scripts\Activate.ps1
```

### 3. Install Dependencies (if creating a new environment)
```bash
pip install fastapi "uvicorn[standard]" sqlalchemy psycopg2-binary psycopg[binary] pydantic PyJWT bcrypt python-dotenv email-validator httpx
```

### 4. Database Setup & Seeding
The database tables, default admin, and default portfolio projects are automatically initialized on startup! To manually trigger seeding:
```bash
python -m backend.seed
```

### 5. Launch the Server
```bash
python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload
```

- Public Website: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- Admin Console: [http://127.0.0.1:8000/admin.html](http://127.0.0.1:8000/admin.html)
- Interactive API Docs (Swagger): [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- Alternative API Docs (ReDoc): [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## ☁️ Production Deployment (Render)

The FastAPI application serves the public website, `admin.html`, and the API from one origin. Deploy the repository as a single Render Web Service and connect it to a Render PostgreSQL database.

### 1. Push the Project to GitHub

Commit and push the project to a GitHub repository. Keep `backend/` and `frontend/` in the repository root. The public site, admin page, styles, scripts, verification HTML, and `assets/` directory belong inside `frontend/`.

### 2. Create a PostgreSQL Database

Create a PostgreSQL database in Render and copy its **internal database URL**. Use the internal URL when the Web Service and database are in the same Render region.

### 3. Create a Web Service

In Render, create a Web Service from the GitHub repository. Set the root directory to the repository root and use these commands:

**Build command**

```sh
pip install fastapi "uvicorn[standard]" sqlalchemy psycopg2-binary psycopg[binary] pydantic PyJWT bcrypt python-dotenv email-validator httpx
```

**Start command**

```sh
python -m uvicorn backend.main:app --host 0.0.0.0 --port $PORT
```

### 4. Configure Environment Variables

Add these in the Web Service's environment settings:

| Variable | Value |
| :--- | :--- |
| `DATABASE_URL` | The PostgreSQL internal database URL from Render |
| `JWT_SECRET_KEY` | A unique, randomly generated secret; do not reuse the development value |
| `ADMIN_DEFAULT_USERNAME` | Your chosen administrator username |
| `ADMIN_DEFAULT_PASSWORD` | A unique, strong administrator password |

Set the admin username and password before the first deployment. Startup creates the initial admin account only if that username does not already exist; changing the environment variables later does not change an existing account's password.

### 5. Verify the Deployment

After deployment, open the service URL:

- Public website: `https://<your-service>.onrender.com/`
- Admin console: `https://<your-service>.onrender.com/admin.html`
- API documentation: `https://<your-service>.onrender.com/docs`

Check the service logs for `[DATABASE] Connected to PostgreSQL successfully.` The current database layer falls back to a local SQLite file if PostgreSQL connection fails. Do not treat deployment as production-ready if the logs show that fallback warning; SQLite files on hosted instances may not be durable across restarts or instance replacement.

The site and API use same-origin URLs, so a separate frontend deployment or CORS configuration is not required for this setup. EmailJS continues to send client-side notifications using the existing frontend configuration.

---

## 🛡️ Critical Bug Prevention Enforced

In compliance with project specifications:
1. **Isolated Project & Lead Management:** Project CRUD operations and lead lifecycle functions are strictly separated in `admin.html`:
   - Projects: `createProject()`, `editProject(id)`, `saveProject(e)`, `deleteProject(id)`.
   - Leads: `loadLeads()`, `updateLeadStatus(id, status)`, `deleteLead(id)`.
   - The project modal submit button strictly executes `saveProject(e)`, guaranteeing that project data is never mistakenly sent to lead endpoints.
2. **EmailJS Coexistence:** EmailJS remains operational alongside the primary PostgreSQL persistence layer. Submitting the public contact form safely commits the inquiry to the database first, followed by EmailJS client dispatch.

---

## 🧪 Local Verification

The repository does not currently include an automated test suite. From the project root, run these syntax checks:

```powershell
.\venv\Scripts\python.exe -m compileall -q backend
node --check frontend/script.js
```

For an HTTP smoke test, start the server with the command in **Quick Start** and check that `/`, `/admin.html`, `/docs`, and `/api/projects` load. Sign in through `/admin.html` to verify the admin login and dashboard. Avoid using write operations against production data when smoke-testing.
