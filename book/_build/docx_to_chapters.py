#!/usr/bin/env python3
"""Rebuild the book's chapter pages from the DOCX manuscript.

    python3 book/_build/docx_to_chapters.py book/ebook.md.docx

What it does
------------
1. Converts the DOCX to one Markdown document (docx2md.py).
2. Splits it into chapters using the `source` headings in _data/book.yml.
3. Promotes headings one level (chapter title becomes the page <h1>, which the
   `book` layout renders from front matter).
4. Replaces the manuscript's figure placeholders (`![][imageN]`, embedded
   images, and `[FIGURE: ...]` author notes) with <figure> blocks pointing at
   the SVGs in images/book/ (see FIGURES below), and inserts figures that have
   no placeholder at a text anchor (see ANCHORED).
5. Applies the small, explicit cleanups in FIXES (conversion artifacts,
   cross-references that only make sense in print, one-cell tables that are
   really code samples, etc.).
6. Renumbers footnotes per page and appends their definitions.
7. Writes each chapter with front matter from _data/book.yml.

Everything that is *not* in the manuscript lives in this file, so a new DOCX
drop is: copy it in, run this script, review `git diff`.
"""
import re, sys, subprocess, pathlib, html

HERE = pathlib.Path(__file__).resolve().parent
BOOK = HERE.parent
ROOT = BOOK.parent
sys.path.insert(0, str(HERE))

# --------------------------------------------------------------------------
# Figures. key = placeholder as it appears in the converted markdown.
# --------------------------------------------------------------------------
def fig(slug, alt, caption):
    return (
        "<figure>\n"
        f"  <img src=\"{{{{ '/images/book/{slug}.svg' | relative_url }}}}\" alt=\"{html.escape(alt, quote=True)}\">\n"
        f"  <figcaption>{caption}</figcaption>\n"
        "</figure>"
    )

