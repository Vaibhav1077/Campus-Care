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
- Higher-tier plans with automation and analytics features carry a subscription cost; free or low-cost plans may lack the workflow capabilities a hostel management system needs.
- Has no built-in concept of hostel blocks, room numbers, or physical location-based complaint grouping — these would require custom fields and configuration.
- Students must navigate an interface designed for business users, which may require additional guidance in a college setting.

### Solution 2 — FixMyStreet (civic issue reporting platform)

FixMyStreet is an open-source platform originally built for UK residents to report public infrastructure problems such as potholes, broken streetlights, and vandalism to local councils.
It allows photo uploads, location pinning on a map, and public visibility of reported issues.
Some institutions have explored adapting it for campus or facility management.

**Limitations in a hostel context:**
- Built around geographic maps and public streets; adapting it for indoor hostel rooms and blocks would require significant customisation.
- Complaints are publicly visible by default, which may not be appropriate for internal hostel issues without reconfiguration.
- The platform does not include built-in role-based access for maintenance staff versus students, or a staff assignment and resolution workflow out of the box.
- Deployment and customisation require technical effort that may not be available in a small college hostel setting.

---

## 3. Why Existing Solutions Are Not Enough

Both Freshdesk and FixMyStreet were built for different audiences and scales. Freshdesk is a business helpdesk tool whose terminology and configuration model does not map cleanly to hostel operations. FixMyStreet is designed for outdoor, map-based, public reporting, which is incompatible with the room-and-block structure of a hostel without substantial modification.

Neither solution provides out of the box:
- A student-facing form scoped to hostel blocks and room numbers
- Automatic priority classification based on complaint category and age
- An admin view tailored for maintenance wardens rather than customer support managers
- Detection of recurring issues in the same room or block to flag systemic problems
- Lightweight file-based storage that works without a database server

CampusCare uses CSV files as its own implementation choice for data storage — a deliberate decision to keep the system deployable without a database server or IT infrastructure. This is not a recommendation from any external source; it reflects the practical constraints of a small-scale hostel setting.

---

## 4. Sources and Research Notes

### Source 1

- **Title:** Smart Complaint Management System
- **Authors:** Malaika Sameer Sayyed, Sumit Navnath Pokale, Arpit Rajesh Gupta, Sakshi Hanumant Bhange, Dr. Sivaram Ponnusamy, Umesh Pawar
- **Published in:** Iconic Research and Engineering Journals, Vol. 9, Issue 11, May 2026
- **DOI:** https://doi.org/10.64388/IREV9I11-1717450
- **URL:** https://www.irejournals.com/paper-details/1717450

**Research Notes:**
1. The abstract states that traditional complaint management systems in educational institutions are often inefficient, lack transparency, and fail to provide timely resolution — directly supporting the problem CampusCare is designed to address.
2. The paper proposes a centralized platform with role-based access control and workflow automation; CampusCare adopts the same design principles through its separate student and admin roles.
3. The abstract identifies improvements in complaint resolution time and system transparency as the primary outcomes, which correspond to CampusCare's status tracking and priority classification features.

---

### Source 2

- **Title:** Design and Implementation of Automated Secure Web-Based Hostel Management System with Automated Room Allocation and Complaint Tracking
- **Published in:** Global Journal of Engineering and Technology Advances (GJETA), 2026, Vol. 26, Issue 2
- **URL:** https://gjeta.com/sites/default/files/fulltext_pdf/GJETA-2025-0345.pdf

**Research Notes:**
1. The abstract states that traditional manual processes for hostel operations — including complaint handling — are often inefficient and susceptible to errors, supporting the case for a structured digital system.
2. The paper identifies complaint tracking as a core functional module within hostel management systems, alongside room allocation and student registration.
3. The work confirms that hostel-specific complaint management is an active area of applied research, and that automating the complaint lifecycle (submission, tracking, resolution) is a recognised technical goal in this domain.

---

## 5. Why CampusCare?

CampusCare addresses a narrow, well-defined problem: a student in a hostel should be able to report a maintenance issue in under a minute, and a warden should be able to see all open complaints, prioritise them, assign them, and mark them resolved — all without installing server software, paying for a subscription, or training staff on a complex platform.

The system is scoped specifically to hostel operations. It uses room numbers and hostel blocks as first-class fields, applies automatic priority classification based on complaint category and age, and flags recurring issues in the same location. These are not features found in generic helpdesk tools without custom configuration.

The choice to store data in CSV files is CampusCare's own implementation decision, made to keep the system deployable by a single person with no IT infrastructure — practical for college hostels that lack dedicated technical support staff.

> **Note:** The research above is based on published academic sources and product documentation. No field observations, student interviews, or primary data collection have been conducted as part of this research step.
