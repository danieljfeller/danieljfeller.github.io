---
layout: book
title: "A Primer on Healthcare Vocabularies"
permalink: /book/intro/vocabularies/
---

If you're new to healthcare data, understanding controlled vocabularies is the single most important foundation you need to build before anything else makes sense. Healthcare vocabularies are the fundamental language through which healthcare information is stored, exchanged, and analyzed. Without understanding these standardized code sets and terminologies, you'll struggle to interpret datasets, follow technical conversations, or conduct meaningful analysis.

When healthcare professionals talk about “data”, they're often talking about vocabularies. A diagnosis isn't just text saying "the patient is diabetic"—it's ICD-10-CM code E11.9. A lab result isn't just "blood sugar was high"—it's LOINC code 2345-7 with a value of 250 mg/dL. A prescription isn't just "amoxicillin 10mg"—it's an NDC code identifying the specific manufacturer, strength, and package size. Nearly every clinical observation, billable service, medication order, and diagnostic finding in a healthcare dataset exists as a manifestation of some controlled vocabulary.

This is fundamentally different from how data works in other industries. In e-commerce, you might have product descriptions in natural language. In social media, posts are free text. But in healthcare, the complexity, precision, and interoperability required means that structured, coded data dominates by necessity. When you open a claims file or query an EHR database, you're looking at rows of codes from dozens of different vocabularies each with a specific purpose.


#### Why are healthcare vocabularies needed?

Healthcare generates staggering complexity: there >70,000 diagnoses, more than 90,000 distinct laboratory tests, tens of thousands of procedures,and more than 20,000 protein-coding genes in the human genome. More than 300,000 unique medications have been produced for human consumption. This motivates the need for standard vocabularies (aka terminologies or code sets) to organize and systematize this complexity. Without vocabularies, healthcare data would be completely unmanageable—imagine trying to analyze or share information across systems when every provider uses their own terms for thousands of different conditions, tests, and treatments.


#### What is in a healthcare vocabulary?

Every healthcare vocabulary has three critical components that you need to know:

Codes (Identifiers): These are unique alphanumeric identifiers assigned to each concept in the vocabulary. Codes provide a compact, unambiguous way to reference concepts in databases and transactions. Some vocabularies use meaningful codes (where the structure conveys information) while others use arbitrary identifiers.

Descriptions (Display Names): Human-readable text that explains what each code represents. A single code often has multiple descriptions for display suitable for different types of usage. For example, the procedure code 99213 has three different display names

Short display name: "Office visit, established patient, level 3"

Longer description: "Office or other outpatient visit for the evaluation and management of an established patient, which requires a medically appropriate history and/or examination and low level of medical decision making"

Full official description: The complete CPT descriptor includes detailed criteria about the typical time spent (20-29 minutes), the nature of presenting problems (low to moderate severity), and specific documentation requirements.

Hierarchies (Parent-Child Relationships): Most vocabularies organize concepts into taxonomies where more specific concepts roll up to broader categories. These hierarchies enable data aggregation—you can query for all subtypes of a specific condition without enumerating every subtype.For example, the ICD-10-CM code S86.011D represents a strain of the right achilles tendon. The first characters - S86 - represent an injury of muscle, fascia, and tendon of the lower leg. The following characters - .011 - localize that injury to the right achilles tendon. The final character - D - asserts that the diagnosis was observed at a subsequent encounter (i.e. not at the initial diagnosis). See below for a breakdown of this code.

<figure>
  <img src="{{ '/images/book/icd10-code-structure.png' | relative_url }}" alt="ICD-10-CM code structure diagram for S86.011D showing category, etiology/anatomic site, and extension components">
  <figcaption>ICD-10-CM code S86.011D broken into its three components: S86 (category — injury of muscle, fascia, and tendon of lower leg), .011 (etiology/anatomic site — strain of right Achilles tendon), and D (extension — subsequent encounter).</figcaption>
</figure>


#### What healthcare vocabularies do you need to know?


##### Foundational Vocabularies

If you're new to healthcare, I suggest familiarizing yourself with a handful of foundational vocabularies. They appear across most healthcare datasets generated from either clinical practice or claims and form the backbone of most analytics and interoperability efforts.


