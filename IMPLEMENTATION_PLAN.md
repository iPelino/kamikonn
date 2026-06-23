# KamConnect — Comprehensive Implementation Plan

## Context

KamConnect is a cross-university academic event discovery platform for Rwanda's 10 major Kigali universities. The problem: academic events are siloed across WhatsApp groups, internal emails, and campus notice boards — students miss opportunities at other institutions, and organizers reach only their home campus audience.

No code exists yet — only a detailed project spec (`rwanda_academic_hub_description.md`), brand identity guidelines (`kamconnect_brand_identity.md`), and a logo asset. This plan takes the project from zero to a deployed, open-source platform within the ~6-month timeline (end of 2026).

The plan is structured as a **monorepo** with Django REST Framework (backend) + React TypeScript (frontend), deployed on DigitalOcean VPS with Docker.

---

## 1. Technology Stack

### Backend
| Technology | Version | Why |
|---|---|---|
| Python | 3.12+ | Founder expertise; strong African dev community |
| Django | 5.2 LTS | Long-term support until April 2028; mature ORM, admin |
| Django REST Framework | 3.15 | Industry standard for Django APIs |
| djangorestframework-simplejwt | 5.5.x | Stateless JWT auth for SPA architecture |
| django-filter | 24.x | Declarative filtering for event search/discovery |
| django-cors-headers | 4.x | SPA cross-origin requests |
| drf-spectacular | 0.29.x | Auto-generated OpenAPI docs + Swagger UI |
| Celery + Redis | 5.4.x / 7.x | Async email, reminders, trust-tier promotion |
| Resend | latest | Transactional email (3K/month free) |
| PostgreSQL | 16 | Full-text search, GIN indexes, JSON fields |
| Pillow | 11.x | Image processing for banners/avatars |
| django-storages | 1.14+ | S3-compatible storage for DigitalOcean Spaces |
| Gunicorn | 23.x | Production WSGI server |

### Frontend
| Technology | Version | Why |
|---|---|---|
| React | 19 | Largest ecosystem; concurrent features |
| TypeScript | 5.6+ | Catches bugs before runtime; essential for solo dev |
| Vite | 6.x | 40x faster builds than CRA; native ESM + instant HMR |
| Tailwind CSS | 4.x | CSS-first config; maps directly to brand palette |
| shadcn/ui | latest | Accessible components (Radix-based); full ownership, no lock-in |
| TanStack Query | v5 | Server state: caching, deduplication, background refetch |
| Zustand | 5.x | Client state (auth, UI); ~2KB, zero boilerplate |
| React Router | v7 | Data-first routing with loaders and error boundaries |
| React Hook Form + Zod | 7.x + 3.x | Minimal re-renders; type-safe schemas for multi-step wizard |
| Axios | 1.x | Interceptors for JWT refresh and error normalization |
| react-i18next | 15.x | Namespace-based lazy loading for future French/Kinyarwanda |
| Vitest | 3.x | Native Vite integration, 2-5x faster than Jest |

### Infrastructure
| Technology | Why |
|---|---|
| Docker + Docker Compose | One-command dev setup; consistent environments |
| Nginx | Reverse proxy, SSL termination, static file serving |
| Let's Encrypt (Certbot) | Free SSL with auto-renewal |
| DigitalOcean Droplet | $24/month 4GB; Amsterdam datacenter (lowest latency to Kigali) |
| DigitalOcean Spaces | S3-compatible media storage with CDN ($5/month) |
| GitHub Actions | CI/CD — free unlimited minutes for public repos |

### Why NOT alternatives
| Rejected | Reason |
|---|---|
| Next.js | SSR adds deployment complexity; SPA + meta tags suffices for SEO needs |
| Redux | Overkill boilerplate; TanStack Query + Zustand covers all state needs |
| Material UI | Fights custom brand identity; shadcn/ui gives full styling control |
| Elasticsearch | PostgreSQL's SearchVector + pg_trgm handles thousands of events fine |
| MongoDB | Data is deeply relational (User→Organizer→Event→RSVP) |
| Firebase/Supabase | Vendor lock-in conflicts with open-source goals |

---

## 2. Repository Structure

Monorepo — solo founder shouldn't manage two repos; Docker Compose needs both services together; contributors clone once.

