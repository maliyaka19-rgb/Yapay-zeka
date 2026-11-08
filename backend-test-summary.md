# Backend Pytest Suite — State & Gap Analysis

**Repository**: C:\Users\HP\Desktop\YAPAY ZEKA\multimodal-studio
**Branch**: main
**Tests directory**: multimodal-studio/backend/tests/

---

## 1. Test Files (all 35 under `tests/`)

| File | Test Functions (def test_) | Coverage Focus |
|---|---|---|
| `test_agents_specialization.py` | 5 | Agent roster integrity, keyword selection, tools/available endpoint |
| `test_agent_strength.py` | 8 | Agent tool payload, safe window enforcement |
| `test_api_live.py` | 5 | Live endpoint reachability, auth, chat, image proxy (marker: live) |
| `test_auto_insights.py` | 5 | Auto insights on/off, deterministic generation, failure handling |
| `test_coding_insights.py` | 13 | Empty history, failure reporting, retry, human decision, status set, de-dup, search |
| `test_coding_manager.py` | 24 | Task classification, workflows, file locking, build report, execute pipeline, parallel, HTTP routes |
| `test_coding_team.py` | 22 | Roster sizes, hierarchy, task routing, keyword selector, insights attribution, delegation |
| `test_cors.py` | 6 | Origin allowlist (desktop 8090, loopback, frontend 8080, external rejected) |
| `test_identity.py` | 2 | Identity chat never calls LLM, fallback has no API error text |
| `test_files_changed.py` | 12 | Report lists changed files, retry merges, plan mode, verification overrides |
| `test_local_llm.py` | 15 | Local server detection, chat end-to-end, fallback chain, status route, env semantics |
| `test_log_redaction.py` | 10 | Token redaction in URLs, groq key, OpenAI-style keys, normal messages, filter attached |
| `test_master_agents.py` | 22 | 22 agents contracts, task messages, deterministic verdict, secret scan, dangerous commands |
| `test_opencode_llm.py` | 22 | Parse tool protocol, code fences, OpenAI style, agent routes, DeepSeek catalog, live DeepSeek |
| `test_provider_health.py` | 34 | Provider health, rate limits, TTL, snapshots without secrets, 404/401 blocks, primary/secondary |
| `test_project_fs.py` | 11 | Create/delete projects, path traversal, recent files, root protection |
| `test_rate_limit_retry.py` | 13 | Retry-After parsing, 429 retry, budget, fallback, exhaustion |
| `test_rag_lazy.py` | 3 | RAG import does not load heavy deps, availability flags, AI agent import fast |
| `test_response_validation.py` | 10 | Content response validation, tool calls, empty/non-assistant, bad types, missing choices |
| `test_root_ui.py` | 6 | Root redirects, follows redirect, API info always available, JSON fallback |
| `test_task_working_dir.py` | 14 | Tool writes into task dir, default behavior, escape prevention, concurrent isolation, manager set/reset |
| `test_team_agents.py` | 12 | Default roster 22, group sizes, hierarchy deterministic, routing, all reachable, insights, fallback |
| `test_tool_allowlist.py` | 8 | Executor deny/allow, none means unrestricted, semantics, readonly override, active tools/model |
| `test_tool_mismatch.py` | 3 | 400 retry with tools disabled, retry failure falls back, unrelated 400 no trigger |
| `test_telegram.py` | 31 | Command parsing, allowlist, plain text triggers, routes status, send, start/stop, config, config encryption |
| `test_tools_spec.py` | Tools spec (functions listed, not test_ functions) |
| `test_identity.py` | 2 | Identity chat, fallback text |
| `test_catalog_memory.py` | 2 | OpenRouter model count, required fields |
| `test_fallback.py` | 7 | 429 rate limit skip, 401 auth error move on, 04 not found model skip, structure trigger, auth header, 429 no retry same model |

---

## 2. Pytest Configuration (`pytest.ini`)

```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_
addopts = -v --tb=short -m "not live"
markers =
    live: canlı backend sunucusu gerektirir (varsayılan olarak hariç tutulur)
```

- **Default marker**: `not live` — live-marked tests are skipped unless `-m live` is passed
- **Test discovery**: `test_*.py` files in `tests/` directory
- **Markers defined**: only `live`; no other custom markers registered beyond that

---

## 3. Registered API Endpoints (by router prefix)

