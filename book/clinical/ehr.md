---
layout: book
title: "Electronic Health Records"
description: "A day in the life of a patient record, every structured, semi-structured, and unstructured data type in the EHR, and when to use FHIR versus OMOP."
permalink: /book/clinical/ehr/
---

The following is a wild story from a blog post written by CT Lin, MD. At the University of Colorado Hospital in Denver in the 1990s, the medical records department maintained a “records room” in the basement with 29 aisles of paper charts.[^1] That basement room held only about three years’ worth of charts and older records were stored off-site in a warehouse. Every day an average of 6 vertical feet of new records were generated and a staff of about fifty people worked full-time pulling, filing, sorting, and managing stacks of charts.

Compared to 30 years ago, today’s Electronic Health Records (EHRs) represent a vast improvement on the era of paper records. Healthcare providers today have faster access to information, improved continuity of care, and relief from the physical and administrative burden of paper-based documentation. However, many doctors find electronic health records frustrating because EHR interfaces are often poorly designed and frequent performance issues can inhibit productivity. A 2024 study found that more than one-quarter of clinicians report feeling dissatisfied with their EHR system.[^2]

## A Day in the Life of An Electronic Patient Record

One of the first lessons that graduate students are taught in academic medical informatics progress is to consider the *data generating process* when working with data from EHRs.

The best way to understand the content of electronic health records is to consider the *data generating process*. A routine outpatient visit without imaging might produce only a few megabytes of structured and unstructured data, while encounters involving medical imaging can generate hundreds of megabytes or even gigabytes - a single chest X-ray may be 15 megabytes, a 3D mammogram can be 300 megabytes, and a digital pathology file can be 3 gigabytes [HealthTech](https://healthtechmagazine.net/article/2023/05/structured-vs-unstructured-data-in-healthcare-perfcon). Regardless of volume, even a simple visit creates data that flows into dozens of different database tables, documents, and systems throughout the healthcare organization's IT infrastructure.

### Ambulatory Visit

Jasmine Williams, a 32-year-old software engineer, arrives at her primary care clinic for her annual wellness visit. She checks in at the front desk for her 10:00 AM appointment, updating her insurance information and confirming her contact details. After a brief wait, a medical assistant brings her back at 10:08 AM, where vital signs are collected: blood pressure 118/76, heart rate 68, temperature 98.4°F, height 5'6", weight 142 lbs. The medical assistant enters all of the information into a computer terminal on wheels that she takes with her as she leaves the room and remarks that the doctor will be in shortly.

Dr. Martinez enters at 10:15 AM and introduces herself to Jasmine. Dr. Martinez sits on a rolling stool in front of a wall-mounted computer monitor, opens her ambient AI scribe app on her iPhone, selects ‘Record’ and then places the iPhone next to the computer keyboard, and then   begins asking questions to Jasmine about her health. The patient reports no current concerns, takes no medications except occasional ibuprofen for menstrual cramps, and has no known allergies. She doesn't consume alcohol, uses cannabis in edible form 2-3 times per week, doesn't smoke tobacco, exercises 4-5 times weekly, and is sexually active with one partner with whom she uses oral contraceptives. Her family history is significant for type 2 diabetes in her father (diagnosed at age 58) and breast cancer in her maternal grandmother (at age 65). Dr. Martinez performs a physical exam for approximately 5 minutes and finds no abnormalities.

Dr. Martinez turns on the computer monitor, opens the Epic EHR, and navigates to the Orders tab within Jasmine's chart. She searches for "Annual Physical Labs" in the order search bar, which brings up a pre-built order set[^3] titled "Adult Preventive Care Labs - Female (18-39)" that her practice has configured. Dr. Martinez clicks on the order set, which automatically selects the following tests as a bundle:

- CBC with differential

- Comprehensive metabolic panel (CMP)

- Lipid panel

- Hemoglobin A1c

- TSH

The order set also has optional checkboxes for additional tests like Vitamin D, urinalysis, and STI screening, which Dr. Martinez leaves unchecked since they're not indicated for Jasmine at this visit. She verifies the performing laboratory is set to Quest Diagnostics (the default for her practice), confirms the order priority is "Routine," and notes that the orders are valid for 30 days.

Dr. Martinez adds "Family history of diabetes" as the indication for the HbA1c test in the free-text field. She reviews the order summary screen showing all five tests grouped together, then clicks "Sign Orders" at 10:28 AM. The orders are electronically transmitted to Quest Diagnostics and also generate a lab requisition that Jasmine can take to any Quest location. The system automatically creates pending result placeholders in the flowsheet for each test, which will populate when Quest sends results back via HL7 interface.

Later that evening, at 6:45 PM after finishing her patient appointments, Dr. Martinez reviews the ambient scribe's AI-generated draft note on her computer using the web scribe’s web application. The draft has automatically populated the HPI, review of systems, physical exam template, and assessment/plan sections based on the recorded conversation. Dr. Martinez copies and pastes the note into the Epic Electronic Health Record and edits the note for accuracy, adds specific physical exam details that weren't captured verbally (such as "peripheral pulses 2+ bilaterally"), verifies the family history coding is correct, and ensures the plan reflects her clinical reasoning. She signs and locks the note at 7:02 PM. The visit is coded as 99395 (preventive visit, 18-39 years) and closes without any diagnoses requiring ongoing management.

#### Summary of Data Created by Jasmine’s Office Visit

The clinical data from Jasmine's preventive care visit is stored across multiple interconnected tables within Epic's Clarity data warehouse, with structured information captured in relational database tables and unstructured clinical documentation stored separately. Below are the specific tables that Jasmine's visit touched, split into the structured records that live in relational tables and the unstructured note content that is stored on its own.

| Structured Data<br>*Epic Clarity Data Warehouse* | PAT_ENC: 1 row added; includes basic details about the patient encounter<br>PAT_ENC_HSP: 1 row added; includes additional encounter details  IP_FLWSHT_MEAS (Flowsheet Measurements; for vital signs): 7 rows added; includes BP systolic, BP diastolic, pulse, temp, RR, height, weight)<br>SOCIAL_HX (Social History): 5 rows added; includes Jasmine’s tobacco, alcohol, cannabis, exercise, and sexual activity<br>FAMILY_HX (Family History): 2 rows added; includes father's diabetes and grandmother's breast cancer<br>ORDER_PROC (Orders): 5 rows added; one for each lab test ordered<br>NOTE_ENC_INFO: 1 row added; connects Jasmine’s encounter to clinical free-text note<br>ARPB_TRANSACTIONS: 1 row added for procedure code 99395  *Additional metadata tables were modified that are not listed here.* |
|---|---|
| Unstructured Data | HNO_INFO: 1 row added with the metadata for the clinical note  NOTE_TEXT  1 row added with the actual text of the note |

### Multi-day Hospitalization

Robert Chen, a 67-year-old retired postal worker, arrives at the emergency department at 2:47 AM on a Tuesday morning via ambulance. His wife called 911 after finding him sitting upright in bed, gasping for air, with his lips appearing slightly blue. The paramedics note his oxygen saturation is 84% on room air, blood pressure 168/95, heart rate 112 and irregular, respiratory rate 28. They place him on 4 liters of oxygen via nasal cannula and establish IV access during transport.

*Admission*

Upon arrival, the ED registration clerk creates a new encounter in Epic while the triage nurse brings Robert directly to a critical care bay. She removes his shirt to place cardiac monitor leads and oxygen saturation probe, documenting his initial vital signs at 2:52 AM: blood pressure 172/98, heart rate 118 (irregular), respiratory rate 26, oxygen saturation 89% on 4 liters nasal cannula, temperature 98.1°F. She opens Epic's ED flowsheet and documents his chief complaint as "shortness of breath," marks his acuity as ESI Level 2 (Emergency Severity Index; 1 is the most severe and 5 the least severe).

Dr. Sarah Williams, the ED attending, enters the room at 2:58 AM. Robert, speaking in fragmented sentences between breaths, reports he's had three days of progressive shortness of breath, worsening leg swelling, and has been sleeping propped up on four pillows. He ran out of his "water pill" two weeks ago and didn't refill it.[^4] He has a history of heart failure, coronary artery disease with prior myocardial infarction (heart attack) in 2019, hypertension, type 2 diabetes, and a 40-pack-year smoking history though he quit five years ago. Current medications include metoprolol, lisinopril, atorvastatin, metformin, and furosemide. No known drug allergies.