```
kamconnect/
├── .github/
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.yml
│   │   └── feature_request.yml
│   ├── PULL_REQUEST_TEMPLATE.md
│   └── workflows/
│       ├── ci-backend.yml
│       ├── ci-frontend.yml
│       └── deploy.yml
├── backend/
│   ├── kamconnect/                  # Django project root
│   │   ├── settings/
│   │   │   ├── base.py             # Shared config
│   │   │   ├── development.py      # DEBUG=True, console email, local DB
│   │   │   ├── production.py       # DEBUG=False, Spaces storage, HSTS
│   │   │   └── test.py             # Fast password hasher, disabled throttles
│   │   ├── urls.py
│   │   ├── wsgi.py / asgi.py
│   │   └── celery.py
│   ├── apps/
│   │   ├── core/                   # TimeStampedModel, base permissions, pagination, utils
│   │   ├── accounts/               # Custom User model, JWT auth, profiles
│   │   ├── events/                 # Event CRUD, search, .ics export
│   │   ├── organizers/             # Organizer profiles, trust tiers
│   │   ├── universities/           # University directory (mostly read-only)
│   │   ├── rsvps/                  # RSVP, SavedEvent, FollowedOrganizer
│   │   ├── moderation/             # FlagReport, VerificationRequest, admin actions
│   │   └── notifications/          # Celery tasks for email dispatch
│   ├── fixtures/                   # universities.json, categories.json, demo_events.json
│   ├── templates/emails/           # Branded HTML email templates
│   ├── requirements/
│   │   ├── base.txt / development.txt / production.txt
│   ├── Dockerfile
│   └── pyproject.toml              # Black, isort, ruff, mypy config
├── frontend/
│   ├── src/
│   │   ├── api/                    # Axios client + interceptors
│   │   │   ├── client.ts
│   │   │   ├── queries/            # TanStack Query hooks (events.ts, user.ts, etc.)
│   │   │   └── mutations/          # Mutation hooks (auth.ts, rsvps.ts, etc.)
│   │   ├── components/
│   │   │   ├── ui/                 # shadcn/ui components
│   │   │   ├── layout/             # Header, Footer, MobileNav, PageContainer
│   │   │   └── shared/             # EventCard, OrganizerBadge, SearchBar
│   │   ├── features/
│   │   │   ├── auth/               # Login, Register, AuthGuard
│   │   │   ├── events/             # EventList, EventDetail, EventWizard
│   │   │   ├── organizers/         # OrganizerProfile, OrganizerDashboard
│   │   │   ├── rsvp/               # RSVPButton, WaitlistBadge
│   │   │   ├── admin/              # AdminDashboard, FlagReview, Verification
│   │   │   └── user/               # UserProfile, SavedEvents, MyRSVPs
│   │   ├── hooks/                  # useAuth, useDebounce, useMediaQuery
│   │   ├── stores/                 # Zustand (authStore.ts, uiStore.ts)
│   │   ├── types/                  # TypeScript interfaces
│   │   ├── schemas/                # Zod validation schemas
│   │   ├── routes/                 # Route definitions, loaders, guards
│   │   ├── providers/              # QueryClient, Auth, I18n providers
│   │   ├── styles/globals.css      # Tailwind v4 @theme with brand colors
│   │   ├── App.tsx / main.tsx
│   ├── Dockerfile
│   └── vite.config.ts
├── nginx/
│   └── nginx.conf / nginx.dev.conf
├── docs/                           # architecture.md, api-reference.md, deployment.md
├── scripts/
│   ├── seed_data.py
│   ├── backup_db.sh
│   └── generate_api_types.sh       # OpenAPI → TypeScript types
├── docker-compose.yml              # Dev: db, redis, backend, frontend, celery
├── docker-compose.prod.yml         # Prod: + nginx, certbot
├── .env.example
├── .pre-commit-config.yaml
├── Makefile                        # dev, build, migrate, seed, test, lint, shell
├── LICENSE (MIT)
├── README.md / CONTRIBUTING.md / CODE_OF_CONDUCT.md / CHANGELOG.md
```

---

## 3. Backend Architecture

### Django App Internals Pattern
Each app follows: `models.py` → `serializers.py` → `views.py` → `filters.py` → `permissions.py` → `services.py` → `tasks.py` → `urls.py` → `tests/` (with `factories.py`).