FIGURES = {
    "![][image3]": fig("medical-claims-structure",
        "Structure of a medical claims data extract showing member and plan info, encounter details, provider information, diagnosis and procedure data, and financials",
        "Structure of a typical medical claims data extract. Each claim record includes five categories of information: member and plan identity, encounter details, provider information, diagnosis and procedure codes, and financial amounts. Illustrative synthetic data."),
    "![][image4]": fig("ehr-bedside-monitor-flowsheet",
        "Example EHR flowsheet with vital signs, ventilator settings, and blood-gas values grouped in sections, with hourly timestamps across the columns",
        "A nursing flowsheet in an EHR system. Measurement types run down the rows, grouped into sections, and time runs across the columns, creating a structured longitudinal record of a patient's physiological status. Values are entered manually by nurses or auto-populated from interfaced bedside monitors. Illustrative synthetic data."),
    "![][image5]": fig("emg-cmap-waveform",
        "Compound Muscle Action Potential (CMAP) waveform showing voltage in millivolts over time in milliseconds, with the characteristic biphasic deflection and dashed lines indicating amplitude measurement",
        "A Compound Muscle Action Potential (CMAP) waveform from a nerve conduction study. The amplitude (measured peak-to-peak, indicated by the arrows) and latency of this waveform help neurologists diagnose neuropathy, radiculopathy, and carpal tunnel syndrome. Illustrative schematic."),
    "![IMAGE:media/image1.png]": fig("ecrf-components",
        "Annotated mock-up of an electronic case report form for laboratory results showing a form label, group labels for renal and hepatic panels, item labels, entry fields with values, a yes/no toggle, and a data-validation message flagging an out-of-range value",
        "Anatomy of an electronic case report form (eCRF) in an EDC system. A form (here, laboratory results) is organized into groups of items; each item has a label, a hint describing the expected units, and a field holding the entered value. Edit checks run as data is entered, so an out-of-range value raises a query for the site coordinator to resolve. Illustrative form; values are synthetic."),
    "![][image6]": fig("fastq-format",
        "Annotated FASTQ read record showing four labeled lines: identifier, nucleotide sequence, plus-sign separator, and per-base quality string, with a note on Phred quality encoding",
        "FASTQ file format. Each sequencing read occupies four lines: (1) an identifier beginning with @ that encodes the instrument, run, and position; (2) the nucleotide sequence; (3) a + separator; and (4) quality scores encoded as ASCII characters, where each character maps to a Phred confidence score for the corresponding base."),
    "![][image7]": fig("read-alignment-puzzle",
        "Schematic showing a pile of unaligned short reads on the left, an arrow labeled align to reference, and on the right the same reads stacked at their mapped positions beneath a reference genome, like puzzle pieces placed into a completed puzzle",
        "From reads to alignments. A FASTQ file is a pile of puzzle pieces: reads in arbitrary order with no positional information (left). Alignment matches each read to its position on the reference genome, producing the ordered pileup stored in a SAM/BAM file (right). Overlapping reads at each position provide the sequencing depth that later gives variant calls their confidence. Illustrative schematic."),
    "![][image8]": fig("sam-bam-format",
        "Annotated SAM file format showing header section and alignment section with labeled fields including QNAME, FLAG, RNAME, POS, MAPQ, CIGAR, RNEXT, PNEXT, TLEN, SEQ, and QUAL",
        "SAM (Sequence Alignment Map) file format. The header section defines the reference genome and sorting order. Each alignment row encodes the read name, bitwise flag (encoding paired/aligned status), reference chromosome, position, mapping quality, CIGAR string (describing insertions/deletions), and the base sequence with per-base quality scores."),
    "![][image9]": fig("cram-block-layout",
        "CRAM block layout diagram showing containers with header slices and data blocks for read name, query score, base flags, and other fields, with skipped containers shown in gray",
        "CRAM file structure. Data is organized into containers, each containing a slice header and a series of data blocks. CRAM achieves compression by storing only differences from a reference genome rather than full sequences. Blocks for fields like original quality scores (OQ:Z) can be omitted entirely to save space."),
    "![][image10]": fig("vcf-format",
        "Annotated VCF file example showing mandatory header lines, optional meta-information lines, and body rows with columns labeled for reference alleles, alternate alleles, quality scores, filter status, and sample genotypes",
        "VCF (Variant Call Format) file structure. The ## header lines define the reference genome, format version, and column definitions. Each body row encodes one variant: chromosome (CHROM), position (POS), reference base (REF), alternate base(s) (ALT), quality score (QUAL), filter status (FILTER), and per-sample genotype fields (FORMAT/SAMPLE)."),
    "![][image11]": fig("sequencing-pipeline",
        "Bioinformatics pipeline flowchart from BCL sequencer output through FASTQ generation and demultiplexing, mapping and aligning, position sorting, duplicate marking, and variant calling to produce VCF/gVCF files containing SNVs, indels, CNVs, and structural variants",
        "Standard short-read sequencing bioinformatics pipeline. Raw BCL files from the sequencer are demultiplexed into per-sample FASTQ files, aligned to a reference genome (BAM/CRAM), sorted, and deduplicated before variant calling produces the final VCF/gVCF output containing SNVs, copy number variants (CNVs), structural variants (SVs), and targeted caller results."),
    "![][image12]": fig("cgm-agp-report",
        "Ambulatory Glucose Profile report showing time-in-range statistics, key glucose metrics, and a modal day plot with the median glucose and percentile bands across a 24-hour day",
        "An Ambulatory Glucose Profile (AGP) report summarizing 14 days of continuous glucose monitor data. The report includes time-in-range statistics (top left), key glucose metrics (top right), and a modal day plot showing the median glucose with 25–75th and 5–95th percentile bands across the day, over the shaded 3.9–10 mmol/L target range (bottom). Illustrative synthetic data."),
    "![][image13]": fig("cardiac-egm-pacemaker",
        "Diagram of cardiac pacemaker lead placement with atrial bipolar and ventricular tip unipolar electrogram (EGM) traces showing marker annotations, timing intervals, and trigger events over 11 seconds",
        "Intracardiac electrograms (EGMs) from a dual-chamber pacemaker. The atrial lead (top trace) and ventricular lead (bottom trace) record electrical activity from inside the heart chambers. Marker annotations (AS = atrial sensed, VS = ventricular sensed, VP = ventricular paced) and inter-beat intervals (ms) allow clinicians to assess arrhythmias and device behavior during an interrogation. Illustrative synthetic data, styled after clinical device interrogation reports."),
    "![][image14]": fig("accelerometer-axes",
        "Three stacked time-series panels showing synthetic accelerometer data along the x, y, and z axes over 25 seconds of walking, each oscillating rhythmically with the gait cycle",
        "Raw accelerometer data from a smartphone in a pocket during moderate-pace walking. The rhythmic oscillations in all three axes reflect the vertical and horizontal forces of each footstep. Step-counting algorithms detect these periodic patterns to infer gait and activity level. Illustrative synthetic data."),
    "![][image15]": fig("wearable-sensor-timeseries",
        "Two-panel time series spanning Thursday through Wednesday showing heart rate in bpm and accelerometer activity, with shaded regions indicating diary sleep, HR-algorithm sleep, and angle-algorithm sleep periods",
        "One week of wrist-worn wearable sensor data showing heart rate (top) and accelerometer activity (bottom). Shaded bands compare sleep periods detected by a heart-rate algorithm (blue) versus an accelerometer-angle algorithm (purple) versus self-reported diary sleep (gray); their disagreement at the edges illustrates why no single signal reliably identifies sleep-stage boundaries. Illustrative synthetic data."),
    "![][image16]": fig("patient-generated-data-types",
        "Overview diagram of seven categories of patient-generated data: wearable data, self-reported outcomes, home monitoring devices, connected medical devices, social and lifestyle data, environmental data, and social network and media data, each with illustrative examples",
        "The landscape of patient-generated health data. Seven broad categories, wearables, self-reported outcomes, home monitoring devices, connected medical devices, social and lifestyle data, environmental sensors, and social network data, collectively represent a comprehensive picture of a patient's health outside the clinic."),
}

