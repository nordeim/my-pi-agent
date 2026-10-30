#!/usr/bin/env python3
"""Post-process the audit report docx for WPS compatibility:
1. Map each section's default footer via document.xml.rels.
2. Patch footer PAGE fields with explicit format switches
   (front matter -> ROMAN, body -> arabic) per docx skill toc.md.
3. Remove empty <w:pgNumType/> elements from document.xml.
Usage: python3 postprocess_footers.py <file.docx>
"""
import re
import shutil
import sys
import zipfile

path = sys.argv[1]
tmp = path + ".tmp"

with zipfile.ZipFile(path, "r") as zin:
    names = zin.namelist()
    data = {n: zin.read(n) for n in names}

doc = data["word/document.xml"].decode("utf-8")

# --- 1. sectPr blocks in order, with their default footer rIds ---
sect_blocks = re.findall(r"<w:sectPr[^>]*>.*?</w:sectPr>", doc, flags=re.S)
section_footer_rids = []
for blk in sect_blocks:
    m = re.search(r'<w:footerReference w:type="default" r:id="(rId\d+)"', blk)
    section_footer_rids.append(m.group(1) if m else None)
print("sections:", len(sect_blocks), "footer rids:", section_footer_rids)

# --- 2. map rIds -> footer files ---
rels = data["word/_rels/document.xml.rels"].decode("utf-8")
rid_to_target = dict(re.findall(r'Id="(rId\d+)"[^>]*Target="(footer\d+\.xml)"', rels))

# Expected layout: section 1 = cover (no footer), section 2 = front matter (Roman),
# section 3 = body (arabic). Patch all footer-bearing sections after the first.
fmt_by_index = {}
for idx in range(1, len(section_footer_rids)):
    fmt_by_index[idx] = "ROMAN" if idx == 1 else "arabic"

for idx, rid in enumerate(section_footer_rids):
    if rid is None or idx not in fmt_by_index:
        continue
    target = rid_to_target.get(rid)
    if not target:
        continue
    key = "word/" + target
    xml = data[key].decode("utf-8")
    fmt = fmt_by_index[idx]
    new_xml, n1 = re.subn(
        r"(<w:instrText[^>]*>)\s*PAGE\s*(</w:instrText>)",
        r"\1 PAGE \\* " + fmt + r" \\* MERGEFORMAT \2", xml)
    new_xml, n2 = re.subn(
        r'(<w:fldSimple[^>]*w:instr=")\s*PAGE\s*(")',
        r"\1 PAGE \\* " + fmt + r" \\* MERGEFORMAT \2", new_xml)
    data[key] = new_xml.encode("utf-8")
    print(f"patched {key} -> {fmt} (instrText:{n1}, fldSimple:{n2})")

# --- 3. remove empty pgNumType from document.xml ---
doc, n3 = re.subn(r"<w:pgNumType/>", "", doc)
data["word/document.xml"] = doc.encode("utf-8")
print("removed empty pgNumType:", n3)

with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zout:
    for n in names:
        zout.writestr(n, data[n])
shutil.move(tmp, path)
print("postprocessed", path)
