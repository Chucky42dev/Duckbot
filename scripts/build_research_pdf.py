from pathlib import Path
import re

from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    ListFlowable,
    ListItem,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "docs" / "research-microduck.md"
OUTPUT = ROOT / "docs" / "research-microduck.pdf"


def register_fonts():
    font_dir = Path(r"C:\Windows\Fonts")
    regular = font_dir / "arial.ttf"
    bold = font_dir / "arialbd.ttf"
    mono = font_dir / "consola.ttf"
    if mono.exists():
        pdfmetrics.registerFont(TTFont("DuckMono", str(mono)))
        mono_name = "DuckMono"
    else:
        mono_name = "Courier"
    if regular.exists() and bold.exists():
        pdfmetrics.registerFont(TTFont("DuckArial", str(regular)))
        pdfmetrics.registerFont(TTFont("DuckArial-Bold", str(bold)))
        pdfmetrics.registerFontFamily(
            "DuckArial", normal="DuckArial", bold="DuckArial-Bold",
            italic="DuckArial", boldItalic="DuckArial-Bold",
        )
        return "DuckArial", "DuckArial-Bold", mono_name
    return "Helvetica", "Helvetica-Bold", mono_name


MONO_FONT = "Courier"


def inline_markup(text):
    text = re.sub(r"\[([^]]+)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"`([^`]+)`", rf"<font name='{MONO_FONT}'>\1</font>", text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", text)
    return text.replace("&", "&amp;").replace("<font", "<font").replace("<b>", "<b>")


def build_pdf():
    global MONO_FONT
    regular, bold, MONO_FONT = register_fonts()
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(
        name="DuckTitle", parent=styles["Title"], fontName=bold,
        fontSize=20, leading=25, alignment=TA_CENTER, spaceAfter=14,
    ))
    styles.add(ParagraphStyle(
        name="DuckHeading", parent=styles["Heading2"], fontName=bold,
        fontSize=13, leading=17, spaceBefore=10, spaceAfter=6,
    ))
    styles.add(ParagraphStyle(
        name="DuckSubheading", parent=styles["Heading3"], fontName=bold,
        fontSize=11, leading=14, spaceBefore=8, spaceAfter=4,
    ))
    styles.add(ParagraphStyle(
        name="DuckBody", parent=styles["BodyText"], fontName=regular,
        fontSize=9.5, leading=13, spaceAfter=6,
    ))
    styles.add(ParagraphStyle(
        name="DuckBullet", parent=styles["BodyText"], fontName=regular,
        fontSize=9.5, leading=13, leftIndent=12, firstLineIndent=0,
        spaceAfter=3,
    ))
    styles.add(ParagraphStyle(
        name="DuckCode", parent=styles["Code"], fontName=MONO_FONT,
        fontSize=7.5, leading=10, leftIndent=12, rightIndent=12,
        backColor="#f1f3f5", borderPadding=5, spaceAfter=7,
    ))

    styles.add(ParagraphStyle(
        name="DuckCell", parent=styles["BodyText"], fontName=regular,
        fontSize=8.5, leading=11,
    ))
    styles.add(ParagraphStyle(
        name="DuckCellHead", parent=styles["BodyText"], fontName=bold,
        fontSize=8.5, leading=11,
    ))

    def is_block_start(text):
        stripped = text.strip()
        return (
            not stripped
            or stripped.startswith(("#", "```", "- ", "|"))
            or re.match(r"^\d+\. ", stripped) is not None
        )

    def collect_continuation(start):
        """Gather wrapped lines that belong to the item starting at `start`."""
        parts = [lines[start].strip()]
        position = start + 1
        while position < len(lines):
            candidate = lines[position]
            if not candidate.strip() or is_block_start(candidate):
                break
            if not candidate.startswith(" "):
                break
            parts.append(candidate.strip())
            position += 1
        return " ".join(parts), position

    def build_table(rows):
        header, *body = rows
        data = [[Paragraph(inline_markup(cell), styles["DuckCellHead"]) for cell in header]]
        for row in body:
            data.append([Paragraph(inline_markup(cell), styles["DuckCell"]) for cell in row])
        available = A4[0] - 36 * mm
        widths = [available * 0.18, available * 0.57, available * 0.25]
        if len(header) != 3:
            widths = [available / len(header)] * len(header)
        table = Table(data, colWidths=widths, repeatRows=1)
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e9ecef")),
            ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#adb5bd")),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("TOPPADDING", (0, 0), (-1, -1), 3),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ]))
        return table

    story = []
    lines = SOURCE.read_text(encoding="utf-8").splitlines()
    index = 0
    while index < len(lines):
        line = lines[index].strip()
        if not line:
            index += 1
            continue
        if line.startswith("# "):
            story.append(Paragraph(inline_markup(line[2:]), styles["DuckTitle"]))
            index += 1
        elif line.startswith("## "):
            story.append(Paragraph(inline_markup(line[3:]), styles["DuckHeading"]))
            index += 1
        elif line.startswith("### "):
            story.append(Paragraph(inline_markup(line[4:]), styles["DuckSubheading"]))
            index += 1
        elif line.startswith("```"):
            code = []
            index += 1
            while index < len(lines) and not lines[index].strip().startswith("```"):
                code.append(
                    lines[index].replace("&", "&amp;").replace("<", "&lt;").replace(" ", "&nbsp;")
                )
                index += 1
            story.append(Paragraph("<br/>".join(code), styles["DuckCode"]))
            index += 1
        elif line.startswith("|"):
            rows = []
            while index < len(lines) and lines[index].strip().startswith("|"):
                cells = [c.strip() for c in lines[index].strip().strip("|").split("|")]
                if not all(re.fullmatch(r":?-+:?", c) for c in cells):
                    rows.append(cells)
                index += 1
            story.append(build_table(rows))
            story.append(Spacer(1, 6))
        elif line.startswith("- "):
            items = []
            while index < len(lines) and lines[index].strip().startswith("- "):
                text, index = collect_continuation(index)
                items.append(ListItem(Paragraph(inline_markup(text[2:]), styles["DuckBullet"])))
            story.append(ListFlowable(items, bulletType="bullet", start="circle", leftIndent=14))
            story.append(Spacer(1, 4))
        elif re.match(r"^\d+\. ", line):
            text, index = collect_continuation(index)
            story.append(Paragraph(inline_markup(text), styles["DuckBody"]))
        else:
            parts = []
            while index < len(lines) and lines[index].strip() and not is_block_start(lines[index]):
                parts.append(lines[index].strip())
                index += 1
            story.append(Paragraph(inline_markup(" ".join(parts)), styles["DuckBody"]))

    document = SimpleDocTemplate(
        str(OUTPUT), pagesize=A4, rightMargin=18 * mm, leftMargin=18 * mm,
        topMargin=16 * mm, bottomMargin=16 * mm,
        title="Microduck a návrh Duckbotu",
        author="Duckbot project",
    )
    document.build(story)


if __name__ == "__main__":
    build_pdf()