# Author notes of the form [FIGURE: ...] -> figure (matched on a distinctive substring)
FIGURE_NOTES = {
    "a single ECG lead trace": fig("ecg-intervals-structured",
        "Two-panel figure: top, a ten-second single-lead ECG waveform; bottom, one heartbeat enlarged with the PR interval, QRS duration, and QT interval bracketed, next to a box listing the handful of measured values and interpretation text that reach the structured EHR record",
        "What the EHR keeps from an ECG. (a) The full waveform, a 10-second, 500 Hz signal, lives in the cardiology information system. (b) What lands in the structured EHR record is a few measured intervals per beat (PR, QRS, QT/QTc), the heart rate, and the machine or cardiologist interpretation as text. Illustrative synthetic waveform."),
    "DICOM Patient": fig("dicom-hierarchy",
        "Tree diagram of the DICOM information hierarchy: one patient with a patient ID, containing studies identified by Study Instance UID, each containing series identified by Series Instance UID, each containing image instances identified by SOP Instance UID",
        "The DICOM Patient → Study → Series → Instance hierarchy. A patient has one or more studies (an imaging exam), each study has one or more series (images acquired together), and each series holds many instances (individual slices). Every level carries a globally unique identifier, the UID, which is how a scattered pile of image files is reassembled into the right exam for the right person. Example UIDs are illustrative."),
    "spectrum diagram": fig("pgd-structure-spectrum",
        "Horizontal spectrum from structured and validated on the left to unstructured and unvalidated on the right, with health data types positioned along it: laboratory results, validated PROs, CGM glucose, home blood pressure, wearable steps and heart rate, patient-captured photos, voice recordings, and digital exhaust such as typing, GPS, and app usage",
        "Patient-generated data on a spectrum from structured and validated to unstructured and unvalidated. Lab results and validated instruments like the PHQ-9 sit at the structured end; device streams occupy the middle; patient photos, voice, and the digital exhaust of everyday life sit at the far end, where signal is rich, interpretation is poor, and much of the data falls outside HIPAA's protections. Placement is illustrative."),
    "12-month multi-track timeline": fig("multimodal-timeline",
        "Five stacked time-series tracks over twelve months for one patient: antidepressant fill coverage with a gap in March and April, hemoglobin A1c falling from 8.4 to 7.6 percent, PHQ-9 scores falling from 16 to 8 with a plateau during the gap, CGM time in range rising from 52 to 68 percent, and daily steps dipping in the spring; the adherence gap is shaded across all tracks",
        "Twelve months of data for a 59-year-old man with type 2 diabetes and moderate depression, one stream per track. The shaded band marks the two-month gap in SSRI fills visible in pharmacy claims; the PHQ-9 improvement stalls and activity dips in exactly that window, while the A1c and CGM time in range improve as the year goes on. No single track tells the story; together they do. Illustrative synthetic data."),
    "coverage maps": fig("stream-coverage-maps",
        "Two side-by-side grids, one per patient, with data streams as rows and the year's care events as columns; filled cells show events captured by a stream, hollow cells show blind spots, highlighting that cash-pay fertility care is invisible to claims data",
        "Which streams see which events. For the man with diabetes (left), claims, EHR, PRO, and device data overlap and corroborate one another. For the woman pursuing fertility treatment (right), the EHR is comprehensive but claims are systematically blind to cash-pay care, and her most continuous record lives in a cycle-tracking app outside the medical record. Filled: captured. Hollow: not captured. Illustrative."),
}

