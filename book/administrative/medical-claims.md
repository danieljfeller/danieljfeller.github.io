---
layout: book
title: "Medical Claims"
permalink: /book/administrative/medical-claims/
---


### The Workhorse of Modern Healthcare Analytics

Administrative claims data represents the financial transactions generated every time a patient receives healthcare services—medical visits, procedures, hospitalizations, and pharmacy fills. These claims flow from providers to insurers, creating a comprehensive record of healthcare utilization. Medical claims capture all doctor visits, hospitalizations, and medical procedures regardless of the office or hospital in which the encounter occurred. Likewise, pharmacy claims capture all of a patient’s medications, regardless of which pharmacy dispensed the drugs. Claims represent the only practical means of generating a complete view of a patient’s medical treatment and as a result represent the de facto source of truth for a patient's healthcare journey across the entire system.


### The World is Awash in Claims Data

Whether for profit or public health, virtually every player in healthcare leverages claims data as their primary operational intelligence. Publicly-traded pharmaceutical manufacturers like Eli Lilly use claims for market research, sales force optimization, competitive intelligence, and to assess how well their drugs are working in the ‘real-world’. Health insurers rely on historical claims data for their actuarial tables, rate-setting, and financial forecasting, making it the backbone of their underwriting. State and federal government agencies operate their own claims ecosystems: each state administers its Medicaid program essentially as a government-run health insurer, while the federal government administers Medicare (I like to think of the US government as an insurance company with an army). Health tech companies across the spectrum—from point solutions like Sword Health (purchased by employers to prevent expensive musculoskeletal surgery) to direct-to-consumer apps like GoodRx—all depend on claims data to understand utilization patterns and identify opportunities to provide value.


### What Do Medical Claims Actually Look Like?

Medical claims are generated each time a healthcare provider delivers services to a patient. After the encounter, the provider's billing department translates the clinical documentation into a standardized claim format - a 1500 form if the claim is to be sent via mail or an 837 file if the claim is to be sent electronically (most commonly as of 2025). Each individual claim will contain the following information:


| Category | Column | Description |
| --- | --- | --- |
| Header | Submitter ID | Unique identifier for the organization or clearinghouse transmitting the claim file to the payer |
|  | Received ID | Unique identifier for the payer or clearinghouse receiving the claim file |
|  | Transaction Control Number | Sequential numbers that uniquely identify each transaction set within the file for tracking and reconciliation |
|  | Datetime Stamps | Timestamps indicating when the claim file was created and transmitted |
| Billing Provider | NPI | National Provider Identifier, a unique 10-digit number assigned to healthcare providers for identification in administrative transactions |
|  | Tax ID | The provider's Employer Identification Number (EIN) or Social Security Number used for tax reporting and payment processing |
|  | Address | Physical location of the billing provider, required for payment remittance and correspondence |
|  | Facility Info | Details about the healthcare facility where services were rendered, including facility NPI, name, and location when different from billing provider |
| Patient Info | Name | Patient's legal name (last, first, middle) as it appears on insurance documents |
|  | DOB | Date of birth used to verify patient identity and determine age-related coverage rules |
|  | Gender | Patient's gender, relevant for coverage determinations and certain procedure eligibility |
|  | Address | Patient's current mailing address for correspondence and coordination of benefits |
|  | Insurance Member ID | Unique identifier assigned by the insurance company to the specific enrolled member |
|  | Insurance Policy ID | Group or policy number under which the patient is covered, often tied to employer or plan type |
| Claim Details | ICD10 Diagnosis Code | Standardized codes describing the patient's conditions, symptoms, or reasons for the encounter that justify medical necessity |
|  | CPT,HCPCS, ICD10PCS Procedure Codes | Codes identifying specific services, procedures, supplies, or equipment provided (CPT/HCPCS for professional/outpatient; ICD-10-PCS for inpatient) |
|  | Service Date | The date(s) when healthcare services were actually rendered to the patient |
|  | Charges & Units | The provider's billed amount and quantity of services performed (e.g., number of units, days, or visits) |
|  | Modifiers | Two-character codes appended to procedure codes to provide additional information about how services were performed or circumstances affecting payment |
|  | Place of Service Code | Two-digit codes identifying the physical location or setting where services were delivered (e.g., office, hospital, emergency room) |
| Supporting Info | Referring Provider NPI | NPIs for physicians who referred the patient (when different from the billing provider) |
|  | Rendering Provider NPI | NPIs for physicians who actually performed the service (when different from the billing provider) |
|  | Prior Authorization Numbers | Reference numbers obtained from the payer approving coverage for specific services before they were rendere |
|  | Coordination of Benefits | Information about other insurance coverage the patient may have to determine primary versus secondary payment responsibility |
|  | Notes | Additional clinical information, explanations, or documentation supporting the claim that doesn't fit in standard fields |

