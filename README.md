# Parma workers

Local source copy of the existing Kapitalist HTTP worker on Parma. Imported on November 25, 2026 from `/home/segvan/workers/` into `C:\d\Code\workers\`. The four imported files are unchanged; their SHA-256 hashes match the server originals. No production schedule was changed. Git was subsequently initialized locally on November 25, 2026, with main as the initial branch; no remote or initial commit was created.

## Files and current behavior

| File | Purpose |
| --- | --- |
| `kapitalist_job.py` | Calls the three Kapitalist endpoints below. |
| `run_kapitalist_job.sh` | Changes working directory, acquires a lock, runs Python through uv, and appends output to a log. |
| `pyproject.toml` | Declares Python >=3.13 and dependencies on requests and python-dotenv. |
| `uv.lock` | Imported dependency resolution; preserve it for reproducible setup. |
| `AGENTS.md` | Instructions for AI agents working in this folder. |

Each invocation sends these requests sequentially, without a request body:

1. `POST http://localhost:30003/api/cron/btc-data`
2. `POST http://localhost:30003/api/cron/price-change-alert`
3. `POST http://localhost:30003/api/cron/portfolio-sync`

All requests include `x-api-key` from `API_KEY` and `Content-Type: application/json`. Each uses `requests.post(..., timeout=30)`. This timeout controls connection/read waits, not a strict total invocation deadline. Each completed response prints its URL and HTTP status.

There is no configurable endpoint list, per-endpoint frequency, retry policy, or persisted scheduling state. HTTP 4xx/5xx responses are printed but do not raise an error or stop later requests. A connection error or timeout raises an uncaught exception and prevents remaining endpoints from running. Earlier requests may already have caused side effects; do not blindly rerun the entire worker after a failure.

## Prerequisites

Production execution requires Linux, Bash, `/usr/bin/flock` (util-linux), uv, Python >=3.13, and a reachable Kapitalist service on localhost port 30003. Cron is needed for recurring execution. An authorized Kapitalist API key must be provisioned privately.

Windows is suitable for editing and Python dependency setup. The imported shell wrapper is Linux-specific and contains absolute Parma paths. Do not run it from WSL or Git Bash expecting it to use this Windows directory. Running the Python entrypoint also sends real requests to the machine where it executes.

## Install uv and Python

These are operator instructions for a new environment, not commands executed during the import. Installing software or changing the production host requires authorization.

