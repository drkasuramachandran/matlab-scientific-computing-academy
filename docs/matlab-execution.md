# Pathway to genuine MATLAB execution

The first release deliberately combines MATLAB code examples with safe, named simulations. There is no supported browser-only mechanism that turns MATLAB source into native MATLAB execution without an execution environment.

## Recommended options to evaluate

1. **MathWorks-supported cloud execution or MATLAB Online integration** — confirm current product availability, embedding/integration capabilities, user authentication model, usage terms and commercial/educational licensing directly with MathWorks.
2. **MATLAB Production Server** — for a licensed deployment of published MATLAB functions behind an API. It is generally designed for production deployment of packaged functions, not as an unrestricted interactive script sandbox.
3. **Institution-hosted MATLAB workers** — a licensed MATLAB installation runs only a reviewed set of jobs in isolated worker processes or containers, with quotas, job queues and strict input schemas.

## Safe staged implementation

- Stage 1: provide editable code examples and browser simulations (current MVP).
- Stage 2: add a “Run example” API that accepts a known example ID and validated numeric parameters, not arbitrary source text.
- Stage 3: connect those IDs to pre-approved MATLAB functions on a licensed backend.
- Stage 4: only if there is a strong educational need, evaluate sandboxed arbitrary-code execution with per-user authentication, quotas, process isolation, network restrictions, filesystem restrictions, CPU/memory/time limits and a security review.

Never expose MATLAB credentials or license server details in browser JavaScript. Do not accept arbitrary uploaded `.m` files and execute them on the web server. MATLAB code can read files, call system functions or consume excessive resources; the runtime must be isolated and monitored.

## API contract suggestion

`POST /api/matlab/run-example` should initially accept `{ "example_id": "single_slit", "parameters": { "wavelength_nm": 550, "slit_width_um": 50 } }`. The server maps the ID to a pre-approved function, validates the allowed parameter names/ranges, queues a bounded job, and returns structured numerical output. It should not accept a raw `code` string.