The ED nurse draws blood at 3:05 AM for a complete blood count (to check red and white blood cells), a comprehensive metabolic panel (to check kidney function, electrolytes, and blood sugar), troponin (a protein that indicates heart muscle damage), and BNP (a hormone that shows how much strain the heart is under), and establishes a second IV line. A portable chest X-ray is performed at 3:12 AM showing fluid around both lungs and fluid inside the lung tissue itself. An electrocardiogram at 3:15 AM shows an irregular heart rhythm called atrial fibrillation with the heart beating too fast at 118 beats per minute. Dr. Williams orders furosemide 40 milligrams intravenously (diuretic given through the IV to help remove excess fluid), initiates a nitroglycerin drip (a medication that helps open up blood vessels and reduce the heart's workload), and starts continuous heart monitoring. She places orders for a heart specialist to see Robert and for admission to the telemetry unit (a hospital floor where patients' heart rhythms are monitored continuously).

*Hospitalization*

At 6:30 AM, after receiving diuretics and seeing improvement (O2 sat now 94% on 2L, respiratory rate 18), Robert is transferred to the 4th floor telemetry unit. The admitting hospitalist, Dr. James Martinez, receives a text page notification through Epic's secure messaging system and heads to Robert’s room at 7:15 AM to perform an assessment.

Dr. Martinez sits on a rolling stool next to Robert's bed, his smartphone recording the conversation. Robert reports feeling "much better" but still short of breath with minimal exertion. Dr. Martinez performs a comprehensive history and physical examination, noting 3+ pitting edema to the knees bilaterally, bibasilar crackles on lung auscultation, irregular heart rhythm, and a displaced point of maximal impulse. His jugular venous pressure is elevated at 12 cm. The physical exam findings suggest acute decompensated heart failure, likely precipitated by medication non-adherence and dietary indiscretion.

Throughout the morning, the telemetry nurse documents vital signs every 4 hours in Epic's flowsheet: 8:00 AM (BP 145/88, HR 94, RR 16, O2 sat 96% on 2L), 12:00 PM (BP 138/82, HR 88, RR 14, O2 sat 97% on 2L). She records fluid intake and urine output meticulously, noting Robert has put out 1,200 mL of urine by noon after receiving two doses of IV furosemide. She weighs him daily at 6 AM using the bed scale, documenting 198.4 lbs on admission day and 194.2 lbs the following morning.

The cardiologist, Dr. Jennifer Park, evaluates Robert at 10:30 AM on hospital day 1. She opens Epic on a mobile workstation outside his room, reviews his echocardiogram from six months ago, observing an ejection fracture of 35% (meaning the heart is pumping only 35% of the blood it should be) and performs an examination. She dictates a consultation note using her voice recognition software directly into Epic, recommending uptitration of guideline-directed medical therapy, cardioversion consideration if he doesn't convert to sinus rhythm, and reinforcement of medication adherence. She places orders for a repeat echocardiogram and adjusts his medication regimen to include spironolactone 25mg daily.

During Robert's three-day hospitalization, a multidisciplinary care team documented his treatment in Epic through interconnected clinical notes including nursing assessments every shift monitoring respiratory status and edema, daily progress notes from Dr. Martinez tracking volume status and diuretic transition, pharmacy medication reconciliation, case management coordination of home health services and follow-up appointments, nutrition consultation for low-sodium diet education with 2-liter fluid restriction, and physical therapy clearance for home discharge. The telemetry system transmitted continuous cardiac monitoring to Epic's flowsheets while HL7 interfaces automatically populated lab results showing improving clinical markers: BNP decreasing from 1,847 to 892, troponin normalizing from 0.08 to unmeasured levels, and stable renal function with creatinine around 1.0-1.1 and potassium maintained between 3.8-4.3. Robert converted to normal sinus rhythm on day 2 with metoprolol rate control, and his repeat echocardiogram demonstrated stable systolic function at 35% ejection fraction with moderate mitral regurgitation and no pericardial effusion.

*Discharge*

On hospital day 4, Dr. Martinez determines Robert is ready for discharge. He opens Epic's discharge navigator workflow at 10:45 AM and begins completing the discharge summary. The ambient scribe's draft notes from each day populate sections of the discharge summary automatically, which he reviews and edits for accuracy.

At 11:30 AM, Dr. Martinez enters Robert's room with his smartphone recording. He explains the discharge plan: continue oral furosemide 40mg twice daily, increase lisinopril to 10mg daily, continue metoprolol 50mg twice daily, add spironolactone 25mg daily, and maintain his statin and metformin. He counsels on smoking cessation maintenance (Robert quit 5 years ago but the history remains relevant), daily weights with instructions to call if weight increases more than 3 pounds in a day, dietary sodium restriction to less than 2 grams daily, and fluid restriction to 2 liters daily.

The case manager schedules follow-up appointments: cardiology in 1 week, primary care in 2 weeks. Home health nursing is arranged for twice-weekly visits to monitor weights, blood pressure, and medication compliance. Prescriptions are sent electronically to Robert's preferred pharmacy via Epic's e-prescribing system at 12:15 PM.

The discharge nurse reviews all medications with Robert and his wife at 1:30 PM, providing printed medication lists and instructions. She documents completion of discharge education in Epic's discharge teaching flowsheet. Robert's IV lines are removed, discharge orders are signed by Dr. Martinez at 2:05 PM, and Robert leaves the hospital with his wife at 2:45 PM.

At 8:30 PM that evening, Dr. Martinez completed his final discharge summary documentation. He opens the AI-generated draft on his home computer, which has populated the hospital course based on his daily ambient scribe recordings. He adds specific details about physical exam findings not captured verbally (such as "no hepatomegaly" and "2/6 systolic murmur at apex"), verifies medication dosing is correct, ensures all lab values and imaging results are accurately reflected, and finalizes the assessment and plan sections. He adds his diagnostic impression: "Acute decompensated heart failure, precipitated by medication non-adherence, with rapid atrial fibrillation that converted to normal sinus rhythm with rate control."

He electronically signs and locks the discharge summary at 8:52 PM. The encounter is coded as DRG 291 (Heart Failure & Shock with MCC) by the hospital's coding team the following morning after reviewing the complete documentation. The final bill includes charges for four days of telemetry monitoring, laboratory studies, imaging, cardiology consultation, pharmacy services, case management, dietary consultation, and physician services totaling $34,847 before insurance adjustments.

#### Data Created by Robert’s Hospitalization

Robert's four-day hospitalization for acute decompensated heart failure generated extensive documentation across Epic's data architecture, with over 250 rows of structured data captured in relational database tables and more than 20 unstructured clinical notes stored separately.