Business logic lives in `services.py` (not views) — keeps views thin, logic testable without HTTP.

### Key Design Decisions

**Custom User model** — Use `AbstractUser` with `email` as `USERNAME_FIELD` from day one. Changing this later is extremely painful.

**Serializer strategy** — Multiple serializers per model:
- List serializer (minimal fields for feed cards — reduces 3G payload)
- Detail serializer (full fields for event page, nested organizer card)
- Create/Update serializer (separate write validation)
- Admin serializer (moderation-specific fields)

**Permission classes** (in `apps/core/permissions.py`):
- `IsOrganizerOwner` — event.organizer.user == request.user
- `IsOrganizer` — user has an associated Organizer profile
- `IsAdminUser` — user.role == 'admin'
- `IsOwnerOrReadOnly` — object.user == request.user OR safe methods

**Pagination** — Cursor-based for event feeds (better for mobile infinite scroll); page-number for admin lists.

**Search** — Two layers, no Elasticsearch needed:
1. `SearchVector` + `SearchRank` on Event (title, description) with GIN index → relevance-ranked results
2. `pg_trgm` + `TrigramSimilarity` → fuzzy fallback for typos ("hackatohn" → "hackathon")

**File uploads** — Local filesystem in dev, DigitalOcean Spaces in prod (via `django-storages`). Validate MIME type server-side, max 5MB, strip EXIF, generate thumbnails with Pillow.

---

## 4. Frontend Architecture

### Tailwind v4 Theme (CSS-first, maps to brand identity)
```css
@theme {
  --color-forest: #0F3D26;
  --color-forest-light: #4B6354;
  --color-amber: #F59E0B;
  --color-sage: #F5F7F2;
  --color-charcoal: #1F2937;
  --font-heading: "Plus Jakarta Sans", sans-serif;
  --font-body: "Inter", sans-serif;
}
```

### Routing Map
```
/                           → EventFeed (public)
/events                     → EventList with filters (public)
/events/:slug               → EventDetail (public)
/search                     → SearchResults (public)
/login, /register           → Auth pages (guest only)
/dashboard                  → UserDashboard (authenticated)
/dashboard/saved            → SavedEvents
/dashboard/rsvps            → MyRSVPs
/organizer/setup            → BecomeOrganizer (authenticated)
/organizer/dashboard        → OrganizerDashboard (organizer)
/organizer/events/new       → EventWizard (organizer)
/organizer/events/:slug/edit → EventWizard (organizer, owner)
/admin                      → AdminDashboard (admin)
/admin/flags                → FlagReview (admin)
/admin/verifications        → VerificationReview (admin)
```

All routes use `React.lazy()` for code splitting. Protected routes check auth store in loaders.

### Event Creation Wizard
Three Zod schemas composed with `.merge()`:
- Step 1 (BasicInfoSchema): title, description, category, tags
- Step 2 (DateLocationSchema): dates, timezone, format, venue/virtual link
- Step 3 (AudienceSchema): eligibility, capacity, registration method, banner upload

Draft auto-save on step transition.

### Performance (targeting < 3s on 3G)
- Route-level code splitting
- Thumbnail URLs from API for list views; full banners only on detail
- TanStack Query: `staleTime: 5min` for events, `Infinity` for categories/universities
- Target < 200KB initial JS (gzipped)
- Preload Plus Jakarta Sans 700 + Inter 400

---

## 5. Database & Indexing

Enable extensions: `pg_trgm`, `unaccent`.

**Events table indexes:**
- GIN on `search_vector` (full-text search)
- GIN on title with `gin_trgm_ops` (fuzzy matching)
- B-tree on `(status, start_datetime)` (feed query)
- B-tree on `category_id`, `organizer_id`, `university_affiliation_id` (filters)
- B-tree on `slug` (unique, detail page)

**RSVPs:** Unique on `(user_id, event_id)`, B-tree on `event_id` and `(user_id, status)`.

**Seed data:** Three fixture files — `universities.json` (10 institutions), `categories.json` (12 categories), `demo_events.json` (15-20 realistic events for dev).

---

## 6. Testing Strategy

**Backend (pytest-django + factory_boy):**
- Model tests, serializer tests, view tests, service tests, permission tests
- Factory traits: `published`, `draft`, `past`, `full_capacity`, `virtual`
- Coverage target: 80%+

