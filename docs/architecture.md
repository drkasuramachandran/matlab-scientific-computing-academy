# Architecture notes

- **Next.js App Router + TypeScript:** public pages and statically generated lesson routes.
- **Browser simulation layer:** immediate parameter changes, SVG charts and no server execution required.
- **FastAPI + NumPy:** named, bounded calculation endpoints and API docs.
- **Content:** version-controlled lesson definitions; no user accounts or database in the initial release.
- **Hosting:** deploy frontend and backend independently; set CORS to the exact frontend origin.

Keep scientific models explicit about units, assumptions, approximation range and validation status. For future production deployment add automated tests for equations and parameter bounds, API rate limits, structured logs, monitoring, and accessibility checks.
