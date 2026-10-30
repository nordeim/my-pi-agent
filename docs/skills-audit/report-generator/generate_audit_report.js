// generate_audit_report.js — builds the Big-Tech skills audit report (.docx)
// Follows docx skill: create route, report scene, R1 cover recipe (IG-1 Ink Gold),
// 3-section page numbering (cover / front matter Roman / body Arabic), TOC field,
// Horizontal-Only business tables, matplotlib chart embedding with true aspect ratio.
"use strict";

const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  ImageRun, Header, Footer, PageNumber, NumberFormat, SectionType,
  AlignmentType, HeadingLevel, WidthType, BorderStyle, ShadingType,
  TableLayoutType, TableOfContents,
} = require("docx");
const fs = require("fs");
const path = require("path");

// Output: explicit path argument wins; default sits next to the package README
// (report-generator/../BigTech_Research_Skills_Audit_Report.docx).
const OUT = process.argv[2]
  || path.join(__dirname, "..", "BigTech_Research_Skills_Audit_Report.docx");

// ---------- Palette: IG-1 Ink Gold (finance) ----------
const P = {
  bg: "1A1A1A", accent: "C9A84C",
  cover: { titleColor: "FFFFFF", subtitleColor: "B0B8C0", metaColor: "90989F", footerColor: "687078" },
  table: { headerBg: "C9A84C", headerText: "1A1A1A", accentLine: "C9A84C", innerLine: "DDD5C0", surface: "F5F2E8" },
};
const INK = "1A1A1A"; // heading color on white body pages (Ink Gold identity)
const BODY_COLOR = "000000"; // report scene: pure black body

const NB = { style: BorderStyle.NONE, size: 0, color: "FFFFFF" };
const noBorders = { top: NB, bottom: NB, left: NB, right: NB };
const allNoBorders = { top: NB, bottom: NB, left: NB, right: NB, insideHorizontal: NB, insideVertical: NB };

function safeText(v, ph) {
  if (v === undefined || v === null || v === "" || String(v) === "NaN" || String(v) === "undefined") {
    return ph || "[missing]";
  }
  return String(v);
}

// ---------- Cover layout helpers (design-system.md, latin-aware width) ----------
function isLatinTitle(t) { return /^[\x00-\x7F]*$/.test(t); }

function splitTitleLines(title, charsPerLine) {
  if (title.length <= charsPerLine) return [title];
  const breakAfter = new Set([..."，。、；：！？", ..."的与和及之在于为", ..."-_—–·/", ..." \t"]);
  const lines = [];
  let remaining = title;
  while (remaining.length > charsPerLine) {
    let breakAt = -1;
    for (let i = charsPerLine; i >= Math.floor(charsPerLine * 0.6); i--) {
      if (i < remaining.length && breakAfter.has(remaining[i - 1])) { breakAt = i; break; }
    }
    if (breakAt === -1) {
      const limit = Math.min(remaining.length, Math.ceil(charsPerLine * 1.3));
      for (let i = charsPerLine + 1; i < limit; i++) {
        if (breakAfter.has(remaining[i - 1])) { breakAt = i; break; }
      }
    }
    if (breakAt === -1) breakAt = charsPerLine;
    lines.push(remaining.slice(0, breakAt).trim());
    remaining = remaining.slice(breakAt).trim();
  }
  if (remaining) lines.push(remaining);
  if (lines.length > 1 && lines[lines.length - 1].length <= 2) {
    const last = lines.pop();
    lines[lines.length - 1] += last;
  }
  return lines;
}

function calcTitleLayout(title, maxWidthTwips, preferredPt = 40, minPt = 24) {
  const charWidth = (pt) => (isLatinTitle(title) ? pt * 10.5 : pt * 20);
  const charsPerLine = (pt) => Math.floor(maxWidthTwips / charWidth(pt));
  let titlePt = preferredPt, lines;
  while (titlePt >= minPt) {
    const cpl = charsPerLine(titlePt);
    if (cpl < 2) { titlePt -= 2; continue; }
    lines = splitTitleLines(title, cpl);
    if (lines.length <= 3) break;
    titlePt -= 2;
  }
  if (!lines || lines.length > 3) {
    lines = splitTitleLines(title, charsPerLine(minPt));
    titlePt = minPt;
  }
  return { titlePt, titleLines: lines };
}

