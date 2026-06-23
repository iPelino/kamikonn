# Rwanda Academic Hub — Complete Project Description

> **Document Version:** 2.0 — Post-Discovery Interview
> **Last Updated:** 2026-06-23
> **Author Role:** System Analyst / Architect
> **Project Owner:** Pelin (Solo Founder)

---

## 1. Executive Summary

**Rwanda Academic Hub (Academia Rwanda)** is an open-source, community-driven event discovery and management platform for Rwanda's academic ecosystem. It solves a critical visibility problem: academic events remain trapped inside isolated channels (WhatsApp groups, internal emails, campus notice boards), causing students, researchers, and professionals to miss relevant opportunities happening at other institutions.

The platform creates a **shared visibility layer** across universities, enabling anyone — students, lecturers, clubs, research labs, and external partners — to publish, discover, and attend academic events beyond their home campus.

**Key Facts:**
- **Founder:** Solo developer (Pelin), open to contributors and institutional partnerships
- **Launch Scope:** Kigali-first, targeting 10 major universities
- **Business Model:** Free and community-driven; grant/partnership funding planned for sustainability
- **Tech Stack (Target):** Django REST Framework + React TypeScript SPA
- **Infrastructure:** DigitalOcean VPS
- **Target Launch:** End of 2026
- **License:** Open Source (public repository)

---

## 2. Problem Statement

University events in Rwanda are distributed across fragmented, institution-specific channels:

- Internal email lists and faculty notice boards
- Class-specific WhatsApp and Telegram groups
- Individual university social media pages
- Word of mouth within single campuses

**This fragmentation creates measurable harm:**

| Stakeholder | Pain Point |
|---|---|
| **Students** | Miss workshops, hackathons, career fairs, and research talks happening at other universities |
| **Organizers** | Reach only their immediate campus audience, resulting in low attendance |
| **Lecturers** | Cannot promote public seminars beyond their own department |
| **Universities** | Lack visibility into the broader academic ecosystem's activity |
| **External Partners** | (NGOs, innovation hubs, employers) have no centralized channel to reach the academic community |

Existing alternatives are either too generic (Eventbrite), too informal (WhatsApp), or too siloed (university-specific apps). No platform is purpose-built for cross-university academic event discovery in Rwanda.

---

## 3. Vision & Core Principles

**Vision:** One trusted platform where anyone in Rwanda's academic ecosystem can discover, publish, and attend meaningful events across institutional boundaries.

**Guiding Principles:**

1. **Discovery over administration** — Optimize for finding events, not managing complex workflows
2. **Cross-university by default** — Every design decision should assume multi-institution usage
3. **Kigali-strong, nationally inclusive** — Dense local experience without excluding other regions
4. **Open by default, trust through transparency** — Low barriers to publish; trust is earned and displayed, not gatekept
5. **Community-driven sustainability** — Free to use; value attracts partnerships and funding
6. **Mobile-first, low-bandwidth aware** — Designed for the realities of Rwandan internet access

---

## 4. Target Users

### 4.1 Attendees (Primary)
- **University students** — Seeking workshops, hackathons, career fairs, research talks, club events, pitch competitions, scholarship info sessions
- **Lecturers & academic staff** — Seeking conferences, seminars, training sessions, guest lectures
- **General public & professionals** — Seeking public lectures, networking events, community outreach

### 4.2 Organizers
- Student club presidents and association leaders
- Academic staff and researchers
- University departments and faculties
- Research labs and innovation centers
- External communities (NGOs, innovation hubs, startup ecosystems, employers)

### 4.3 Platform Administrators
- Pelin (initially solo), expanding to a small moderation team

---

## 5. Target Institutions (Kigali Pilot)

| # | University | Abbreviation |
|---|---|---|
| 1 | African Leadership University | ALU |
| 2 | University of Rwanda | UR |
| 3 | Adventist University of Central Africa | AUCA |
| 4 | Carnegie Mellon University Africa | CMU Africa |
| 5 | University of Kigali | UOK |
| 6 | Mount Kigali University | MKU |
| 7 | Université Libre de Kigali | ULK |
| 8 | University of Technology and Arts of Byumba (Kigali campus) | UTAB |
| 9 | University of Lay Adventists of Kigali | UNILAK |
| 10 | Rwanda Polytechnic | RP |

