---
layout: book
title: "Pharmacy Claims"
permalink: /book/administrative/pharmacy-claims/
---


### Structured, Standardized, and Ready to Analyze

When a patient picks up their medication, the pharmacy submits a claim to the insurer documenting what was dispensed, how much it cost, and who paid what portion. This creates a comprehensive record of every pill bottle, inhaler, and injectable that crosses the pharmacy counter. As a result, pharmacy claims capture every prescription filled by patients. Unlike medical claims, pharmacy claims are generated in real-time. When a pharmacy types a patient’s insurance information into their system, a query is submitted to the patient’s insurance company (these are called PBMs, or pharmacy benefit managers). Within seconds, the system will accept or reject the claim and identify the copay amount that the patient must pay. This real-time adjudication means pharmacy claims are remarkably clean and complete compared to medical claims, which can take weeks to process and often contain errors.


### What Do Pharmacy Claims Actually Look Like?

The National Council for Prescription Drug Programs (NCPDP) created a standard transaction format to ensure interoperability between all pharmacies and PBMs. As of 2026, over 90% of US prescriptions are transmitted electronically using NCPDP standards (the remaining 10% are transmitted via handwritten prescriptions and faxed orders).

An example NCPDP SCRIPT message can be seen below. This message contains a new prescription for 30 tablets of Lisinopril 10mg with instructions to take one tablet daily. The message includes identifying information for the prescriber (Dr. John Smith with NPI 1234567890) and patient (Jane Doe, female, born May 15, 1980). The header contains routing information showing which systems are sending and receiving the prescription, along with a message ID and timestamp. The XML below has been edited for brevity:


| <?xml version="1.0" encoding="UTF-8"?> <NewRx xmlns="http://www.ncpdp.org/schema/SCRIPT/2017071" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"> <MessageHeader> <MessageID>MSG20231212001</MessageID> <SentTime>2023-12-12T10:30:00</SentTime> <Sender> <SenderID>1234567890</SenderID> </Sender> <Receiver> <ReceiverID>9876543210</ReceiverID> </Receiver> </MessageHeader> <Patient> <PatientID> <ID>PAT12345</ID> </PatientID> <Name> <LastName>Doe</LastName> <FirstName>Jane</FirstName> </Name> <Gender>F</Gender> <DateOfBirth> <Date>19800515</Date> </DateOfBirth> </Patient> <MedicationPrescribed> <DrugCoded> <ProductCode>197361</ProductCode> <ProductCodeQualifier>RXNORM</ProductCodeQualifier> <DrugDescription>Lisinopril 10 MG Oral Tablet</DrugDescription> </DrugCoded> |
| --- |

Thankfully, this is not a format that an analyst would ever need to work with, as Pharmacy Benefit Managers stored hundreds of thousands of transactions in relational databases and this tabular format is what is typically used for analysis.


### Aggregated Pharmacy Claims for Analytics & Machine Learning

PBMs aggregate individual pharmacy claims by extracting de-identified records from their transactional adjudication databases, applying HIPAA Safe Harbor or Expert Determination methods to remove direct patient identifiers while retaining clinically relevant attributes like age ranges, geographic regions, and diagnosis codes. They typically standardize drug codes to NDC-11 format, map prescriber information to specialty taxonomies, and calculate summary statistics across therapeutic classes, time periods, and member populations to create analytical datasets. These aggregated datasets are then enriched with additional context like formulary tier assignments, therapeutic interchange patterns, and adherence metrics before being packaged for sale to manufacturers, researchers, or employers seeking market intelligence.

Data vendors like IQVIA, Optum, and Komodo Health also aggregate de-identified prescription claims across multiple health insurers and pharmacies to create national and regional prescription datasets. Such data can be collected from pharmacy chains, mail-order pharmacies, and PBMs themselves and then standardized and anonymized before being sold to drug manufacturers, researchers, and insurers for market analyses and drug utilization studies.