# Figures with no placeholder in the manuscript: inserted after the paragraph
# that contains the anchor text.
ANCHORED = [
    ("See below for a breakdown of this code.", fig("icd10-code-structure",
        "ICD-10-CM code structure diagram for S86.011D showing category, etiology/anatomic site, and extension components",
        "ICD-10-CM code S86.011D broken into its three components: S86 (category: injury of muscle, fascia, and tendon of lower leg), .011 (etiology/anatomic site: strain of right Achilles tendon), and D (extension: subsequent encounter).")),
    ("rather than reading genetic letters.", fig("short-vs-long-read",
        "Two-panel schematic comparing short and long reads tiling a genome region with two identical repeat copies: many short reads that cannot be placed uniquely within a repeat, versus few long reads that span the repeat with unique flanking sequence",
        "Short read vs. long read sequencing across a region containing two identical repeat copies. Short reads (left) tile the region densely and accurately, but a read falling entirely within a repeat cannot be placed uniquely. Long reads (right) span the repeat with unique flanking sequence, anchoring it unambiguously, which is why long reads better resolve large structural variants, at the cost of per-base accuracy. Illustrative schematic.")
      + "\n\n" + fig("illumina-sequencing-workflow",
        "Three-panel diagram of Illumina sequencing workflow: a) cluster generation on a flow cell, b) high-throughput sequencing with fluorescent reversible terminators, c) demultiplexing and read mapping from BCL to FASTQ to mapped reads",
        "The Illumina sequencing workflow. (a) A DNA fragment binds the flow cell and is amplified by bridge amplification into a dense clonal cluster. (b) Fluorescently labeled nucleotides are incorporated one base at a time and imaged, each base read on its own channel. (c) Raw BCL output is demultiplexed into per-sample FASTQ files, quality-trimmed, and aligned to a reference genome to produce mapped reads. Illustrative schematic.")),
    ("compared to similar common data models focused on observational health data.", fig("omop-search-trends",
        "Chart of search interest over time for OMOP and related healthcare data model terms from 2020 to 2024, with a sharp spike in 2024",
        "Search interest for OMOP and related common data model terms, 2020–2024. The sharp spike reflects growing industry attention to standardized observational research infrastructure, driven in part by large-scale real-world evidence initiatives. Illustrative recreation of Google Trends data.")),
]