function calcCoverSpacing(params) {
  const {
    titleLineCount = 1, titlePt = 36, hasSubtitle = false, hasEnglishLabel = false,
    metaLineCount = 0, fixedHeight = 800, pageHeight = 16838, marginTop = 0, marginBottom = 0,
  } = params;
  const SAFETY = 1200;
  const usableHeight = pageHeight - marginTop - marginBottom - SAFETY;
  const titleHeight = titleLineCount * (titlePt * 23 + 200);
  const subtitleHeight = hasSubtitle ? (12 * 23 + 600) : 0;
  const englishLabelHeight = hasEnglishLabel ? (9 * 23 + 600) : 0;
  const metaHeight = metaLineCount * (10 * 23 + 100);
  const implicitParaHeight = 3 * 300;
  const contentHeight = titleHeight + subtitleHeight + englishLabelHeight + metaHeight + fixedHeight + implicitParaHeight;
  const remainingSpace = usableHeight - contentHeight;
  const safeRemaining = Math.max(remainingSpace, 400);
  const FOOTER_MIN = 800;
  const rawTop = Math.floor(safeRemaining * 0.45);
  const rawBottom = Math.floor(safeRemaining * 0.45);
  const bottomSpacing = Math.max(rawBottom, FOOTER_MIN);
  const topSpacing = Math.max(rawTop - Math.max(0, FOOTER_MIN - rawBottom), 400);
  const midSpacing = Math.max(safeRemaining - topSpacing - bottomSpacing, 0);
  return { topSpacing, midSpacing, bottomSpacing };
}

// ---------- Recipe R1: Pure Paragraph Cover (left-aligned) ----------
function buildCoverR1(config) {
  const CP = { bg: P.bg, accent: P.accent, ...P.cover };
  const padL = 1200, padR = 800;
  const availableWidth = 11906 - padL - padR - 300;
  const { titlePt, titleLines } = calcTitleLayout(config.title, availableWidth, 40, 24);
  const titleSize = titlePt * 2;
  const spacing = calcCoverSpacing({
    titleLineCount: titleLines.length, titlePt,
    hasSubtitle: !!config.subtitle, hasEnglishLabel: !!config.englishLabel,
    metaLineCount: (config.metaLines || []).length, fixedHeight: 400,
  });
  const accentLeft = { style: BorderStyle.SINGLE, size: 8, color: CP.accent, space: 12 };
  const children = [];
  children.push(new Paragraph({ spacing: { before: spacing.topSpacing } }));
  if (config.englishLabel) {
    children.push(new Paragraph({
      indent: { left: padL, right: padR }, spacing: { after: 500 },
      border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: CP.accent, space: 8 } },
      children: [new TextRun({ text: config.englishLabel.split("").join("  "),
        size: 18, color: CP.accent, font: { ascii: "Calibri", eastAsia: "SimHei" }, characterSpacing: 40 })],
    }));
  }
  for (let i = 0; i < titleLines.length; i++) {
    children.push(new Paragraph({
      indent: { left: padL },
      spacing: { after: i < titleLines.length - 1 ? 100 : 300, line: Math.ceil(titlePt * 23), lineRule: "atLeast" },
      children: [new TextRun({ text: titleLines[i], size: titleSize, bold: true,
        color: CP.titleColor, font: { eastAsia: "SimHei", ascii: "Arial" } })],
    }));
  }
  if (config.subtitle) {
    children.push(new Paragraph({
      indent: { left: padL, right: padR }, spacing: { after: 800 },
      children: [new TextRun({ text: config.subtitle, size: 24, color: CP.subtitleColor,
        font: { eastAsia: "Microsoft YaHei", ascii: "Arial" } })],
    }));
  }
  for (const line of (config.metaLines || [])) {
    children.push(new Paragraph({
      indent: { left: padL + 200, right: padR }, spacing: { after: 80 },
      border: { left: accentLeft },
      children: [new TextRun({ text: safeText(line), size: 24, color: CP.metaColor,
        font: { eastAsia: "Microsoft YaHei", ascii: "Arial" } })],
    }));
  }
  children.push(new Paragraph({ spacing: { before: spacing.bottomSpacing } }));
  children.push(new Paragraph({
    indent: { left: padL, right: padR },
    border: { top: { style: BorderStyle.SINGLE, size: 2, color: CP.accent, space: 8 } },
    spacing: { before: 200 },
    children: [
      new TextRun({ text: safeText(config.footerLeft, ""), size: 16, color: CP.footerColor, font: { ascii: "Arial" } }),
      new TextRun({ text: "                                        " }),
      new TextRun({ text: safeText(config.footerRight, ""), size: 16, color: CP.footerColor, font: { ascii: "Arial" } }),
    ],
  }));
  return [new Table({
    width: { size: 100, type: WidthType.PERCENTAGE },
    layout: TableLayoutType.FIXED,
    borders: allNoBorders,
    rows: [new TableRow({
      height: { value: 16838, rule: "exact" },
      children: [new TableCell({
        shading: { type: ShadingType.CLEAR, fill: CP.bg }, borders: noBorders,
        children,
      })],
    })],
  })];
}