---

## 6. Comprehensive Feature Specification

### 6.1 Event Discovery (Attendee-Facing)

**Discovery Feed:**
- Dynamic, paginated feed of upcoming events across all participating institutions
- Featured/promoted events section ("Happening in Kigali")
- Curated collections (e.g., "This Week in Kigali", "Research & Innovation", "Careers & Scholarships")

**Search & Filtering:**
- Full-text keyword search across event titles, descriptions, and tags
- Filter by: University, City, Category, Date range, Event format (In-Person / Virtual / Hybrid), Audience eligibility (Open / Academic-only / Institution-specific / Invite-only), Free vs. Paid
- Applied filters are visible as removable chips
- Empty states guide users back to broader discovery

**Event Detail Page:**
- Full description with rich text
- Banner image
- Date, time, and timezone
- Venue details (address, map embed) or virtual meeting link
- Schedule/agenda breakdown
- Speaker list with bios
- Capacity indicator and registration status
- Organizer card with verification badge
- "Add to Calendar" (.ics download)
- Social sharing (WhatsApp, X/Twitter, copy link)
- Related events suggestions
- "Report this event" flag link

**Virtual Event Link Visibility:**
- Virtual/hybrid join links are only revealed to users who have RSVPed, preventing link abuse

### 6.2 RSVP & Attendance Management

- One-click RSVP for logged-in users
- Organizer-defined capacity limits; automatic waitlist when capacity is reached
- `.ics` calendar file generated on RSVP
- Organizers see a real-time attendee list with RSVP counts
- Support for external registration links (e.g., Google Forms, Typeform) as an alternative to in-platform RSVP
- Users can cancel their RSVP at any time

**Organizer's implicit attendance:** An organizer is automatically considered an attendee of their own event (no self-RSVP needed), but cannot RSVP to their own event as an attendee.

### 6.3 User Accounts & Personalization

- Sign up / Sign in (email + password; OAuth with Google planned)
- Profile with optional university affiliation (not required — no university email gate)
- Interest selection during onboarding (categories they care about)
- Saved/bookmarked events
- Followed organizers and universities
- Personalized "Recommended for you" feed based on interests, follows, and past RSVPs
- Notification preferences

**No institutional email requirement:** Some Rwandan universities delay issuing student emails. Requiring them would be a barrier to adoption. Attendee verification (when needed) is handled at the event level, not the platform level.

### 6.4 Organizer Experience

**Organizer Profiles:**
- Public-facing page with: name, type (club, department, lab, community, etc.), institution affiliation, verification badge, bio, contact info, social links
- Upcoming events listing
- Past events archive
- Follower count

**Event Creation Wizard (Multi-step):**
- Step 1: Basic info (title, description, category, tags)
- Step 2: Date/time, location (physical address or virtual link), event format selection
- Step 3: Audience, capacity, registration method, banner upload
- Draft saving at any step
- Edit and unpublish after publishing

**Recurring Events:**
- Support for recurring event series (weekly, biweekly, monthly)
- Each occurrence is a distinct event instance but linked to a series
- Organizers can edit individual occurrences or the entire series

**Event Management Dashboard:**
- List of all events (draft, published, past, cancelled)
- RSVP/attendee list per event with export capability
- Basic analytics: page views, saves, RSVP count

### 6.5 Progressive Trust & Verification System

Instead of a binary verified/unverified model (which creates gatekeeping friction), the platform uses a **Progressive Trust** approach:

| Tier | Label | How It's Earned | Privileges |
|---|---|---|---|
| **Tier 1** | New Organizer | Automatic on profile creation | Can publish events; profile shows "New Organizer" label |
| **Tier 2** | Established | Automatic after 3+ events published without flags | "Established" badge; events may appear in featured sections |
| **Tier 3** | Verified | Manual verification by admin (proof: university website listing, social media page, email exchange) | Prominent verified checkmark; priority in search results and featured collections |

### 6.6 Event Moderation (Publish-First, Moderate Reactively)

