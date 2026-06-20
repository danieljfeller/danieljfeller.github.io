---
layout: book
title: "Methods to De-Identify Health Data"
permalink: /book/working-with-data/de-identification/
---

Without de-identification, the secondary use of health data would be prohibited by the various data protection regulations across the globe.  Regulations like HIPAA in the United States and GDPR in the European Union set specific legal requirements for ensuring that data cannot be associated with the individual it represents. In the brief section below, the five most common models for de-identification are described.


### HIPAA Safe Harbor

HIPAA’s Safe Harbor method provides a checklist of 18 patient identifiers that must be removed if data is to be considered ‘de-identified’. Safe Harbor’s appeal lies in its ease of implementation.. However, this comes at the cost of analytical precision, as the data loses its temporal precision for longitudinal analysis and geographic analyses can’t get any more detailed than the state level. Despite these limitations, Safe Harbor remains the most commonly used de-identification method in commercial health data sales because it provides legal certainty without ongoing expert review (unlike HIPAA Expert Determination - see below).


| HIPAA Safe Harbor Prohibited Elements |  |
| --- | --- |
| Category | Element |
| Direct Personal Identifiers | Names Social Security numbers Telephone numbers Fax numbers Email addresses |
| Geographical Identifiers | Geographic subdivisions smaller than state (street address, city, county, ZIP code*) |
| Temporary Identifiers | Dates (birth, admission, discharge, death, etc.) except year |
| System & Record Identifiers | Medical record numbers Health plan beneficiary numbers Account numbers Certificate/license numbers |
| Device & Asset Identifiers | Vehicle identifiers and serial numbers Device identifiers and serial numbers |
| Network Identifiers | Web URLs IP addresses |
| Biometric & Image Identifiers | Biometric identifiers (fingerprints, voiceprints) Full-face photographs and comparable images |


### HIPAA Expert Determination

Expert determination is the second method under HIPAA for deidentifying protected health information wherein a statistician determines whether the risk of patient re-identification is ‘very small’ (<0.04% or <0.09% depending on interpretation). The expert must have appropriate knowledge and experience in statistical and scientific methods for rendering information not individually identifiable, and they must document their methodology, including which variables were considered, what re-identification attacks were modeled, and why the residual risk is acceptably low. This approach can preserve specific dates (enabling time-to-event analyses), detailed geographic information (down to ZIP codes or even smaller areas in low-risk scenarios), and exact ages including for elderly populations. The tradeoff for expanded feasibility of analysis is the cost, as organizations must hire PhD statisticians or consulting firms who in turn document their analysis thoroughly. Pharmaceutical companies and academic medical centers frequently use Expert Determination for high-value research collaborations where the inclusion of potentially identified data elements are required.


### GDPR Anonymization

The first of the two GDPR standards for de-identification is anonymization, which  requires that re-identification become practically impossible. This sets an extraordinarily high bar and requires the removal of direct identifiers and additional data elements such as rare diagnosis codes, employer names (especially if the company is small). European regulators often reference the data elements in HIPAA's Safe Harbor method, though GDPR requires risk assessment beyond any fixed list. The advantage of anonymization is that the data ceases to be subject to GDPR requirements, which are very strict and make data analysis and machine learning very challenging. However, true anonymization


### GDPR Pseudonymization

Pseudonymization under GDPR involves replacing direct identifiers with pseudonyms or encrypted tokens and storing the linkage key separately under strict access controls, thereby allowing re-identification only when necessary. This works by executing hash functions on patient identifiers and storing the identity of the patient in a different system than the hashed patient data. GDPR has multiple exemptions that allow researchers to use pseudonymized data without explicit patient consent. In contrast,  commercial entities must have a valid legal basis to use the data like patient consent, contractual necessity, or legal obligation. While pseudonymization is recognized as good security practice, it doesn't exempt companies from core GDPR requirements like data minimization, breach notification, and individual rights and EU regulators scrutinize commercial uses much more heavily than academic research.


### k-Anonymity and Differential Privacy

K-anonymity and differential privacy represent mathematically rigorous approaches to de-identification that provide formal privacy guarantees rather than relying on identifier removal alone. K-anonymity ensures that each record in a dataset is indistinguishable from at least k-1 other records when considering quasi-identifiers (attributes like age, gender, ZIP code that could enable re-identification when combined), typically implemented through generalization (broadening categories like "age 34" to "age 30-39") and suppression (removing outlier values). While k-anonymity is conceptually straightforward, it's vulnerable to attacks when the dataset includes homogeneous sensitive attributes (everyone in a group has the same rare disease) or when attackers have background knowledge; variants like l-diversity and t-closeness address these weaknesses by ensuring diversity of sensitive attributes within each group. Differential privacy takes a fundamentally different approach by adding carefully calibrated statistical noise to query results, mathematically guaranteeing that including or excluding any single individual's data doesn't meaningfully change the output—Apple uses this for iOS usage analytics, and the 2020 US Census applied it to published statistics. The privacy budget (epsilon parameter) controls the privacy-utility tradeoff: stronger privacy (lower epsilon) means more noise and less accurate results. These methods are increasingly popular in federated learning systems and research data enclaves where multiple queries are run against sensitive data, as they provide provable privacy bounds that traditional de-identification cannot offer, though they require sophisticated implementation and can significantly reduce data utility if applied too aggressively.
