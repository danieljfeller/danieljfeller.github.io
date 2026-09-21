---
layout: book
title: "Putting It All Together: Multimodal Data Streams"
description: "Two patients, twelve months, every data stream at once, and why record linkage is the quiet hard problem underneath it all."
permalink: /book/working-with-data/multimodal-streams/
---

## Charting Patient Journeys Across Time and Space

Every chapter until now has taken a single data stream and examined it in isolation—the discipline this book was built on, because each stream really does have its own ecosystem. But no patient experiences their health one stream at a time. A real person generates claims and clinical records and device data and questionnaire scores simultaneously, and the streams overlap, contradict, and complement one another in ways that only become visible when you lay them side by side. This closing chapter does exactly that: it follows two patients across twelve months and watches every data stream from the book fire at once. The goal is not new facts but new *seeing*—recognizing how the pieces you now understand individually assemble into a life.

### 12 months of data for 59 year old male with diabetes and moderate depression

Consider a 59-year-old man with type 2 diabetes and moderate depression—the archetypal patient behind much value-based care, because his conditions are chronic, common, and manageable if the data is used well. Over twelve months, here is what he generates.

From pharmacy claims: recurring fills for metformin and an SSRI, each with a fill date and days' supply. Run the adherence math from Part II and a story emerges—a proportion of days covered that dips below 0.8 in the spring, a two-month gap in the antidepressant, telltale evidence that he stopped taking it. Note what the claims *cannot* tell you: only that the prescriptions were filled, never that the pills were swallowed.

From medical claims and the EHR: quarterly primary-care visits, an endocrinology referral, and the labs that anchor diabetes care—a hemoglobin A1c that reads 8.4% in January and 7.6% by autumn. In the EHR these arrive as clean, LOINC-coded lab results (the most trustworthy data in the whole record), alongside a problem list carrying both diabetes and depression, and encounter diagnoses that exist mostly to justify the billing.

From patient-reported outcomes: PHQ-9 scores administered by his primary-care practice's collaborative-care program—16 in February, 11 in May, 8 by August. This is the depression trajectory made legible, and crucially it *rhymes with the pharmacy data*: the PHQ-9 improvement stalls during exactly the window when the SSRI fills lapse. Neither stream proves causation, but together they tell a coherent clinical story that neither tells alone.

From patient-generated devices: a continuous glucose monitor reporting time in range climbing from 52% to 68% as his A1c falls—continuous confirmation of the twice-a-year lab—and a wrist wearable logging steps and sleep, with a visible dip in activity and a rise in fragmented sleep during his low-mood, low-adherence stretch.

The lesson of the composite is that the streams are partial and mutually correcting. The A1c is accurate but sparse; the CGM is dense but siloed in a manufacturer's portal; the pharmacy claims reveal a gap the clinician may never have known about; the PHQ-9 quantifies a mood the labs can't see; the wearable hints at the behavioral undercurrent beneath all of it. Assembled on one timeline, they reconstruct something close to the lived year. Held apart—which is how the health system actually stores them—each is a fragment, and the connections that make them meaningful are invisible.

<figure>
  <img src="{{ '/images/book/multimodal-timeline.svg' | relative_url }}" alt="Five stacked time-series tracks over twelve months for one patient: antidepressant fill coverage with a gap in March and April, hemoglobin A1c falling from 8.4 to 7.6 percent, PHQ-9 scores falling from 16 to 8 with a plateau during the gap, CGM time in range rising from 52 to 68 percent, and daily steps dipping in the spring; the adherence gap is shaded across all tracks">
  <figcaption>Twelve months of data for a 59-year-old man with type 2 diabetes and moderate depression, one stream per track. The shaded band marks the two-month gap in SSRI fills visible in pharmacy claims; the PHQ-9 improvement stalls and activity dips in exactly that window, while the A1c and CGM time in range improve as the year goes on. No single track tells the story; together they do. Illustrative synthetic data.</figcaption>
</figure>

### 12 months of data from 29 year old woman with infertility

The second patient illustrates the opposite and equally important lesson: what happens when the data streams have *holes*. A 29-year-old woman pursuing fertility treatment generates a year of intense medical activity—and much of it is invisible to the sources analysts most rely on.

From the EHR at a reproductive-endocrinology clinic: a dense record of monitoring. Serial labs—AMH, FSH, estradiol, LH, progesterone—tracked across cycles, and frequent transvaginal ultrasounds counting and measuring follicles. Clinically this is some of the richest, most tightly time-stamped data any patient produces, all of it structured and coded.