**Frontend (Vitest + React Testing Library + MSW):**
- Component tests, hook tests, integration flow tests
- MSW for API mocking at the network level
- Coverage target: 70%+

**API contract:** drf-spectacular exports OpenAPI schema → `openapi-typescript` generates frontend types → compile-time contract validation.

**E2E (Phase 3+):** Playwright for critical flows — browse events, register + RSVP, create event, admin moderation. Run nightly, not on every PR.

---

## 7. Security

| OWASP Risk | Mitigation |
|---|---|
| Injection | Django ORM parameterized queries; Zod frontend + serializer backend validation |
| Broken Auth | JWT 30min access / 7d refresh; token blacklisting on logout; rate-limit login (5/min) |
| Data Exposure | HTTPS only (HSTS); virtual links only visible to RSVPed users |
| Access Control | Per-object permissions on every ViewSet |
| XSS | React auto-escapes; CSP headers via Nginx |
| Known Vulnerabilities | `pip-audit` + `npm audit` in CI; Dependabot |

**Throttle rates:** Anon 100/hour, User 1000/hour, Login 5/min, RSVP 30/min.

---

## 8. CI/CD

**`ci-backend.yml`** (on push + PRs): ruff + black + isort + mypy → pytest with coverage → pip-audit + bandit

**`ci-frontend.yml`** (on push + PRs): eslint + prettier + tsc → vitest with coverage → npm run build

**`deploy.yml`** (manual trigger): SSH → pull → docker compose build → up → migrate → collectstatic → health check

---

## 9. Phase-by-Phase Sprint Breakdown

### Phase 1: Foundation (Weeks 1–8)

**Sprint 1 (Weeks 1–2): Project Bootstrap**
- Backend: Django project with custom User model, split settings, DRF + SimpleJWT, drf-spectacular, `apps/core/` base classes, `apps/universities/` + `apps/events/Category` with fixtures
- Frontend: Vite + React + TS, Tailwind v4 theme, shadcn/ui init (Button, Card, Input, Badge, Skeleton), React Router layout, Axios client, TanStack Query + Zustand, Header/Footer/MobileNav
- Infra: docker-compose.yml (5 services), Dockerfiles, Makefile, .env.example, pre-commit hooks, GitHub Actions CI, README

**Sprint 2 (Weeks 3–4): Auth + Event CRUD**
- Backend: JWT auth endpoints (register/login/logout/refresh), user profile endpoint, Event model + slug generation, EventViewSet (list/retrieve/create/update/delete), list + detail serializers
- Frontend: Login/Register pages (RHF + Zod), JWT flow in Zustand + Axios interceptors, protected routes, event list page with skeletons, EventCard component, event detail page

**Sprint 3 (Weeks 5–6): Search + Filtering**
- Backend: pg_trgm extension, SearchVectorField + GIN index + trigger, EventFilter (university, category, city, format, date range, full-text search), cursor pagination, query optimization with select_related
- Frontend: Debounced search bar, filter sidebar/sheet, search results page, category chips, university dropdown, date range picker, format toggles, empty states

**Sprint 4 (Weeks 7–8): Seed Data + Polish**
- Backend: Demo events fixture, category/university list endpoints, pagination meta
- Frontend: Home page with featured section, category browsing, university listing, infinite scroll, 404 page, error boundaries, favicon + meta tags, mobile audit

**Milestone:** A stranger browses events, searches, filters, and views details without an account.

### Phase 2: Participation Loop (Weeks 9–16)

**Sprint 5 (Weeks 9–10): User Profiles + RSVP**
- Backend: RSVP model + service layer (capacity, waitlist, promotion), .ics generation, SavedEvent, user profile with interests, virtual link visibility (RSVPed users only)
- Frontend: RSVPButton states (RSVP/RSVPed/Waitlist), capacity indicator, calendar download, save toggle, user dashboard, My RSVPs, Saved Events, social sharing

**Sprint 6 (Weeks 11–12): Organizer Profiles + Follow**
- Backend: Organizer model + trust tiers, become-organizer flow, organizer events listing, FollowedOrganizer, follower count annotation, self-RSVP prevention
- Frontend: Become Organizer page, organizer public profile, trust badge component, follow button, followed organizers page