// ---------- Body renderers ----------
const EN_FONT = { ascii: "Times New Roman", eastAsia: "SimSun" };
const HEAD_FONT = { ascii: "Times New Roman", eastAsia: "SimHei" };

function runsFromMarkup(text, base) {
  // Parses **bold** markers into TextRuns; no other markdown is honored.
  const parts = String(text).split(/\*\*(.+?)\*\*/g);
  const runs = [];
  for (let i = 0; i < parts.length; i++) {
    if (parts[i] === "") continue;
    runs.push(new TextRun(Object.assign({}, base, { text: parts[i], bold: i % 2 === 1 ? true : (base.bold || false) })));
  }
  return runs.length ? runs : [new TextRun(Object.assign({}, base, { text: "" }))];
}

function bodyPara(text) {
  return new Paragraph({
    alignment: AlignmentType.LEFT, // English body: left, no first-line indent
    spacing: { line: 312, after: 120 },
    children: runsFromMarkup(text, { size: 24, color: BODY_COLOR, font: EN_FONT }),
  });
}

function bulletPara(text) {
  return new Paragraph({
    bullet: { level: 0 },
    alignment: AlignmentType.LEFT,
    spacing: { line: 312, after: 80 },
    children: runsFromMarkup(text, { size: 24, color: BODY_COLOR, font: EN_FONT }),
  });
}

function heading(text, level) {
  return new Paragraph({ heading: level, children: [new TextRun({ text: safeText(text) })] });
}

const CELL_MARGINS = { top: 60, bottom: 60, left: 120, right: 120 };

function cellPara(text, opts) {
  const o = opts || {};
  return new Paragraph({
    alignment: AlignmentType.LEFT,
    spacing: { line: 312 },
    children: runsFromMarkup(text, {
      size: o.size || 21, bold: !!o.bold,
      color: o.color || BODY_COLOR, font: EN_FONT,
    }),
  });
}

