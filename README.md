# Cloud-Based Smart Food Sharing & Donation Network

Runnable scaffold matching the chosen stack: FastAPI + PostgreSQL(PostGIS)/SQLite,
Bootstrap + Leaflet frontend, OR-Tools route optimization, AWS S3/RDS/SNS hooks.

Notifications and freshness AI are still stubbed (logged to console / placeholder
score) so you can run and demo the app before wiring up real AWS services — see
section 4. The database layer supports both SQLite and Postgres+PostGIS out of
the box; `app/database.py` auto-detects which one you're using from `DATABASE_URL`.

## 1. Backend — run locally

```bash
cd backend
python -m venv venv
venv\Scripts\activate          # Windows
pip install -r requirements.txt
copy .env.example .env         # Windows; edit values if needed
uvicorn app.main:app --reload
```

API docs (auto-generated): http://localhost:8000/docs
Tables are created automatically on first run.

**Database**: `.env.example` defaults to Postgres. If you have PostgreSQL +
PostGIS installed (see below), set your real password in `.env`:
```
DATABASE_URL=postgresql+psycopg2://postgres:YOUR_PASSWORD@localhost:5432/foodshare
```
and make sure the database + extension exist:
```sql
CREATE DATABASE foodshare;
\c foodshare
CREATE EXTENSION postgis;
```
Don't have Postgres set up yet? Just use SQLite instead — no setup needed:
```
DATABASE_URL=sqlite:///./foodshare.db
```
The app detects which one you're using automatically (nearby-search uses a real
`ST_DWithin` PostGIS query on Postgres, and falls back to a Python haversine
calculation on SQLite) — no code changes needed either way.

## 2. Frontend — run locally

No build step needed — plain HTML/JS. Easiest: open `frontend/index.html`
directly, or serve it so relative paths behave consistently:

```bash
cd frontend
python -m http.server 5500
```
Visit http://localhost:5500. `js/api.js` points at `http://localhost:8000` —
update `API_BASE` there when you deploy the backend.

## 3. Try it end-to-end

1. Sign up (`pages/signup.html`) as a donor.
2. Log in, go to **Donate Food**, click the map to set a pickup point, submit.
3. Open **Browse Nearby** (allow location access) — you should see the listing
   and be able to request it, which creates a match and logs a notification
   in the backend console.

## 4. Swapping in the real cloud pieces

| Component | Current (local) | Upgrade to |
|---|---|---|
| Database | Local Postgres or SQLite | Point `DATABASE_URL` in `.env` to your AWS RDS Postgres URL instead — same code path, `CREATE EXTENSION postgis;` on the RDS DB too |
| Photo storage | `photo_url` is a plain string field | Generate S3 presigned upload URLs via `boto3` in a new `/uploads` route, store the resulting S3 URL |
| Freshness AI | Random stub in `services/freshness_ai.py` | Train `ml/freshness_model.py` (needs `pip install tensorflow opencv-python-headless`), save the model, load it in the service |
| Notifications | Logged to console | Set `SNS_TOPIC_ARN` + AWS keys in `.env` — `services/notify.py` auto-switches to real SNS publishing |
| Route optimization | Already using real OR-Tools (falls back to nearest-neighbor if not installed) | No change needed |

## 5. Deploying

- **Frontend** → Vercel or Netlify (static hosting, set `API_BASE` to your live backend URL)
- **Backend** → `docker build -t foodshare-api backend/` then deploy to Render or EC2
- **Database** → AWS RDS (PostgreSQL, PostGIS extension enabled)

### Shutdown checklist (avoid AWS charges)
- Stop RDS instance when not developing (`aws rds stop-db-instance`) — re-stop weekly, it auto-restarts after 7 days
- Stop EC2 instance when idle
- Set an AWS Budgets alert (e.g. $5) as a safety net

## 6. What's left to build

- File upload endpoint for S3 (photo capture on the donate page)
- Delivery tracking UI page (`pages/track.html` — backend routes already exist under `/deliveries`)
- Admin/verification step before a listing goes live (currently auto-approved)
- Real freshness model training (dataset + `ml/freshness_model.py`)
- Alembic migrations (currently using `create_all` — fine for coursework, add Alembic before real users)