| Prefix | Router File | Key Endpoints (path after prefix) |
|---|---|---|
| `/api/v1/agent` | `agent_routes.py` | `/run`, `/run-async`, `/status`, `/tools`, `/memory/query`, `/memory/stats`, `/memory/consolidate`, `/memory/clear`, `/sessions`, `/stop` |
| `/api/v1/ai` | `ai_agent_routes.py` | `/chat`, `/chat/stream`, `/info`, `/conversations`, `/conversations/{id}`, `/conversations/{id}`, `/delete`, `/learning/stats` |
| `/api/v1/auth` | `auth_routes.py` | `/register`, `/forgot-password`, `/reset-password`, `/login`, `/guest`, `/me`, `/logout`, `/oauth/token`, `/oauth/google/url`, `/oauth/apple/url`, `/oauth/callback`, `/oauth/link`, `/chats`, `/chats`, `/chats/{id}`, `/chats/{id}/patch`, `/chats/{id}/delete` |
| `/api/v1/brain` | `brain_routes.py` | `/stats`, `/lessons`, `/skills`, `/reflections`, `/feedback`, `/predict`, `/context`, `/reset`, `/experiences` |
| `/api/v1/coding` | `coding_routes.py` | `/health`, `/workflows`, `/run`, `/tasks`, `/tasks/{id}`, `/insights`, `/insights/analyze`, `/insights/{id}/approve`, `/insights/{id}/reject` |
| `/api/v1/agents` | `custom_agent_routes.py` | `""` (list), `/hierarchy`, `/{agent_id}`, `""` (create), `""` (put), `""` (delete), `""` (duplicate), `/tools/available` |
| `/api/v1/fs` | `fs_routes.py` | `/drives`, `/browse`, `/open-project`, `/close-project`, `/current-project`, `/recent-projects`, `/delete/recent-projects`, `/create-project`, `/project/delete`, `/home`, `/desktop` |
| `/api/v1/models` | `model_routes.py` | `/catalog`, `/activate`, `/api-key`, `/active`, `/providers`, `/opencode/status`, `/local/status` |
| `/api/v1/project` | `project_routes.py` | `/tree`, `/file`, `/create`, `/file` (post), `/rename`, `/file` (delete), `/stats` |
| `/api/v1/telegram` | `telegram_routes.py` | `/status`, `/config`, `/start`, `/stop`, `/send` |

### Key endpoints from `app.py` direct routes:
- `/health` — system health check
- `/api/v1/generate/code` — code generation
- `/api/v1/generate/visual` — visual prompt generation
- `/api/v1/generate/image` — real image generation (Pollinations.ai)
- `/api/v1/upload/file` — file/document upload
- `/api/v1/upload/video` — video upload
- `/api/v1/image/proxy` — image proxy
- `/api/v1/generate/video` — video generation
- `/api/v1/videos/{video_id}` — video retrieval
- `/api/v1/learning/report` — learning report
- `/api/v1/learning/summary` — learning summary
- `/api/v1/learning/lessons/{category}` — lessons by category

---

## 4. Cross-Referencing: Which Endpoints Have Tests / Don't

### Endpoints tested in `test_api_live.py` (live tests, excluded by default):

| Path | Method |
|---|---|
| `/` | GET |
| `/health` | GET |
| `/api/v1/models/catalog` | GET |
| `/api/v1/models/providers` | GET |
| `/api/v1/models/active` | GET |
| `/api/v1/agents` | GET (implied) |
| `/api/v1/agents/tools/available` | GET |
| `/api/v1/ai/info` | GET |
| `/api/v1/ai/conversations` | GET |
| `/api/v1/ai/learning/stats` | GET |
| `/api/v1/agent/tools` | GET |
| `/api/v1/agent/sessions` | GET |
| `/api/v1/agent/memory/stats` | GET |
| `/api/v1/brain/stats` | GET |
| `/api/v1/brain/skills` | GET |
| `/api/v1/brain/lessons` | GET |
| `/api/v1/brain/experiences` | GET |
| `/api/v1/brain/reflections` | GET |
| `/api/v1/fs/drives` | GET |
| `/api/v1/fs/home` | GET |
| `/api/v1/fs/current-project` | GET |
| `/api/v1/project/stats` | GET |
| `/api/v1/project/tree` | GET |
| `/api/v1/learning/report` | GET |
| `/api/v1/learning/summary` | GET |