- **Events go live immediately** upon publishing — zero friction for organizers
- Every event page has a "Report this event" link for community flagging
- Admin dashboard shows flagged events for review
- Admin actions: dismiss flag, unpublish event, warn organizer, ban organizer
- Optional: first event from a Tier 1 organizer has a 30-minute soft delay before appearing in the main feed
- Audit log for all moderation actions

### 6.7 Admin Dashboard

- Organizer verification request queue
- Flagged event review queue
- Category and taxonomy management (add/rename/merge categories)
- Featured event/collection curation
- University directory management
- Platform-wide analytics (active organizers, events published, RSVP rates, cross-university traffic)

### 6.8 Categories & Taxonomy

Categories are **admin-managed but expandable** — organizers select from a curated list, and can request new categories. Initial set:

| Category | Example Events |
|---|---|
| Technology & Computing | Hackathons, coding bootcamps, tech talks |
| Research & Innovation | Research presentations, paper discussions, lab open days |
| Entrepreneurship & Startups | Pitch competitions, startup weekends, founder talks |
| Careers & Professional Development | Career fairs, CV workshops, interview prep |
| Leadership & Governance | Student leadership summits, governance forums |
| Arts, Culture & Creativity | Exhibitions, poetry nights, film screenings |
| Health & Wellness | Mental health workshops, sports tournaments |
| Community Service & Social Impact | Volunteer drives, community outreach |
| Scholarships & Opportunities | Info sessions, application workshops, exchange programs |
| Science & Engineering | Lab demos, engineering expos, science fairs |
| Business & Finance | Investment talks, business case competitions |
| Languages & Humanities | Debate tournaments, language exchanges, book clubs |

### 6.9 Notifications

- RSVP confirmation email with `.ics` attachment
- Event reminder (24 hours before)
- New event alerts from followed organizers
- Updates/changes to RSVPed events
- Weekly digest of recommended events (opt-in)

### 6.10 Multi-Language Readiness

Architecturally planned for **English** (primary), **French**, and **Kinyarwanda**. Not implemented in v1, but:
- All user-facing strings are externalized (i18n-ready)
- Database schema supports multilingual event content
- Language preference stored in user profile

---

## 7. Technical Architecture

### 7.1 Stack Decision

| Layer | Technology | Rationale |
|---|---|---|
| **Backend API** | Django REST Framework (Python) | Founder expertise; mature ecosystem; excellent ORM for complex queries |
| **Frontend SPA** | React + TypeScript | Type safety; component reuse; large ecosystem; SPA for fluid UX |
| **Database** | PostgreSQL | Full-text search, JSON fields, robust relational model |
| **Infrastructure** | DigitalOcean VPS | Cost-effective; full control; suitable for solo founder |
| **File Storage** | DigitalOcean Spaces (S3-compatible) or local volume | Event banners, organizer avatars |
| **Email** | Transactional provider (e.g., Resend, Mailgun, or SendGrid free tier) | RSVP confirmations, reminders, digests |
| **Reverse Proxy** | Nginx | Static file serving, SSL termination, API proxying |
| **CI/CD** | GitHub Actions | Automated testing, linting, deployment |

### 7.2 High-Level Architecture

```
┌──────────────────────────────────────────────────┐
│                   Nginx (Reverse Proxy)           │
│              SSL Termination + Static Files       │
├──────────────────┬───────────────────────────────┤
│  React SPA       │  Django REST API              │
│  (Static Build)  │  /api/v1/*                    │
│                  │                               │
│  - Discovery     │  - Auth (JWT)                 │
│  - Event Detail  │  - Events CRUD                │
│  - Dashboards    │  - Organizers CRUD            │
│  - Auth Pages    │  - RSVP Management            │
│  - Admin Panel   │  - Search & Filtering         │
│                  │  - File Uploads               │
│                  │  - Notifications              │
│                  │  - Admin/Moderation           │
├──────────────────┴───────────────────────────────┤
│              PostgreSQL Database                  │
│       + Full-Text Search (pg_trgm / tsvector)    │
├──────────────────────────────────────────────────┤
│         DigitalOcean Spaces (File Storage)        │
└──────────────────────────────────────────────────┘
```

