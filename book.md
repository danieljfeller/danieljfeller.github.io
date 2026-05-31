---
layout: default
title: Book
permalink: /book/
---

<h2>Decoding Health Data</h2>

<div class="book-section">
  <h3>The raw data types, models, and ontologies behind health AI</h3>

  <p>What's actually in a <code>VCF</code>? Why does the same diagnosis have a different code in ICD-10-CM, SNOMED CT, and an OMOP <code>concept_id</code>? How do you join an X12 837 claim to a FHIR <code>Observation</code> to a BAM file? This book is about the bytes — the formats, schemas, vocabularies, and identifiers you parse, map, and model when you build on health data.</p>

  <p>Written for programmers, bioinformaticians, and data scientists. Light on theory, heavy on the concrete encodings: field layouts, controlled vocabularies, reference standards, and the edge cases that break your pipeline.</p>

  <a href="https://docs.google.com/document/d/102JwC1cz2CvnRvApnWZ4AUrmqxcEDisi2-U6mPLXeYc/edit?usp=sharing" target="_blank" class="book-cta book-cta-lg">Read Decoding Health Data &rarr;</a>

  <h3>What's Inside</h3>
  <ul class="book-topics">
    <li><strong>Data models:</strong> OMOP CDM tables and <code>concept_id</code> mapping, FHIR resources and references, HL7 v2 segments, i2b2 star schema, CDISC SDTM/ADaM.</li>
    <li><strong>Ontologies &amp; code systems:</strong> ICD-10-CM/PCS, CPT/HCPCS, SNOMED CT, LOINC, RxNorm, NDC, ATC, UMLS CUIs — crosswalks, hierarchies, and why mappings are lossy.</li>
    <li><strong>Genomics:</strong> FASTQ/BAM/CRAM/VCF, GRCh37 vs GRCh38, variant calling, HGVS nomenclature, SNVs/indels/CNVs/SVs, annotation with VEP/SnpEff, ClinVar and gnomAD allele frequencies.</li>
    <li><strong>Claims:</strong> X12 837/835, NCPDP scripts, DRGs, revenue codes — what the coding actually encodes versus what happened clinically.</li>
    <li><strong>Imaging &amp; signals:</strong> DICOM tags and pixel arrays, PACS, waveform formats (EDF), and turning raw acquisitions into arrays you can train on.</li>
    <li><strong>EHR data:</strong> structured vs free-text, LOINC-coded labs and units, flowsheets, medication records, and identifier resolution across systems.</li>
    <li><strong>Multi-omics &amp; PGHD:</strong> linking sequence, expression, and phenotype (HPO, MONDO); wearables and CGM streams.</li>
  </ul>

  <h3>Format</h3>
  <p>A living document, continuously updated. Each data type gets the same treatment: what it is, what's actually in it, the standard(s), the reality, and a quick reference.</p>

  <a href="https://docs.google.com/document/d/102JwC1cz2CvnRvApnWZ4AUrmqxcEDisi2-U6mPLXeYc/edit?usp=sharing" target="_blank" class="book-cta book-cta-lg">Start reading &rarr;</a>
</div>