| Structured Data<br>Epic Clarity Data Warehouse | PAT_ENC: 1 row added. includes basic details about the emergency department encounter starting at 2:47 AM PAT_ENC_HSP: 1 row added. includes additional encounter details including admission from ED to telemetry unit, 4-day length of stay, and discharge disposition<br>IP_FLWSHT_REC (Flowsheet Records): Multiple rows added for each vital sign documentation session throughout the 4-day hospitalization<br>IP_FLWSHT_MEAS (Flowsheet Measurements) Approximately 120+ rows added; includes vital signs documented every 4 hours in telemetry unit (blood pressure systolic, blood pressure diastolic, heart rate, respiratory rate, oxygen saturation, temperature), daily weights, fluid intake/output measurements<br>PAT_ENC_DEPT_HX (Department History) 2 rows added; tracks Robert's movement from emergency department to telemetry unit ORDER_PROC (Procedure Orders) 15+ rows added; includes initial ED lab orders (complete blood count, comprehensive metabolic panel, troponin, BNP), chest X-ray, electrocardiogram, repeat echocardiogram, daily labs on hospital days 1-3, cardiology consultation order<br>ORDER_MED (Medication Orders) 10+ rows added; includes ED medications (furosemide IV, nitroglycerin drip), admission medications (metoprolol, lisinopril, atorvastatin, metformin), new medications (spironolactone), transition from IV to oral furosemide, discharge prescriptions<br>MAR_ADMIN_INFO (Medication Administration Records) 40+ rows added; documents each time nurses administered medications throughout the 4-day stay<br>LAB_RESULTS (Laboratory Results) 30+ rows added; includes all individual lab test results from admission labs and daily monitoring (BNP, troponin, creatinine, potassium, sodium, glucose, complete blood counts)<br>ORDER_IMAGING (Imaging Orders) 2 rows added; portable chest X-ray in ED, repeat echocardiogram on hospital day 1 IMAGING_EXAM_INFO (Imaging Results) 2 rows added; includes chest X-ray findings (bilateral pleural effusions, pulmonary edema) and echocardiogram results (ejection fraction 35%, moderate mitral regurgitation)<br>ORDER_DIAGNOSTICS (Diagnostic Tests) 1 row added; electrocardiogram order and interpretation<br>PROBLEM_LIST 5 rows added or updated; acute decompensated heart failure (new), atrial fibrillation with rapid ventricular response (new or updated), heart failure with reduced ejection fraction (existing), coronary artery disease (existing), type 2 diabetes (existing)<br>CLARITY_ADT (Admission/Discharge/Transfer) 3 rows added; ED arrival, admission to telemetry unit, discharge to home NOTE_ENC_INFO 20+ rows added; connects Robert's encounter to all clinical documentation (ED physician note, cardiology consultation, daily progress notes, nursing shift notes, pharmacy notes, case management notes, nutrition consult, physical therapy evaluation, discharge summary)<br>RX_ORDERS (Prescription Orders) 5 rows added; electronic prescriptions sent to pharmacy for discharge medications ARPB_TRANSACTIONS (Professional Billing Transactions) Multiple rows added; includes charges for ED physician services, hospitalist daily visits, cardiology consultation, nursing care, pharmacy services, case management, dietary consultation HSP_ACCT_DX_LIST (Hospital Account Diagnosis List) 1 row added for principal diagnosis: acute decompensated heart failure 3+ rows added for secondary diagnoses: atrial fibrillation, chronic systolic heart failure, coronary artery disease with history of myocardial infarction<br>CLARITY_EAP_HOSP (Hospital Procedure Codes) 1 row added; DRG 291 (Heart Failure & Shock with Major Complications/Comorbidities)<br>F_SCHED_APPT (Future Appointments) 2 rows added; cardiology follow-up in 1 week, primary care follow-up in 2 weeks HOME_HEALTH_ORDERS 1 row added; twice-weekly home health nursing visits for weight and blood pressure monitoring CLARITY_DEP (Department references) No new rows; existing records for emergency department and telemetry unit referenced IDENTITY_ID (Provider information) No new rows; existing records for Dr. Williams (ED attending), Dr. Martinez (hospitalist), Dr. Park (cardiologist) referenced Additional metadata tables were modified that are not listed here. |
|---|---|
| Unstructured Data | HNO_INFO 20+ rows added with metadata for each clinical note: Emergency department physician note (Dr. Williams) Admission history and physical (Dr. Martinez) Daily progress notes (Dr. Martinez, hospital days 1-4) Cardiology consultation note (Dr. Park) Nursing assessment notes (every 12-hour shift × 4 days = 8 notes) Pharmacy consultation notes Case management notes Nutrition consult note Physical therapy evaluation note Discharge summary (Dr. Martinez)<br>NOTE_TEXT (or similar table containing actual note content) 20+ rows added with the actual text of all clinical notes listed above RADIOLOGY_REPORT_TEXT 2 rows added; narrative text of chest X-ray interpretation and echocardiogram report EKG_INTERPRETATION_TEXT 1 row added; narrative interpretation of electrocardiogram findings PATIENT_EDUCATION_TEXT Multiple rows added; documentation of education provided on heart failure management, medications, diet, fluid restriction, daily weights, when to seek medical attention |

## Structured Data in EHRs

This section provides a detailed description of the structured data available in the EHR. These elements are presented in order of their typical usefulness to data scientists and researchers; laboratory results, for example, are presented first, are highly accurate, and offer deep insight into a patient’s conditions.

### Laboratory Results

Laboratory tests are biological samples such as blood, urine, or other bodily fluids analyzed to measure specific compounds, cells, or organisms. Physicians order laboratory tests for a variety of reasons including diagnosing suspected diseases, monitoring known conditions, and assessing whether a treatment is working. Because the data is captured by machines and flows directly into EHRs, laboratory results represent one of the few data types where the EHR genuinely captures structured and accurate information.

Laboratory testing occurs across all healthcare settings, though with dramatically different frequencies. 98% of inpatient stays include at least one laboratory test, as clinicians need baseline values, monitor disease progression, and track treatment response.[^5]  Emergency departments test about 56% of patients, prioritizing those with acute symptoms requiring rapid diagnosis. Outpatient visits have the lowest testing rate at just 29%, since many visits address minor complaints, medication refills, or preventive care that doesn't warrant lab work.The sheer volume of outpatient encounters means they're responsible for a substantial share of total lab utilization even though most individual visits don't involve testing. There are between 4 and 5 billion laboratory tests performed each year in the United States, making them the most common medical procedure in healthcare.

The table below presents a sample of laboratory data from the famed MIMIC dataset, which has been the most commonly used open-source sample of EHR data for more than a decade. This sample has the foundational data elements that typically accompany labs:

| subject_id | specimen_id | lab_name | fluid | valuenum | ref_range_low | ref_range_high | valueuom | flag |
|---|---|---|---|---|---|---|---|---|
| 10002013 | 93257536 | MCH | Blood | 33.5 | 27 | 32 | pg | abnormal |
| 10002013 | 93257536 | MCHC | Blood | 35.2 | 31 | 35 | % | abnormal |
| 10002013 | 93257536 | MCV | Blood | 95 | 82 | 98 | fL |  |
| 10002013 | 93257536 | Platelet Count | Blood | 242 | 150 | 440 | K/uL |  |
| 10002013 | 93257536 | RDW | Blood | 12.8 | 10.5 | 15.5 | % |  |
| 10002013 | 93257536 | Red Blood Cells | Blood | 3.74 | 4.2 | 5.4 | m/uL | abnormal |
| 10002013 | 93257536 | White Blood Cells | Blood | 10.1 | 4 | 11 | K/uL |  |

- Subject_id: The unique identifier of the patient.

- specimen_id: The unique identifier of the collected specimen. Each vial of blood, for example, would have its own id.

- lab_name: This typically represents the name of the lab that the doctor selected within their EHR. While this field sometimes is standardized to reflect a lab test name as encoded in LOINC (see [Core Concepts](/book/intro/core-concepts/)), it can also be institution specific and thus require mapping to LOINC, as it is in the data below.

- fluid: Knowing the type of sample is critical, as some biological compounds can be measured in multiple types of fluids and thus have distinct reference ranges.

- valuenum: This is the actual test result. While this is typically a number, there are also often strings expressing some lower or upper bound on what is measurable by the test (e.g. ‘Undetectable’ or ‘>1000’).

- ref_range_low: Typically the lower bound on the 95% confidence interval on the result in a healthy population.

- ref_range_high: Typically the upper bound on the 95% confidence interval on the result in a healthy population.

- valueuom: Also known as ‘Units’ or ‘Units of Measure’ (UOM), this field specifies the units in which the numerical result is expressed.

#### Unit of Measurement

Laboratory results are meaningless without their units and this data is not always standardized. This can be a challenge, because analytes such as glucose are often reported as mg/dL (milligrams per deciliter) in the US and mmol/L (millimoles per liter) internationally. As a result, analysts must be careful to avoid inconsistent units when aggregating lab data across institutions and geographies.

UCUM (Unified Code for Units of Measure) is the international standard for representing units in healthcare data and establishes a single canonical representation for each measurement type. Examples of UCUM codes are mg/dL for milligrams per deciliter or  mmol/L for millimoles per liter. The UCUM standard is foundational to the HL7 FHIR interoperability standard as well as the LOINC terminology for lab results. While other standards for units exist, UCUM dominates modern healthcare data because it's designed specifically for electronic systems.

#### Reference Ranges

Reference ranges accompany most laboratory tests and provide a range of expected values. For example, most labs report a reference range of roughly 4.0-5.6% for a hemoglobin A1C test measuring the percentage of sugar (glucose) in one’s blood. These ranges aren’t standardized, are generated by individual labs, and typically represent the 95% confidence interval of the lab value within a healthy population. As a result, it is expected that 5% of healthy individuals fall outside the reference range for a given test. Ideally reference ranges are conditional on a patient’s age and gender, but often they are generalized within an adult population (typically 18-65 years old).

### Medical Devices

