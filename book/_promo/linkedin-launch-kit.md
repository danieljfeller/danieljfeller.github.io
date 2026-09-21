# LinkedIn launch kit — *The Health Data Handbook*

Working drafts for the fall/winter distribution push. This folder starts with an
underscore, so Jekyll never publishes it. Edit freely.

**Share mechanics that matter on LinkedIn**
- Every chapter URL now unfurls with a title, the chapter's one-line description, and
  `images/book/social-card.png` (Open Graph tags from jekyll-seo-tag). Paste the link
  in the post body *or* in the first comment; both render the card.
- LinkedIn truncates posts after ~210 characters with "…see more". Put the hook in the
  first two lines. No links in the first two lines.
- Native images outperform link cards for reach. For chapter posts, attach the
  chapter's figure as an image (export the SVG to PNG at 1200 px wide) and put the
  chapter link in the first comment.
- One chapter per post, one post per week, gets you through the book by early spring.
  Suggested order below follows the book, but the EHR, claims, and multimodal chapters
  are the strongest standalone reads and can be pulled forward.
- Canonical link: https://danieljfeller.github.io/book/

---

## Launch post (long form)

I wrote a free book about health data, and today the full text is online.

It's called The Health Data Handbook. It exists because every "intro to healthcare data" I could find was either a 600-page informatics textbook or a vendor whitepaper, and neither would tell a data scientist joining a health tech company the three things they actually needed to know on Monday:

→ what a medical claim actually looks like, and why you can't trust the diagnosis codes in it
→ why "the ECG is in the EHR" is almost never true
→ what FASTQ, BAM, and VCF files are, and which one you'll be handed

So I wrote the version I wish I'd had. Sixteen chapters, one per data stream: medical and pharmacy claims, EHRs (the long one), medical imaging, clinical trials, molecular sequencing, wearables and home devices, patient-reported outcomes, de-identification, and a closing chapter that follows two patients through twelve months of data across every stream at once.

It's written for two kinds of readers: engineers and data scientists moving into healthcare from another industry, and people already deep in one healthcare domain (claims, genomics, EHR) who want to speak the others fluently.

It's free, CC BY-NC, no email gate. I'll be traveling across the country this fall and winter and would love to talk about it, argue about it, or hear what's wrong with it. Link in the comments.

#HealthData #HealthcareAI #DigitalHealth #HealthIT #DataScience #Interoperability

---

## Launch post (short form)

Every intro to healthcare data I could find was a 600-page textbook or a vendor PDF. So I wrote the one I wanted: sixteen short chapters, one per data stream, free online, no email gate.

The Health Data Handbook: claims, EHRs, imaging, trials, genomics, wearables, PROs, de-identification, and one chapter that follows two patients across all of it.

Link in the comments. Tell me what I got wrong.

---

## Chapter-by-chapter hooks (one post each)

Each block is a hook (first two lines), a body, and the link for the first comment.

### 1. Introduction
**Hook:** "Health data" is not one thing. It's at least eight, and they don't agree with each other.
**Body:** The opening chapter of The Health Data Handbook maps the streams: EHRs, imaging, sequencing, claims, trials, and the growing share of data collected outside the clinic entirely. If you're new to healthcare, start here. If you've been in one corner of it for a decade, start here too.
**Link:** https://danieljfeller.github.io/book/intro/introduction/

### 2. Core Concepts
**Hook:** A diagnosis isn't "the patient is diabetic." It's E11.9. A lab isn't "blood sugar was high." It's LOINC 2345-7, value 250.
**Body:** If you learn one thing before touching a health dataset, learn how controlled vocabularies work: ICD-10-CM, CPT, LOINC, RxNorm, NDC, SNOMED. This chapter is the table-stakes primer, with the seven vocabularies you must know and the twenty you should recognize.
**Link:** https://danieljfeller.github.io/book/intro/core-concepts/

### 3. Medical Claims
**Hook:** Only about 80% of patients with an HIV diagnosis code in claims data actually have HIV. The rest got the code for a screening test and nobody fixed it.
**Body:** Claims are the workhorse of healthcare analytics: the only practical view of a patient's care across the whole system. They're also optimized for getting paid, not for being clinically true. This chapter is what a claim contains, what an extract looks like, and where to be suspicious.
**Link:** https://danieljfeller.github.io/book/administrative/medical-claims/

### 4. Pharmacy Claims
**Hook:** Pharmacy claims are adjudicated in seconds at the counter. Medical claims take weeks. Guess which dataset is cleaner.
**Body:** The most structured, standardized data stream in healthcare, and the one behind adherence measurement (PDC, MPR), pharma market intelligence, and drug-safety surveillance. Includes what an NCPDP SCRIPT message looks like and the fields that make the analytics work.
**Link:** https://danieljfeller.github.io/book/administrative/pharmacy-claims/

