# MATLAB Scientific Computing Academy

A public, responsive learning website for MATLAB fundamentals, numerical methods, computational physics, optics/photonics and optical instrumentation. The starter project includes eight lesson paths, two parameter-driven browser simulations, a Python API for named numerical models, deployment configuration, and a clear route toward licensed MATLAB execution.

> **Important:** The frontend's interactive models run their fixed mathematical formulas in the browser. The lesson code examples are MATLAB source text; they are not executed in the browser. The FastAPI backend provides specific, validated simulation endpoints and deliberately does not execute arbitrary submitted code.

## Project structure

```text
matlab-scientific-computing-academy/
├── frontend/                 # Next.js App Router + TypeScript
│   ├── app/
│   │   ├── page.tsx          # Academy homepage
│   │   ├── globals.css       # Responsive visual design
│   │   ├── simulations/      # Interactive simulation page
│   │   └── lessons/[slug]/   # Lesson template, statically generated
│   ├── components/SimulationLab.tsx
│   ├── lib/lessons.ts        # Eight lesson definitions
│   ├── package.json
│   └── .env.example
├── backend/                  # FastAPI + NumPy
│   ├── app/main.py           # Health, lesson metadata and simulation APIs
│   ├── requirements.txt
│   └── Dockerfile
├── content/lessons/          # Markdown lesson authoring area
└── docs/                     # Architecture and MATLAB execution notes
```

## Requirements

- Node.js 20 LTS or newer and npm
- Python 3.11+ (the included Docker image uses Python 3.12)
- Git (recommended)

## Run locally on Windows

Open **two** terminals in the project folder.

### 1. Start the Python API

```powershell
cd backend
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

If the `py` launcher is unavailable, use `python -m venv .venv` instead. If PowerShell blocks activation, run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` in that terminal, or invoke `.venv\Scripts\python.exe -m pip install -r requirements.txt` directly.

Test the API at `http://127.0.0.1:8000/health`; interactive API docs are at `http://127.0.0.1:8000/docs`.

### 2. Start the website

```powershell
cd frontend
npm install
Copy-Item .env.example .env.local
npm run dev
```

Open `http://localhost:3000`. The homepage and browser-based simulations work without an API connection; the backend is included for future live API-backed features.

### Production build check

```powershell
cd frontend
npm run build
npm run start
```

## Included pages

- `/` — Academy homepage and eight curriculum cards
- `/lessons/fundamentals`
- `/lessons/programming`
- `/lessons/numerical-methods`
- `/lessons/visualization`
- `/lessons/physics`
- `/lessons/optics`
- `/lessons/instrumentation`
- `/lessons/projects`
- `/simulations` — single-slit diffraction and trapezoidal integration
- `/api` — backend API when the Python service is running, not a Next.js page

## API endpoints

- `GET /health`
- `GET /api/lessons`
- `GET /api/examples/sine`
- `GET /api/examples/diffraction`
- `GET /api/examples/integration`
- `POST /api/simulate/diffraction`
- `POST /api/simulate/integration`

Example request:

```powershell
Invoke-RestMethod -Method Post -Uri http://127.0.0.1:8000/api/simulate/diffraction `
  -ContentType 'application/json' `
  -Body '{"wavelength_nm":550,"slit_width_um":50,"screen_distance_m":1,"points":401}'
```

The API validates numerical parameters and bounds response sizes. It is not a code runner and does not accept arbitrary MATLAB/Python scripts.

## Deploy to your personal domain

A simple production arrangement is **Vercel for the Next.js frontend** plus **Render, Railway, or a VPS for FastAPI**. Keep the frontend and backend as separate services.

### A. Push the project to GitHub

1. Create an empty GitHub repository.
2. From this project root run:

```bash
git init
git add .
git commit -m "Build MATLAB Scientific Computing Academy"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/matlab-scientific-computing-academy.git
git push -u origin main
```

Replace the example repository URL with your own.

### B. Deploy the API

For Render, create a **Web Service** from the same repository:

- Root directory: `backend`
- Runtime: Docker (uses `backend/Dockerfile`) or Python
- If using the Python runtime: build command `pip install -r requirements.txt`; start command `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- Set environment variable `CORS_ORIGINS` to your production frontend origin, for example `https://academy.yourdomain.com`, plus any required preview origin.
- After deploy, test `https://YOUR-API-HOST/health` and `https://YOUR-API-HOST/docs`.

For a non-Docker Python service, note that some providers set a dynamic `$PORT`; use the provider's required port variable. Do not put secrets in frontend environment variables.

### C. Deploy the frontend

1. Import the GitHub repository into Vercel.
2. Set **Root Directory** to `frontend`.
3. Add environment variable `NEXT_PUBLIC_API_URL=https://YOUR-API-HOST` (no trailing slash).
4. Deploy and check all lesson routes, responsive layout and browser console.

The current starter's interactive demonstrations run locally in the browser; the environment variable is provided for future API-connected features. If you add API calls to the frontend, ensure the backend CORS list includes the deployed frontend origin.

### D. Connect your existing domain

1. In Vercel, open the project **Settings → Domains** and add your chosen hostname, such as `academy.yourdomain.com`.
2. Follow the exact DNS records Vercel displays. A subdomain commonly uses a CNAME; an apex/root domain may require A/ALIAS records depending on the DNS provider.
3. In your domain registrar's DNS panel, add those records exactly. Remove conflicting records only after confirming they are not used by email or other services.
4. Wait for DNS propagation, then confirm Vercel reports the domain as configured and HTTPS is active.
5. If you want the academy on the root domain rather than a subdomain, configure that explicitly in Vercel and preserve existing mail-related MX/TXT records.

Do not share domain registrar passwords or API keys. DNS setup values differ by domain and hosting configuration, so use the values shown in your actual hosting dashboard rather than copying generic IP addresses from a tutorial.

## Content editing

Lesson content is defined in `frontend/lib/lessons.ts`. Each lesson has an intro, learning objectives, explanation, MATLAB code example, short self-check and application note. Edit those fields to add content. Add a new slug to the `lessons` object and its `next` link if needed. `generateStaticParams()` creates static lesson pages at build time.

Markdown source drafts can be stored in `content/lessons/`; the live site currently uses the TypeScript lesson definitions so it does not need a CMS or database.

## Adding real MATLAB execution later

See [`docs/matlab-execution.md`](docs/matlab-execution.md). Do not run arbitrary learner code inside the Next.js process or an ordinary shared web worker. Use a licensed MATLAB execution environment or a vendor-supported online service, authentication/quotas where required, isolated jobs, time and memory limits, audit logs, and an explicit terms-of-use notice.

## Current MVP limitations

- No student login or progress persistence (as requested: public access, no account required).
- No arbitrary live MATLAB execution; code examples are educational source text.
- Browser simulations are teaching models, not validated engineering design software or clinical tools.
- No CMS yet; lesson content is version-controlled in TypeScript.
- Add monitoring, rate limiting, backups, accessibility review and automated tests before broad production use.

## License and trademark

Choose and add an explicit license before redistributing the project. MATLAB is a registered trademark of The MathWorks, Inc.; this independent learning project is not affiliated with or endorsed by MathWorks.