### 7.3 Core Data Model (Entities)

```
User
├── id, email, password_hash, full_name
├── avatar_url, bio
├── university_affiliation (FK → University, nullable)
├── interests (M2M → Category)
├── role (attendee | organizer | admin)
├── language_preference
├── notification_preferences (JSON)
└── timestamps

Organizer (extends User via OneToOne)
├── id, user (FK → User)
├── organizer_name, organizer_type (enum: club, department, lab, community, individual, institution)
├── institution_affiliation (FK → University, nullable)
├── trust_tier (enum: new, established, verified)
├── verification_proof_url
├── bio, contact_email, phone
├── social_links (JSON)
├── logo_url
├── is_active
└── timestamps

University
├── id, name, abbreviation, city, province
├── campus_address, latitude, longitude
├── website_url, logo_url
├── description
├── is_active
└── timestamps

Event
├── id, title, slug (unique)
├── description (rich text)
├── category (FK → Category)
├── tags (M2M → Tag)
├── organizer (FK → Organizer)
├── university_affiliation (FK → University, nullable)
├── city, venue_name, venue_address, latitude, longitude
├── virtual_link (visible only to RSVPed users)
├── event_format (enum: in_person, virtual, hybrid)
├── start_datetime, end_datetime, timezone
├── audience_eligibility (enum: open, academic_only, institution_specific, invite_only)
├── registration_type (enum: in_platform, external_link, none)
├── external_registration_url
├── capacity (nullable — null means unlimited)
├── banner_image_url
├── status (enum: draft, published, cancelled, past)
├── is_featured
├── series (FK → EventSeries, nullable)
└── timestamps

EventSeries
├── id, title, recurrence_rule (iCal RRULE string)
├── organizer (FK → Organizer)
└── timestamps

RSVP
├── id, user (FK → User), event (FK → Event)
├── status (enum: confirmed, waitlisted, cancelled)
├── rsvped_at
└── unique_together(user, event)

SavedEvent
├── id, user (FK → User), event (FK → Event)
├── saved_at
└── unique_together(user, event)

FollowedOrganizer
├── id, user (FK → User), organizer (FK → Organizer)
└── followed_at

Category
├── id, name, slug, icon, description, sort_order
└── is_active

Tag
├── id, name, slug
└── timestamps

FlagReport
├── id, reporter (FK → User), event (FK → Event)
├── reason (enum: spam, misleading, inappropriate, duplicate, other)
├── details (text)
├── status (enum: pending, dismissed, actioned)
├── reviewed_by (FK → User, nullable)
└── timestamps

VerificationRequest
├── id, organizer (FK → Organizer)
├── proof_url, proof_description
├── status (enum: pending, approved, rejected)
├── reviewed_by (FK → User, nullable), review_notes
└── timestamps
```

### 7.4 API Structure (Key Endpoints)

```
Auth:       POST /api/v1/auth/register | /login | /logout | /refresh
Users:      GET/PATCH /api/v1/users/me
Events:     GET /api/v1/events (list + search + filter)
            GET /api/v1/events/{slug}
            POST /api/v1/events (organizer)
            PATCH/DELETE /api/v1/events/{slug} (owner)
RSVPs:      POST/DELETE /api/v1/events/{slug}/rsvp
            GET /api/v1/events/{slug}/attendees (organizer)
Saved:      POST/DELETE /api/v1/events/{slug}/save
            GET /api/v1/users/me/saved-events
Organizers: GET /api/v1/organizers | /{id}
            POST /api/v1/organizers (become organizer)
            GET /api/v1/organizers/{id}/events
Follows:    POST/DELETE /api/v1/organizers/{id}/follow
Unis:       GET /api/v1/universities | /{id}
Categories: GET /api/v1/categories
Admin:      GET /api/v1/admin/flags | /verification-requests
            PATCH /api/v1/admin/flags/{id} | /verification-requests/{id}
Calendar:   GET /api/v1/events/{slug}/ics
```

---

## 8. Role-Based Access Control