From medications, an instructive split. Oral agents like clomiphene appear as ordinary pharmacy claims. But the injectable gonadotropins central to IVF are often administered or billed differently, and—critically—much fertility care is paid out of pocket, because coverage is inconsistent and many patients have no infertility benefit at all. Cash-pay care is nearly invisible to the claims data that this book calls the closest thing to a complete view of a patient. An analyst looking only at claims would see a young, apparently healthy woman with a few scattered charges, and would completely miss the most significant medical undertaking of her year.

From patient-generated data, a stream that is often *primary* rather than supplementary: cycle-tracking apps, basal body temperature, and ovulation (LH) test results, logged daily by a highly engaged patient. For fertility, the patient's own longitudinal record can be more continuous than the clinic's, and it lives entirely outside the medical record.

From patient-reported outcomes: infertility carries a heavy psychological burden, and validated anxiety and depression measures (PROMIS domains, PHQ-9) may capture a mental-health trajectory that runs alongside the physical treatment—and that, like the treatment itself, may never surface in claims.

The composite lesson is the mirror image of the first patient. There, the streams corroborated one another. Here, the *dominant* stream (the EHR) is comprehensive while the stream we usually trust most (claims) is systematically blind, because the care was cash-pay. This is the trap of assuming any single source is complete: the same claims data that gives a near-total view of the diabetic man gives a badly distorted view of this woman, and only knowing *why*—which streams see which kinds of care, and which kinds of payment—keeps an analyst from drawing confidently wrong conclusions.

<figure>
  <img src="{{ '/images/book/stream-coverage-maps.svg' | relative_url }}" alt="Two side-by-side grids, one per patient, with data streams as rows and the year&#x27;s care events as columns; filled cells show events captured by a stream, hollow cells show blind spots, highlighting that cash-pay fertility care is invisible to claims data">
  <figcaption>Which streams see which events. For the man with diabetes (left), claims, EHR, PRO, and device data overlap and corroborate one another. For the woman pursuing fertility treatment (right), the EHR is comprehensive but claims are systematically blind to cash-pay care, and her most continuous record lives in a cycle-tracking app outside the medical record. Filled: captured. Hollow: not captured. Illustrative.</figcaption>
</figure>

## The Challenge of Record Linkage

Both vignettes above quietly assumed the hard part was already solved: that all of a patient's claims, records, device readings, and questionnaire scores could be gathered under one person. In reality, that assembly is one of the deepest unsolved problems in health data, and it deserves the book's final word.

The root cause is structural and specifically American: the United States has no national patient identifier. A 1990s federal law that envisioned one was effectively blocked by privacy concerns, and Congress has renewed the funding ban on it almost every year since the early 1990s.[^1] The consequence is that the same person has a different ID in every system—a member ID at each insurer, a medical record number at each hospital, an account at each device manufacturer—and nothing ties them together by design. Every cross-system view of a patient in this book is therefore an act of *inference*.

That inference takes two forms. Deterministic matching links records only when specified identifiers agree exactly (same name, date of birth, and Social Security number, say). It is precise but brittle: a typo, a maiden name, a transposed birthdate, and the match silently fails. Probabilistic matching scores partial agreement across many fields and links records above a confidence threshold, tolerating the messiness of real data at the cost of introducing uncertainty. Large organizations run an Enterprise Master Patient Index (EMPI) to maintain these links at scale, and even good ones live with two opposing failure modes: false negatives (one patient's records split across multiple identities, fragmenting their history) and false positives (two different people merged into one, which can be clinically dangerous).

There is also a privacy tension at the heart of linkage: matching people across datasets requires identifiers, but the whole thrust of the de-identification chapter was to *remove* identifiers. The reconciliation is privacy-preserving record linkage, most visibly the tokenization approach commercialized by vendors like Datavant, in which identifiers are irreversibly hashed into tokens that can be matched across datasets without exposing the underlying PHI. It is an elegant answer, but not a perfect one—match rates are imperfect, tokens degrade with the same dirty-data problems as any linkage, and different tokenization schemes don't interoperate.

The honest closing note is that record linkage is a quiet determinant of quality in nearly every multi-source health-data project, and it is usually underestimated. The composite patient journeys that make this data so powerful are only as trustworthy as the links beneath them, and those links are probabilistic guesses standing in for an identifier the country chose not to build. Anyone assembling a patient's story across streams is, whether they realize it or not, betting on record linkage—and should size that bet honestly.

[^1]: amia.org/public-policy/public-comments/patient-id-now-urges-congress-remove-longstanding-ban-national