# --------------------------------------------------------------------------
# Explicit text fixes applied to every chapter (after heading promotion).
# (pattern, replacement, reason). Regex, DOTALL off, MULTILINE on.
# --------------------------------------------------------------------------
FIXES = [
    # --- conversion / print-only artifacts ---
    (r"\$SpO_2\$", "SpO<sub>2</sub>", "kramdown does not render $..$ inline math"),
    (r"\(http://google\.com/url\?q=(.+?)&sa=[^)]*\)", r"(\1)", "unwrap Google redirect link"),
    (r"\?utm_source=chatgpt\.com", "", "strip tracking parameter"),
    (r"(\]\(https://en\.wikipedia\.org/wiki/[^)#]+)#:~:text=[^)]*\)", r"\1)", "strip text-fragment anchors from Wikipedia links"),
    (r"\(see figure at right\)", "(see the figures below)", "print layout reference"),
    (r"\(to be discussed at length in Chapter X\)", "(discussed at length in the [Electronic Health Records](/book/clinical/ehr/) chapter)", "unresolved cross-reference"),
    (r"as encoded in LOINC \(see Part 1\)", "as encoded in LOINC (see [Core Concepts](/book/intro/core-concepts/))", "cross-reference"),
    (r"ESILevel 2", "ESI Level 2", "missing space"),
    # soft line breaks inside body paragraphs (Word shift-enter) -> space
    (r"(?<!\|)  \n(?=\S)", " ", "soft line break inside paragraph"),
    # --- manuscript typos that break meaning ---
    (r"This data is then by the device to monitor", "This data is then used by the device to monitor", "missing word"),
    (r"controlling for medication adherenceThe cardiovascular events", "controlling for medication adherence. The cardiovascular events", "missing sentence break"),
    (r"treatment initiation\.\.", "treatment initiation.", "double period"),
    (r"this field specifies how the numerical results$", "this field specifies the units in which the numerical result is expressed.", "sentence left unfinished in manuscript"),
    # --- unfinished draft fragments removed (reported to author) ---
    (r"^While this book considers data generated by consumer health devices such as wearables and smart scales to be important, the vast majority of\n\n", "", "unfinished sentence (Healthcare 101)"),
    (r"^While there is not one monolithic structure for clinical trial data,\n\n- SDTM \(Study Data Tabulation Model\)[^\n]*\n\n- ADaM \(Analysis Data Model\)[^\n]*\n\nMoreover, within a single phase there is considerable heterogeneity\n\n", "", "unfinished fragment; the SDTM/ADaM bullets repeat verbatim in the CDISC list below"),
    # a paragraph accidentally styled as a heading
    (r"^#+ (But the reason clinical trial data deserves its own chapter is CDISC)", r"\1", "paragraph styled as Heading 4 in manuscript"),
    # labels that read as headings in the vignettes
    (r"^Summary of Data Created by Jasmine’s Office Visit$", "#### Summary of Data Created by Jasmine’s Office Visit", "plain paragraph used as a heading"),
    (r"^\*Data Created by Robert’s Hospitalization\*$", "#### Data Created by Robert’s Hospitalization", "italic paragraph used as a heading"),
]

# --------------------------------------------------------------------------
def load_book_yml():
    """Tiny YAML reader for _data/book.yml (avoids a PyYAML dependency)."""
    try:
        import yaml
        return yaml.safe_load((ROOT / "_data/book.yml").read_text())
    except ImportError:
        pass
    parts, cur_part, cur_ch, key_list = [], None, None, None
    for raw in (ROOT / "_data/book.yml").read_text().splitlines():
        line = raw.rstrip()
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        indent = len(line) - len(line.lstrip())
        s = line.strip()
        if indent == 2 and s.startswith("- name:"):
            cur_part = {"name": s.split(":",1)[1].strip().strip('"'), "chapters": []}
            parts.append(cur_part); cur_ch = None; key_list = None
        elif indent == 4 and cur_part is not None and not s.startswith("-") and cur_ch is None:
            k, v = s.split(":",1); cur_part[k.strip()] = v.strip().strip('"')
        elif indent == 6 and s.startswith("- title:"):
            cur_ch = {"title": s.split(":",1)[1].strip().strip('"')}
            cur_part["chapters"].append(cur_ch); key_list = None
        elif indent == 8 and cur_ch is not None:
            k, v = s.split(":",1); k = k.strip(); v = v.strip().strip('"')
            if v == "":
                cur_ch[k] = []; key_list = k
            else:
                cur_ch[k] = v; key_list = None
        elif indent == 10 and key_list and s.startswith("- "):
            cur_ch[key_list].append(s[2:].strip())
    return {"parts": parts}