| Data Stream | Vocabulary | Example |
| --- | --- | --- |
| Billing | ICD-10-CM: With over 70,000 codes, it captures everything from common conditions like diabetes to rare genetic disorders. You'll see these codes on every medical claim and encounter summary. | E11.9 Type 2 diabetes mellitus without complications |
|  | CPT: Represent the procedures and visits outside of hospital settings. Determine how much providers get paid for their services. | 99213 Office visit, established patient, level 3 |
|  | ICD-10-PCS: Represent inpatient hospital procedures with extreme specificity through its seven-character structure. | 0DT60ZZ Resection of stomach, open approach |
|  | HCPCS: Cover medical supplies, durable medical equipment, ambulance services, and other items that fall outside the CPT system. | E0607 Home blood glucose monitor |
|  | NDC: Identify manufacturer, formulation, and package size of drug products. With over 300,000 active codes, NDCs are essential for pharmacy claims and medication dispensing records. | 00781-1506-10 Amoxicillin 500mg capsules, 21-count bottle |
|  | RxNorm: Provides normalized medication names that link different drug vocabularies together. | 197361 Amoxicillin 500 MG Oral Capsule |
| EHR Data | LOINC: Standardizes laboratory tests and clinical observations. | 2345-7 Glucose [Mass/volume] in serum or plasma |

Becoming familiar with the vocabularies above represents 'table stakes' for anyone operating in the healthcare data space. These vocabularies are the shared language that connects clinical care, billing operations, quality measurement, population health, and regulatory compliance. If you’re able to speak with confidence about these vocabularies, any peers in the health tech field will recognize you as someone who knows what they are talking about.


##### Advanced Vocabularies by Data Stream

As a data professional, you'll encounter more specialized vocabularies depending on the specific healthcare data you're working with. The table below presents vocabularies organized by data stream—from genomics to quality measurement to clinical  research—that are used in specialized contexts but won't be encountered in everyday healthcare data work. These don't require memorization, and this list is far from exhaustive; there are hundreds of additional vocabularies in active use across healthcare. The purpose of the table below is to provide you with awareness, not encyclopedic knowledge, so that you can understand that each domain of medicine and research has specific vocabularies to encode the concepts they frequently encounter.


| Data Stream | Vocabulary | Example |
| --- | --- | --- |
| Medications | ATC: International system that groups drugs by organ system and therapeutic use. Particularly common in European data and research contexts. | J01CA04 Amoxicillin (antibacterial for systemic use, beta-lactam penicillin) |
|  | GPI: Alternative drug classification system found in some pharmacy benefit management systems and commercial databases. | 12150010000310 Amoxicillin 500mg oral capsule |
| EHR Data | SNOMED: Most comprehensive clinical terminology, covering diagnoses, findings, procedures, body structures, organisms, and more. Features concept-based structure and rich hierarchies. | 73211009 Diabetes mellitus |
|  | UCUM: Standardizes units of measurement for lab values and vital signs. Ensures that "mg/dL" means the same thing everywhere and enables proper comparisons across systems. | mg/dL Milligrams per deciliter |
|  | RadLex: Provides specialized terminology for radiology, capturing the detailed concepts that appear in imaging reports and structured radiology data. | RID5825 Pneumonia |
| Provider Identity | NPI: Unique identifier for every healthcare provider in the US. Used to link claims to specific physicians, practices, and facilities. | 1234567893 Dr. Jane Smith, Family Medicine |
|  | Taxonomy Codes: Classify provider specialties and roles. Help distinguish between cardiologists and cardiac surgeons, or nurse practitioners and registered nurses. | 207R00000X Internal Medicine |
| Genomics | HGNC: Provides standardized names for human genes, ensuring that researchers and clinicians refer to genes consistently. | BRCA1 BRCA1 DNA repair associated gene |
|  | HGVS: Describes genetic sequence variants in a structured format that precisely communicates mutations and alterations. | NM_000059.3:c.68_69delAG BRCA1 frameshift deletion |
|  | ClinVar: Catalogs the clinical significance of genetic variants, linking specific mutations to disease risk and treatment implications. | VCV000017666.5 BRCA1 c.68_69delAG Pathogenic for breast/ovarian cancer |
|  | HPO: Describes phenotypic abnormalities in a standardized way, crucial for linking clinical presentations to underlying genetic causes. | HP:0001513 Obesity |
|  | OMIM: Catalogs genetic disorders and their associated genes, serving as a comprehensive reference for genetic diseases. | 114480 Breast-ovarian cancer, familial, susceptibility to, 1 |
| Devices & Supplies | GMDN: Classifies medical devices internationally, essential for regulatory reporting and device tracking. | 34022 Blood glucose meter |
| Research | MedDRA: Standardizes adverse event reporting in clinical trials and post-market surveillance, required by regulatory agencies worldwide. | 10019211 Hyperglycaemia (high-level term for adverse event reporting) |
|  | OMOP Domains: Provide a unified framework for observational research that integrates multiple source vocabularies into a common data model, enabling large-scale comparative effectiveness research. | 201826 Type 2 diabetes mellitus |
|  | NCI Thesaurus: Offers comprehensive cancer-related terminology used in oncology research and clinical trials. | C2926 Breast carcinoma |
