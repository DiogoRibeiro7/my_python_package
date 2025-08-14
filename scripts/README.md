# pyproject-up

Automate safe edits to `pyproject.toml` and keep dependency constraints fresh.

This repo contains two small, typed CLIs and two GitHub Actions:

* `scripts/pyproject_editor.py` — **edit** fields deterministically (version bumps, deps, Python range) while preserving comments.
* `scripts/pyproject_updater.py` — **upgrade** dependency constraints to latest releases from PyPI with strategies (caret/tilde/exact/floor).
* `.github/workflows/auto-pyproject-update.yml` — bump project version on pushes (commit-message driven major/minor/patch).
* `.github/workflows/auto-upgrade-pyproject.yml` — weekly PR to raise dependency constraints to current PyPI releases.

Both CLIs support **Poetry layout** (`[tool.poetry]`) and **PEP 621** (`[project]`). Formatting and comments are preserved via `tomlkit`.

---

## Quick start

```bash
# Clone and enter the repo
git clone <YOUR-REPO-URL> pyproject-up && cd pyproject-up

# Create a virtual environment (recommended)
python -m venv .venv && . .venv/bin/activate  # Windows: .venv\\Scripts\\activate

# Install runtime deps for the CLIs
pip install tomlkit packaging
```

### Files

```
scripts/
  pyproject_editor.py          # structural edits (bump version, set/remove deps, set Python)
  pyproject_updater.py         # upgrade dependency constraints from PyPI
  check_imports_vs_pyproject.py# scan imports; report & optionally fix missing deps in pyproject
.github/workflows/
  auto-pyproject-update.yml    # version bump on push
  auto-upgrade-pyproject.yml   # weekly upgrade PR
```

---

## `pyproject_editor.py` — deterministic edits

**Purpose.** Make precise changes to `pyproject.toml` without losing formatting/comments.

**Usage.**

```bash
# Show help
python scripts/pyproject_editor.py -h

# Bump semantic version (patch|minor|major)
python scripts/pyproject_editor.py bump-version patch

# Add or update a dependency
python scripts/pyproject_editor.py set-dep numpy "^1.26"

# Add a dev/group dependency
python scripts/pyproject_editor.py set-dep ruff "^0.5" --group dev

# Remove a dependency
python scripts/pyproject_editor.py remove-dep numpy

# Set Python version constraint
python scripts/pyproject_editor.py set-python ">=3.10,<3.13"

# Dry-run (print a unified diff, do not write)
python scripts/pyproject_editor.py set-dep pandas "^2.2" --check
```

**Notes.**

* Supports Poetry legacy `dev-dependencies` and Poetry 1.2+ `group.<name>.dependencies`.
* For PEP 621 projects, dependencies in arrays are updated in place.
* Non-PyPI dependencies (git/path/table without a `version`) are left unchanged.

---

## `pyproject_updater.py` — upgrade constraints to latest

**Purpose.** Look up the latest non-yanked releases on PyPI and rewrite your constraint strings accordingly.

**Strategies.**

* `exact` → `==X.Y.Z`
* `caret` → Poetry: `^X.Y.Z`; PEP 621: `>=X.Y.Z,<X+1.0.0`
* `tilde` → Poetry: `~X.Y.Z`; PEP 621: `>=X.Y.Z,<X.(Y+1).0`
* `floor` → `>=X.Y.Z`

**Safety defaults.**

* Pre-releases are **excluded** unless you pass `--pre`.
* Major version jumps are **prevented** unless you pass `--allow-major`.
* Git/path/table deps are skipped.

**Usage.**

```bash
# Show help
python scripts/pyproject_updater.py -h

# Update main+dev groups, caret strategy, no majors, no pre-releases, dry-run
python scripts/pyproject_updater.py \
  --strategy caret --groups main,dev --respect-major --no-prerelease --check

# Write the changes
python scripts/pyproject_updater.py --strategy caret --groups main,dev --respect-major --no-prerelease

# Only touch specific packages
python scripts/pyproject_updater.py --only numpy,pandas --strategy exact

# Accept pre-releases and allow major bumps
python scripts/pyproject_updater.py --allow-major --pre
```

**Tips.**

* If your project pins `requires-python`, keep it realistic to avoid choosing releases that need a newer interpreter.
* Use `--check` in CI to preview diffs without committing.

---

## `check_imports_vs_pyproject.py` — detect & fix missing dependencies

**Purpose.** Scan your Python sources for imports, compare them with the dependencies declared in `pyproject.toml`, and optionally **write missing packages** into the desired group — preserving formatting/comments.

**What it does.**

* Detects **missing** deps (imported but not declared) and **unused** deps (declared but not imported).
* Maps modules → distributions using `importlib.metadata` when available, with sensible fallbacks (e.g., `cv2` → `opencv-python`).
* Supports **Poetry** (`[tool.poetry]`) and **PEP 621** (`[project]`).
* `--fix` mode adds missing deps to `[tool.poetry.(dev-)?dependencies]` or to `[project.dependencies]` / `[project.optional-dependencies.<group>]`.
* Can resolve the **latest version from PyPI** and write a constraint using a chosen strategy.

**Install.**

```bash
pip install tomlkit packaging
```

**Usage.**

```bash
# Help
python scripts/check_imports_vs_pyproject.py -h

# Detect only (text report)
python scripts/check_imports_vs_pyproject.py

# Detect and fail CI if there are missing deps (default policy)
python scripts/check_imports_vs_pyproject.py --fail-on missing

# Fix: add missing to MAIN group, resolve latest version from PyPI, caret constraints
python scripts/check_imports_vs_pyproject.py --fix --resolve-latest --strategy caret

# Fix into DEV group (Poetry) or optional group 'dev' (PEP 621), no network (floor >=0)
python scripts/check_imports_vs_pyproject.py --fix --fix-to dev --strategy floor

# Dry-run only (print unified diff, do not write)
python scripts/check_imports_vs_pyproject.py --fix --resolve-latest --check
```