### Likely UNTESTED / Gaps (not in `test_api_live.py` parametrization):

| Category | Endpoints |
|---|---|
| **Agent endpoints** | `/api/v1/agent/run`, `/api/v1/agent/run-async`, `/api/v1/agent/status`, `/api/v1/agent/memory/{query}`, `/api/v1/agent/memory/stats`, `/api/v1/agent/memory/consolidate`, `/api/v1/agent/memory/clear`, `/api/v1/agent/sessions`, `/api/v1/agent/stop` |
| **AI chat** | `/api/v1/ai/chat`, `/api/v1/ai/chat/stream` |
| **Auth** | `/api/v1/auth/register`, `/api/v1/auth/login`, `/api/v1/auth/me`, `/api/v1/auth/oauth/*` |
| **Brain** | `/api/v1/brain/feedback`, `/api/v1/brain/predict`, `/api/v1/brain/context`, `/api/v1/brain/experiences` |
| **Coding** | `/api/v1/coding/health`, `/api/v1/coding/workflows`, `/api/v1/coding/run`, `/api/v1/coding/tasks/{id}`, `/api/v1/coding/insights/analyze`, `/api/v1/coding/insights/{id}/approve/reject` |
| **Custom agents** | `/api/v1/agents/`, `/api/v1/agents/{id}`, `/api/v1/agents/{id}/duplicate`, `/api/v1/agents/tools/available` |
| **Filesystem** | `/api/v1/fs/drives`, `/api/v1/fs/browse`, `/api/v1/fs/open-project`, `/api/v1/fs/close-project`, `/api/v1/fs/current-project`, `/api/v1/fs/recent-projects`, `/api/v1/fs/create-project`, `/api/v1/fs/project`, `/api/v1/fs/home`, `/api/v1/fs/desktop` |
| **Models** | `/api/v1/models/catalog`, `/api/v1/models/activate`, `/api/v1/models/api-key`, `/api/v1/models/active`, `/api/v1/models/providers`, `/api/v1/models/opencode/status`, `/api/v1/models/local/status` |
| **Project** | `/api/v1/project/tree`, `/api/v1/project/file` (GET/POST/DELETE/RENAME), `/api/v1/project/stats` |
| **Direct app routes** | `/api/v1/generate/code`, `/api/v1/generate/visual`, `/api/v1/generate/image`, `/api/v1/upload/file`, `/api/v1/upload/video`, `/api/v1/image/proxy`, `/api/v1/generate/video`, `/api/v1/videos/{id}` |
| **Learning** | `/api/v1/learning/lessons/{category}` |
| **Telegram** | All `/api/v1/telegram/*` endpoints |

### Observed patterns:

1. **`test_api_live.py`** covers a broad but selective set of public endpoints (29 paths). It does **not** include any coding-manager, brain, custom-agent, or filesystem endpoints beyond the basics.

2. **Unit tests** (non-live) cover specific functionality in isolation:
   - `test_coding_manager.py` — tests `/api/v1/coding/health` and `/api/v1/coding/workflows` via `TestClient`
   - `test_agents_specialization.py` — tests `/api/v1/agents/tools/available`
   - `test_provider_health.py` — tests provider health logic (not HTTP endpoints directly)
   - `test_fallback.py` — tests fallback/rate-limit logic

3. **Missing test coverage by type**:
   - **No unit tests** for: `/api/v1/ai/chat`, `/api/v1/ai/chat/stream`, most `/api/v1/agent/*`, most `/api/v1/coding/*` (beyond health/workflows), `/api/v1/brain/*` (beyond stats/lessons), `/api/v1/project/file` variants, `/api/v1/fs/*` (beyond create/delete/project), `/api/v1/models/activate`, `/api/v1/models/api-key`
   - **No integration tests** for auth-protected endpoints (those requiring `auth_headers`) outside `test_api_live.py`
   - **Live tests only** for the full API surface — all others are unit/isolated

---

## 5. Concrete Observations — Tests Likely to Fail / Issues

### A. `test_local_llm.py` — `test_chat_forwards_tools_to_local_model` (line 128)
- **Issue**: Uses `local_server` fixture that may not be set up correctly. The test monkeypatches `ai_agent.chat` but the actual endpoint `/api/v1/ai/chat` requires auth headers in live mode; this test appears to be a unit test with mocks.