let tableCounter = 0;
function dataTable(spec) {
  tableCounter += 1;
  const caption = new Paragraph({
    keepNext: true,
    spacing: { before: 240, after: 60, line: 312 },
    children: [new TextRun({ text: "Table " + tableCounter + ": " + spec.caption, bold: true, size: 21, color: INK, font: EN_FONT })],
  });
  const widths = spec.widths || spec.headers.map(() => Math.floor(100 / spec.headers.length));
  const headerRow = new TableRow({
    tableHeader: true, cantSplit: true,
    children: spec.headers.map((h, i) => new TableCell({
      children: [cellPara(h, { bold: true, color: P.table.headerText })],
      shading: { type: ShadingType.CLEAR, fill: P.table.headerBg },
      margins: CELL_MARGINS,
      width: { size: widths[i], type: WidthType.PERCENTAGE },
    })),
  });
  const rows = spec.rows.map((r, ri) => new TableRow({
    cantSplit: true,
    children: r.map((c, ci) => new TableCell({
      children: [cellPara(c, { bold: ci === 0 && !spec.zebra })],
      shading: spec.zebra
        ? { type: ShadingType.CLEAR, fill: ri % 2 === 0 ? P.table.surface : "FFFFFF" }
        : undefined,
      margins: CELL_MARGINS,
      width: { size: widths[ci], type: WidthType.PERCENTAGE },
    })),
  }));
  const tbl = new Table({
    width: { size: 100, type: WidthType.PERCENTAGE },
    borders: {
      top: { style: BorderStyle.SINGLE, size: 2, color: P.table.accentLine },
      bottom: { style: BorderStyle.SINGLE, size: 2, color: P.table.accentLine },
      left: NB, right: NB,
      insideHorizontal: { style: BorderStyle.SINGLE, size: 1, color: P.table.innerLine },
      insideVertical: NB,
    },
    rows: [headerRow, ...rows],
  });
  const spacer = new Paragraph({ spacing: { after: 120, line: 312 }, children: [] });
  return [caption, tbl, spacer];
}

function findingBlock(f) {
  const out = [];
  out.push(heading(f.id + " \u00b7 " + (f.short || f.title) + " (" + f.severity + ")", HeadingLevel.HEADING_3));
  const rows = [
    ["Location", f.location],
    ["Description", f.description],
    ["Evidence", f.evidence],
    ["Impact", f.impact],
    ["Recommended fix", f.fix],
    ["Confidence", f.confidence],
  ];
  out.push(...dataTable({
    caption: "Finding " + f.id + " \u2014 " + f.title,
    headers: ["Field", "Content"],
    widths: [18, 82],
    rows,
  }));
  return out;
}

let figureCounter = 0;
function pngSize(buf) {
  return { width: buf.readUInt32BE(16), height: buf.readUInt32BE(20) };
}
function chartBlock(spec) {
  figureCounter += 1;
  const chartPath = spec.path.startsWith("/")
    ? spec.path : path.resolve(__dirname, spec.path);
  const buf = fs.readFileSync(chartPath);
  const dims = pngSize(buf);
  const displayWidth = 560;
  const displayHeight = Math.round(displayWidth * (dims.height / dims.width));
  return [
    new Paragraph({
      alignment: AlignmentType.CENTER, spacing: { before: 200, after: 60, line: 312 },
      children: [new ImageRun({ data: buf, transformation: { width: displayWidth, height: displayHeight }, type: "png" })],
    }),
    new Paragraph({
      alignment: AlignmentType.CENTER, spacing: { after: 160, line: 312 },
      children: [new TextRun({ text: "Figure " + figureCounter + ": " + spec.caption, bold: true, size: 21, color: INK, font: EN_FONT })],
    }),
  ];
}

// ---------- Assemble body from content modules ----------
const content = [
  ...require(path.join(__dirname, "report_content_1.js")).blocks,
  ...require(path.join(__dirname, "report_content_2.js")).blocks,
];

const bodyChildren = [];
for (const b of content) {
  if (b.h1) bodyChildren.push(heading(b.h1, HeadingLevel.HEADING_1));
  else if (b.h2) bodyChildren.push(heading(b.h2, HeadingLevel.HEADING_2));
  else if (b.h3) bodyChildren.push(heading(b.h3, HeadingLevel.HEADING_3));
  else if (b.p) bodyChildren.push(bodyPara(b.p));
  else if (b.bullets) b.bullets.forEach((t) => bodyChildren.push(bulletPara(t)));
  else if (b.table) bodyChildren.push(...dataTable(b.table));
  else if (b.finding) bodyChildren.push(...findingBlock(b.finding));
  else if (b.chart) bodyChildren.push(...chartBlock(b.chart));
}

