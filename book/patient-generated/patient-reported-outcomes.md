---
layout: book
title: "Patient-Reported Outcomes"
description: "PROMIS and the PHQ-9: the validated instruments that measure health from the patient's point of view."
permalink: /book/patient-generated/patient-reported-outcomes/
---

Every data stream so far measures the patient from the outside—what a machine recorded, what a clinician documented, what a pharmacy dispensed. Patient-reported outcomes are the one stream that measures the patient from the *inside*: symptoms, function, and quality of life as reported directly by the patient, with no clinician interpretation in between. A lab can tell you a cancer patient's neutrophil count; only the patient can tell you whether they are too fatigued to get out of bed. As healthcare shifts toward valuing outcomes that matter to patients, PROs have moved from a research niche toward routine clinical data.

The important thing to understand is that a PRO is not casual free text. Usable PRO data comes from validated instruments: standardized questionnaires whose scoring and psychometric properties have been formally established, so that a score means the same thing across patients and over time. Two instruments are worth knowing in detail.

## PROMIS

PROMIS (Patient-Reported Outcomes Measurement Information System) is an NIH-funded family of measures designed to be a common metric for self-reported health across conditions. Rather than a single fixed questionnaire, PROMIS is organized into item banks—large calibrated pools of questions—covering domains like physical function, fatigue, pain interference, sleep disturbance, depression, and anxiety.

Two design features make PROMIS distinctive. First, scores are reported on a standardized T-score metric, calibrated so that 50 is the mean of a reference population and 10 points is one standard deviation. That means a fatigue T-score of 60 is immediately interpretable—one SD worse than average—and is comparable across studies and populations, which is exactly what most homegrown symptom scales fail to deliver. Second, because the items are calibrated to an underlying trait, PROMIS supports computer-adaptive testing (CAT): the software picks each next question based on prior answers, so a precise score can be obtained from a handful of items instead of a long fixed form. The result is a flexible, comparable, low-burden measurement system—at the cost of more machinery (item banks, calibration, scoring engines) than a simple sum-the-answers questionnaire.

## PHQ9

The PHQ-9 (Patient Health Questionnaire–9) is the opposite of PROMIS in spirit: a short, fixed, free, ubiquitous instrument that does one job extremely well. Its nine items map directly onto the nine DSM criteria for depression; each is scored 0–3 based on how often the patient has been bothered by that symptom over the past two weeks, giving a total of 0–27.  A two-item pre-screen, the PHQ-2, is often administered first, with a positive result triggering the full nine.

For data teams, the PHQ-9 is a model of what makes a PRO analytically usable. It produces a single validated numeric score with well-defined cutoffs; it is repeated over time, so it yields a trajectory rather than a snapshot (a patient's PHQ-9 falling from 16 to 8 over three months is a legible treatment response); and both the individual items and the total score carry LOINC codes, so in a well-run EHR they land in structured, queryable fields rather than buried in a note.[^1]This is precisely the data behind the "moderate depression" patient introduced in the multimodal chapter, and it is what lets a collaborative-care program track a whole panel of patients by score.

The caveat with PROs is administration, not measurement. The instruments are sound; whether they get *given*—consistently, to the right patients, at regular intervals—is not. PRO data is frequently missing, and the missingness is rarely random (sicker or less-engaged patients skip surveys), so an analyst must treat gaps as informative rather than ignorable. A validated instrument administered haphazardly still produces biased data.

[^1]: Example: https://loinc.org/44249-1
