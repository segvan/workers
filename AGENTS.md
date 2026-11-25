# Workers instructions for AI agents

## Purpose and scope

This folder contains an unchanged source copy of Parma's existing production Kapitalist HTTP worker, imported November 25, 2026. Read README.md and the relevant source before changing behavior. Git was initialized locally on November 25, 2026 with main as the initial branch. No remote or initial commit was created during initialization.

Future configurable scheduling belongs in a separate parma_job.py and run_parma_job.sh when authorized. Preserve kapitalist_job.py, run_kapitalist_job.sh, and the existing Kapitalist cron schedule unless the user explicitly requests changes to them. Console integration belongs to C:\d\Code\parma and must follow that repository's AGENTS.md.

## Source layout

- kapitalist_job.py: sequential POST requests to three localhost:30003 endpoints; loads private configuration at module import.
- run_kapitalist_job.sh: Linux-only absolute paths, flock, uv invocation, and appended stdout/stderr.
- pyproject.toml: Python >=3.13, requests, and python-dotenv.
- uv.lock: imported locked dependency resolution; preserve unless a dependency change is requested.
- README.md: setup, configuration, observed cron schedule, behavior, and limitations.

## Development workflow

1. Inspect the source and README; distinguish local Windows paths from live Linux paths.
2. Make only requested changes. Keep setup instructions aligned with actual code, and date production observations.
3. Preserve LF line endings and source bytes during imports. Do not apply automatic formatting to imported originals.
4. For approved dependency setup, use uv sync --locked with a compatible Python version. Do not regenerate uv.lock to silence errors. Do not install software on Parma as part of local development.
5. Use static validation first. Add focused isolated tests for consequential future behavior, with mocked HTTP and temporary configuration. Never target production endpoints in tests.
6. Report what was checked and which operational behavior remains unverified.

## Safe verification

- Bash syntax: bash -n run_kapitalist_job.sh. Do not invoke the wrapper.
- Python syntax: parse the source with ast.parse; never import it for validation because module-level load_dotenv() loads private configuration.
- Dependency metadata can be inspected without importing the worker.
- Neither script supports a dry run. Passing --help to the worker does not stop real HTTP requests.
- Do not run uv run python kapitalist_job.py, the wrapper, or a test that calls real endpoints without explicit authorization for those requests.
- Locking, HTTP error behavior, and cron success are separate from syntax validation; do not claim them verified from static checks.

## Secrets and runtime data

Never read, print, copy, edit, load, or commit private environment files, credentials, keys, raw production logs, or secret-bearing process environments. Have the user provision required secrets locally. Use synthetic values and isolated configuration for tests. Never put API keys in README examples, shell command arguments, command history, or cron entries.

Keep .env files, virtual environments, caches, logs, lock files, and future runtime configuration/state out of source control. Maintain .gitignore exclusions before staging anything; keep uv.lock tracked as dependency metadata. Do not copy an entire server directory recursively without a reviewed source allowlist or exclusions.

## Production boundaries

Source access is not deployment authorization. Obtain explicit authorization before production endpoint calls, installing dependencies on Parma, uploading/deploying files, changing cron, enabling recurring execution, changing permissions, restarting services, or making other production changes. Use authorization already provided for the specific action.

For authorized live Parma work, read the Galaxy Raspberry Pi instructions and use its Parma SSH skill and visible shared terminal:
C:\Users\strot\OneDrive\Cloud Documents\galaxy\raspberrypi\AGENTS.md
C:\Users\strot\OneDrive\Cloud Documents\galaxy\.agents\skills\parma-ssh\SKILL.md

Begin with scoped read-only checks. Preserve unrelated cron entries, secrets, logs, and existing worker behavior. Before a production change, establish impact, validation, and rollback. Avoid duplicate endpoint schedules. Do not assume a saved cron reference proves current execution health.
