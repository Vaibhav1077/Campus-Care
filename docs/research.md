# CampusCare – Problem Research

## 1. Problem Statement

Hostels in colleges typically handle maintenance complaints through verbal requests, paper registers, or informal WhatsApp messages sent to wardens.
There is no structured way for students to submit, track, or follow up on issues such as broken fans, water leakage, or faulty electrical fixtures.
Maintenance staff have no central view of pending work, which leads to complaints being forgotten, duplicated, or resolved without documentation.
Without priority classification, urgent safety issues like electrical faults are treated the same as low-impact requests like a missing lightbulb.
The result is student frustration, repeated complaints about the same recurring problems, and no data available to identify systemic maintenance failures.

---

## 2. Existing Solutions

### Solution 1 — Freshdesk (helpdesk SaaS platform)

Freshdesk is a commercial customer support and ticketing platform used by businesses and some educational institutions to manage complaints and service requests.
It supports ticket creation, status tracking, agent assignment, priority levels, and reporting dashboards.
Some universities use it as a general-purpose complaint system for IT helpdesks or student services.

**Limitations in a hostel context:**
- Designed for customer support teams, not hostel maintenance workflows. Concepts like "agents", "SLA policies", and "CSAT surveys" do not map naturally to a warden-student context.
- Requires paid subscription and IT setup; not viable for a small hostel with limited budget.
- Has no concept of hostel blocks, room numbers, or physical location-based complaint grouping.
- Students must create accounts and navigate a complex interface designed for business users.

### Solution 2 — FixMyStreet (civic issue reporting platform)

FixMyStreet is an open-source platform originally built for UK residents to report public infrastructure problems such as potholes, broken streetlights, and vandalism to local councils.
It allows photo uploads, location pinning on a map, and public visibility of reported issues.
Some institutions have explored adapting it for campus or facility management.

**Limitations in a hostel context:**
- Built around geographic maps and public streets, not indoor hostel rooms or blocks.
- Complaints are publicly visible by default, which may not be appropriate for internal hostel issues.
- No role-based access for maintenance staff versus students; no built-in assignment or resolution workflow.
- Requires significant customisation to work in a closed institutional environment.

---

## 3. Why Existing Solutions Are Not Enough

Both Freshdesk and FixMyStreet were built for different audiences and scales. Freshdesk is enterprise software with pricing and complexity that far exceeds what a hostel needs. FixMyStreet assumes outdoor, map-based, public reporting, which is incompatible with the room-and-block structure of a hostel.

Neither solution provides:
- A simple student-facing form scoped to hostel blocks and room numbers
- Automatic priority classification based on complaint category and age
- An admin view tailored for maintenance wardens rather than customer support managers
- Detection of recurring issues in the same room or block to flag systemic problems
- Lightweight CSV-based data storage that works without a database server

A hostel-specific tool that handles these concerns without requiring subscriptions, servers, or IT departments is a practical gap worth filling.

---

## 4. Sources and Research Notes

### Source 1

- **Title:** Smart Complaint Management System
- **Authors:** Malaika Sameer Sayyed, Sumit Navnath Pokale, Arpit Rajesh Gupta, Sakshi Hanumant Bhange, Dr. Sivaram Ponnusamy, Umesh Pawar
- **Published in:** Iconic Research and Engineering Journals, Vol. 9, Issue 11, May 2026
- **DOI:** https://doi.org/10.64388/IREV9I11-1717450
- **URL:** https://www.irejournals.com/paper-details/1717450

**Research Notes:**
1. The paper directly states that traditional complaint management systems in educational institutions are often inefficient, lack transparency, and fail to provide timely resolution — this supports the core problem CampusCare addresses.
2. The proposed system in this paper uses role-based access control and workflow automation, the same design approach taken in CampusCare's student and admin role separation.
3. The paper identifies complaint resolution time and system transparency as the two key metrics for evaluating such systems, which aligns with CampusCare's status tracking and priority engine features.

---

### Source 2

- **Title:** Design and Implementation of Automated Secure Web-Based Hostel Management System with Automated Room Allocation and Complaint Tracking
- **Published in:** Global Journal of Engineering and Technology Advances (GJETA), 2025
- **URL:** https://gjeta.com/sites/default/files/fulltext_pdf/GJETA-2025-0345.pdf

**Research Notes:**
1. The paper identifies that traditional manual processes for hostel complaint handling are inefficient and error-prone, and argues that a digital system is necessary even at smaller institutions.
2. It specifically covers complaint tracking as a core module within hostel management, confirming that complaint submission and status updates are the two most requested features by students in hostel settings.
3. The paper notes that most existing hostel systems are over-engineered for small campuses, which supports CampusCare's decision to use lightweight CSV storage rather than a full database.

---

## 5. Why CampusCare?

CampusCare addresses a narrow, well-defined problem: a student in a hostel should be able to report a maintenance issue in under a minute, and a warden should be able to see all open complaints, prioritise them, assign them, and mark them resolved — all without installing server software, paying for a subscription, or training staff on a complex platform.

The system is scoped specifically to hostel operations. It uses room numbers and hostel blocks as first-class fields, applies automatic priority classification based on complaint category and age, and flags recurring issues in the same location. These are not features found in generic helpdesk tools.

By running as a local Streamlit application with CSV storage, CampusCare can be deployed by a single person with no IT infrastructure, making it practical for college hostels that lack technical support staff.

> **Note:** The research above is based on published academic sources and product documentation. No field observations, student interviews, or primary data collection have been conducted as part of this research step.