Although millions of individual claims are submitted each day, most analysts and data scientists won’t ever see an actual claim. The most common format of medical claims data are commonly referred to as claims extracts. These are all paid claims (which have been processed and settled by insurance providers) and come in large flat files - often CSVs or Excel files. The claims extracts that  insurance carriers generate are guaranteed to look a bit different from one another, mostly in the column names and ordering of the columns will vary. However, the content is largely standardized between them.

No standard for storing medical claims has gained widespread adoption, perhaps because standardizing medical claims is trivial compared to other health data streams like EHR data. While both FHIR and OMOP Data Models (to be discussed at length in Chapter X) include dedicated tables for claims and cost data, these are used only in specific use cases and applications. In practice, claims data remains stored in proprietary relational schemas.

Warning! Don’t Trust The Diagnostic Information In Claims

The simplicity and comprehensiveness of medical claims can be enticing, as it looks like a long-term representation of a patient’s healthcare experience. While this data provides a comprehensive view of patient encounters across the healthcare system, the diagnostic codes in claims are very often inaccurate. Validation studies have consistently shown that diagnosis codes are often assigned to individuals who lack that diagnosis. HIV diagnosis codes are a classic example, as studies have found that only about 80% of patients with such a code in medical claims actually have the disease. In such cases, HIV is often incorrectly assigned as a diagnosis code for HIV screening procedures and never corrected. While workarounds exist - algorithms that combine multiple diagnosis codes have improved accuracy - the challenge of using medical claims as robust clinical indicators remain.


### Quick Reference


| Data Stream | Medical Claims Data |
| --- | --- |
| Description | Healthcare's operational backbone—financial transactions capturing every patient encounter across the entire healthcare system |
| Access & Availability | Owned by payers (commercial insurers, Medicare, Medicaid state programs); Access via data vendors (Optum, IQVIA, Komodo Health), direct payer agreements, claims clearinghouses, CMS limited datasets for researchers; HIPAA-governed—requires Business Associate Agreement for identified data, Safe Harbor or Expert Determination for de-identified data |
| Key Data Elements | Claim ID (unique identifier for each submission), Patient Member ID (links to insurance enrollment), Provider NPI (identifies rendering/billing provider), Diagnosis Codes ICD-10-CM (conditions justifying medical necessity), Procedure Codes CPT/HCPCS/ICD-10-PCS (services/procedures delivered), Service Date (when care was provided), Billed/Paid Amounts (charges and actual payments), Place of Service (where care occurred) |
| Data Models | Data extracts from individual insurers and data vendors come in bespoke formats - there is no widely used data model. |
| Standard Vocabularies: | ICD-10-CM (diagnoses), CPT (procedures), HCPCS (supplies/equipment), ICD-10-PCS (inpatient procedures) |
| Data Storage | Relational databases and flat files (CSV). |
| Expected Data Quality | Structural completeness is excellent ( >99% fields populated) due to the use of this data in reimbursement. Clinical information has moderate accuracy (~80%) because the data is optimized for billing, not clinical prevision. |
| Integration Considerations: | Links to pharmacy claims via Member ID. Enriches with NPI Registry for provider information. Can append social determinants (ZIP to census data). Difficult to link to EHR clinical data without patient consent or trusted third party. |
| Further Resources: | CMS Claims Data Dictionary and documentation (cms.gov/data-research); Tuva Health open-source claims data model (thetuvaproject.com) |