def convert(docx_path):
    out = HERE / "_ebook.md"
    subprocess.run([sys.executable, str(HERE / "docx2md.py"), str(docx_path), str(out)], check=True)
    return out.read_text()

def split_footnotes(md):
    body, _, notes = md.rpartition("\n---\n\n")
    defs = {}
    for m in re.finditer(r"^\[\^(\d+)\]: (.*)$", notes, flags=re.M):
        defs[m.group(1)] = m.group(2).strip()
    return body, defs

def sections(md):
    """Return list of (level, title, line_index) for every heading."""
    lines = md.split("\n")
    heads = []
    for i, l in enumerate(lines):
        m = re.match(r"^(#{1,6}) (.*)$", l)
        if m and m.group(2).strip():
            heads.append((len(m.group(1)), m.group(2).strip(), i))
    return lines, heads

def extract(lines, heads, source, until=None):
    for idx, (lvl, title, i) in enumerate(heads):
        if title.startswith(source):
            end = len(lines)
            for lvl2, title2, j in heads[idx+1:]:
                if (until and title2.startswith(until)) or lvl2 <= lvl:
                    end = j; break
            return lvl, "\n".join(lines[i+1:end]).strip("\n")
    raise SystemExit(f"chapter heading not found in manuscript: {source!r}")

def promote(text, by):
    if by <= 0: return text
    return re.sub(r"^(#{1,6}) ", lambda m: "#"*max(1, len(m.group(1))-by) + " ", text, flags=re.M)

def code_block_from_cell(cell):
    """One-cell tables in the manuscript are code samples (XML, log lines)."""
    cell = html.unescape(cell.replace("<br>", "\n"))
    if cell.lstrip().startswith("<?xml"):
        # crude pretty-printer for the (deliberately truncated) SCRIPT sample
        cell = re.sub(r"\]\([^)]*\)", "", cell)          # drop auto-links
        cell = cell.replace("[", "").replace("\\>", ">")
        tokens = [re.sub(r"\s{2,}", " ", t.strip()) for t in re.split(r"(?=<)", cell.strip()) if t.strip()]
        out, depth, prev_open_with_text = [], 0, False
        for t in tokens:
            if t.startswith("</"):
                if prev_open_with_text:
                    out[-1] += t                      # <Tag>text</Tag> on one line
                    prev_open_with_text = False
                else:
                    depth -= 1
                    out.append("  "*max(depth,0) + t)
                continue
            out.append("  "*max(depth,0) + t)
            prev_open_with_text = False
            if t.startswith("<?") or t.endswith("/>"):
                continue
            if re.match(r"^<[^>]+>[^<]+$", t):        # opening tag followed by text
                prev_open_with_text = True
            else:
                depth += 1
        return "```xml\n" + "\n".join(out) + "\n```"
    if "timestamp:" in cell:
        rows = re.split(r"\s+(?=timestamp:)", cell.strip())
        return "```text\n" + "\n".join(r.strip() for r in rows) + "\n```"
    return "```\n" + cell.strip() + "\n```"