Linux, following the [official uv installer documentation](https://docs.astral.sh/uv/getting-started/installation/):

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Windows PowerShell alternative:

```powershell
winget install --id astral-sh.uv --exact
```

Open a fresh terminal if needed, then verify and install Python:

```text
uv --version
uv python install 3.13
```

The project permits newer Python versions as well; 3.13 is a compatible setup default, not a verified production interpreter version. The wrapper expects uv specifically at `/home/segvan/.local/bin/uv`. Check that location when preparing a host; an installation under another account or location will not satisfy the hard-coded path.

## Restore locked dependencies

On Windows, start in `C:\d\Code\workers`. On Parma, the corresponding source directory is `/home/segvan/workers`.

```text
uv sync --locked --python 3.13
```

This prepares the project virtual environment using the existing lockfile. It does not run the worker. If the lockfile and project metadata disagree, investigate rather than regenerating the imported lockfile automatically. See [uv locking and syncing](https://docs.astral.sh/uv/concepts/projects/sync/).

The existing wrapper uses plain `uv run`, which may synchronize dependencies or update the lockfile when needed. Its behavior has been preserved; the setup command above does not make the wrapper enforce locked execution.

## Private API key configuration

`kapitalist_job.py` invokes `load_dotenv()` and reads the `API_KEY` environment variable. Missing or empty configuration raises `RuntimeError("API_KEY not set in environment")` before sending requests. An existing process environment value normally takes precedence over dotenv values.

The operator must provision the real key locally on the execution host, either in the worker process environment or in a private `.env` file in the worker directory. The file format is a single assignment named `API_KEY`; obtain its real value from the existing private configuration. Do not put the value in this README, command history, cron arguments, source control, chat, or logs. Restrict a privately provisioned file to its owner, for example with mode 600 on Linux.

No private configuration was copied. Agents must not read, copy, create, or load private environment files. A normal interactive-shell export does not automatically configure cron; cron must receive configuration independently, or the script must find the privately provisioned dotenv file. The wrapper changes to `/home/segvan/workers` before invoking Python.

## Wrapper paths and manual execution

The unchanged wrapper sets:

| Setting | Existing value |
| --- | --- |
| Working directory | `/home/segvan/workers` |
| uv executable | `/home/segvan/.local/bin/uv` |
| Lock file | `/tmp/kapitalist_job.lock` |
| Output log | `/home/segvan/workers/kapitalist_job.log` |

It uses `set -euo pipefail` and invokes:

```bash
/usr/bin/flock -n -w 1 "$LOCKFILE" "$UV_BIN" run python kapitalist_job.py >> "$LOGFILE" 2>&1
```

The lock covers the Python process and protects wrapper invocations from overlapping. The existing flags combine a nonblocking request (`-n`) and a one-second timeout (`-w 1`); their runtime interaction was not tested during this import. A lock acquisition failure prevents that invocation from running. Calling Python directly bypasses this lock. Do not delete an active lock file to force another run.

Only after authorization to call the production endpoints, an operator can run:

```bash
/home/segvan/workers/run_kapitalist_job.sh
```

If preparing a fresh Linux copy, executable permission may need to be set with `chmod u+x /home/segvan/workers/run_kapitalist_job.sh`. This import did not change server permissions.

For an explicitly authorized direct diagnostic run:

```bash
cd /home/segvan/workers
/home/segvan/.local/bin/uv run --locked python kapitalist_job.py
```

This sends real POST requests, bypasses wrapper locking, and writes output to the terminal instead of the wrapper log. Do not run alongside cron. Neither entrypoint has a dry-run mode.

## Cron configuration

Verified November 25, 2026 in segvan's user crontab:

```cron
1-56/5 * * * * /home/segvan/workers/run_kapitalist_job.sh
```

This runs at minutes 01, 06, 11, 16, 21, 26, 31, 36, 41, 46, 51, and 56 of every hour, according to cron's configured timezone. The import did not verify the host timezone or recent execution success. User crontab entries have five schedule fields followed by the command, with no username field.

To configure a new installation, an authorized operator should confirm the paths, dependencies, private key configuration, executable permission, and cron service first. Review the existing user crontab with `crontab -l`, preserve unrelated entries, and use `crontab -e` as segvan to add or replace the intended entry. Do not add a duplicate or replace the entire crontab with a one-line command.

A future, separate Parma runner is proposed to run every minute:

```cron
# FUTURE EXAMPLE ONLY: this script does not exist yet. Do not install this line.
* * * * * /home/segvan/workers/run_parma_job.sh
```

Keep the Kapitalist schedule unchanged. Do not configure the same endpoint in both workers without an explicit migration plan.

## Logging and troubleshooting

The wrapper appends stdout and stderr to `kapitalist_job.log`. Python output redirected to a file can be buffered. Existing entries contain URL/status lines and exception tracebacks; they do not provide reliable execution timestamps, durations, or structured history. Log rotation and retention are not implemented by these source files; external rotation was not inspected. No production logs were copied or read during this import.

| Symptom | Check |
| --- | --- |
| API_KEY missing | Operator verifies private provisioning and the execution working directory without printing the value. |
| uv not found | Check the wrapper's absolute uv path and the execution account. |
| Dependency or Python failure | Restore with `uv sync --locked --python 3.13`; inspect metadata compatibility without regenerating the lockfile. |
| Connection refused or timeout | Verify the intended local service and port; determine which earlier requests completed before retrying. |
| HTTP 401/403 | Operator checks API key validity and endpoint authorization; status alone does not make the worker fail. |
| No new log output | Check cron service/account/schedule, path permissions, possible lock contention, and output buffering. |
| Wrapper exits without requests | Inspect a bounded, sanitized diagnostic and exit status; check lock acquisition and uv startup. |

Authorized operators may inspect a bounded tail of the log locally. Do not upload raw logs or configuration. Disk growth must be considered before introducing new recurring jobs; this import adds no rotation policy.

## Safe verification

Syntax checks do not execute endpoint calls:

```bash
bash -n run_kapitalist_job.sh
python -c 'import ast, pathlib; ast.parse(pathlib.Path("kapitalist_job.py").read_text())'
```

Do not import `kapitalist_job.py` for a check: its module-level code loads private configuration. Do not use `uv run kapitalist_job.py --help` as a check; the script has no argument parser and will still make requests.

At import, Bash syntax passed on Parma and all four copied source hashes matched. Production request success, dependency installation, and cron execution were not tested. Source hashes were rechecked locally after documentation was added.

## Future work

Add a separate `parma_job.py` and wrapper when requested, preserving the existing Kapitalist worker. Configurable endpoints, frequencies, pause/remove controls, shared runtime storage, and console log viewing remain design work. No new worker, console integration, deployment, or cron modification is included in this source import. Local Git initialization was completed separately on November 25, 2026.