The devices on hospital wards and in surgical suites generate rich physiological data from multiple types of sensors. Ventilators track every breath, infusion pumps record every milliliter of drug delivered, and bedside monitors capture thousands of heartbeats throughout a patient's stay. Yet only a portion of this data flows into structured EHR fields accessible to analysts and applications. As of 2026, the data typically lives within manufacturer silos and thus clinicians often review real-time waveforms [^6] on device screens or PDF printouts, and then draft free-text notes summarizing the data. However, there is hope that in the future this data will have greater interoperability and be available for analysis alongside routine laboratory tests and clinical diagnoses.

#### Bedside Physiological Monitors

Walk into any surgical suite or Intensive Care Unit (ICU) and you'll see walls of monitors. The number of monitors and the modality of their sampling (e.g. blood pressure cuff vs. arterial catheter) is dependent on the acuity of the patient as well as the care setting (ER vs. outpatient surgery vs. ICU).

1. Electrocardiogram (ECG/EKG ) -Records the heart's electrical activity through electrodes placed on the chest, arms, and legs, capturing the coordinated polarization of cardiac muscle that drives each heartbeat. A standard 12-lead ECG samples electrical signals at 500 Hz for about 10 seconds, producing waveforms that reveal the heart's rhythm, conduction pathways, and evidence of ischemia or structural damage.  ECGs enable diagnosis of life-threatening arrhythmias like ventricular fibrillation, myocardial infarctions requiring immediate intervention, conduction blocks that may need pacemakers, and left ventricular hypertrophy from longstanding hypertension.

1. Blood Pressure - Non-critically ill patients have blood pressure measured intermittently via automated cuffs placed around the arm while critically ill ICU patients often have arterial blood pressure (ABP) monitored continuously via a small catheter inserted directly into an artery, converting the mechanical pressure waves from heartbeats into continuous electrical signals. This invasive waveform reveals the shape and quality of each pulse, helping clinicians detect problems like decreased cardiac output, severe hypovolemia, or catheter malfunction.

1. Blood Oxygen Saturation (SpO2) - Measures blood oxygen saturation by shining red and infrared light through a fingertip and detecting how much light is absorbed by hemoglobin. These devices, called *pulse oximeters*, alert staff to patients experiencing respiratory distress. During surgery, anesthesiologists continuously monitor each patient's oxygen saturation and adjust ventilation according to the real-time feedback provided by the pulse oximeter. Any SpO2 measurement below 90% is considered problematic and typically motivates a medical intervention.

1. Respiratory Rate - Measured in ICUs from one of three sources: impedance pneumography (measures changes in electrical impedance across the chest as it expands and contracts with breathing), capnography (detecting CO2 in exhaled breath for intubated patients), or sometimes from variations in arterial blood pressure. These automated measurements work reasonably well but are prone to measurement error from patient movement, shallow breathing, and cardiac oscillations for respirations. Respiratory rate matters clinically because it is a sensitive indicator of patient deterioration, as rapid breathing (*tachypnea*) often precedes cardiac arrest, respiratory failure, or septic shock.

1. Temperature - ICU patients have temperature monitored continuously via electronic probes inserted into body cavities that accurately measure core temperature. Non-intubated or less critically ill ICU patients may have intermittent measurements using standard ear or oral electronic thermometers every few hours.  Temperature is a critical vital sign because fever signals infection or inflammation requiring treatment, while hypothermia indicates shock, environmental exposure, or metabolic crisis.

There are additional bedside monitors that are used less frequently and typically reserved for the highest acuity patients in ICUs.

1. Intracranial Pressure (ICP) - Measured via an intraventricular catheter, epidural sensor, or subdural bolt placed directly into the brain or its surrounding spaces. ICP monitoring is critical for patients with traumatic brain injury, cerebral edema after stroke, or other conditions where brain swelling is a concern. Normal ICP is 5-15 mmHg; elevations above 20 mmHg warrant intervention to prevent herniation and permanent neurological damage.

1. Pulmonary Artery Pressure (PAP) - Measured through a pulmonary artery catheter inserted through a central vein into the right heart chambers. This is most commonly used to monitor acute heart failure patients or patients experiencing septic shock.

1. Cerebral Oximetry (rSO2) - Uses near-infrared spectroscopy (NIRS) to measure regional oxygen saturation in brain tissue non-invasively. Sensors placed on the forehead detect light absorption by hemoglobin, providing a proxy for cerebral perfusion. Most common during cardiac surgery to detect inadequate brain oxygen delivery during cardiopulmonary bypass.