// ---------- Cover config ----------
const coverConfig = {
  englishLabel: "INDEPENDENT AUDIT REPORT",
  title: "Equity Research Audit",
  subtitle: "Three big-tech research agent skills evaluated against institutional research standards",
  metaLines: [
    "Repository: github.com/nordeim/my-pi-agent @ 48cd3f97 (2026-10-30)",
    "Scope: analyzing-us-bigtech-stocks \u00b7 big-tech-earnings-postmortem \u00b7 bigtech-equity-research",
    "Evidence: 17 files \u00b7 2,078 lines \u00b7 3 executed scripts \u00b7 19 verification checks",
    "Prepared by: GLM coding-specialist agent \u00b7 Mode C audit (review without modification)",
  ],
  footerLeft: "Informational audit \u2014 not investment advice",
  footerRight: "2026-10-30 \u00b7 Asia/Singapore",
};

// ---------- Page furniture ----------
function pageNumFooter() {
  return new Footer({
    children: [new Paragraph({
      alignment: AlignmentType.CENTER,
      children: [new TextRun({ children: [PageNumber.CURRENT], size: 18, color: "808080", font: EN_FONT })],
    })],
  });
}
function bodyHeader() {
  return new Header({
    children: [new Paragraph({
      alignment: AlignmentType.CENTER,
      children: [new TextRun({ text: "Equity Research Skill Audit \u2014 nordeim/my-pi-agent", size: 18, color: "808080", font: EN_FONT })],
    })],
  });
}

// ---------- TOC front matter ----------
const frontMatter = [
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 480, after: 360, line: 312 },
    children: [new TextRun({ text: "Table of Contents", bold: true, size: 32, color: INK, font: HEAD_FONT })],
  }),
  new TableOfContents("Table of Contents", { hyperlink: true, headingStyleRange: "1-3" }),
  new Paragraph({
    spacing: { before: 200, line: 312 },
    children: [new TextRun({
      text: "Note: This Table of Contents is generated via field codes. To ensure page number accuracy after editing, please right-click the TOC and select \u201cUpdate Field.\u201d",
      italics: true, size: 18, color: "888888", font: EN_FONT,
    })],
  }),
];

// ---------- Document ----------
const pgSize = { width: 11906, height: 16838 };
const pgMargin = { top: 1440, bottom: 1440, left: 1701, right: 1417 };

const doc = new Document({
  styles: {
    default: {
      document: {
        run: { font: EN_FONT, size: 24, color: BODY_COLOR },
        paragraph: { spacing: { line: 312 } },
      },
      heading1: {
        run: { font: HEAD_FONT, size: 32, bold: true, color: INK },
        paragraph: { spacing: { before: 360, after: 160, line: 312 } },
      },
      heading2: {
        run: { font: HEAD_FONT, size: 28, bold: true, color: INK },
        paragraph: { spacing: { before: 240, after: 120, line: 312 } },
      },
      heading3: {
        run: { font: HEAD_FONT, size: 24, bold: true, color: INK },
        paragraph: { spacing: { before: 200, after: 100, line: 312 } },
      },
    },
  },
  sections: [
    { // Section 1: Cover — margin 0, no footer, no page numbers
      properties: { page: { size: pgSize, margin: { top: 0, bottom: 0, left: 0, right: 0 } } },
      children: buildCoverR1(coverConfig),
    },
    { // Section 2: Front matter (TOC) — Roman numerals
      properties: {
        type: SectionType.NEXT_PAGE,
        page: { size: pgSize, margin: pgMargin, pageNumbers: { start: 1, formatType: NumberFormat.UPPER_ROMAN } },
      },
      footers: { default: pageNumFooter() },
      children: frontMatter,
    },
    { // Section 3: Body — Arabic numerals restarting at 1
      properties: {
        type: SectionType.NEXT_PAGE,
        page: { size: pgSize, margin: pgMargin, pageNumbers: { start: 1, formatType: NumberFormat.DECIMAL } },
      },
      headers: { default: bodyHeader() },
      footers: { default: pageNumFooter() },
      children: bodyChildren,
    },
  ],
});

Packer.toBuffer(doc).then((buf) => {
  fs.writeFileSync(OUT, buf);
  console.log("WROTE", OUT, buf.length, "bytes");
  console.log("tables:", tableCounter, "figures:", figureCounter,
    "body blocks:", content.length);
});