def fix_tables(text):
    # single-cell tables -> code blocks
    text = re.sub(r"^\| (.*?) \|\n\|---\|(?!-)\n?", lambda m: code_block_from_cell(m.group(1)) + "\n", text, flags=re.M)
    # HIPAA Safe Harbor table: a title row above the real header
    text = text.replace("| HIPAA Safe Harbor Prohibited Elements |  |\n|---|---|\n| Category | Element |\n", "| Category | Element |\n|---|---|\n")
    return text

def place_figures(text):
    for key, block in FIGURES.items():
        if key not in text: continue
        # inline placeholder inside a paragraph -> split the paragraph around it
        text = re.sub(r"[ \t]*" + re.escape(key) + r"[ \t]*", "\n\n" + block.replace("\\", "\\\\") + "\n\n", text)
    for needle, block in FIGURE_NOTES.items():
        text = re.sub(r"[ \t]*\[FIGURE:[^\]]*" + re.escape(needle) + r"[^\]]*\][ \t]*", "\n\n" + block.replace("\\", "\\\\") + "\n\n", text)
    for anchor, block in ANCHORED:
        if anchor in text:
            text = text.replace(anchor, anchor + "\n\n" + block, 1)
    leftover = re.findall(r"!\[\]\[image\d+\]|!\[IMAGE:[^\]]*\]|\[FIGURE:[^\]]*\]", text)
    if leftover:
        print("  WARNING unplaced figure placeholders:", leftover)
    return text

def apply_fixes(text):
    for pat, rep, _reason in FIXES:
        text = re.sub(pat, rep, text, flags=re.M)
    return text

def renumber_footnotes(text, defs):
    order = []
    def sub(m):
        k = m.group(1)
        if k not in order: order.append(k)
        return f"[^{order.index(k)+1}]"
    text = re.sub(r"\[\^(\d+)\]", sub, text)
    if order:
        text += "\n\n" + "\n".join(f"[^{n+1}]: {defs.get(k, 'MISSING FOOTNOTE ' + k)}" for n, k in enumerate(order))
    return text

def tidy(text):
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"[ \t]+$", "", text, flags=re.M)
    return text.strip("\n") + "\n"

def front_matter(ch):
    fm = ["---", "layout: book", f"title: \"{ch['title']}\""]
    if ch.get("description"):
        fm.append(f"description: \"{ch['description']}\"")
    fm.append(f"permalink: {ch['url']}")
    if ch.get("redirect_from"):
        fm.append("redirect_from:")
        fm += [f"  - {u}" for u in ch["redirect_from"]]
    fm.append("---")
    return "\n".join(fm) + "\n\n"

UNTIL = {"Introduction": "Chapter 1: Core Concepts"}

def main(docx_path):
    md = convert(docx_path)
    md = md.replace("## ![][image16]", "")                 # a figure got a Heading 2 style in the manuscript
    body, defs = split_footnotes(md)
    lines, heads = sections(body)
    book = load_book_yml()
    written = []
    for part in book["parts"]:
        for ch in part["chapters"]:
            lvl, text = extract(lines, heads, ch["source"], UNTIL.get(ch["source"]))
            by = 1 if lvl >= 2 else 0
            text = promote(text, by)
            text = fix_tables(text)
            text = apply_fixes(text)
            if ch["source"] == "The Patient-Generated Data of the Future":
                # the overview figure belongs after the opening paragraph, not at the end
                text = text.replace("![][image16]", "").rstrip()
                first_para_end = text.index("\n\n")
                text = text[:first_para_end] + "\n\n![][image16]" + text[first_para_end:]
            text = place_figures(text)
            text = renumber_footnotes(text, defs)
            text = tidy(text)
            out = BOOK / ch["file"]
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(front_matter(ch) + text)
            written.append((ch["file"], text.count("\n"), text.count("<figure>"), text.count("[^")//2))
    print(f"{'file':50s} {'lines':>5s} {'figs':>4s} {'notes':>5s}")
    for f, n, fg, fn in written:
        print(f"{f:50s} {n:5d} {fg:4d} {fn:5d}")
    (HERE / "_ebook.md").unlink(missing_ok=True)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    main(pathlib.Path(sys.argv[1]).resolve())
