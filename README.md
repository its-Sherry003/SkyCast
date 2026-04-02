# SkyCast

SkyCast is a cloud-based weather application that provides users with real-time weather information for any location worldwide. The application allows users to enter a city name and instantly receive details such as temperature, weather conditions, and humidity.

A Flask weather application deployed on Railway PaaS.
Searches real-time weather via OpenWeatherMap API and saves history to a MySQL database.

---

## Features

- Search weather by city name
- Save search history to MySQL (full CRUD)
- Delete individual history records
- Deployed on Railway with CI/CD via GitHub

---

## Tech Stack

- **Backend:** Python Flask
- **Database:** MySQL (Railway-managed) via SQLAlchemy
- **API:** OpenWeatherMap
- **Deployment:** Railway PaaS
- **Server:** Gunicorn

---

## Local Setup

### 1. Clone the repo

```bash
git clone https://github.com/its-Sherry003/SkyCast.git
cd SkyCast
```

### 2. Create virtual environment

```bash
python -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set environment variables

```bash
cp .env.example .env
# Edit .env and fill in your API key and DB URL
```

### 5. Run locally

```bash
python app.py
```

Visit http://localhost:5000

---

## Railway Deployment

### Step 1 — Create Railway account

Go to https://railway.app and sign up with GitHub.

### Step 2 — New Project

- Click **New Project** → **Deploy from GitHub repo**
- Select this repository

### Step 3 — Add MySQL Database

- In your Railway project, click **+ New** → **Database** → **MySQL**
- Railway provisions it automatically

### Step 4 — Set Environment Variables

In Railway → your Flask service → **Variables**, add:

```
OPENWEATHER_API_KEY = your_key_here
DATABASE_URL        = mysql+pymysql://user:pass@host:port/railway
```

(Copy DATABASE_URL from the MySQL service's **Connect** tab — use the internal URL)

### Step 5 — Deploy

Railway auto-deploys on every push to your main branch.

---

## Environment Variables

| Variable              | Description                  |
| --------------------- | ---------------------------- |
| `OPENWEATHER_API_KEY` | Your OpenWeatherMap API key  |
| `DATABASE_URL`        | Full MySQL connection string |
| `PORT`                | Auto-set by Railway          |

---

## API Endpoints

| Method | Endpoint        | Description                 |
| ------ | --------------- | --------------------------- |
| GET    | `/`             | Homepage                    |
| POST   | `/weather`      | Search weather + save to DB |
| GET    | `/history`      | Get all search history      |
| PUT    | `/history/<id>` | Update a record             |
| DELETE | `/history/<id>` | Delete a record             |

---

## Getting OpenWeatherMap API Key

1. Go to https://openweathermap.org/api
2. Sign up for a free account
3. Go to **API Keys** tab
4. Copy your default key (free tier allows 60 calls/minute)