| Category | Column | Description |
| --- | --- | --- |
| Claim Identifiers | Prescription Number | The pharmacy's internal tracking number, unique to that fill at that pharmacy. |
|  | Refill Number | Distinguishes the original fill (0) from first refill (1), second refill (2), etc. Most prescriptions allow a limited number of refills. |
|  | Fill Date | When the prescription was dispensed, not when it was written. |
|  | Service Provider ID | Identifies the specific pharmacy location. National chains have different IDs for each store. |
| Patient Information | Member ID | Unique identifier assigned by the insurance company to the enrolled member. |
|  | Date of Birth | Patient's date of birth used to verify identity and determine age-related coverage rules. |
|  | Gender | Patient's gender, relevant for coverage determinations and certain procedure eligibility. |
| Medication Information | NDC Code | The 11-digit National Drug Code identifies the exact product dispensed—manufacturer, strength, and package size. NDC 00781-1506-10 specifies Sandoz's amoxicillin 500mg capsules in a 21-count bottle, not the 30-count bottle or another manufacturer's version. |
|  | Drug Name | Both brand and generic names appear. A claim might show "Lipitor (atorvastatin)" so analysts can search either way. |
|  | Therapeutic Class | Drugs are categorized by what they treat. All statins get grouped together, all SSRIs together, making it easy to analyze treatment patterns without listing every individual medication. |
|  | Quantity Dispensed | Number of pills, milliliters of liquid, or doses in an inhaler. |
|  | Days Supply | How long the prescription should last. Typically either 30 or 90 days. |
|  | Strength | The dose per unit. Metformin comes in 500mg, 850mg, and 1000mg tablets, and the claim specifies which was dispensed. |
| Cost and Payment | Ingredient Cost | What the pharmacy paid to acquire the drug from the wholesaler. |
|  | Dispensing Fee | The pharmacy's charge for filling the prescription—typically $2-5 per prescription. |
|  | Patient Paid Amount | What the patient paid at the counter—their copay or full cash price if uninsured. |
|  | Plan Paid Amount | What the insurance company paid. The sum of patient paid and plan paid equals the total allowed amount. |
|  | Usual & Customary Charge | The pharmacy's standard retail price before any insurance or discounts. This is often much higher than what actually gets paid. |
| Prescriber Information | Prescriber NPI | The physician's unique identifier, linking the prescription back to the ordering doctor. |
|  | DEA Number | Required for controlled substances, this identifies providers authorized to prescribe narcotics and other scheduled drugs. |

In the following section, the utility of these fields are demonstrated in each of the paragraphs describing an analytic use case for pharmacy claims.


### How Pharmacy Claims Are Used Today

Pharmaceutical manufacturers use aggregated pharmacy claims for market intelligence to track market share, prescribing trends, and competitive dynamics. A manufacturer of diabetes drugs might monitor trends in the number of prescriptions filled grouped by product (NDC Code, Drug Name), geography (Service Provider ID linked to ZIP codes), and prescriber specialty (Prescriber NPI mapped to taxonomy codes), to assess whether their competitors are gaining market share in the United States.

Health plans and care management programs continuously monitor medication adherence of their members. Medication adherence approximates whether a patient is taking their drugs as prescribed, which is critically important for persons with chronic conditions. For example, a person living with HIV must take medications as prescribed at least 8 out of 10 days to achieve viral load suppression. There are a few ways to calculate adherence, including Medication Possession Ratio (MPR), which divides the total days' supply of medication (Days Supply) dispensed by the number of days in a specified period, or the Proportion of Days Covered (PDC), which measures the percentage of days a patient has medication available during a treatment period (Fill Date + Days Supply) while accounting for overlapping prescriptions. It must be noted that both these measures are based on refills and thus are proxy measures for whether the patient is actually taking their medication.

When linked with medical claims, pharmacy claims can be used for comparative effectiveness studies to examine the effectiveness of drugs and understand their safety profiles in the real-world rather than controlled clinical trials. A retrospective study might compare cardiovascular outcomes among patients taking different statin medications (identified via NDC Code or Therapeutic Class) while controlling for medication adherenceThe cardiovascular events are identified using Diagnosis Codes (heart attacks or strokes) from linked medical claims occurring within 6 months of treatment initiation.. These analyses are often conducted by PBMs and professional societies  to inform formulary decisions and clinical guidelines.