**Key options.**

* `--fix` enable writing to `pyproject.toml`.
* `--fix-to <group>` target group: `main` (default), `dev`, or any named group.
* `--strategy {caret,tilde,exact,floor}` how to express the version:

  * `caret` → Poetry `^X.Y.Z` / PEP 621 `>=X.Y.Z,<X+1.0.0`
  * `tilde` → Poetry `~X.Y.Z` / PEP 621 `>=X.Y.Z,<X.(Y+1).0`
  * `exact` → `==X.Y.Z`
  * `floor` → `>=X.Y.Z`
* `--resolve-latest` query PyPI for latest non‑yanked version (use `--pre` to include pre‑releases).
* `--groups` which groups count as already declared during checking (defaults to `main,dev`).
* `--src-hints` where local packages live (defaults to `src`).

**Exit codes.** `0` OK, `1` missing only, `2` unused only, `3` both (when `--fail-on both`).

**CI snippet.**

```yaml
- name: Check & fix missing deps in pyproject (dry-run)
  run: |
    python -m pip install --upgrade pip
    pip install tomlkit packaging
    python scripts/check_imports_vs_pyproject.py --fix --resolve-latest --strategy caret --check

- name: Fail if there are missing deps
  run: |
    python scripts/check_imports_vs_pyproject.py --fail-on missing --format text
```

---

## GitHub Actions

### 1) Version bump on push — `auto-pyproject-update.yml`

* **When**: every push to `main`.
* **Logic**: last commit message decides the bump level:

  * contains `BREAKING CHANGE` → `major`
  * starts with `feat:` → `minor`
  * otherwise → `patch`

**Install.** Copy to `.github/workflows/auto-pyproject-update.yml`.

```yaml
name: Auto update pyproject

on:
  push:
    branches: [ "main" ]

permissions:
  contents: write

jobs:
  bump:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: |
          python -m pip install --upgrade pip
          pip install tomlkit
      - name: Decide bump level from commit message
        id: decide
        run: |
          msg="$(git log -1 --pretty=%B)"
          level="patch"
          if echo "$msg" | grep -qi "breaking change"; then level="major"; fi
          if echo "$msg" | grep -qi "^feat:"; then level="minor"; fi
          echo "level=$level" >> "$GITHUB_OUTPUT"
      - name: Bump version
        run: |
          python scripts/pyproject_editor.py bump-version "${{ steps.decide.outputs.level }}"
      - name: Commit & push if changed
        run: |
          if ! git diff --quiet; then
            git config user.name "github-actions[bot]"
            git config user.email "41898282+github-actions[bot]@users.noreply.github.com"
            git add pyproject.toml
            git commit -m "chore: bump version (${{ steps.decide.outputs.level }}) [skip ci]"
            git push
          fi
```

**Notes.**

* Uses the repo-scoped `GITHUB_TOKEN` for pushes. No extra secrets required.
* Adjust the commit-message rules to your conventions if needed.

---

### 2) Weekly dependency upgrade PR — `auto-upgrade-pyproject.yml`

* **When**: every Monday at 06:00 UTC (and manual dispatch).
* **What**: runs the updater, commits the changes on a branch, opens a PR.

**Install.** Copy to `.github/workflows/auto-upgrade-pyproject.yml`.

```yaml
name: Auto upgrade pyproject constraints

on:
  schedule:
    - cron: "0 6 * * 1"   # Mondays 06:00 UTC
  workflow_dispatch:

permissions:
  contents: write
  pull-requests: write

jobs:
  upgrade:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - name: Install deps
        run: |
          python -m pip install --upgrade pip
          pip install tomlkit packaging
      - name: Run updater (caret, no majors, no pre-releases)
        run: |
          python scripts/pyproject_updater.py --strategy caret --groups main,dev --respect-major --no-prerelease
      - name: Create PR if changed
        env:
          GH_TOKEN: ${{ github.token }}
        run: |
          if ! git diff --quiet; then
            git checkout -b chore/upgrade-pyproject-constraints
            git config user.name "github-actions[bot]"
            git config user.email "41898282+github-actions[bot]@users.noreply.github.com"
            git add pyproject.toml
            git commit -m "chore: upgrade dependency constraints in pyproject"
            git push --force --set-upstream origin chore/upgrade-pyproject-constraints
            gh pr create --title "chore: upgrade pyproject constraints" \
                         --body "Automated update of dependency constraints via PyPI latest." \
                         --base "${GITHUB_REF_NAME:-main}" || true
          fi
```

**Notes.**

* Requires the GitHub CLI `gh` (it is preinstalled on `ubuntu-latest`).
* The built-in `${{ github.token }}` is sufficient for creating the PR.
* Tune schedule, branch name, or strategy to match your policy.

---

## Behavior & limitations

* **Formatting preserved**: `tomlkit` keeps your comments and layout intact.
* **Layouts**: Poetry and PEP 621 are both supported.
* **Non-PyPI deps**: git/path/table dependencies are left unchanged.
* **Major bumps**: blocked by default; enable with `--allow-major`.
* **Pre-releases**: excluded by default; include with `--pre`.

---

## Troubleshooting

* *Corporate proxy blocks PyPI:* set `HTTP_PROXY`/`HTTPS_PROXY` in the workflow/job.
* *Package not on PyPI:* the updater will skip it silently.
* *Interpreter too old/new:* enforce `requires-python` in your `pyproject.toml` and keep CI Python in sync.

---

## License

MIT (see `LICENSE`).
