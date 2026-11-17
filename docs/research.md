# Research Document — CampusCare

> **Status:** Initial desk research. No field visit has been conducted yet.
> All statements marked [ASSUMPTION] have not been verified by fieldwork.
> Statements marked [VERIFIED] are drawn from published sources cited below.

---

## Problem Hypothesis

[ASSUMPTION] Hostel maintenance complaints at NIT Jamshedpur are currently
logged informally — through WhatsApp messages, verbal reports to wardens, or
handwritten registers — with no centralised tracking.

[ASSUMPTION] The absence of a formal complaint lifecycle (submitted → assigned
→ in-progress → resolved) means issues can remain unacknowledged for extended
periods, and neither students nor staff have a shared view of outstanding work.

[ASSUMPTION] Staff workload is unevenly distributed because there is no
priority-scoring mechanism: a leaking pipe and a broken fan receive equal
treatment until someone escalates manually.

[ASSUMPTION] Resolution times and recurring problem categories are not recorded,
so the hostel administration cannot make data-driven decisions about maintenance
budgets or staff allocation.

[ASSUMPTION] A lightweight, CSV-backed Streamlit application accessible on any
browser — requiring no installation by residents or staff — could lower the
barrier to formal complaint logging and generate the first useful maintenance
dataset for the hostel.

---

## Existing Solutions

### 1. FixMyStreet Platform (mySociety)

FixMyStreet is a free, open-source platform that lets people report local
infrastructure problems. A resident pins a problem on a map and the system
routes the report to the correct authority by email or via the Open311 API.
Reports are public and trackable.

**Why it may not fit this context:**

- Designed for geographic, street-level problems in public spaces, not for
  indoor room-by-room issues inside a hostel building.
- Requires a persistent server, database, and administrator to map problem
  categories to the correct hostel department — significant setup overhead for
  a warden or maintenance clerk with limited technical capacity.
- The public-report model may not be appropriate for an institutional setting
  where complaint ownership and staff accountability need to be internal.

**Sources:** [fixmystreet.org](https://fixmystreet.org/) and
[IADB Open Knowledge entry](https://knowledge.iadb.org/en/open-knowledge/code-development/open-source-solution/fixmystreet)

---

### 2. OpenEduCat Hostel Management Module

OpenEduCat is a campus management ERP built on Odoo that covers room
allocation, complaint management with photo uploads, mess billing, and visitor
registration. Wardens manage everything from a mobile dashboard.

**Why it may not fit this context:**

- It is a full ERP suite; deploying even one module requires Odoo server
  installation, a PostgreSQL database, and ongoing system administration —
  a disproportionate investment for a single hostel's maintenance tracking need.
- Licensing and hosting costs are non-trivial for an institution that currently
  uses no digital tool at all.
- Complex UIs optimised for administrative staff may be harder for a maintenance
  clerk who is accustomed to paper registers and WhatsApp.

**Source:** [openeducat.org — Hostel Management System](https://openeducat.org/solutions/hostel-management-system/)

---

## Source Notes

### Source 1 — FixMyStreet Platform (fixmystreet.org)

[VERIFIED] FixMyStreet is an open-source, map-based reporting platform
originally developed by mySociety in the UK. It routes citizen-submitted problem
reports to the responsible authority using geographic boundaries and the Open311
standard. The platform has been deployed in multiple countries and is freely
available under an open-source licence.

The platform's design is civic and geographic: it is built for public streets,
not private institutional premises. This makes it a useful reference point for
understanding what a complaint lifecycle looks like technically, but not a
direct fit for a hostel context.

The source is current (official project site, accessed November 2026) and
authoritative (maintained by the original developer organisation).

---

### Source 2 — DHMS: A Digital Hostel Management System (arXiv:2507.17759)

[VERIFIED] A peer-reviewed paper published on arXiv describing a Digital Hostel
Management System (DHMS) that integrates AI, cloud infrastructure, and a
natural-language chatbot for grievance redressal and room allotment automation.

The paper confirms [VERIFIED] that existing hostel management processes —
including complaint handling — are "often inefficient and susceptible to errors"
when managed manually, and that digitisation is a recognised research problem in
the academic hostel context.

The system described is significantly more complex (AI, cloud, chatbot) than
what a 24-hour assignment can deliver; it validates the problem domain but does
not provide a reusable implementation.

**URL:** https://arxiv.org/pdf/2507.17759v1

---

## Open Questions (to be answered by fieldwork)

- [ ] How does the hostel currently log complaints? (register, WhatsApp, verbal?)
- [ ] Who is the primary point of contact for maintenance — warden or dedicated clerk?
- [ ] What is the most common category of complaint?
- [ ] What is the typical time between complaint and resolution?
- [ ] Is there any existing digital tool, however informal, in use?