**Sprint 7 (Weeks 13–14): Event Creation Wizard**
- Backend: Event create/update serializers, draft support, banner upload with Pillow thumbnails, recurring series, Tag model
- Frontend: 3-step wizard (RHF + Zod per step), progress indicator, draft auto-save, event edit, rich text editor (Tiptap), image upload with preview

**Sprint 8 (Weeks 15–16): Organizer Dashboard**
- Backend: Dashboard data endpoints, RSVP analytics, CSV attendee export, auto-archive past events (Celery task)
- Frontend: Organizer dashboard (events list + status badges + RSVP counts), attendee list view, CSV export, toast notifications

**Milestone:** Complete publish → discover → RSVP loop works end to end.

### Phase 3: Trust & Polish (Weeks 17–20)

**Sprint 9 (Weeks 17–18): Trust System + Moderation**
- Backend: Auto-promotion Celery task (3+ events, 0 flags → Established), VerificationRequest flow, FlagReport model + endpoints, admin review actions, moderation audit log
- Frontend: Report event modal, admin dashboard layout, flag review queue, verification review queue, trust badges throughout app

**Sprint 10 (Weeks 19–20): Notifications + SEO + Final Polish**
- Backend: Celery email tasks (RSVP confirmation with .ics, 24h reminder, event updates, new events from followed), Resend integration, notification preferences
- Frontend: University profile pages, featured events section, SEO meta tags (react-helmet-async + OG tags), WCAG 2.1 AA audit (focus, ARIA, contrast, keyboard), notification preferences, error handling audit, loading skeletons, mobile final pass

**Milestone:** Production-ready platform with trust system, moderation tools, email notifications, and polished mobile UX.

### Phase 4: Launch & Growth (Weeks 21–24)

**Sprint 11 (Weeks 21–22): Production Deployment**
- Provision DigitalOcean Droplet (4GB, AMS3 datacenter)
- docker-compose.prod.yml with Nginx + Certbot SSL
- DigitalOcean Spaces for media
- PostgreSQL backup cron (daily → Spaces, 30-day retention)
- Celery beat for periodic tasks
- Domain setup (kamconnect.rw), deploy, smoke test, uptime monitoring
- Curate 20-30 real events from university websites
- Google Form bridge for external submissions

**Sprint 12 (Weeks 23–24): Soft Launch + Open Source**
- Clean up README with screenshots
- CONTRIBUTING.md, CODE_OF_CONDUCT.md, LICENSE (MIT), CHANGELOG.md
- Label 5-10 issues as `good-first-issue`
- Soft launch with ALU community + 3-5 club leaders
- WhatsApp seeding with specific event links
- Performance verification (< 3s on 3G via Chrome DevTools)
- Bug fixes from user feedback
- Launch blog post

**Milestone:** Live platform with real events, real users, public GitHub repo.

---

## 10. Verification Plan

After each phase:

1. **Phase 1:** Open browser → browse event feed → search by keyword → filter by category + university → view event detail page → all works without login
2. **Phase 2:** Register → log in → RSVP to event → verify capacity decrements → download .ics → save event → become organizer → create event via wizard → verify it appears in feed → check organizer dashboard shows attendees
3. **Phase 3:** Flag an event → verify it appears in admin queue → review and unpublish → verify trust badge displays correctly → trigger event reminder email → verify RSVP confirmation email with .ics → run Lighthouse for mobile/accessibility scores
4. **Phase 4:** Load site over throttled 3G (< 3s) → share event link on WhatsApp (verify OG preview) → run `docker compose up` in a fresh clone (verify one-command setup works) → verify daily backup runs

Run `pytest` (backend) and `vitest` (frontend) in CI on every PR. Run Playwright E2E nightly from Phase 3 onward.

---

## 11. Contingency Plans

| Risk | Fallback |
|---|---|
| Phase 1 runs long | Cut fuzzy search (Layer 2) and advanced filters to Phase 2; ship basic keyword search |
| Event wizard too complex | Ship single-page form first, upgrade to multi-step in Phase 3 |
| Resend email issues | Switch to SendGrid free tier |
| No contributors | Platform works fully without them; contributors are a bonus |
| Solo burnout | Each phase delivers a usable product — Phase 1 alone is a functional directory |
