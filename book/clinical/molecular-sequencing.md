---
layout: book
title: "Molecular Sequencing"
permalink: /book/clinical/molecular-sequencing/
---


### Why Molecular Sequencing Is The Present - and Future - of Healthcare

Molecular sequencing represents a complete or partial reading of an organism's DNA to identify genetic variations, mutations, and sequences. In healthcare, this data has become indispensable as precision medicine accelerates and clinical outcomes increasingly depend on understanding a patient's genetic profile. Genomic sequencing drives drug development by pinpointing disease-causing mutations like BRCA (increase risk of breast cancer) and EGFR (increases risk of lung cancer) that can be targeted with novel therapeutics, while enabling rare-disease diagnosis through whole-genome sequencing to catch mutations that targeted tests miss. Perhaps most impactfully, integrating genomic data with patient clinical records enables treatment response prediction—studies show this integration can achieve up to 75% accuracy in predicting how well cancer patients respond to specific therapies.  As the field matures, the critical challenge ahead is systematically linking genomic sequencing results with clinical outcomes data to unlock the full potential of personalized treatment strategies.

Sequencing data is stored and analyzed by organizations performing research and major medical centers for treatment.  All global biopharmaceutical companies rely on genomic  data to accelerate drug discovery, validate therapeutic targets, and improve clinical trial design. <Which healthcare providers are using it?>


### What Does Molecular Sequencing Data Actually Look Like?

In its most basic form, molecular sequencing data typically contains sequences of amino acids - adenine (A), thymine (T), guanine (G), and cytosine (C). This gives you six possible base pair combinations: A-T, T-A, G-C, C-G, plus A-A, T-T, G-G, C-C. RNA uses uracil (U) instead of thymine, so its bases are A, U, G, C. RNA is typically single-stranded, so you don't get the same strict pairing rules as DNA.

Generating this data from biological molecules is performed by a few different technologies. Short read sequencing is the most common clinical DNA sequencing method and scans tiny DNA fragments one letter at a time across millions of samples simultaneously—it's fast, cheap, and accurate but misses large deletions (see figure at right). Long-read sequencing reads entire longer DNA sections at once, catching big structural changes but slower and less accurate. RNA sequencing uses the same core sequencing platforms as DNA but are first converted to complementary DNA (cDNA) before sequencing since the machines are designed to read only DNA. Protein sequencing uses a completely different method based on weighing protein fragments rather than reading genetic letters.

However, most files containing molecular sequencing data contain additional data elements that provide context around the sequenced amino acids. These include the following:

Variant Calls — Spots where a patient's DNA differs from a typical reference DNA sequence.

Sequencing Depth — The number of times the machine reads each position in the DNA; more reads mean more confidence in the result.

Quality Scores — A confidence level for each base the machine reads, showing how likely it got the letter right.

Chromosome Location — Which chromosome and what position on that chromosome the variant is found.

Variant Type — What kind of change happened—a single letter swap, extra letters added, or letters deleted.

Allele Frequency — How common a particular DNA change is in the general population; rare changes are more likely to cause disease than common ones.


### Standard Formats for Molecular Sequencing Data

While there are lots of different standards for storing molecular sequencing data, we will only focus on the relatively few standard that you ‘need to know’.


#### FASTQ

The basic form of molecular sequencing data with minimal metadata are FASTQ files. FASTQ is the de facto standard for storing unaligned sequencing reads with quality scores. All commercial sequencing platforms (Illumina, PacBio, Oxford Nanopore) generate FASTQ files. An example of the structure of FASTQ file can be seen below:

Quality scores in FASTQ files are confidence levels for each individual base the sequencer reads, indicating how likely the machine got that letter correct. They're encoded as ASCII characters and converted to Phred scores (typically 0-60), where higher scores mean higher confidence—a score of 30 means 99.9% accuracy, while a score of 20 means 99% accuracy.


#### BAM

As mentioned previously, FASTQ files contain unaligned ‘reads’—raw sequences directly from the sequencer with quality scores, but no information about where they map to the genome. Each FASTQ file can be thought of as a puzzle piece, and those puzzle pieces must be assembled into a completed puzzle.

The Binary Alignment Map (BAM) format is the industry standard for compressing aligned sequence reads.

FASTQ files are converted to BAM or CRAM through a two-step process, typically using an open-source bioinformatics software like samtools.  First, an alignment module reads each raw DNA sequence from the FASTQ file and matches it to the correct position in a reference genome. Once all reads are aligned and their positions identified, compression software packages them into the more compact BAM or CRAM format, discarding redundant information and adding helpful labels about where each read came from and how confident the alignment is. The sequence reads from the machine (typically manufactured by PacBio or Illumina) are never 100% accurate, and thus there are additional software programs to identify and correct misread base-pairs.


#### CRAM

Compressed Reference-oriented Alignment Map (CRAM)  is a more heavily compressed alternative to BAM and is increasingly preferred for long-term storage due to significant file size savings; major academic consortia and biopharmaceutical companies now recommend or require CRAM. Variant Call Format (VCF) is the standard for storing identified genetic variants extracted from aligned reads. For RNA-seq data, the same FASTQ → BAM/CRAM → VCF pipeline applies since RNA is converted to cDNA before sequencing. Protein sequencing data lacks a single dominant standard; mass spectrometry output is typically stored in formats like mzML or mzXML, and protein identification results are often in tab-delimited or proprietary formats. Popular bioinformatics packages can convert between these formats, and most major research consortia and pharmaceutical companies now store sequence reads predominantly in CRAM for cost and efficiency. Multiple high-profile consortia either recommend or require CRAM. It is important to note that most major academic bioinformatics consortia store sequence reads, and predominantly in CRAM.


#### VCF (Variant Call Format)

VCF is the standard format for storing genetic variants identified from aligned sequencing reads. Where BAM and CRAM store every read across the entire genome, VCF is much more compact—it records only the positions where a sample's DNA differs from the reference, along with metadata describing the nature of each variant.

A VCF file contains a header section that defines the reference genome, the calling software used, and the meaning of each data field. Each subsequent data row represents a single variant and includes the chromosome, position, reference base(s), alternate base(s), a quality score for the call, filter status (e.g., whether it passed quality thresholds), and an INFO field containing annotations like allele frequency, depth, and variant type.

Producing a clean VCF from raw reads is computationally intensive. The standard pipeline takes FASTQ reads through alignment, sorting, duplicate marking, and variant calling—a multi-step process that can take many hours per sample and requires careful coordination of multiple open-source tools. Each step introduces choices about quality thresholds, reference genomes, and filtering logic that affect which variants ultimately appear in the output VCF. This means that VCF files generated by different pipelines or institutions are not always directly comparable, which is a practical consideration when working with variant data across multiple sites.

Variant calling pipelines have evolved significantly in recent years toward more integrated, hardware-accelerated solutions. Illumina's DRAGEN platform, for example, consolidates the entire alignment-to-VCF workflow onto FPGA hardware, reducing whole-genome processing from hours to under 30 minutes while outputting standard BAM/CRAM and VCF files. DRAGEN has been widely adopted at large sequencing centers and biopharma organizations, making it a common provenance for VCF files encountered in clinical and research settings.

Regardless of the pipeline used, VCF is the practical endpoint of the sequencing workflow: it distills gigabytes of raw read data into a compact, interoperable representation of what is actually different about a given sample's genome.
