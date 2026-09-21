"""Minimal DOCX -> Markdown converter (headings, runs, links, lists, tables, footnotes, images).

Usage: python3 docx2md.py <input.docx> <output.md>
Normally invoked by docx_to_chapters.py rather than directly."""
import re, sys, zipfile, html
from xml.etree import ElementTree as ET

W = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
R = '{http://schemas.openxmlformats.org/officeDocument/2006/relationships}'
A = '{http://schemas.openxmlformats.org/drawingml/2006/main}'

z = zipfile.ZipFile(sys.argv[1])
doc = ET.fromstring(z.read('word/document.xml'))
rels = ET.fromstring(z.read('word/_rels/document.xml.rels'))
relmap = {r.get('Id'): (r.get('Type').rsplit('/',1)[-1], r.get('Target')) for r in rels}
try:
    fn_xml = ET.fromstring(z.read('word/footnotes.xml'))
except KeyError:
    fn_xml = None
numbering = {}
try:
    num_xml = ET.fromstring(z.read('word/numbering.xml'))
    absmap = {}
    for an in num_xml.iter(W+'abstractNum'):
        aid = an.get(W+'abstractNumId')
        lvls = {}
        for lvl in an.iter(W+'lvl'):
            fmt = lvl.find(W+'numFmt')
            lvls[lvl.get(W+'ilvl')] = fmt.get(W+'val') if fmt is not None else 'bullet'
        absmap[aid] = lvls
    for n in num_xml.iter(W+'num'):
        nid = n.get(W+'numId'); a = n.find(W+'abstractNumId').get(W+'val')
        numbering[nid] = absmap.get(a, {})
except KeyError:
    pass

fn_relmap = {}
try:
    fn_rels = ET.fromstring(z.read('word/_rels/footnotes.xml.rels'))
    fn_relmap = {r.get('Id'): (r.get('Type').rsplit('/',1)[-1], r.get('Target')) for r in fn_rels}
except KeyError:
    pass
footnotes = {}
if fn_xml is not None:
    for fn in fn_xml.iter(W+'footnote'):
        fid = fn.get(W+'id')
        if fn.get(W+'type') in ('separator','continuationSeparator'): continue
        footnotes[fid] = fn

def run_text(r):
    out = []
    for ch in r:
        tag = ch.tag
        if tag == W+'t': out.append(ch.text or '')
        elif tag == W+'tab': out.append('\t')
        elif tag == W+'br': out.append('  \n')
        elif tag == W+'footnoteReference':
            out.append(f"[^{ch.get(W+'id')}]")
        elif tag == W+'drawing':
            for blip in ch.iter(A+'blip'):
                rid = blip.get(R+'embed')
                out.append(f"![IMAGE:{relmap.get(rid,('',''))[1]}]")
    return ''.join(out)

def fmt_run(r):
    t = run_text(r)
    if not t: return ''
    rpr = r.find(W+'rPr')
    b = i = code = False
    if rpr is not None:
        b = rpr.find(W+'b') is not None and rpr.find(W+'b').get(W+'val','true') not in ('0','false')
        i = rpr.find(W+'i') is not None and rpr.find(W+'i').get(W+'val','true') not in ('0','false')
        rs = rpr.find(W+'rStyle')
        fonts = rpr.find(W+'rFonts')
        if fonts is not None and any('Courier' in (fonts.get(k) or '') or 'Mono' in (fonts.get(k) or '') or 'Consolas' in (fonts.get(k) or '') for k in fonts.keys()):
            code = True
    if t.strip() == '': return t
    lead = t[:len(t)-len(t.lstrip())]; trail = t[len(t.rstrip()):]; core = t.strip()
    if code and '\n' not in core: core = f"`{core}`"
    if b and i: core = f"***{core}***"
    elif b: core = f"**{core}**"
    elif i: core = f"*{core}*"
    return lead + core + trail