Most bedside monitors generate waveform data in proprietary formats specific to each manufacturer. DICOM waveforms provide a standardized format for storing and exchanging these continuous signals. Waveforms are contained in a Waveform Sequence within a DICOM dataset, with each multiplex group representing a set of channels synchronized at a common sampling frequency [Pydicom](https://pydicom.github.io/pydicom/dev/tutorials/waveforms.html). When captured in DICOM format, waveform samples are encoded with specifications for the number of bits stored per sample and are stored channel-interleaved (meaning all channels at sample 1, then all channels at sample 2, etc.) [Innolitics](https://dicom.innolitics.com/ciods/general-ecg/waveform/54000100/54001010). The standard supports various signal types—ECG, respiratory waveforms, hemodynamic curves, and audio. However, adoption remains incomplete: while the DICOM standard included rules for ECG waveforms starting in 2000, manufacturers were slow to implement it, with the first diagnostic ECG device supporting DICOM appearing in 2006 [ResearchGate](https://www.researchgate.net/figure/DICOM-is-able-to-unite-diagnostic-images-with-diagnostic-ECG-waveforms-The-clinician-has_fig1_224369482). In practice, bedside monitor data typically remains trapped in manufacturer-specific formats, with waveforms either manually exported as PDFs or converted to DICOM through third-party gateway software—creating a disconnect between the real-time clinical data streams and standardized archival formats.

<figure>
  <img src="{{ '/images/book/ehr-bedside-monitor-flowsheet.svg' | relative_url }}" alt="Example EHR flowsheet with vital signs, ventilator settings, and blood-gas values grouped in sections, with hourly timestamps across the columns">
  <figcaption>A nursing flowsheet in an EHR system. Measurement types run down the rows, grouped into sections, and time runs across the columns, creating a structured longitudinal record of a patient's physiological status. Values are entered manually by nurses or auto-populated from interfaced bedside monitors. Illustrative synthetic data.</figcaption>
</figure>

The massive number of data points from the physiological monitors are not automatically transferred into EHRs but rather are interpreted and then documented by nurses in EHR flowsheets. Flowsheets are tabular data entry interfaces in the EHR where clinicians document time-stamped observations to create structured longitudinal data. The use of flowsheets varies from monitoring vital signs to interviewing patients about drug and alcohol use.  The data entry interface typically resembles a spreadsheet with time running down the rows (hourly, every 4 hours, or custom intervals) and measurement types across the columns (temperature, heart rate, blood pressure systolic/diastolic, respiratory rate, SpO2). Nurses click into cells to enter values, and the EHR enforces data type validation (numeric ranges, required fields, acceptable units) and some systems flag out-of-range values with color coding (e.g. red for critical). Modern flowsheets offer auto-population buttons that pull current values directly from interfaced bedside monitors, reducing transcription errors but also potentially importing errors if nurses don't perform the necessary validation. Different hospitals configure their flowsheets differently; for example, some require documenting patient position and activity level in adjacent columns, others don't capture this context at all. When you query vital signs or even patient-reported responses to a questionnaire  from an EHR database, you're likely extracting whatever made it into flowsheet cells during nurse documentation workflows.

#### Other Diagnostic Testing

The nervous system within the human body is like the wiring in a house, with separate circuits for sending sensory information to the brain or and commands to muscles and organs. But electrical activity in the body isn’t confined to neurons, as cardiac and muscle cells can generate and propagate electrical signals independently. Electrophysiology (EP) data captures all of this electrical activity and is used by doctors to assess the functioning of the heart, brain, muscles, and nerves. This data consists of waveforms[^7] sampled hundreds or thousands of times per second, producing time-series data that can reveal normal and abnormal physiology.  In electrophysiology specifically, waveforms show voltage measurements plotted continuously over time. The most common electrophysiology tests performed as as follows:

1. Electroencephalogram (EEG) - Standard for seizure diagnosis and monitoring epilepsy. Common in neurology but nowhere near ECG volumes. Routine EEGs take 30-60 minutes; extended monitoring can last days.

1. EMG/Nerve conduction studies - Common in neurology for diagnosing neuropathy, radiculopathy, carpal tunnel syndrome, and other nerve/muscle disorders. More specialized than ECG/EEG.

1. Sleep studies (Polysomnography) - Include EEG plus other sensors. Very common for sleep apnea diagnosis but require overnight stays in sleep labs or home testing equipment.

<figure>
  <img src="{{ '/images/book/emg-cmap-waveform.svg' | relative_url }}" alt="Compound Muscle Action Potential (CMAP) waveform showing voltage in millivolts over time in milliseconds, with the characteristic biphasic deflection and dashed lines indicating amplitude measurement">
  <figcaption>A Compound Muscle Action Potential (CMAP) waveform from a nerve conduction study. The amplitude (measured peak-to-peak, indicated by the arrows) and latency of this waveform help neurologists diagnose neuropathy, radiculopathy, and carpal tunnel syndrome. Illustrative schematic.</figcaption>
</figure>

#### Cardiac Electrophysiology

Cardiac electrophysiology data captures the heart's electrical activity, and it arrives in the EHR at wildly different resolutions depending on how it was collected. The workhorse is the 12-lead electrocardiogram (ECG), a roughly ten-second recording sampled at 250–500 Hz that produces both a waveform and a machine-generated interpretation. Here is the practical catch for data teams: what actually lands in the structured database is almost never the waveform. It's the interpretation text and a handful of measured intervals (heart rate, PR, QRS, QT/QTc), while the waveform itself sits in a separate cardiology system (a "cardiology information system" or the ECG management platform, e.g., MUSE) and is exposed to clinicians as a PDF or a proprietary format. If you want the raw signal for machine learning, you will usually be negotiating with that ancillary system, not querying Clarity.

Beyond the resting ECG, several modalities extend the recording in time:

- Ambulatory monitoring — Holter monitors (continuous 24–48 hours), extended patch monitors (Zio and similar, up to ~14 days), and event/loop recorders that capture rhythm only when the patient is symptomatic or an algorithm fires. These generate long time-series but reach the chart as a summarizing report.

- Invasive electrophysiology (EP) studies — catheter-based recordings of intracardiac electrograms taken inside the heart during procedures to map and ablate arrhythmias. This is dense, high-value signal that lives almost entirely inside the EP lab's mapping system (e.g., CARTO, EnSite) and rarely leaves it.

- Implantable device data — pacemakers, ICDs, and loop recorders, covered in depth in the patient-generated data chapter, produce their own intracardiac electrograms during "interrogations."

The recurring lesson is the one this book keeps returning to: the *interpretation* is structured and queryable, the *signal* is trapped. Analysts who assume "the ECG is in the EHR" are usually holding a text impression and a few interval measurements, not the millivolt-by-millivolt trace a model would need.

<figure>
  <img src="{{ '/images/book/ecg-intervals-structured.svg' | relative_url }}" alt="Two-panel figure: top, a ten-second single-lead ECG waveform; bottom, one heartbeat enlarged with the PR interval, QRS duration, and QT interval bracketed, next to a box listing the handful of measured values and interpretation text that reach the structured EHR record">
  <figcaption>What the EHR keeps from an ECG. (a) The full waveform, a 10-second, 500 Hz signal, lives in the cardiology information system. (b) What lands in the structured EHR record is a few measured intervals per beat (PR, QRS, QT/QTc), the heart rate, and the machine or cardiologist interpretation as text. Illustrative synthetic waveform.</figcaption>
</figure>

#### Neurological Electrophysiology

Neurological electrophysiology measures electrical activity in the brain, nerves, and muscles, and as a data source it is both clinically important and analytically frustrating. The electroencephalogram (EEG) records brain activity from an array of scalp electrodes (the standard 10–20 montage places 19+ electrodes) sampled at 256–512 Hz. A routine EEG runs 20–40 minutes; epilepsy monitoring units record continuously for days, and the resulting files are enormous. EMG and nerve conduction studies (NCS) assess muscle and peripheral-nerve function for neuropathy, radiculopathy, and conditions like carpal tunnel or ALS. Polysomnography—the overnight sleep study—bundles EEG with airflow, oximetry, EMG, and EKG channels to stage sleep and diagnose apnea.

The data-availability story mirrors cardiac EP almost exactly. The neurologist reads the study and dictates a narrative report; that report is what enters the EHR as unstructured text. The underlying multichannel waveform lives in a specialized acquisition system (often stored in EDF, the European Data Format, the closest thing to a lingua franca for biosignals) and is not something you can pull from the clinical warehouse. There is no widely adopted standard vocabulary for coding EEG findings the way LOINC codes a lab, so aggregating these studies across sites means parsing prose. For most analytic and research purposes, neurological electrophysiology behaves like unstructured data with a very expensive signal attached.

### Vital Signs

Vital signs in EHRs represent snapshots of physiological measurements captured at specific points in time rather than continuous monitoring data. In outpatient settings, medical assistants measure and manually enter vitals during patient rooming - typically one set per visit including blood pressure, heart rate, temperature, respiratory rate, height, weight, and sometimes oxygen saturation and pain score. These entries flow into structured fields with standardized LOINC codes and UCUM units, making them relatively clean for analysis. Inpatient vital signs follow a different pattern: nurses document measurements at regular intervals (every 4-6 hours on med-surg floors, every 1-2 hours in step-down units, every 15-60 minutes in ICUs), often transcribing values from bedside monitors into the EHR's flowsheet documentation. While ICU monitors capture continuous waveforms sampled hundreds of times per second, only the nurse-validated periodic measurements make it into the structured database tables that researchers and analysts can access. The raw physiological waveforms that anesthesiologists watch during surgery or intensivists monitor in real-time almost never get stored in analyzable formats - they're displayed, maybe printed to PDFs, but rarely preserved as time-series data.

### Medication Orders

It is worth separating three things that beginners routinely conflate: a medication order, a medication administration, and the medication list. This section is about orders; the list has its own section below, and pharmacy *dispensing* is covered by pharmacy claims in Part II.

A medication order is the discrete event in which a clinician, through computerized provider order entry (CPOE), directs that a drug be given or prescribed. The order records the drug (usually coded to RxNorm), dose, route, frequency, start/stop, indication, and ordering provider. What happens next depends entirely on the setting, and this is where data quality diverges sharply:

- Inpatient orders feed a downstream Medication Administration Record (MAR), where a nurse documents each individual dose actually given, scanning the medication and the patient's wristband. The MAR is one of the highest-fidelity data sources in the entire EHR: it records what was truly administered, when, and by whom. If you want to know whether a hospitalized patient received a drug, the MAR—not the order—is your source of truth.

- Outpatient orders are e-prescriptions transmitted to a pharmacy. Here the order captures only *intent*. Whether the patient filled it, and whether they took it, is invisible to the EHR; that story lives in pharmacy claims (fill) and nowhere at all (ingestion). A prescribed statin and a taken statin are very different facts, and the order confirms only the former.

So the same table can be gold or fool's gold depending on care setting. Inpatient medication data, validated dose-by-dose through the MAR, is excellent. Outpatient prescribing data tells you what a clinician wanted to happen, which—as the pharmacy-claims and medication-list sections both warn—is not the same as what did.

### Problem Lists

The problem list is meant to be the curated, longitudinal summary of a patient's active diagnoses.  It differs from encounter diagnoses, which justify a specific visit's billing (see "Principal and Secondary Diagnoses"). In principle the problem list is the cleaner clinical picture, because it is supposed to reflect ongoing conditions rather than billing convenience, and its entries are typically coded to SNOMED-CT with an ICD-10 mapping for downstream use.

In practice, treat the problem list with the same skepticism the rest of this book applies to EHR-derived diagnoses. Problem lists are notoriously poorly maintained. Resolved conditions linger for years because no one takes the time to mark them inactive; duplicate entries accumulate as different clinicians add their own phrasing of the same disease; and genuinely active problems go missing because documenting them wasn't necessary to get paid for today's visit. Studies of problem-list completeness and accuracy have found meaningful rates of both omission and stale, incorrect entries.[^8] The safest mental model is that a problem list is a *helpful but unreliable* index of a patient's conditions—useful for hypothesis generation, dangerous as ground truth without corroboration from labs, medications, and procedures.

### Principal and Secondary Diagnoses

Diagnosis codes that are assigned as the principal and secondary diagnosis associated with an encounter are heavily concentrated in common, billable conditions. Providers won't code "unstable living environment contributing to patient’s medication non-adherence", they code "Type 2 diabetes mellitus without complications" because that's what justifies the A1C order and the prescription refill. The diagnosis list in an EHR is better understood as "conditions that justified billable services" rather than "conditions the patient actually has." Moreover, the timing of diagnoses is equally revealing. A patient might have had hypertension for years, but it only appears in their problem list when a physician needs to justify prescribing an antihypertensive or when a quality metric flags that the diagnosis should be documented.

### Medication List

Caution is warranted when analyzing a patient’s medication list. The medication list shows what was prescribed, not what the patient is actually taking. A patient might be prescribed four different blood pressure medications, but if they can't afford them or experience side effects, the prescriptions sit in the EHR as if they represent reality. The physician might not discover the non-adherence for months, and even then might not remove the medications from the active list because "we tried this once, might need to reference it later." Over-the-counter medications, supplements, and drugs prescribed by other providers often don't appear at all unless the patient happens to mention them and someone takes the time to enter them manually.

### Social History

Social history captures the behavioral and social factors that shape health: tobacco, alcohol, and substance use, occupation, living situation, and—increasingly—social determinants of health (SDOH) such as food insecurity, housing instability, and transportation barriers. Some of this is well-structured. Smoking status in particular is one of the more reliably coded fields in the EHR, largely because U.S. Meaningful Use rules required structured capture of it, so you can usually trust a coded current/former/never smoker value. Alcohol and drug use are captured in structured fields too, though with more variability and more blanks.

SDOH is the frontier and, as of 2026, the weak spot. Health systems have begun administering standardized screening instruments (PRAPARE, the CMS Accountable Health Communities HRSN tool) and recording results with ICD-10-CM Z-codes (the Z55–Z65 range for social circumstances) , but capture is sparse and inconsistent: Z-code documentation rates in claims and EHR data are low single digits meaning that absence of a housing-insecurity code tells you almost nothing about whether the patient is housing-insecure. When social history is present it is valuable; the problem is that it is missing far more often than it is wrong, and the missingness is not random but rather correlates with exactly the population's SDOH data is meant to help.[^9]

### Diagnostic Test Orders

Diagnostic test orders are the requests a clinician places for labs, imaging, and other studies. Much of what matters about the *results* is covered under Laboratory Results and Medical Imaging; this section is about the order itself, which is analytically useful in its own right for three reasons.

First, orders carry the reason for the study and the ordering provider, which is often more informative about clinical suspicion than the result. An ordered troponin at 3 a.m. tells you someone was worried about a heart attack, regardless of how the value came back. Second, orders have a lifecycle (e.g. ordered, in-process, resulted, or canceled) and the gaps between states are meaningful; a canceled MRI or a lab ordered but never drawn is a real event that a results-only analysis will miss entirely. Third, order data lets you study utilization and appropriateness: over-ordering, defensive testing, and the effect of clinical decision support all show up in the order stream before they show up anywhere else. The caveat is that an order is a request, not an outcome: many ordered tests are never performed, so counting orders as if they were results will overstate what actually happened to the patient.

### Family History

Family history records conditions in a patient's biological relatives—typically a structured pairing of a relationship (mother, father, sibling) with a condition and sometimes an age at onset. It is clinically important out of proportion to how much data it contains, because it drives risk stratification and screening decisions: the maternal-grandmother breast cancer and paternal diabetes in Jasmine's ambulatory visit earlier in this book are exactly the entries that would prompt earlier screening or genetic referral.

The dominant data-quality problem is staleness and incompleteness. Family history is usually captured once and then rarely revisited, so a parent's later cancer diagnosis may never make it into the child's chart. Coding is inconsistent (structured relationship-plus-SNOMED in the best systems, free text in many), which makes cross-site aggregation painful. And it is only as good as patient recall, which is imperfect for relatives' exact diagnoses and ages. Family history is genuinely useful for identifying high-risk patients, but analysts should expect it to be sparsely populated and to undercount rather than overcount familial risk.

### Adverse Reactions

Adverse reactions and allergies are frequently stored together and just as frequently confused, so it is worth drawing the line clearly. A true allergy is an immune-mediated response (hives, anaphylaxis). An adverse reaction or intolerance is an unwanted effect that is not immunologic—the nausea from an antibiotic, the muscle aches from a statin. The clinical and analytic stakes of the distinction are real: a documented "penicillin allergy" that is actually a remembered childhood stomachache can steer a patient toward broader, more expensive, more resistance-promoting antibiotics for the rest of their life.

Structurally, a reaction entry pairs a causative agent (coded to RxNorm for drugs, or to a food/environmental concept) with a reaction (SNOMED-CT) and a severity. The data-quality pattern here is the mirror image of most EHR fields: adverse reactions are typically over-documented, not under-documented. Because listing a reaction has no billing downside and clinicians are cautious, nuisance side effects get recorded as allergies, entries are copied forward across encounters, and few are ever removed or reconciled. Large "penicillin allergy" delabeling studies have found that the large majority of documented penicillin allergies are not true allergies on testing.[^10] For analytics, the reaction list is best read as a record of clinical caution rather than a validated list of immunologic hypersensitivities.

### Procedure Orders (CPT/HCPCS/DRGs)

Procedure orders direct that something be *done* to a patient—a surgery, an injection, a physical therapy course. The heading groups three vocabularies, but they do not play the same role, and the distinction trips people up:

- CPT and HCPCS are the codes attached to the procedures themselves. CPT covers professional and outpatient procedures; HCPCS covers supplies, equipment, and services outside CPT. These are what appear on the order and, later, the claim.

- DRGs (Diagnosis-Related Groups) are *not* something anyone orders. A DRG is assigned to an entire inpatient stay after discharge, by coders, to determine a single bundled reimbursement (recall Robert's hospitalization closing as "DRG 291, Heart Failure & Shock with MCC"). Grouping DRGs under "procedure orders" is a common but misleading shorthand; a DRG is an encounter-level billing classification, not an order.

The analytic value of procedure orders is that they capture *what was planned and by whom*, with timestamps, before the billing view flattens everything into claim lines. The same caveat as diagnostic test orders applies: an ordered procedure is not a performed one. And as always, the vocabularies here are optimized for reimbursement, so the granularity reflects what payers need to adjudicate, not necessarily what a clinician or researcher would consider the clinically salient detail.

### Allergies

The allergy list is the structured companion to the adverse-reactions discussion above, and it deserves its own note because of how it is *used*. Allergy entries pair an allergen (drug coded to RxNorm; food or environmental agents to their own concepts) with a reaction and severity, and unlike most documentation they are wired directly into clinical decision support: when a clinician orders a drug, the EHR checks it against the allergy list and can fire an interruptive alert.

That wiring creates the field's defining pathology—alert fatigue. Because the allergy list is over-populated with intolerances and low-severity reactions (see Adverse Reactions), the CDS system generates a high volume of low-value warnings, clinicians override the large majority of them reflexively, and the occasional genuinely dangerous alert can be lost in the noise.[^11] There is also a structural quirk analysts must handle: "No Known Drug Allergies" (NKDA) is itself a documented status, and an empty allergy list is ambiguous—it may mean the patient has no allergies, or that no one asked. Distinguishing "confirmed none" from "not assessed" is essential before drawing any conclusion from an absent allergy.

### Immunization Records

Immunization data records vaccines administered—vaccine, date, lot, site, and administering provider—coded with CVX (the vaccine product) and MVX (the manufacturer). What makes immunizations distinctive among EHR data streams is that they are the one domain with a mature, government-run *aggregation* layer: state and regional Immunization Information Systems (IIS), the immunization registries that pull records together across the many places a person gets vaccinated.

That aggregation exists precisely because immunization is the most fragmented care event most people experience. A single adult might get flu shots at a pharmacy, childhood vaccines at a pediatrician, a tetanus booster at an urgent care, and travel vaccines at a specialty clinic—four systems, four partial records. The IIS is designed to reconcile these, and it makes state registries a more complete source of immunization truth than any single EHR. The remaining data-quality issues are the seams: pharmacy-to-registry reporting is uneven, historical (patient-reported) immunizations are less reliable than administered ones, and adult immunization capture lags childhood capture, which is bolstered by school-entry requirements. For any analysis of vaccination status, the registry is usually the better source; a single EHR will systematically undercount.

### Care Team Assignments

Care team assignments record who is responsible for a patient and in what role—primary care physician, attending, specialists, care manager, and so on. The data seems mundane until you need it, and then it is load-bearing for two things: care coordination (routing messages, results, and hand-offs to the right person) and, increasingly, attribution in value-based care, where a payer or ACO must decide which provider is accountable for a patient's cost and quality.

The predictable problem is that care team fields are not reliably maintained. A patient's listed PCP may have left the practice; a specialist involved in one episode may stay attached long after the relationship ended; and the difference between "attending of record," "treating provider," and "assigned care manager" is modeled inconsistently across systems. Because so much value-based-care money now rides on attribution, mis-maintained care team data is not just a coordination annoyance—it can misassign financial and quality accountability. Analysts should validate care team assignments against actual encounter activity (who is really seeing the patient) rather than trusting the assignment field on its own.

## Semi-Structured Data in EHRs

If there is one stream of data in the EHR that clinicians who I’ve worked with universally despise it is what is called ‘semi-structured’ data. The interfaces in the EHR allow idiosyncratic clinical procedures to be precisely modeled so that nurses at a hospital can quickly document quantitative and qualitative information about a patient’s health status without endless clicking through the EHR. However, this flexibility makes it difficult to extract information to be used for analytics and artificial intelligence. Interestingly, GPT-4 performed poorly when attempting to extract information from nursing flowsheets and thus it is likely the case that foundation models must be trained specifically on flowsheets.[^12]

### Nursing Flowsheets

Flowsheets are the reason this book needs a "semi-structured" category at all. Structurally they look like a spreadsheet but what makes them *semi*-structured is that the columns themselves are not fixed. Each health system configures its own flowsheet templates, rows, and groupings, so the "same" observation may be recorded under different flowsheet row IDs at different hospitals, and there is no universal vocabulary (no LOINC-for-flowsheets) that guarantees "heart rate here" means "heart rate there."

This is where the largest volume of discrete clinical data in the EHR actually lives. Nursing documentation including vital signs, intake and output, pain scores, neuro checks, wound assessments, lines and drains, fall-risk and pressure-injury scores, and screening questionnaires are entered  into flowsheet rows, and a single ICU stay can generate tens of thousands of flowsheet measurements. In Epic these land in tables like `IP_FLWSHT_MEAS`, keyed by a flowsheet measure ID that means nothing until you join it to the institution's own metadata dictionary.

For analysts, flowsheets are a paradox: enormously rich and almost entirely local. Getting value out of them means investing in a mapping layer that translates thousands of site-specific flowsheet IDs into standardized concepts—the unglamorous data-engineering work that determines whether an ICU dataset is usable or just voluminous. When someone says a project "extracted vital signs from the EHR," what they usually mean is that they successfully navigated the flowsheet metadata.

## Unstructured Data in EHRs

By volume, most of the information in an EHR is unstructured free text: clinical notes (history and physical, daily progress notes, consults, nursing narratives, discharge summaries) plus radiology and pathology reports. The commonly cited figure is that roughly 80% of healthcare data is unstructured[^13], and while the exact number is soft, the direction is not—the narrative record dwarfs the coded record, and it contains much of what clinicians actually reason about: the nuance behind a diagnosis, the reasoning behind a plan, the symptoms that never became a billable code.

Three realities shape working with this text. First, it is information-dense but noisy: extracting structured facts (does this note assert the patient is a current smoker? is this a rule-out or a confirmed diagnosis?) requires natural-language processing, and negation, hedging, and family-versus-patient attribution are genuinely hard. Second, it suffers from note bloat: copy-forward and templating mean a ten-page note may contain one paragraph of new information, so length is a poor proxy for content and naïve text models drown in boilerplate. Third, it is a privacy minefield—names, dates, and identifiers are scattered through prose, so de-identifying free text (the Safe Harbor and Expert Determination methods discussed later) is far harder than dropping columns from a table.

The important shift, already visible in the vignettes earlier in this book, is that large language models have changed the economics of this data. The ambient scribes that draft Dr. Martinez's notes are the generation side; on the analysis side, LLMs can now extract structured variables from notes at a quality and cost that made prior clinical-NLP pipelines look artisanal. As of 2026 the unstructured record is shifting from "the data we couldn't use" toward "the data we're only beginning to use," and it is where much of the near-term value in clinical data now sits.

## Representing EHR data using Common Data Models

If you’ve spent any time working with healthcare data, you probably intuitively understand the need for a common data model. A common data model is a way to standardize the structure and content of data across different settings. If you are *new* to healthcare data, you will soon learn that hospitals, health systems, insurers, and other institutions typically store their data in formats all their own. When you are a researcher using observational data to study a disease or the effectiveness of a drug, it’ll be much harder to achieve your aims if the majority of your time is spent harmonizing data.

### HL7 FHIR: Exchanging data between hospitals and health systems

If OMOP is the model you reach for to *analyze* clinical data, FHIR is the model you reach for to *move* it. FHIR—Fast Healthcare Interoperability Resources, pronounced "fire," from the standards body HL7—is the modern standard for exchanging healthcare data between systems, and understanding the "exchange, not analysis" distinction is the key to not misusing it.

FHIR represents clinical concepts as resources—Patient, Encounter, Observation, Condition, MedicationRequest, and dozens more—each a self-contained JSON (or XML) object with defined fields and references to other resources. Systems expose these over a RESTful API, so an app can request `GET /Patient/123/Observation?code=...` and receive a patient's lab results the same way a web app fetches any other JSON. This is a deliberate break from HL7's older standards: the pipe-and-hat HL7 v2 messages that still run most hospital interfaces, and the XML CDA documents used for care summaries. FHIR kept the clinical modeling and adopted the conventions of ordinary web development, which is why developers who would never touch v2 will happily build on FHIR.

Two forces made FHIR unavoidable rather than optional. The first is regulation: in the U.S., the 21st Century Cures Act and the subsequent ONC and CMS rules require certified EHRs to expose a FHIR API and prohibit "information blocking," and national exchange frameworks like TEFCA lean on it. The second is standardization of *content*: US Core profiles and the USCDI data classes specify which resources and fields must be supported, so "supports FHIR" means something concrete rather than a vendor's private dialect.

Here is the trap to avoid. FHIR's resource-graph design—everything is an object pointing at other objects—is excellent for handing one patient's record to an app in real time and terrible for the population-scale, set-based queries that research demands ("give me every diabetic who started a statin in 2024"). That is precisely the job OMOP's flat, analytics-friendly tables are built for. The two standards are complements, not competitors: FHIR to exchange, OMOP to analyze, and mature organizations run both, using FHIR at the edges where data enters and leaves and OMOP in the warehouse where it is studied.

### OMOP: For research using EHR data

#### What is OMOP?

OMOP is a *common data model* for healthcare data generated in healthcare settings. OMOP is an acronym for the Observational Medical Outcomes Partnership, which was a partnership between the FDA, drug companies, and health systems in the early 2010s whose goal was to create infrastructure to study the effectiveness of medical products using *observational data*. Observational data is data that is collected outside of a controlled research study (and is different from *clinical trial data*). Since then, OMOP has increased in popularity compared to similar common data models focused on observational health data.

<figure>
  <img src="{{ '/images/book/omop-search-trends.svg' | relative_url }}" alt="Chart of search interest over time for OMOP and related healthcare data model terms from 2020 to 2024, with a sharp spike in 2024">
  <figcaption>Search interest for OMOP and related common data model terms, 2020–2024. The sharp spike reflects growing industry attention to standardized observational research infrastructure, driven in part by large-scale real-world evidence initiatives. Illustrative recreation of Google Trends data.</figcaption>
</figure>

#### Understanding OMOP tables

Now that you understand why healthcare needs a common data model, let's talk about how OMOP actually structures your data.Think of OMOP as a filing system that everyone agrees to use. If you and I both organize our healthcare data using the same filing system, then I can write a query once and run it against both of our databases. That's the fundamental value proposition.

The OMOP data model consists of several dozen tables, but you can understand 80% of what matters by focusing on six core clinical tables:

1. Person - One row per patient. Demographics like birth year, gender, race, and ethnicity. No names or addresses—OMOP is designed for de-identified data.

1. Visit_Occurrence - Every time a patient interacts with the healthcare system. An emergency room visit, an outpatient appointment, an inpatient hospitalization. Each visit has a start date, end date, and visit type.

1. Condition_Occurrence - Diagnoses and problems. Every time a clinician documents that a patient has diabetes, hypertension, or a broken arm, it goes here.

1. Drug_Exposure - Medications. Prescriptions, administrations, dispensing events. Both inpatient medications and outpatient prescriptions.

1. Measurement - Lab tests and vital signs. Hemoglobin A1c results, blood pressure readings, COVID test results. Anything that produces a numeric or categorical measurement.

1. Procedure_Occurrence - Things done to patients. Surgeries, imaging studies, physical therapy sessions. If someone performed a procedure, it's documented here.

These six tables handle the vast majority of clinical data. There are additional tables for things like observations, notes, specimens, and device exposures, but the pattern is the same: one table per broad category of clinical event.

#### Understanding OMOP’s vocabulary

Here's where OMOP gets powerful but complex. It's not enough to agree that all diagnoses go in the Condition_Occurrence table. We also need to agree on how to represent "Type 2 diabetes."

In the wild, you'll see Type 2 diabetes represented dozens of ways:

- ICD-10 code E11.9 (most common in US billing)

- ICD-9 code 250.00 (older US standard)

- SNOMED-CT concept 44054006 (international clinical standard)

- Textual Diagnoses: "T2DM", "Type II DM", "NIDDM", "diabetes mellitus type 2"

OMOP solves this through a standardized vocabulary system. Every clinical concept in OMOP is represented by a concept_id—a unique integer that points to a standardized term. All of those variations above map to a single standard SNOMED-CT concept that OMOP recognizes as "Type 2 diabetes mellitus."

The vocabulary tables (CONCEPT, CONCEPT_RELATIONSHIP, CONCEPT_ANCESTOR) store these mappings. When you load data into OMOP, your ETL process looks up the appropriate concept_id for each diagnosis, drug, lab test, and procedure. Then when you analyze the data, you query using these standardized concept_ids, and you can be confident you're capturing all the variations.

This is the hardest part of building an OMOP database, and it's where most implementations run into trouble. More on that later.

#### OMOP as a Healthcare Database Template

Here's how I think about OMOP: it's not software or a tool, it's a database schema specification. It's a blueprint that says "here's how to structure your tables, here's what columns each table should have, and here's how they should relate to each other."

When you "implement OMOP," you're taking that blueprint and:

1. Creating an empty database with the OMOP table structure

1. Loading the standardized vocabularies

1. Extracting data from your source systems (EHR, claims, etc.)

1. Transforming that data to match OMOP's structure and vocabularies

1. Loading the transformed data into your OMOP database

Once you've done that, you have a database that looks like every other properly implemented OMOP database. That means:

- Queries written for one OMOP database will work on another

- Tools built for OMOP (like ATLAS, the OHDSI web-based analytics platform) will work on your database

- Research studies using OMOP can easily add your data as a new site

#### When to use (and not to use) OMOP

Having more than a decade of experience with OMOP, I cannot provide a blanket recommendation to use OMOP as a common data model for storing clinical data. It is a perfectly useful data model for storing several different streams of data, especially if that data lacks a consistent terminology to represent one or more clinical events (SNOMED, LOINC, etc). However, if you are storing a more limited set of data without the need for significant mapping to controlled terminologies, it is likely not the best choice. In the following two paragraphs I share one experience where OMOP was a powerful tool and another where it became an unnecessary burden.

At Columbia's medical center, having access to a mature OMOP database transformed my productivity as a researcher. Instead of spending months deciphering messy data dictionaries and hunting across dozens of tables, I could query standardized structures where all lab tests lived in a single Measurements table and all diagnoses followed consistent vocabularies. The research IT team had already done the hard work of mapping local codes to standard terminologies and resolving semantic conflicts between source systems, which meant I could skip data engineering entirely and focus on feature engineering and modeling. OMOP databases are de-identified by design, making access easier for researchers, and the OHDSI community's open-source tools automatically generate SQL queries that work across any properly implemented OMOP instance. This was an enormous privilege that I didn't fully appreciate until later experiences showed me how rare it is.

When I joined a Series A health tech startup to build their analytics infrastructure, we chose OMOP because we anticipated ingesting EHR data, wearables, and insurance claims. We spent weeks setting up PostgreSQL with the full 40+ table OMOP schema and building complex Python ETL pipelines to map claims data through OMOP's foreign key relationships and standardized vocabularies. As the business matured, we realized we'd primarily work with insurance claims—flat CSV files that just needed column name standardization and light cleaning. OMOP's elaborate schema was overkill for what amounted to simple field mapping. After two years we abandoned it for a purpose-built claims model with a single table (one row per claim). If we were building this data stack today, I'd simply have used the [Tuva Project's pre-built medical claims data model with DBT](https://thetuvaproject.com/core-data-model/medical-claim). The Tuva Project is an incredible resource for data engineering and provides ready-made table structures specifically designed for healthcare data, eliminating the need to build complex ETL pipelines from scratch. Instead of spending weeks setting up OMOP's 40+ tables and writing custom Python code, we could have used Tuva's streamlined claims schema and transformation logic out of the box—a solution that's purpose-built for exactly our use case.

[^1]: [https://ctlin.blog/2020/06/10/all-yall-ehr-using-folks-dont-know-how-good-you-have-it/](https://ctlin.blog/2020/06/10/all-yall-ehr-using-folks-dont-know-how-good-you-have-it/)
[^2]: Holmgren, A Jay et al. “Electronic Health Record Usability, Satisfaction, and Burnout for Family Physicians.” *JAMA network open* vol. 7,8 e2426956. 1 Aug. 2024, doi:10.1001/jamanetworkopen.2024.26956
[^3]: Order sets group several orders together to make order entry convenient and efficient. They can be as small as two orders together such as a test and the test prep. At the other end of the spectrum, they can offer a comprehensive plan of care focused on a patient’s health issues.
[^4]: Diuretic medications are commonly prescribed to heart failure patients to help the body get rid of excess fluid by increasing urine production
[^5]: Andy Ngo, Paras Gandhi, W Greg Miller, Frequency that Laboratory Tests Influence Medical Decisions, *The Journal of Applied Laboratory Medicine*, Volume 1, Issue 4, 1 January 2017, Pages 410–414, [https://doi.org/10.1373/jalm.2016.021634](https://doi.org/10.1373/jalm.2016.021634)
[^6]: Formally, a waveform is a line graph with time on the x-axis and the measured value on the y-axis.
[^7]: Formally, a waveform is a line graph with time on the x-axis and the measured value on the y-axis.
[^8]: King BL, Meyer ML, Chari SV, Hurka-Richardson K, Bohrmann T, Chang PP, Rodgers JE, Busby-Whitehead J, Casey MF. Accuracy of the electronic health record's problem list in describing multimorbidity in patients with heart failure in the emergency department. PLoS One. 2022 Dec 13;17(12):e0279033. doi: 10.1371/journal.pone.0279033. PMID: 36512600; PMCID: PMC9747000.
[^9]: Feldman SS, Davlyatov G, Hall AG. Toward Understanding the Value of Missing Social Determinants of Health Data in Care Transition Planning. Appl Clin Inform. 2020 Aug;11(4):556-563. doi: 10.1055/s-0040-1715650. Epub 2020 Aug 26. PMID: 32851616; PMCID: PMC7449791.
[^10]: Sousa-Pinto B, Tarrio I, Blumenthal KG, Araújo L, Azevedo LF, Delgado L, Fonseca JA. Accuracy of penicillin allergy diagnostic tests: A systematic review and meta-analysis. J Allergy Clin Immunol. 2021 Jan;147(1):296-308. doi: 10.1016/j.jaci.2020.04.058. Epub 2020 May 21. PMID: 32446963; PMCID: PMC8019189.
[^11]: Cara E Ray, Geneva M Wilson, Ashley M Hughes, Cassie Cunningham Goedken, Eric Ping-Fei Liu, Margaret A Fitzpatrick, Katie J Suda, Satya Manasa Kota, Chinonyerem Nwankpa, Charlesnika T Evans, Alert fatigue measurement in clinical decision support: a systematic review, *Journal of the American Medical Informatics Association*, Volume 33, Issue 8, August 2026, Pages 1523–1531, [https://doi.org/10.1093/jamia/ocag064](https://doi.org/10.1093/jamia/ocag064)
[^12]: Diamond CJ, Thate J, Withall JB, Lee RY, Cato K, Rossetti SC. Generative AI Demonstrated Difficulty Reasoning on Nursing Flowsheet Data. AMIA Annu Symp Proc. 2025 May 22;2024:349-358. PMID: 40417556; PMCID: PMC12099445.
[^13]: Hashir M, Sawhney R. Towards unstructured mortality prediction with free-text clinical notes. J Biomed Inform. 2020 Aug;108:103489. doi: 10.1016/j.jbi.2020.103489. Epub 2020 Jun 25. PMID: 32592755.