| Capability | Guest | Attendee | Organizer | Admin |
|---|---|---|---|---|
| Browse events | ✅ | ✅ | ✅ | ✅ |
| Search & filter | ✅ | ✅ | ✅ | ✅ |
| View event detail | ✅ | ✅ | ✅ | ✅ |
| RSVP to event | ❌ | ✅ | ✅ | ✅ |
| Save/bookmark event | ❌ | ✅ | ✅ | ✅ |
| Follow organizer | ❌ | ✅ | ✅ | ✅ |
| Create organizer profile | ❌ | ✅ | — | ✅ |
| Publish events | ❌ | ❌ | ✅ | ✅ |
| View attendee list | ❌ | ❌ | ✅ (own events) | ✅ |
| Manage own events | ❌ | ❌ | ✅ | ✅ |
| Request verification | ❌ | ❌ | ✅ | — |
| Moderate flags | ❌ | ❌ | ❌ | ✅ |
| Approve verifications | ❌ | ❌ | ❌ | ✅ |
| Manage categories | ❌ | ❌ | ❌ | ✅ |
| View platform analytics | ❌ | ❌ | ❌ | ✅ |

---

## 9. Phased Delivery Plan

Given the solo-founder constraint and end-of-2026 deadline (~6 months), the build is structured into 4 phases:

### Phase 1: Foundation (Months 1–2)
**Goal:** Core backend + frontend scaffold + public browsing

- Django project setup with DRF, JWT auth, PostgreSQL
- React TS project with routing, layout shell, design system
- User registration, login, logout
- University seed data (10 Kigali institutions)
- Category seed data
- Event model with CRUD API
- Public event listing page with pagination
- Event detail page (read-only)
- Basic search (full-text) and category filtering
- Manual event seeding (15-20 real upcoming events)

**Milestone:** A stranger can visit the site, browse events, search, and view details.

### Phase 2: Participation Loop (Months 3–4)
**Goal:** Users can interact; organizers can publish

- User profiles with interests and university affiliation
- RSVP flow with capacity/waitlist logic
- `.ics` calendar export on RSVP
- Saved/bookmarked events
- Organizer profile creation (any user can become an organizer)
- Multi-step event creation wizard with drafts
- Event banner upload
- Organizer dashboard (my events, attendee lists)
- User dashboard (my RSVPs, saved events, followed organizers)
- Follow organizer functionality
- Recurring event series support

**Milestone:** The complete publish → discover → RSVP loop works end to end.

### Phase 3: Trust & Polish (Month 5)
**Goal:** Platform is trustworthy and production-ready

- Progressive Trust tier system (auto-promotion from New → Established)
- Verification request flow (organizer submits proof → admin reviews)
- Flag/report event functionality
- Admin moderation dashboard (flags, verifications, event management)
- Email notifications (RSVP confirmation, event reminders, organizer updates)
- University profile pages
- Featured events curation (admin)
- SEO meta tags and OpenGraph for social sharing
- Error handling, empty states, loading skeletons
- Mobile responsiveness audit

**Milestone:** The platform is ready for real users and can be demoed to university stakeholders.

### Phase 4: Launch & Growth (Month 6)
**Goal:** Ship it, seed content, and begin outreach

- Production deployment on DigitalOcean (Nginx, SSL, backups)
- Data seeding from university websites and social media
- Open-source repository preparation (see Section 11)
- Soft launch with ALU community and personal network
- Outreach to 3-5 club leaders to publish their next event
- Google Form bridge for event submissions from WhatsApp groups
- Basic analytics (platform-wide event/user counts for admin)
- Bug fixes and feedback iteration

**Milestone:** Live platform with real events, real users, and a public GitHub repository.

---

## 10. Launch & Adoption Strategy

**The #1 risk is non-adoption.** Mitigation plan:

### Content Bootstrap (Pre-Launch)
1. Manually curate 20-30 real upcoming events from university websites and social media pages of ALU, UR, CMU Africa, AUCA
2. Follow official Instagram/X/Facebook pages of target universities and their major clubs
3. Create a Google Form ("Submit your event to Academia Rwanda") for easy submissions

