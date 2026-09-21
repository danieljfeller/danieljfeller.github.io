---
layout: book
title: "Clinical Trial Data"
description: "Case report forms, EDC systems, and the CDISC pipeline (CDASH, SDTM, ADaM) that regulators require."
permalink: /book/clinical/clinical-trials/
---

Most of the data streams in this book are *observational* and generated as a byproduct of healthcare delivery. In contrast, clinical trial data is collected under strict protocols in order to test a specific hypothesis about whether a treatment is safe and effective.This results in data that is much more structured and standardized than other data streams. The nature of the data collected varies on the *phase* of the clinical trial:

- Phase I: safety and dosing in a small group.

- Phase II: efficacy signal and side effects.

- Phase III: large, often randomized and controlled confirmatory trials that support approval.

- Phase IV: post-market surveillance.

Phases I-III are all similar in that data is prospectively collected, whereas Phase IV relies on retrospectively collected data from claims and EHRs. This chapter will focus on Phases I-III, as the data associated with Phase IV trials is described in the chapters on administrative claims and EHRs.

## What the data actually looks like

### Data Collection

Most clinical trial data is captured on Case Report Forms (CRFs) entered into EDC (Electronic Data Capture) systems such as Medidata Rave or Veeva Vault. CRFs are populated by clinical trial coordinators at each site and capture demographics, medical history, vital signs, laboratory results, and other variables that might impact safety and efficacy outcomes.The CRFs used in each trial are specific to that trial and collect relevant safety and efficacy information. Case report forms are usually constructed directly from SDTM domains and CDISC vocabularies before data collection starts.

<figure>
  <img src="{{ '/images/book/ecrf-components.svg' | relative_url }}" alt="Annotated mock-up of an electronic case report form for laboratory results showing a form label, group labels for renal and hepatic panels, item labels, entry fields with values, a yes/no toggle, and a data-validation message flagging an out-of-range value">
  <figcaption>Anatomy of an electronic case report form (eCRF) in an EDC system. A form (here, laboratory results) is organized into groups of items; each item has a label, a hint describing the expected units, and a field holding the entered value. Edit checks run as data is entered, so an out-of-range value raises a query for the site coordinator to resolve. Illustrative form; values are synthetic.</figcaption>
</figure>

In most modern clinical trials, laboratory and imaging results bypass manual CRF entry into EDC systems because they provide structured data that is transferred directly into clinical databases via SFTP or API feeds. If there is no direct integration between a site’s laboratory information system (LIS) and the clinical database, study coordinators at each clinical site will populate CRFs with relevant results (e.g. serum creatinine to assess liver function).

### Data Preparation

But the reason clinical trial data deserves its own chapter is CDISC, the Clinical Data Interchange Standards Consortium, whose standards the FDA and other regulators now effectively *require* for submission. CDISC is best understood as a pipeline of three standards:

- CDASH:  standards for how data is *collected* on the CRF.

- SDTM (Study Data Tabulation Model) — the standard for how *collected* data is organized for submission. This is the one to know.

- ADaM (Analysis Data Model): Analysis-ready datasets derived from SDTM, structured to support the specific statistical analyses in the study.

SDTM organizes every observation into domains, each a table with a two-letter code and one record per observation. A working analyst will recognize:

| Domain | Contents |
|---|---|
| DM | Demographics (one row per subject) |
| AE | Adverse Events |
| CM | Concomitant Medications |
| EX | Exposure (study drug actually given) |
| LB | Laboratory results |
| VS | Vital Signs |
| MH | Medical History |
| DS | Disposition (did the subject complete/withdraw) |

Two controlled vocabularies dominate inside these domains and are worth committing to memory: MedDRA codes adverse events (the same terminology introduced in Part I's advanced-vocabulary table), and WHODrug codes concomitant medications. Alongside the datasets, a Define-XML file acts as the machine-readable data dictionary that describes the submitted structure to the regulator.

## How it's used, and its trade-offs

Trial data flows to regulators (the FDA's electronic submissions), to the sponsors who run the trials, and sometimes to the public through ClinicalTrials.gov, which records trial designs and, increasingly, results. Because trials are conducted under Good Clinical Practice with monitoring and source-data verification, the data quality is the highest in this book: fields are complete, values are checked against source documents, and the provenance is auditable.

The trade-offs are the flip side of that rigor, and they are exactly why the observational streams in this book exist at all. Trials are slow and expensive; their strict eligibility criteria mean the enrolled population often looks little like the patients who will actually receive the drug (the classic external-validity problem); and they end, so they say nothing about long-term or rare effects that only emerge across millions of real-world patients. This is the tension the whole field lives in: trials give you clean causal answers about a narrow population, and real-world data (claims, EHR, pharmacy) gives you messy, confounded answers about everyone. Modern evidence generation increasingly tries to get both, hence the growth of real-world evidence to complement, and sometimes extend, the trial.

## Quick Reference: Clinical Trial Data

| Data Stream | Clinical Trial Data (CDISC / SDTM) |
|---|---|
| Description | Prospectively collected, protocol-driven data testing the safety and efficacy of an intervention; the most rigorously standardized data in healthcare |
| Data Generating Process | Data captured on CRFs into EDC systems under a study protocol and Good Clinical Practice, then transformed into CDISC SDTM (tabulation) and ADaM (analysis) datasets for regulatory submission |
| Access & Availability | Owned by sponsors (pharma/biotech/CROs). Public: ClinicalTrials.gov registrations and results; some data-sharing platforms (e.g., Vivli, YODA) for de-identified patient-level data. Regulatory submissions are confidential |
| Key Data Elements | Subject ID, treatment arm, demographics (DM), adverse events (AE), exposure (EX), labs (LB), vitals (VS), disposition (DS), visit/timing variables |
| Data Models | CDISC: CDASH (collection), SDTM (tabulation), ADaM (analysis), Define-XML (metadata) |
| Standard Vocabularies | MedDRA (adverse events), WHODrug (medications), plus CDISC Controlled Terminology; LOINC/SNOMED in some domains |
| Data Storage | EDC databases during conduct; SAS transport (XPT) datasets for SDTM/ADaM submission; increasingly cloud clinical data platforms |
| Expected Data Quality | Highest in healthcare—monitored, source-verified, near-complete—at the cost of speed, expense, and limited real-world generalizability |
| Integration Considerations | Standardized within CDISC but siloed by study/sponsor; linking trial subjects to real-world data is rare and consent-dependent; external validity limits pooling with observational data |
| Further Resources | CDISC standards (cdisc.org); FDA Study Data Technical Conformance Guide; ClinicalTrials.gov |
