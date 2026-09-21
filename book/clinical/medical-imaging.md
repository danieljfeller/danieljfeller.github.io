---
layout: book
title: "Medical Imaging"
description: "DICOM, PACS, and the Patient→Study→Series→Instance hierarchy behind every X-ray, CT, and MRI."
permalink: /book/clinical/medical-imaging/
---

## Introduction to the DICOM Standard

Medical imaging is the most data-heavy stream in this entire book. A routine visit generates kilobytes; imaging generates megabytes to gigabytes per study—recall the earlier figures of roughly 15 MB for a chest X-ray, hundreds of megabytes for a 3D mammogram, and multiple gigabytes for a digital pathology slide. It is also the stream with the strongest, oldest, and most universally adopted standard, which makes it a refreshing change of pace after the fragmentation of patient-generated data: essentially every imaging device on earth speaks DICOM.

DICOM—Digital Imaging and Communications in Medicine—is both a file format and a network protocol, developed by the ACR and NEMA and in wide use since the early 1990s . It covers the full range of imaging modalities: plain radiography (X-ray, coded CR/DX), computed tomography (CT), magnetic resonance imaging (MRI), ultrasound (US), mammography (MG), nuclear medicine and PET, and increasingly digital pathology. Whatever the modality, DICOM gives every image a common envelope.

The ecosystem around DICOM is worth knowing by name, because these are the systems you will actually be querying:

- PACS (Picture Archiving and Communication System) — the archive and viewing system where images live and where radiologists read them. When people say "pull it from PACS," this is what they mean.

- Modality Worklist — how a scanner knows which patient it's imaging, pulling the order so the tech doesn't retype demographics (and so the image is correctly linked to the right person).

- The DICOM network services — historically the C-STORE / C-FIND / C-MOVE operations for sending and querying images, now increasingly complemented by DICOMweb (the RESTful WADO/QIDO/STOW services) that expose images over ordinary HTTP for web and cloud applications.

A crucial architectural point: the *image* and the *report* are usually separate objects in separate systems. The pixels sit in PACS as DICOM; the radiologist's narrative interpretation sits in the EHR (and the RIS, the radiology information system) as unstructured text. This is why "the imaging data" can mean two very different things—the diagnostic-quality pixel data a computer-vision model needs, or the report text a clinician reads—and why so many imaging-AI projects stall not on modeling but on getting the DICOM out of PACS in the first place.

## DICOM Tags: Rich Metadata

A DICOM file is best understood as two things bolted together: a large block of pixel data (the actual image) and a rich block of metadata describing it. That metadata is organized as tags, and understanding tags is most of what a data person needs to know about DICOM internals.

Every DICOM tag is identified by a pair of hexadecimal numbers written `(group, element)`, and each tag has a defined meaning in the DICOM data dictionary. A few you will see constantly:

| Tag | Name | Example value |
|---|---|---|
| (0010,0010) | Patient Name | CHEN^ROBERT |
| (0010,0020) | Patient ID | MRN00483921 |
| (0008,0060) | Modality | CT |
| (0008,0020) | Study Date | 20260214 |
| (0020,000D) | Study Instance UID | 1.2.840.113619.2.55.3.… |
| (0020,000E) | Series Instance UID | 1.2.840.113619.2.55.3.… |
| (0008,0018) | SOP Instance UID | 1.2.840.113619.2.55.3.… |

Those last three rows encode DICOM's core organizing idea, a strict four-level hierarchy: a Patient has one or more Studies (an imaging exam, e.g., "CT chest with contrast"), each Study contains one or more Series (a set of images acquired together, e.g., one sequence or one reconstruction), and each Series contains many Instances (the individual image slices). Every level gets a globally unique identifier (a UID), which is how a scattered pile of image files can be reassembled into the correct exam for the correct patient. A single CT chest can be hundreds of instances; the hierarchy is what keeps them coherent.

Two more concepts round out the practical picture. The transfer syntax specifies how the pixel data is encoded and compressed (uncompressed, JPEG, JPEG 2000, and others), which matters enormously for storage and for whether your tooling can actually read a file. And the SOP Class identifies what *kind* of object a file is (a CT image, an MR image, a structured report, an ECG waveform)—the same mechanism that, as the bedside-monitor section noted, lets DICOM also carry waveforms.

The data-quality and privacy story is specific to imaging and important. Because tags are free-form and locally configured, the *same* conceptual field can be populated inconsistently across scanners and sites, so harmonizing DICOM metadata across institutions is real work. More seriously, PHI hides in two places: in the tags (patient name, ID, dates, and often a scattering of identifiers in private/vendor tags) and, insidiously, burned into the pixels themselves—ultrasound and screen-capture images frequently have the patient's name rendered directly onto the image. De-identifying DICOM therefore means both scrubbing tags (per profiles like DICOM PS3.15) *and* detecting and redacting text within pixels, which is why imaging de-identification is harder than the column-dropping that suffices for a claims extract. On the terminology side, imaging findings are increasingly coded with RadLex (radiology-specific), and SNOMED and LOINC also appear for procedures and observations.

<figure>
  <img src="{{ '/images/book/dicom-hierarchy.svg' | relative_url }}" alt="Tree diagram of the DICOM information hierarchy: one patient with a patient ID, containing studies identified by Study Instance UID, each containing series identified by Series Instance UID, each containing image instances identified by SOP Instance UID">
  <figcaption>The DICOM Patient → Study → Series → Instance hierarchy. A patient has one or more studies (an imaging exam), each study has one or more series (images acquired together), and each series holds many instances (individual slices). Every level carries a globally unique identifier, the UID, which is how a scattered pile of image files is reassembled into the right exam for the right person. Example UIDs are illustrative.</figcaption>
</figure>

## Quick Reference: Medical Imaging

| Data Stream | Medical Imaging (DICOM) |
|---|---|
| Description | Diagnostic images (X-ray, CT, MRI, ultrasound, mammography, nuclear/PET, digital pathology) plus rich per-image metadata, stored under a single near-universal standard |
| Data Generating Process | A scanner acquires images against an ordered exam (via Modality Worklist) and stores them to PACS as DICOM; a radiologist reads the study and dictates a separate narrative report into the EHR/RIS |
| Access & Availability | Owned by imaging providers; images in PACS, reports in the EHR. Research access via institutional PACS export, de-identified public sets (e.g., TCIA), and increasingly cloud imaging stores. HIPAA-governed; de-identification uniquely hard due to pixel-burned PHI |
| Key Data Elements | Pixel data; identifying tags (Patient Name/ID); Modality; Study/Series/SOP Instance UIDs; Study Date; acquisition parameters; transfer syntax; SOP Class |
| Data Models | DICOM (file format + network protocol); DICOMweb (WADO/QIDO/STOW) for web/cloud access |
| Standard Vocabularies | RadLex (radiology terms); SNOMED and LOINC for procedures/observations; DICOM's own defined terms for modality, body part, etc. |
| Data Storage | PACS archives; DICOM files (per-instance); increasingly object storage in the cloud. Studies range from ~15 MB (chest X-ray) to multiple GB (digital pathology) |
| Expected Data Quality | Pixel data excellent and standardized; metadata tags inconsistently populated across sites; report text is unstructured and separate from the images |
| Integration Considerations | Linking images to the EHR relies on accession/order numbers and patient IDs; harmonizing tags across scanners is nontrivial; de-identification must scrub both tags and pixels |
| Further Resources | DICOM standard (dicomstandard.org); The Cancer Imaging Archive (TCIA) |