def para_inline(p, rm=None):
    rm = relmap if rm is None else rm
    parts = []
    for ch in p:
        if ch.tag == W+'r': parts.append(fmt_run(ch))
        elif ch.tag == W+'hyperlink':
            rid = ch.get(R+'id'); anchor = ch.get(W+'anchor')
            txt = ''.join(fmt_run(r) for r in ch.iter(W+'r'))
            if rid and rid in rm: parts.append(f"[{txt}]({rm[rid][1]})")
            elif anchor: parts.append(f"[{txt}](#{anchor})")
            else: parts.append(txt)
        elif ch.tag in (W+'smartTag', W+'ins', W+'sdt'):
            parts.append(''.join(fmt_run(r) for r in ch.iter(W+'r')))
    s = ''.join(parts)
    # merge adjacent same-format runs: **a****b** -> **ab**
    for m in ('**','*','`'):
        s = s.replace(f"{m}{m}", '')
    return s

def pstyle(p):
    ppr = p.find(W+'pPr')
    if ppr is None: return '', None, None
    st = ppr.find(W+'pStyle'); s = st.get(W+'val') if st is not None else ''
    numpr = ppr.find(W+'numPr')
    if numpr is not None:
        ilvl = numpr.find(W+'ilvl'); nid = numpr.find(W+'numId')
        return s, (nid.get(W+'val') if nid is not None else None), (ilvl.get(W+'val') if ilvl is not None else '0')
    return s, None, None

def table_md(tbl):
    rows = []
    for tr in tbl.findall(W+'tr'):
        cells = []
        for tc in tr.findall(W+'tc'):
            ctext = '<br>'.join(para_inline(p).strip().replace('  \n', '<br>') for p in tc.findall(W+'p') if para_inline(p).strip())
            cells.append(ctext.replace('|','\\|'))
        rows.append(cells)
    if not rows: return ''
    n = max(len(r) for r in rows)
    rows = [r + ['']*(n-len(r)) for r in rows]
    out = ['| ' + ' | '.join(rows[0]) + ' |', '|' + '---|'*n]
    for r in rows[1:]: out.append('| ' + ' | '.join(r) + ' |')
    return '\n'.join(out)

lines = []
last_ordered = False
body = doc.find(W+'body')
for el in body:
    if el.tag == W+'p':
        s, nid, ilvl = pstyle(el)
        txt = para_inline(el).strip()
        m = re.match(r'Heading(\d)', s or '')
        if m:
            lines.append('#'*int(m.group(1)) + ' ' + txt if txt else '')
        elif s == 'Title': lines.append('# ' + txt)
        elif nid is not None and txt:
            fmt = numbering.get(nid, {}).get(ilvl, 'bullet')
            lvl = int(ilvl or 0)
            if fmt == 'bullet' and lvl == 0 and last_ordered:
                lvl = 1
            if fmt != 'bullet' and lvl == 0:
                last_ordered = True
            indent = '    ' * lvl
            lines.append(f"{indent}{'1.' if fmt != 'bullet' else '-'} {txt}")
            continue
        else:
            lines.append(txt)
        if txt: last_ordered = False
    elif el.tag == W+'tbl':
        last_ordered = False
        lines.append(''); lines.append(table_md(el)); lines.append('')

md = '\n\n'.join(l for l in lines)
md = re.sub(r'\n{3,}', '\n\n', md)
if footnotes:
    md += '\n\n---\n\n'
    for fid, fn in footnotes.items():
        t = ' '.join(para_inline(p, fn_relmap).strip() for p in fn.findall(W+'p')).strip().replace('`','')
        md += f"[^{fid}]: {t}\n"
open(sys.argv[2],'w').write(md)
print("wrote", sys.argv[2], len(md), "chars,", md.count('\n'), "lines;", len(footnotes), "footnotes;", md.count('![IMAGE:'), "embedded images;", md.count('![]['), "md image placeholders")