### B. `test_provider_health.py` — provider health snapshot secrets
- **Observation**: Tests verify snapshots contain no secrets (line 178, 210+). These are hermetic — they mock the provider calls and verify no API keys leak into logs/metadata.

### C. `test_api_live.py` — `test_get_endpoints_200` parametrization gap
- The parametrized list (51 paths) includes `/api/v1/agents/tools/available` and `/api/v1/agent/tools` — **but these are different paths**. The `agent_routes.py` defines `/api/v1/agent/tools` (note: single "agent", not "agents"). The live test references `/api/v1/agents/tools/available` which maps to `custom_agent_routes.py`. This could cause a 404 in the live test if the server doesn't have both routes.

### D. `test_coding_team.py` — `test_default_roster_is_exactly_official_22`
- **Issue**: Relies on `load_agents()` from `custom_agents.py`. If the agent roster changes (add/remove), this test breaks. The test at line 174 expects exactly 22 agents — matches the commit history note "Kadro: sadece Ana Yönetici + Kodlama Yöneti + 20 uzman" (1 + 1 + 20 = 22).

### E. `test_telegram.py` — 31 test functions, extensive mocking
- Uses `httpx.MockTransport` for all Telegram API calls. All 31 tests are unit-level, no real network. Coverage is thorough for the telegram bot module.

### F. `test_coding_manager.py` — HTTP test client setup
- The `_client` fixture (line 244) creates a `FastAPI` app and includes only `coding_routes.router`. It does **not** include auth dependencies, so `/api/v1/coding/run` etc. are accessible without a token. This is fine for unit testing but means these endpoints are not tested under auth.

### G. `test_auto_insights.py` — `test_disabled_by_default_in_tests`
- Line 44: explicitly disables auto-insights via `NEXUS_AUTO_INSIGHTS=0` env var in conftest.py. The test verifies it's off by default in the test context.

### H. Marker `live` — 5 tests in `test_api_live.py` have `pytestmark = pytest.mark.live`
- These are **excluded by default** (`-m "not live"` in pytest.ini). To run them: `pytest tests/test_api_live.py -m live`. They require a running backend at `http://localhost:8000`.

### I. `test_files_changed.py` — many tests use `tmp_files` fixture and `monkeypatch`
- Tests verify file-change reporting, retry behavior, plan mode, and verification overrides. All are hermetic (no real file I/O outside tmp_path).

### J. `test_cors.py` — 6 tests for origin allowlist
- Tests that specific origins are allowed/denied. The CORS config in `app.py` has a `_dev_origins` list and `_env_origins` (truncated in output). Tests cover desktop 8090, loopback, frontend 8080, and external rejection.

---

## Summary of Gaps

| Gap | Severity | Notes |
|---|---|---|
| No unit tests for `/api/v1/ai/chat` or `/api/v1/ai/chat/stream` | High | Core AI chat endpoint untested at unit level |
| No unit tests for most `/api/v1/agent/*` endpoints | High | Agent run/status/memory endpoints not tested |
| No unit tests for `/api/v1/coding/run`, `/tasks/*`, `/insights/*` (beyond health/workflows) | Medium | Coding manager routes have some HTTP tests but not full coverage |
| No unit tests for `/api/v1/brain/*` beyond stats/lessons/skills | Medium | Brain routes largely untested at unit level |
| No unit tests for `/api/v1/project/file` (POST/DELETE/RENAME) | Medium | Project file operations not unit-tested |
| No unit tests for `/api/v1/fs/*` beyond create/delete | Medium | FS routes have basic create/delete/project tests |
| `test_api_live.py` live tests excluded by default | Medium | Requires `-m live` and running backend |
| Potential mismatch: `/api/v1/agents/tools/available` vs `/api/v1/agent/tools/available` | Low | Different routers, could cause 404 in live tests |
| `test_coding_team.py` hardcodes expected roster size of 22 | Low | Brittle if agent roster changes |

**Most critical gap**: The core AI chat endpoint (`/api/v1/ai/chat`) and agent run endpoints (`/api/v1/agent/run`, `/status`) have no dedicated unit tests outside the live test suite. All other test coverage is good for the modules they test (coding manager, agent specialization, provider health, CORS, Telegram, etc.), but the primary interaction paths are under-tested.