### Soft Launch (Week 1-2)
1. Share with personal ALU network and 3-5 club leaders directly
2. Ask those leaders to publish one real event each
3. Share in relevant academic WhatsApp groups with a specific event link (not just the homepage)

### Growth (Month 1-3 post-launch)
1. Approach university Student Affairs offices with a demo and value pitch
2. Position as a free tool that increases their event visibility
3. Highlight cross-university traffic data as proof of value
4. Write a short blog post: "Why Rwanda needs a shared academic event platform"

---

## 11. Open Source Strategy

Following industry best practices for community-driven open source projects:

### Repository Structure
```
rwanda-academic-hub/
├── backend/          # Django DRF project
├── frontend/         # React TS SPA
├── docs/             # Project documentation
├── .github/
│   ├── ISSUE_TEMPLATE/
│   ├── PULL_REQUEST_TEMPLATE.md
│   └── workflows/    # CI/CD
├── LICENSE            # MIT or Apache 2.0
├── README.md          # Project overview, setup guide, screenshots
├── CONTRIBUTING.md    # How to contribute
├── CODE_OF_CONDUCT.md # Community standards
├── CHANGELOG.md       # Version history
└── docker-compose.yml # One-command local development setup
```

### Key Practices
- **License:** MIT (maximum adoption) or Apache 2.0 (patent protection)
- **README:** Must include screenshots, quick-start guide, and architecture overview
- **CONTRIBUTING.md:** Clear guide covering local setup, coding standards, PR process
- **Issue Labels:** `good-first-issue`, `help-wanted`, `bug`, `feature-request`, `documentation`
- **Docker Compose:** One-command local dev setup (`docker compose up`) to minimize contributor friction
- **CI Pipeline:** Automated tests + linting on every PR via GitHub Actions
- **Semantic Versioning:** For releases once stable
- **Launch open-source after Phase 2** — the core loop works, contributors can see a functional product and contribute meaningfully

---

## 12. Non-Functional Requirements

| Requirement | Target |
|---|---|
| **Mobile-first** | All pages must be fully functional on mobile viewports |
| **Performance** | Initial page load < 3s on 3G connections |
| **Accessibility** | WCAG 2.1 AA compliance for forms and navigation |
| **i18n Readiness** | All strings externalized; schema supports multilingual content |
| **Security** | JWT auth, CORS policy, rate limiting, input sanitization, HTTPS only |
| **Backup** | Automated daily PostgreSQL backups |
| **Uptime** | 99% (acceptable for a community project on VPS) |

---

## 13. Success Metrics

| Metric | 3-Month Target | 6-Month Target |
|---|---|---|
| Universities represented | 5+ | 8+ |
| Active organizers | 10+ | 30+ |
| Events published/month | 15+ | 40+ |
| Registered users | 100+ | 500+ |
| Cross-university event views (%) | 30%+ | 50%+ |
| Monthly returning users | 20%+ | 35%+ |

---

## 14. Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Low organizer adoption | High | Critical | Manual content seeding; personal outreach to club leaders; Google Form bridge |
| Solo founder burnout | Medium | High | Phased delivery; AI-assisted development; open-source contributors post-launch |
| No open-source contributors | Medium | Medium | Docker one-command setup; `good-first-issue` labels; clear CONTRIBUTING.md |
| Spam/fake events | Low (initially) | Medium | Progressive Trust model; community flagging; reactive moderation |
| Low student awareness | High | High | WhatsApp/social media seeding with specific event links, not just homepage |
| University resistance to external platform | Medium | Medium | Position as complementary visibility tool, not a replacement for internal systems |

---

## 15. Competitive Positioning

| Alternative | Weakness Rwanda Academic Hub Addresses |
|---|---|
| **University-specific apps** | Siloed; no cross-campus visibility |
| **WhatsApp groups** | Ephemeral; no search/filter; information overload |
| **Eventbrite** | Not academic-focused; paid features; not Rwanda-specific |
| **Facebook Events** | Requires Facebook account; poor discoverability; no academic trust layer |
| **Notice boards / emails** | Not accessible outside the institution |

**Rwanda Academic Hub's positioning:** The only platform purpose-built for cross-university academic event discovery in Rwanda, with a trust system designed for the academic context.