### 5. Electronic Health Records
**Hook:** A 4-day hospital stay touched 250+ rows across two dozen Epic tables and generated 20 clinical notes. Here's the full inventory.
**Body:** The longest chapter in the book follows two patients through the EHR (a wellness visit, a heart-failure admission), then walks every data type: labs, devices, vitals, orders, problem lists, allergies, flowsheets, notes, and when to use FHIR versus OMOP. If you only read one chapter, this is the one.
**Link:** https://danieljfeller.github.io/book/clinical/ehr/

### 6. Medical Imaging
**Hook:** Most imaging-AI projects don't stall on the model. They stall on getting the DICOM out of PACS.
**Body:** Imaging is the heaviest data stream in healthcare and the one with the oldest, most universal standard. This chapter covers DICOM tags, the Patient → Study → Series → Instance hierarchy, PACS, and why de-identifying images is harder than dropping columns.
**Link:** https://danieljfeller.github.io/book/clinical/medical-imaging/

### 7. Clinical Trial Data
**Hook:** Clinical trial data is the cleanest data in healthcare. That's exactly why the other fifteen chapters exist.
**Body:** CRFs, EDC systems, and the CDISC pipeline (CDASH → SDTM → ADaM) regulators require. Plus the trade-off: clean causal answers about a narrow population versus messy answers about everyone.
**Link:** https://danieljfeller.github.io/book/clinical/clinical-trials/

### 8. Molecular Sequencing
**Hook:** FASTQ → BAM → CRAM → VCF. If you can explain what each one adds, you're ahead of most people who "work with genomic data."
**Body:** From raw reads to variants, with a figure for every file format and the pipeline that connects them. Written for people who will be handed a VCF, not people who will build a sequencer.
**Link:** https://danieljfeller.github.io/book/clinical/molecular-sequencing/

### 9. Vital Signs Monitoring
**Hook:** Blood pressure cuffs have been in a third of US homes for years. Almost none of that data ever reaches a medical record.
**Body:** CGMs, pulse oximeters, smart scales, and cardiac implantables: how each one measures, what it reports, and the manufacturer portals where the data actually lives.
**Link:** https://danieljfeller.github.io/book/patient-generated/vital-signs/

### 10. Adherence Monitoring Technology
**Hook:** Half of patients don't take their medications as prescribed. Smart pill bottles know. The EHR doesn't.
**Body:** Smart inhalers, ingestible sensors, connected injection pens: the technology works and the data goes nowhere. A short, honest chapter.
**Link:** https://danieljfeller.github.io/book/patient-generated/adherence/

### 11. Activity & Lifestyle
**Hook:** Insurers started paying people to hit step goals. Then they discovered the Fitbits were on the dog.
**Body:** How accelerometers count steps, how wearables guess at sleep stages (60–70% agreement with a sleep lab), and how to actually get the data out via Fitbit, Garmin, and HealthKit APIs.
**Link:** https://danieljfeller.github.io/book/patient-generated/activity-lifestyle/

### 12. Patient-Reported Outcomes
**Hook:** A lab can tell you a cancer patient's neutrophil count. Only the patient can tell you they're too tired to get out of bed.
**Body:** PROMIS and the PHQ-9: what makes a validated instrument analytically usable, why a score trajectory beats a snapshot, and why the real problem is administration, not measurement.
**Link:** https://danieljfeller.github.io/book/patient-generated/patient-reported-outcomes/

### 13. Complex & Unstructured Data
**Hook:** Your phone's camera and microphone are becoming clinical instruments. Most of that data sits outside HIPAA entirely.
**Body:** Patient-captured photos, vocal biomarkers, and digital phenotyping: signal-rich, interpretation-poor, and running ahead of the ethics. The frontier chapter.
**Link:** https://danieljfeller.github.io/book/patient-generated/complex-unstructured/

### 14. The Patient-Generated Data of the Future
**Hook:** Sweat patches that read cortisol. Wi-Fi that measures breathing. E-tattoos that record muscle activity. All of it is coming for your data model.
**Body:** The sensor advances (clinical-grade PPG, electrochemical sensing, contactless monitoring, electronic skin) that the medical domain needs to plan for now.
**Link:** https://danieljfeller.github.io/book/patient-generated/future/

### 15. Methods to De-Identify Health Data
**Hook:** "De-identified" means five different things depending on which regulation you're standing under.
**Body:** HIPAA Safe Harbor and Expert Determination, GDPR anonymization and pseudonymization, k-anonymity, and differential privacy, with what each one costs you analytically.
**Link:** https://danieljfeller.github.io/book/working-with-data/de-identification/

### 16. Putting It All Together
**Hook:** Two patients. Twelve months. Every data stream at once. One of them is nearly invisible to the data everyone trusts most.
**Body:** The closing chapter follows a man with diabetes and depression and a woman in fertility treatment across claims, EHR, PROs, and devices, then ends on the quiet hard problem underneath all of it: the US has no national patient identifier, so every cross-system view is a probabilistic guess.
**Link:** https://danieljfeller.github.io/book/working-with-data/multimodal-streams/