Pharmaceutical sales and marketing teams aggregate claims by Prescriber NPI to build detailed prescribing profiles quantifying total prescription volume, therapeutic area mix (Therapeutic Class), brand versus generic preferences (branded vs. generic NDC Code), and new drug adoption velocity (Fill Date relative to FDA approval). A company launching a novel migraine medication identifies neurologists (Prescriber NPI) prescribing high volumes of competing drugs (NDC Code). Moreover, regulatory bodies might use pharmacy claims to identify prescribers with excessive opioid prescribing (high Quantity Dispensed via DEA Number claims) or inappropriate antibiotic selection patterns (NDC Code).

PBMs and health plans implement real-time drug utilization review (DUR) algorithms to make sure that patients won’t be harmed by their prescribed medications. These reviews might uncover drug-drug interactions where medications prescribed by different providers interact poorly with each other, as well as therapeutic duplication where patients unknowingly receive multiple drugs with similar therapeutic effects. Adolescents or elderly patients might be harmed by inappropriate dosages and contraindications based on patient conditions or allergies, and overutilization that suggest potential abuse.


### Quick Reference: Pharmacy Claims


| Data Stream | Pharmacy  Claims |
| --- | --- |
| Description | Real-time transactional records of every prescription filled, capturing medication dispensing with exceptional completeness and accuracy |
| Data Generating Process | When a patient picks up medication, the pharmacy submits a claim to the patient's insurance company (PBM - Pharmacy Benefit Manager) documenting what was dispensed, cost, and payment split. Unlike medical claims, pharmacy claims are adjudicated in real-time (within seconds), creating remarkably clean and complete records. Over 90% of US prescriptions use NCPDP electronic standards as of 2026. |
| Access & Availability | Owned by PBMs (CVS Caremark, Express Scripts, OptumRx) and health insurers; Access via data vendors (IQVIA, Optum, Komodo Health), direct PBM agreements, retail pharmacy chains, Medicare Part D datasets; HIPAA-governed—requires Business Associate Agreement for identified data; Real-time adjudication data stays within PBM systems, while aggregated/de-identified extracts sold for analytics |
| Key Data Elements | Prescription Number (pharmacy's internal tracking ID), NDC Code (11-digit identifier specifying exact product—manufacturer, strength, package size), Fill Date (when dispensed, not written), Days Supply (intended duration, typically 30 or 90 days), Quantity Dispensed (number of pills/doses), Patient Paid Amount (copay at counter), Plan Paid Amount (insurance payment), Prescriber NPI (ordering physician identifier) |
| Data Models | NCPDP SCRIPT standard (XML format for prescription transmission between prescribers, pharmacies, and PBMs); OMOP Drug_Exposure table (for research datasets); FHIR MedicationDispense resource (emerging but limited adoption); Most analytics use proprietary flat-file schemas |
| Standard Vocabularies: | NDC (National Drug Code - primary identifier for dispensed products), RxNorm (normalized medication names linking vocabularies), GPI (Generic Product Identifier - alternative classification in some PBM systems), ATC (Anatomical Therapeutic Chemical - international drug classification), Therapeutic Class groupings (vendor-specific hierarchies) |
| How is Data Typically Stored? | Transaction format: NCPDP SCRIPT (XML) for real-time adjudication; Analytics extracts: flat CSV files with one row per fill; Enterprise systems: relational databases (SQL Server, Oracle) with star schemas; Research datasets: de-identified CSV/SAS files or loaded into OMOP CDM; Typical fields: 30-50 columns per record |
| Expected Data Quality: | Grade: AStructural completeness: AClinical Accuracy: A Temporal Precision: A |
| Limitations: | Captures dispensing, not consumption. Patients may not take medications as prescribed. Missing cash-pay transactions when patients bypass insurance (e.g., GoodRx coupons, cheap generics) Therapeutic intent ambiguous. Same drug is often prescribed for multiple conditions. |
| Integration Considerations: | Can easily be integrated with medical claims as long as there is a common member ID. This can be challenging when different insurers cover medical and pharmacy benefits. |
| Further Resources: |  |
