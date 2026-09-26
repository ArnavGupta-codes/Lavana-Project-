#!/usr/bin/env python3
"""
Generate a comprehensive professional PDF report on Indian Salt Pans.
Uses reportlab to produce a LaTeX-styled academic document.
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm, mm
from reportlab.lib.colors import HexColor, black, white, Color
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable, KeepTogether, ListFlowable, ListItem,
    Indenter
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.platypus.flowables import Flowable
from reportlab.lib import colors
import os

OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "..", "Salt_Pans_India_Report.pdf")

# ── Color Palette ──────────────────────────────────────────────────────────────
DEEP_TEAL   = HexColor("#00524A")   # title bar / section headers
MED_TEAL    = HexColor("#007A6E")   # sub-section headers
LIGHT_TEAL  = HexColor("#E0F4F2")   # table header bg
ACCENT      = HexColor("#C8820A")   # rule lines / table rule
DARK_TEXT   = HexColor("#1A1A1A")
BODY_TEXT   = HexColor("#2D2D2D")
MUTED       = HexColor("#5A5A5A")
TABLE_ODD   = HexColor("#F4FAFA")
TABLE_EVEN  = HexColor("#FFFFFF")
RULE_COLOR  = HexColor("#C8820A")

PAGE_W, PAGE_H = A4
L_MARGIN = R_MARGIN = 2.5 * cm
T_MARGIN = B_MARGIN = 2.2 * cm
CONTENT_W = PAGE_W - L_MARGIN - R_MARGIN


# ── Header / Footer ────────────────────────────────────────────────────────────
def on_page(canvas, doc):
    canvas.saveState()
    w, h = A4

    if doc.page == 1:
        # Decorative top bar
        canvas.setFillColor(DEEP_TEAL)
        canvas.rect(0, h - 1.2*cm, w, 1.2*cm, fill=True, stroke=False)
        canvas.setFillColor(ACCENT)
        canvas.rect(0, h - 1.5*cm, w, 0.3*cm, fill=True, stroke=False)
    else:
        # Running header
        canvas.setFillColor(DEEP_TEAL)
        canvas.rect(0, h - 1.0*cm, w, 1.0*cm, fill=True, stroke=False)
        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(white)
        canvas.drawString(L_MARGIN, h - 0.65*cm,
                          "Salt Pans of India: A Comprehensive Study")
        canvas.drawRightString(w - R_MARGIN, h - 0.65*cm,
                               "Gupta & Srinivas, 2026")

    # Footer
    canvas.setFillColor(DEEP_TEAL)
    canvas.rect(0, 0, w, 0.8*cm, fill=True, stroke=False)
    canvas.setFillColor(ACCENT)
    canvas.rect(0, 0.8*cm, w, 0.18*cm, fill=True, stroke=False)
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(white)
    if doc.page > 1:
        canvas.drawCentredString(w / 2, 0.28*cm, f"— {doc.page} —")
    canvas.restoreState()


# ── Style Sheet ────────────────────────────────────────────────────────────────
def build_styles():
    base = getSampleStyleSheet()

    def ps(name, **kw):
        parent = kw.pop("parent", "Normal")
        return ParagraphStyle(name, parent=base[parent], **kw)

    styles = {
        # ── Title block ──
        "title": ps("title",
                    fontName="Helvetica-Bold", fontSize=26,
                    textColor=DEEP_TEAL, alignment=TA_CENTER,
                    spaceAfter=4, leading=32),
        "subtitle": ps("subtitle",
                       fontName="Helvetica", fontSize=13,
                       textColor=MED_TEAL, alignment=TA_CENTER,
                       spaceAfter=3, leading=16),
        "authors": ps("authors",
                      fontName="Helvetica-Bold", fontSize=12,
                      textColor=ACCENT, alignment=TA_CENTER,
                      spaceAfter=2),
        "affil": ps("affil",
                    fontName="Helvetica-Oblique", fontSize=10,
                    textColor=MUTED, alignment=TA_CENTER,
                    spaceAfter=2),
        "date": ps("date",
                   fontName="Helvetica", fontSize=10,
                   textColor=MUTED, alignment=TA_CENTER,
                   spaceAfter=12),

        # ── Abstract ──
        "abs_head": ps("abs_head",
                       fontName="Helvetica-Bold", fontSize=10,
                       textColor=DEEP_TEAL, alignment=TA_CENTER,
                       spaceAfter=4),
        "abstract": ps("abstract",
                       fontName="Helvetica", fontSize=9.5,
                       textColor=BODY_TEXT, alignment=TA_JUSTIFY,
                       leftIndent=1.5*cm, rightIndent=1.5*cm,
                       spaceAfter=6, leading=14),

        # ── Sections ──
        "h1": ps("h1",
                 fontName="Helvetica-Bold", fontSize=14,
                 textColor=white, alignment=TA_LEFT,
                 spaceBefore=14, spaceAfter=6, leading=18,
                 leftIndent=-0.3*cm,
                 backColor=DEEP_TEAL,
                 borderPadding=(5, 8, 5, 8)),
        "h2": ps("h2",
                 fontName="Helvetica-Bold", fontSize=11.5,
                 textColor=MED_TEAL, alignment=TA_LEFT,
                 spaceBefore=10, spaceAfter=4, leading=14),
        "h3": ps("h3",
                 fontName="Helvetica-BoldOblique", fontSize=10.5,
                 textColor=ACCENT, alignment=TA_LEFT,
                 spaceBefore=8, spaceAfter=3, leading=13),

        # ── Body ──
        "body": ps("body",
                   fontName="Helvetica", fontSize=10,
                   textColor=BODY_TEXT, alignment=TA_JUSTIFY,
                   spaceAfter=6, leading=15),
        "bullet": ps("bullet",
                     fontName="Helvetica", fontSize=10,
                     textColor=BODY_TEXT, alignment=TA_LEFT,
                     leftIndent=0.7*cm, bulletIndent=0.2*cm,
                     spaceAfter=3, leading=14),
        "caption": ps("caption",
                      fontName="Helvetica-Oblique", fontSize=8.5,
                      textColor=MUTED, alignment=TA_CENTER,
                      spaceAfter=6),
        "kw": ps("kw",
                 fontName="Helvetica-Oblique", fontSize=9.5,
                 textColor=MUTED, alignment=TA_CENTER, spaceAfter=8),
    }
    return styles


# ── Helpers ────────────────────────────────────────────────────────────────────
def rule(w=CONTENT_W, color=RULE_COLOR, thickness=1):
    return HRFlowable(width=w, thickness=thickness, color=color,
                      spaceAfter=4, spaceBefore=4)

def section_header(text, styles, number=""):
    label = f"{number}  {text}" if number else text
    return Paragraph(label, styles["h1"])

def sub_header(text, styles):
    return Paragraph(text, styles["h2"])

def sub_sub_header(text, styles):
    return Paragraph(text, styles["h3"])

def body(text, styles):
    return Paragraph(text, styles["body"])

def bullet(text, styles):
    return Paragraph(f"• {text}", styles["bullet"])

def sp(n=6):
    return Spacer(1, n)

def make_table(data, col_widths, styles_list, style_obj):
    t = Table(data, colWidths=col_widths, repeatRows=1)
    t.setStyle(TableStyle(styles_list))
    return t

def state_table(styles):
    """Production data by state (2021-22)."""
    header = ["State / UT", "Production\n(Lakh Tonnes)", "Share (%)", "Primary Method"]
    rows = [
        ["Gujarat", "227.64", "85.6", "Coastal solar / sub-soil brine"],
        ["Tamil Nadu", "17.21", "6.5", "Coastal solar evaporation"],
        ["Rajasthan", "16.90", "6.4", "Lake brine / sub-soil brine"],
        ["Andhra Pradesh", "4.35*", "1.6", "Coastal solar evaporation"],
        ["Maharashtra", "—", "~0.5", "Coastal solar evaporation"],
        ["Other States", "~4.24", "1.6", "Various"],
        ["India Total", "266.00", "100", "—"],
    ]
    data = [header] + rows
    col_w = [CONTENT_W*0.32, CONTENT_W*0.20, CONTENT_W*0.15, CONTENT_W*0.33]
    ts = [
        ("BACKGROUND",  (0,0), (-1,0), DEEP_TEAL),
        ("TEXTCOLOR",   (0,0), (-1,0), white),
        ("FONTNAME",    (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTSIZE",    (0,0), (-1,-1), 9),
        ("ALIGN",       (0,0), (-1,-1), "CENTER"),
        ("ALIGN",       (0,0), (0,-1), "LEFT"),
        ("ALIGN",       (3,0), (3,-1), "LEFT"),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [TABLE_ODD, TABLE_EVEN]),
        ("GRID",        (0,0), (-1,-1), 0.5, HexColor("#C0D0CE")),
        ("FONTNAME",    (0,-1), (-1,-1), "Helvetica-Bold"),
        ("BACKGROUND",  (0,-1), (-1,-1), LIGHT_TEAL),
        ("BOTTOMPADDING",(0,0),(-1,-1), 5),
        ("TOPPADDING",  (0,0),(-1,-1), 5),
        ("LEFTPADDING", (0,0),(0,-1), 6),
    ]
    return make_table(data, col_w, ts, styles)

def sites_table(styles):
    """Key salt pan sites table."""
    header = ["Site / Region", "State", "Type", "Area / Output", "Notable Feature"]
    rows = [
        ["Little Rann of Kutch", "Gujarat", "Regional Area",
         "~45,000 workers\n(Agariya families)", "Sub-soil brine; wildass sanctuary"],
        ["Sambhar Salt Lake", "Rajasthan", "Salt Lake",
         "~2 lakh t/yr", "Ramsar site #464; largest inland saline lake"],
        ["Thoothukudi (Tuticorin)", "Tamil Nadu", "Production Cluster",
         "~25,000 acres†", "Salt Capital of Tamil Nadu"],
        ["Vedaranyam", "Tamil Nadu", "Production Cluster",
         "—", "Ramsar site; 1930 Salt Satyagraha endpoint"],
        ["Tata Chemicals Mithapur", "Gujarat", "Salt Works",
         "—", "Est. 1939; marine national park adjacency"],
        ["Chinnaganjam", "Andhra Pradesh", "Production Cluster",
         "7,867 acres‡", "Sand-mining threat; protest history"],
        ["Marakkanam", "Tamil Nadu", "Production Cluster",
         "~60,000 TN workers", "Women-majority workforce"],
        ["Pachpadra Lake", "Rajasthan", "Salt Lake",
         "~98% NaCl", "Traditional Khara community methods"],
        ["Mumbai Salt Pans", "Maharashtra", "Regional Area",
         "~5,379 acres", "Urban flood buffer; flamingo habitat"],
        ["Bhavnagar Coast", "Gujarat", "Regional Area",
         "4 lakh t/yr§", "Cyclone-risk zone; private manufacturers"],
    ]
    data = [header] + rows
    col_w = [CONTENT_W*0.24, CONTENT_W*0.14, CONTENT_W*0.18, CONTENT_W*0.19, CONTENT_W*0.25]
    ts = [
        ("BACKGROUND",  (0,0), (-1,0), DEEP_TEAL),
        ("TEXTCOLOR",   (0,0), (-1,0), white),
        ("FONTNAME",    (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTSIZE",    (0,0), (-1,-1), 8.5),
        ("ALIGN",       (0,0), (-1,-1), "LEFT"),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [TABLE_ODD, TABLE_EVEN]),
        ("GRID",        (0,0), (-1,-1), 0.4, HexColor("#C0D0CE")),
        ("BOTTOMPADDING",(0,0),(-1,-1), 5),
        ("TOPPADDING",  (0,0),(-1,-1), 5),
        ("LEFTPADDING", (0,0),(-1,-1), 5),
        ("VALIGN",      (0,0),(-1,-1), "TOP"),
    ]
    return make_table(data, col_w, ts, styles)

def health_table(styles):
    """Worker health issues table."""
    header = ["Health Concern", "Cause / Mechanism", "Prevalence"]
    rows = [
        ["Skin lesions & burns", "Prolonged contact with hypersaline brine;\nsun exposure at 45–50 °C", "Very High"],
        ["Eye irritation / loss of vision", "Salt spray, UV radiation, lack of PPE", "High"],
        ["Musculoskeletal disorders", "Repetitive manual harvesting; carrying loads", "High"],
        ["Kidney dysfunction", "Chronic dehydration; high NaCl intake", "Moderate–High"],
        ["Hypertension", "High sodium intake; heat stress", "Moderate"],
        ["Respiratory issues", "Salt dust inhalation during harvesting", "Moderate"],
        ["Malnutrition / anaemia", "Low wages; seasonal unemployment", "High (women)"],
    ]
    data = [header] + rows
    col_w = [CONTENT_W*0.30, CONTENT_W*0.45, CONTENT_W*0.25]
    ts = [
        ("BACKGROUND",  (0,0), (-1,0), MED_TEAL),
        ("TEXTCOLOR",   (0,0), (-1,0), white),
        ("FONTNAME",    (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTSIZE",    (0,0), (-1,-1), 9),
        ("ALIGN",       (0,0), (-1,-1), "LEFT"),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [TABLE_ODD, TABLE_EVEN]),
        ("GRID",        (0,0), (-1,-1), 0.4, HexColor("#C0D0CE")),
        ("BOTTOMPADDING",(0,0),(-1,-1), 5),
        ("TOPPADDING",  (0,0),(-1,-1), 5),
        ("LEFTPADDING", (0,0),(-1,-1), 5),
        ("VALIGN",      (0,0),(-1,-1), "TOP"),
    ]
    return make_table(data, col_w, ts, styles)

def tech_table(styles):
    """Technology & quality improvement table."""
    header = ["Technology / Practice", "Benefit", "Status in India"]
    rows = [
        ["Geo-Membrane (GM) Liners\nin crystallisation ponds",
         "Reduces brine seepage by 15–20%;\nimproves purity by 12–15%",
         "Pilot scale; promoted by CSIR-CSMCRI"],
        ["Concrete / fly-ash hardened beds",
         "Prevents contamination;\nenables mechanical harvesting",
         "Partial adoption; larger works"],
        ["Solar PV brine pumps",
         "Replaces diesel; lowers cost\nand carbon footprint",
         "SEWA-supported rollout in Gujarat"],
        ["Heat exchanger / solar-assisted\nevaporation systems",
         "Increases yield 60→85 t/acre;\nshortens cycle by 30–40%",
         "Research stage; CSIR-CSMCRI"],
        ["Mechanised harvesting",
         "Improves efficiency;\nreduces impurities",
         "Large private works; not SMEs"],
        ["Automated spray iodisation",
         "Uniform iodine mixing;\nFSSAI compliance",
         "Mandated; adoption ongoing"],
        ["Model Salt Farms",
         "Demonstrates best practices\nto smaller producers",
         "SCO initiative; Gujarat, TN, Odisha"],
        ["Salt Testing Kits (STKs)",
         "Field-level iodine quality\nverification",
         "Distributed by state health depts."],
    ]
    data = [header] + rows
    col_w = [CONTENT_W*0.33, CONTENT_W*0.38, CONTENT_W*0.29]
    ts = [
        ("BACKGROUND",  (0,0), (-1,0), MED_TEAL),
        ("TEXTCOLOR",   (0,0), (-1,0), white),
        ("FONTNAME",    (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTSIZE",    (0,0), (-1,-1), 8.8),
        ("ALIGN",       (0,0), (-1,-1), "LEFT"),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [TABLE_ODD, TABLE_EVEN]),
        ("GRID",        (0,0), (-1,-1), 0.4, HexColor("#C0D0CE")),
        ("BOTTOMPADDING",(0,0),(-1,-1), 5),
        ("TOPPADDING",  (0,0),(-1,-1), 5),
        ("LEFTPADDING", (0,0),(-1,-1), 5),
        ("VALIGN",      (0,0),(-1,-1), "TOP"),
    ]
    return make_table(data, col_w, ts, styles)


# ── Abstract Box ───────────────────────────────────────────────────────────────
class AbstractBox(Flowable):
    def __init__(self, text, width, style):
        super().__init__()
        self.text = text
        self.width = width
        self.style = style
        self._p = Paragraph(text, style)
        self._p.wrap(width - 2*cm, 9999)

    def wrap(self, avW, avH):
        self._p.wrap(self.width - 2*cm, avH)
        h = self._p.height + 1.4*cm
        return self.width, h

    def draw(self):
        c = self.canv
        h = self._p.height + 1.4*cm
        c.setStrokeColor(DEEP_TEAL)
        c.setFillColor(LIGHT_TEAL)
        c.setLineWidth(1.5)
        c.roundRect(0, 0, self.width, h, 6, fill=True, stroke=True)
        c.setStrokeColor(ACCENT)
        c.setLineWidth(4)
        c.line(0, h/2, 0, h)  # left accent bar top
        self._p.drawOn(c, cm, 0.7*cm)


# ── Build Document ─────────────────────────────────────────────────────────────
def build_pdf():
    styles = build_styles()
    doc = SimpleDocTemplate(
        OUTPUT_PATH,
        pagesize=A4,
        leftMargin=L_MARGIN, rightMargin=R_MARGIN,
        topMargin=T_MARGIN + 1.0*cm, bottomMargin=B_MARGIN + 0.8*cm,
        title="Salt Pans of India: A Comprehensive Study",
        author="Arnav Gupta; Satvik Srinivas",
        subject="Indian Salt Industry, Worker Welfare, Quality Improvement",
        creator="Salt Pans India Research Team",
    )

    story = []

    # ══════════════════════════════════════════════════════
    # TITLE PAGE
    # ══════════════════════════════════════════════════════
    story += [
        sp(40),
        Paragraph("Salt Pans of India", styles["title"]),
        sp(4),
        Paragraph("A Comprehensive Study of Production, Worker Welfare,",
                  styles["subtitle"]),
        Paragraph("Quality Improvement, and Ecological Significance",
                  styles["subtitle"]),
        sp(10),
        rule(CONTENT_W, ACCENT, 2),
        sp(8),
        Paragraph("Arnav Gupta &nbsp;&nbsp;·&nbsp;&nbsp; Satvik Srinivas",
                  styles["authors"]),
        Paragraph("Lavana Project Research Initiative", styles["affil"]),
        Paragraph("September 2026", styles["date"]),
        sp(16),
    ]

    # Abstract
    abs_text = (
        "India is the world's third-largest producer of salt, generating approximately "
        "<b>266 lakh tonnes</b> (26.6 million tonnes) annually, of which <b>Gujarat alone "
        "contributes 85.6%</b>. Salt pans—ranging from vast coastal solar-evaporation "
        "works and inland saline lakes to traditional community pans—underpin a sector "
        "that employs over 77,000 registered workers and sustains an informal workforce "
        "estimated at several hundred thousand. This report synthesises geographic, "
        "socioeconomic, and ecological data drawn from the Lavana GIS dataset (48 sites "
        "across 11 states/UTs), the Indian Minerals Yearbook 2022, the Salt Commissioner's "
        "Organisation, peer-reviewed literature, and field journalism to present a "
        "holistic account of India's salt pans. Topics covered include: the geography and "
        "geology of major production centres; historical significance; the working "
        "conditions, health challenges, and welfare initiatives targeting the salt-pan "
        "labour force; best practices in quality improvement and iodisation; technological "
        "modernisation; ecological roles in supporting migratory bird populations; and "
        "the regulatory and legal landscape governing this ancient industry."
    )
    story += [
        Paragraph("Abstract", styles["abs_head"]),
        sp(4),
        AbstractBox(abs_text, CONTENT_W, styles["abstract"]),
        sp(8),
        Paragraph("<b>Keywords:</b> salt pans, India, Agariyas, solar evaporation, "
                  "iodisation, worker welfare, flamingos, Little Rann of Kutch, "
                  "Sambhar Lake, Lavana GIS dataset",
                  styles["kw"]),
        PageBreak(),
    ]

    # ══════════════════════════════════════════════════════
    # 1. INTRODUCTION
    # ══════════════════════════════════════════════════════
    story += [
        section_header("Introduction", styles, "1"),
        sp(4),
        body(
            "Salt — chemically sodium chloride (NaCl) — is among humanity's oldest "
            "and most essential commodities. In India, the salt industry carries "
            "profound historical weight, having been at the centre of Mahatma Gandhi's "
            "celebrated <b>Salt Satyagraha (Dandi March, 1930)</b>, a defining act of "
            "civil disobedience against British colonial taxation. Today, India ranks "
            "third globally in salt production (after China and the United States), "
            "producing roughly <b>30–32 million tonnes per year</b> in the 2022–2024 period.",
            styles),
        body(
            "The industry is structured around three broad production systems: "
            "<b>(i) coastal solar-evaporation works</b>, which dominate Gujarat, Tamil Nadu, "
            "Andhra Pradesh, Maharashtra, and Goa; "
            "<b>(ii) inland saline lake and sub-soil brine operations</b>, centred on "
            "Rajasthan's lakes (Sambhar, Pachpadra, Didwana) and Gujarat's Little Rann "
            "of Kutch; and "
            "<b>(iii) smaller artisanal and cooperative pans</b> found along the Konkan, "
            "Odisha, and West Bengal coasts.",
            styles),
        body(
            "Despite its scale and strategic importance, the industry is characterised by "
            "informality, low mechanisation, and persistent deficits in worker welfare. "
            "This report aims to provide a data-grounded, multi-dimensional analysis of "
            "the sector to inform policy, research, and public understanding.",
            styles),

        # ── 1.1 Scope ──
        sub_header("1.1  Scope and Data Sources", styles),
        body(
            "The primary geographic dataset used in this report is the <b>Lavana GIS "
            "Dataset v1</b> (compiled September 2026), which documents 48 salt pan sites "
            "across 11 Indian states and union territories. Quantitative production "
            "statistics are drawn from the <b>Indian Minerals Yearbook 2022</b> (IBM/Salt "
            "Commissioner's Organisation). Socioeconomic data are sourced from the "
            "Journal of Management Research and Analysis (JMRA, 2025), the Berkeley "
            "Journal of Sociology, PARI (People's Archive of Rural India), Mongabay India, "
            "and The Hindu. Ecological information is drawn from Ramsar Site Information "
            "Service (RSIS), Bombay Natural History Society (BNHS), and peer-reviewed "
            "ornithological literature. Welfare and policy information is sourced from "
            "government announcements, SEWA, and GeoJuris Today.",
            styles),
    ]

    # ══════════════════════════════════════════════════════
    # 2. GEOGRAPHY & PRODUCTION
    # ══════════════════════════════════════════════════════
    story += [
        PageBreak(),
        section_header("Geography and Production Landscape", styles, "2"),
        sp(4),
        body(
            "India's coastline stretches over 7,500 km along the Arabian Sea, Bay of "
            "Bengal, and Indian Ocean, providing extensive evaporation potential. The "
            "interior plateaux of Rajasthan add significant inland saline resources. "
            "Salt production is highly concentrated: <b>Gujarat accounts for over 85%</b> "
            "of national output.",
            styles),

        sub_header("2.1  State-wise Production (2021–22)", styles),
        sp(4),
        state_table(styles),
        Paragraph(
            "Table 1: State-wise salt production, 2021–22. Source: IBM Indian Minerals "
            "Yearbook 2022 / Salt Commissioner's Organisation. "
            "* AP figure from Hans India (Apr 2022); † journalist estimate (PARI); "
            "‡ 2008 district figure; § manufacturer self-report (Mongabay, 2024).",
            styles["caption"]),
        sp(8),

        sub_header("2.2  Key Sites and Regions", styles),
        body(
            "The Lavana Dataset v1 identifies 43 documented entries across 10 states "
            "and one union territory (Dadra and Nagar Haveli and Daman and Diu). The "
            "following table summarises the most significant sites.",
            styles),
        sp(4),
        sites_table(styles),
        Paragraph(
            "Table 2: Key salt pan sites in India. Sources: Lavana GIS Dataset v1 (2026), "
            "IBM IMYB 2022, SCO Salient Features, Wikipedia, PARI, Tata Group.",
            styles["caption"]),
        sp(8),

        sub_header("2.3  Gujarat: The Dominant Producer", styles),
        body(
            "Gujarat's dominance stems from its 1,600 km coastline, arid climate, "
            "low annual rainfall (400–600 mm on the Saurashtra coast), and high "
            "solar insolation. The <b>Little Rann of Kutch (LRK)</b> — a seasonal "
            "saline marsh of ~5,000 km² — is home to the <i>Agariya</i> community, "
            "traditional sub-soil brine salt farmers. Approximately <b>45,000 Agariyas</b> "
            "work within or adjacent to the Indian Wild Ass Sanctuary, producing the "
            "iconic 'white gold' of Kutch. The Gujarat coast from Jamnagar through "
            "Bhavnagar, Dahej, and south to Valsad supports a dense belt of marine "
            "solar-evaporation works.",
            styles),
        body(
            "Average yields have declined in recent years — from approximately "
            "<b>80 tonnes/acre in 2016–17 to 68 tonnes/acre in 2020–21</b> in Jamnagar "
            "(JMRA, 2025) — driven by erratic monsoon patterns and increasingly frequent "
            "cyclones that disrupt the October–May production season.",
            styles),

        sub_header("2.4  Rajasthan: Inland Saline Heritage", styles),
        body(
            "Rajasthan's salt landscape is centred on three ancient saline lakes. "
            "<b>Sambhar Salt Lake</b> (Ramsar site No. 464, designated 1990) is India's "
            "largest inland saline lake with a catchment of ~5,700 km². Sambhar Salts "
            "Ltd (a subsidiary of Hindustan Salts Ltd) produces approximately "
            "<b>2 lakh tonnes/yr</b> of raw salt. <b>Pachpadra Lake</b> near Balotra "
            "has been mined by the traditional Khara (Kharwal) community for centuries "
            "using the <i>morli</i> shrub crystallisation technique; its salt is "
            "approximately 98% NaCl. <b>Didwana Lake</b> produces lower-grade industrial "
            "salt, primarily used for sodium sulphate extraction.",
            styles),

        sub_header("2.5  Tamil Nadu, Andhra Pradesh, and Other States", styles),
        body(
            "Tamil Nadu's production belt stretches from Thoothukudi ('Salt Capital') "
            "northward through Marakkanam and Vedaranyam. The state produces "
            "approximately <b>17.21 lakh tonnes/yr</b>, though PARI estimates the "
            "district of Thoothukudi alone covers 25,000 acres of pans. "
            "Andhra Pradesh's coast from Nellore to Srikakulam — especially the 'Salt "
            "Bowl' of Naupada — contributes roughly 4.35 lakh tonnes/yr. "
            "Maharashtra's Mumbai salt pans (~5,379 acres) serve a dual ecological–industrial "
            "function; much of this land is under development pressure for urban "
            "infrastructure, raising conservation concerns.",
            styles),
    ]

    # ══════════════════════════════════════════════════════
    # 3. HISTORICAL SIGNIFICANCE
    # ══════════════════════════════════════════════════════
    story += [
        PageBreak(),
        section_header("Historical Significance", styles, "3"),
        sp(4),
        body(
            "Salt's role in Indian history transcends economics. As a universal dietary "
            "necessity in a tropical country, it was a natural lever for both state "
            "revenue and popular mobilisation.",
            styles),

        sub_header("3.1  Ancient and Medieval Trade", styles),
        body(
            "Large-scale salt production around Patadi, Jhinjuwada, and Kharaghoda in "
            "the Little Rann of Kutch is documented as early as the <b>10th century CE</b> "
            "(Campbell, 1887, via Berkeley Journal of Sociology). A <b>Mughal firman of "
            "1669–70</b> reinstating the King of Halvad as owner of <i>agar</i> (salt pans) "
            "illustrates the commodity's political economy in the pre-colonial period. "
            "Rajputana salt lakes — Sambhar, Pachpadra, Didwana — were administered "
            "under the Rajputana salt agency and yielded revenues to multiple princely "
            "states; between <b>1870 and 1905–06</b>, approximately <b>3.67 million tonnes</b> "
            "of salt were extracted from Sambhar alone.",
            styles),

        sub_header("3.2  The British Salt Monopoly", styles),
        body(
            "Under colonial rule, the 1882 <b>Salt Act</b> established a British monopoly, "
            "criminalising the independent production or collection of salt. This "
            "generated enormous revenue but imposed a regressive burden on ordinary "
            "Indians — salt being disproportionately costly relative to incomes. The "
            "Tata group's acquisition of the Okha Salt Works at Mithapur in <b>1939</b> "
            "(with a soda ash plant starting production in 1944) represents the early "
            "industrialisation of the sector under private enterprise.",
            styles),

        sub_header("3.3  The Dandi March (Salt Satyagraha, 1930)", styles),
        body(
            "On <b>12 March 1930</b>, Mahatma Gandhi and 78–80 volunteers began a "
            "241-mile (387 km) march from Sabarmati Ashram, Ahmedabad, to the coastal "
            "village of Dandi, Gujarat. Upon reaching Dandi on <b>6 April 1930</b>, "
            "Gandhi broke the Salt Act by collecting natural salt from the seashore, "
            "triggering nationwide civil disobedience. Simultaneously, C. Rajagopalachari "
            "led a parallel salt march from Tiruchirapalli to <b>Vedaranyam</b>, Tamil Nadu "
            "(now a Ramsar-listed site), underscoring that salt transcended geography "
            "in its unifying power. The Satyagraha is widely credited with internationalising "
            "India's independence movement and demonstrating the moral power of non-violent "
            "resistance.",
            styles),

        sub_header("3.4  Post-Independence Development", styles),
        body(
            "After 1947, the Salt Commissioner's Organisation (SCO) — housed under the "
            "Ministry of Commerce and Industry (later DPIIT) — became the nodal body for "
            "production regulation, land leasing, welfare, and iodisation policy. "
            "Universal Salt Iodisation (USI) became national policy in the 1990s to "
            "address widespread iodine-deficiency disorders; FSSAI now mandates specific "
            "iodine concentrations in all edible salt. The establishment of Sambhar "
            "Salts Ltd as a public-sector undertaking and Hindustan Salts Ltd as its "
            "parent entity reflect the government's role in managing key assets while "
            "the bulk of production remains in private and cooperative hands.",
            styles),
    ]

    # ══════════════════════════════════════════════════════
    # 4. WORKER WELFARE
    # ══════════════════════════════════════════════════════
    story += [
        PageBreak(),
        section_header("The Salt Pan Workforce: Conditions and Welfare", styles, "4"),
        sp(4),
        body(
            "The salt industry employs approximately <b>77,086 average workers</b> "
            "(IBM IMYB 2022, registered/formal). The informal workforce — including "
            "migrant Agariya families in Gujarat and seasonal workers in Tamil Nadu "
            "and Andhra Pradesh — is estimated at several hundred thousand. "
            "Women constitute a significant proportion of the workforce, particularly "
            "in harvesting and post-harvest processing, yet face compounded "
            "disadvantages in pay, health, and social recognition.",
            styles),

        sub_header("4.1  Working Conditions", styles),
        body(
            "Salt workers endure some of the harshest occupational conditions in India. "
            "Key challenges include:",
            styles),
        *[bullet(b, styles) for b in [
            "<b>Extreme heat:</b> Temperatures on salt pan surfaces routinely reach 45–50°C; "
            "reflective white salt amplifies UV radiation exposure.",
            "<b>Saline immersion:</b> Workers wade through hypersaline brine for hours, "
            "causing rapid skin degradation, particularly on feet and lower limbs.",
            "<b>Seasonal precarity:</b> Coastal operations run October–May; during the "
            "monsoon, income ceases entirely, pushing workers into debt or migration.",
            "<b>Lack of PPE:</b> Most workers lack rubber boots, gloves, and UV-protective "
            "eyewear; injuries from salt crystals are common.",
            "<b>Absence of amenities:</b> Potable water, sanitation facilities, rest sheds, "
            "and childcare are absent at the majority of pan sites.",
            "<b>Child labour and migration:</b> Agariya families relocate to the LRK for "
            "months, often with children, who miss schooling.",
        ]],
        sp(4),

        sub_header("4.2  Health Impact Assessment", styles),
        sp(4),
        health_table(styles),
        Paragraph(
            "Table 3: Occupational health concerns among salt pan workers. "
            "Sources: NIH studies; IJFMR; Human Rights Research (2024); JMRA (2025).",
            styles["caption"]),
        sp(6),

        sub_header("4.3  Government and NGO Welfare Initiatives", styles),
        body(
            "Several initiatives have been launched in recent years to address "
            "these deficiencies, though implementation gaps remain significant:",
            styles),
        sub_sub_header("4.3.1  Tamil Nadu Salt Pan Workers Welfare Board (2023)", styles),
        body(
            "In <b>July 2023</b>, the Government of Tamil Nadu established a "
            "<b>Welfare Board for Salt Pan Workers</b> under the Tamil Nadu Manual Workers "
            "Act, 1982. The board is mandated to provide: financial relief during the "
            "monsoon off-season; health insurance; housing assistance; and educational "
            "scholarships for workers' children. As of mid-2026, workers' associations "
            "report that benefit delivery remains slow and coverage gaps persist "
            "(The Hindu, Tamil Vahini, 2026).",
            styles),
        sub_sub_header("4.3.2  Gujarat Salt Empowered Committee", styles),
        body(
            "The Gujarat government's <b>Salt Empowered Committee</b> has deployed "
            "health vans offering laboratory services and maternity testing at LRK pan "
            "sites. In partnership with <b>SEWA (Self Employed Women's Association)</b>, "
            "the scheme has promoted the adoption of solar-powered brine pumps, "
            "reducing physical labour and diesel expenditure for Agariya households. "
            "HSL (Hindustan Salts Ltd) operates a hospital in Kharaghoda, documented "
            "in Wikipedia as part of its community footprint.",
            styles),
        sub_sub_header("4.3.3  Proposed National Salt Workers Welfare Bill", styles),
        body(
            "A <b>Salt Workers Welfare Bill</b> has been introduced in Parliament in "
            "2014, 2023, and 2024. The proposed legislation would establish a "
            "<b>National Commission for the Welfare of Salt Workers</b> with powers to: "
            "register all workers nationally; set minimum wages; mandate PPE use; "
            "and ensure regular health check-ups. As of September 2026, the bill "
            "has not been enacted, and advocates continue to press for its passage "
            "(GeoJuris Today, 2024).",
            styles),
        sub_sub_header("4.3.4  Agariya Land Rights (LRK)", styles),
        body(
            "Agariya families work within the <b>Indian Wild Ass Sanctuary</b> (declared "
            "1971/1973; 4,953.71 km²), creating a persistent tension between "
            "conservation law and livelihood. A formal land-rights decision on "
            "Agariya tenure within the sanctuary was, as of 2025, still pending "
            "(Berkeley Journal of Sociology, 2025). Advocacy groups argue that "
            "recognising customary tenure rights would improve both social security "
            "and ecological stewardship.",
            styles),

        sub_header("4.4  Remaining Gaps and Priority Actions", styles),
        *[bullet(b, styles) for b in [
            "Enact and fund the national Salt Workers Welfare Bill.",
            "Extend the Employees' State Insurance (ESI) and Provident Fund (PF) "
            "schemes to cover informal and migrant salt workers.",
            "Mandate provision of potable water, rest sheds, and sanitation at all pan sites.",
            "Subsidise distribution of PPE (boots, gloves, UV goggles) through SCO.",
            "Scale up mobile health units to Andhra Pradesh, Tamil Nadu, and Maharashtra "
            "coastal belts.",
            "Formalise Agariya land tenure in the LRK through a community rights "
            "notification under the Forest Rights Act.",
        ]],
    ]

    # ══════════════════════════════════════════════════════
    # 5. QUALITY IMPROVEMENT
    # ══════════════════════════════════════════════════════
    story += [
        PageBreak(),
        section_header("Quality Improvement and Technological Modernisation", styles, "5"),
        sp(4),
        body(
            "The quality of Indian salt is measured along several axes: purity (NaCl "
            "content), moisture content, granule size, colour, and iodine content for "
            "edible grades. The industry's primary quality challenge is reducing "
            "impurities — particularly sulphates, calcium, and magnesium salts — "
            "while simultaneously improving production efficiency in the face of "
            "climate variability.",
            styles),

        sub_header("5.1  Traditional vs. Modern Production Methods", styles),
        body(
            "Traditional coastal solar evaporation involves pumping seawater through a "
            "series of concentrator beds (from ~3–4°Baumé to ~25°Baumé) before "
            "crystallisation occurs. In the LRK, sub-soil brine is pumped from the "
            "ground and spread across shallow hardened-earth pans, which are raked "
            "daily and harvested after approximately <b>six months</b> starting in October. "
            "These methods produce acceptable quality salt but are vulnerable to "
            "contamination from bed material, biological growth, and weather events.",
            styles),

        sub_header("5.2  Technology and Best Practices", styles),
        sp(4),
        tech_table(styles),
        Paragraph(
            "Table 4: Key technologies for quality improvement in Indian salt production. "
            "Sources: CSIR-CSMCRI; SEWA; SCO; FSSAI; Mongabay India (2024).",
            styles["caption"]),
        sp(6),

        sub_header("5.3  Universal Salt Iodisation (USI)", styles),
        body(
            "India's USI programme — one of the world's largest — mandates that all "
            "edible salt be iodised at <b>15 ppm at the consumer level</b> "
            "(FSSAI IS 7224:2018). Iodisation is performed at the production or "
            "processing stage using the <b>spray method</b>, in which a potassium iodate "
            "solution is uniformly applied to salt during packaging. Quality control "
            "involves:",
            styles),
        *[bullet(b, styles) for b in [
            "Regular sampling by the <b>Salt Commissioner's Office</b> at production sites.",
            "Distribution of <b>Salt Testing Kits (STKs)</b> to state health directorates "
            "for community-level monitoring.",
            "Mandatory labelling of iodine content on all packaged edible salt.",
            "Prosecution of producers failing FSSAI standards under the Food Safety Act.",
        ]],
        body(
            "Despite these measures, studies in remote tribal and coastal communities "
            "continue to document sub-optimal iodine intake, partly due to iodine loss "
            "in storage (inadequate packaging) and cooking practices.",
            styles),

        sub_header("5.4  Climate Impacts on Quality and Yield", styles),
        body(
            "Climate change poses a dual threat: erratic monsoon onset/withdrawal "
            "shortens the production window, while cyclone frequency has increased. "
            "Manufacturers in Bhavnagar report <b>25% production losses</b> in years with "
            "two cyclone events (Mongabay, 2024). Extended rains also lead to "
            "dilution of brine in concentrators, forcing producers to restart the "
            "evaporation cycle and reducing annual yield. Adaptation strategies include:",
            styles),
        *[bullet(b, styles) for b in [
            "Use of <b>geo-membrane liners</b> in concentrator ponds to prevent "
            "dilution and seepage.",
            "<b>Weather-based insurance</b> pilots for salt workers (proposed by SCO).",
            "Early-warning integration with the <b>India Meteorological Department</b> "
            "for pan management decisions.",
        ]],

        sub_header("5.5  Proposed National Institute for Salt Technology", styles),
        body(
            "The Marine Salt Manufacturers Association and several state associations "
            "have advocated for a dedicated <b>National Institute for Salt Technology</b>. "
            "The proposed institute would conduct applied R&D on evaporation science, "
            "crystallisation chemistry, and materials science for pan construction; "
            "provide skill development and certification for salt workers; and "
            "benchmark Indian salt quality against global standards for export "
            "competitiveness. No such institution exists as of 2026.",
            styles),
    ]

    # ══════════════════════════════════════════════════════
    # 6. ECOLOGICAL SIGNIFICANCE
    # ══════════════════════════════════════════════════════
    story += [
        PageBreak(),
        section_header("Ecological Significance", styles, "6"),
        sp(4),
        body(
            "Salt pans — though largely human-made — function as critical wetland "
            "ecosystems in the Ramsar Convention framework (Ramsar 1971; India's "
            "Wetlands Rules 2017). Their shallow, hypersaline waters and exposed mudflats "
            "provide irreplaceable habitat for migratory and resident waterbirds along "
            "the <b>Central Asian Flyway</b>.",
            styles),

        sub_header("6.1  Bird Habitat and Migratory Importance", styles),
        body(
            "Salt pans are feeding and roosting sites for numerous species, most notably "
            "<b>Greater Flamingo</b> (<i>Phoenicopterus roseus</i>) and "
            "<b>Lesser Flamingo</b> (<i>Phoeniconaias minor</i>). "
            "Key documented observations include:",
            styles),
        *[bullet(b, styles) for b in [
            "<b>Thane Creek Flamingo Sanctuary</b> (Mumbai, Ramsar Aug. 2022): BNHS "
            "recorded over <b>130,000 flamingos</b> in 2022; the salt pans of adjacent "
            "eastern suburbs form essential foraging areas.",
            "<b>Great Rann of Kutch / LRK</b>: breeding ground for Greater Flamingo; "
            "seasonal water bodies and salt flats support Indian Wild Ass and thousands "
            "of waders.",
            "<b>Sambhar Lake</b> (Ramsar #464): wintering and staging ground for "
            "flamingos, migratory ducks, and waders; a 2019 avian botulism event "
            "killed thousands of birds, underscoring the lake's ecological fragility.",
            "<b>Vedaranyam / Point Calimere</b> (Ramsar #1210): ~257 bird species "
            "recorded; up to <b>30,000 flamingos</b> during peak season; Spoonbill "
            "Sandpiper and Grey Pelican documented.",
            "<b>Tata Chemicals Mithapur</b>: biodiversity programme documents over "
            "<b>150 bird species</b> within the industrial salt works estate.",
        ]],
        body(
            "Salt pans also support diverse invertebrate communities — brine shrimp "
            "(<i>Artemia</i>), halophytic algae, and nematodes — which form the base of "
            "the food web sustaining large bird aggregations.",
            styles),

        sub_header("6.2  Ramsar and Protected Area Status", styles),
        body(
            "Of the 43 sites in the Lavana Dataset v1, <b>2 are confirmed Ramsar sites</b> "
            "(Sambhar Lake #464; Point Calimere #1210) and <b>3 are within designated "
            "Protected Areas</b> (Indian Wild Ass Sanctuary; Kutch Desert Wildlife "
            "Sanctuary; Point Calimere Wildlife and Bird Sanctuary). Many more sites "
            "overlap with Important Bird Areas (IBAs) and Key Biodiversity Areas (KBAs), "
            "though formal designation has not been extended to most.",
            styles),

        sub_header("6.3  Urban Salt Pans as Flood Buffers", styles),
        body(
            "The salt pans of Mumbai's eastern suburbs provide an often-overlooked "
            "hydrological service: <b>absorption of monsoon floodwater</b>. During the "
            "2005 Mumbai floods, intact salt pan areas demonstrably reduced inundation "
            "in adjacent neighbourhoods (The Federal; Question of Cities, 2026). "
            "The redevelopment of 256 acres of Kanjurmarg/Bhandup/Wadala/Mulund salt "
            "pans for the Dharavi rehabilitation project (approved by the Centre in 2024) "
            "has raised significant concern among urban ecologists and flood-risk analysts.",
            styles),

        sub_header("6.4  Conservation Challenges", styles),
        *[bullet(b, styles) for b in [
            "<b>Urban encroachment:</b> Development pressure on periurban pans (Mumbai, "
            "Chennai, Thoothukudi) reduces habitat extent.",
            "<b>Unregulated borewell extraction:</b> At Sambhar Lake, private producers "
            "illegally pump sub-soil brine, reducing lake water levels and altering "
            "salinity gradients critical for flamingo feeding.",
            "<b>Pollution:</b> Pesticide runoff from adjacent agriculture and shrimp "
            "farms degrades water quality at Point Calimere and Chilika-adjacent pans.",
            "<b>Sand mining:</b> Illegal sand extraction from salt lands in Chinnaganjam "
            "(AP) destroys pan infrastructure and nesting habitat.",
            "<b>Avian disease:</b> The 2019 Sambhar botulism event demonstrated that "
            "dense bird aggregations at saline lakes can experience catastrophic "
            "mortality from naturally occurring or pollution-induced pathogens.",
        ]],
    ]

    # ══════════════════════════════════════════════════════
    # 7. REGULATORY AND LEGAL FRAMEWORK
    # ══════════════════════════════════════════════════════
    story += [
        PageBreak(),
        section_header("Regulatory and Legal Framework", styles, "7"),
        sp(4),
        body(
            "The governance of salt pans involves a complex, overlapping array of "
            "central and state authorities, environmental regulations, and land laws.",
            styles),
        *[bullet(b, styles) for b in [
            "<b>Salt Commissioner's Organisation (SCO):</b> Central authority (under DPIIT) "
            "responsible for production regulation, quality control, iodisation "
            "oversight, land leasing, and welfare schemes.",
            "<b>Coastal Regulation Zone (CRZ) Rules:</b> Salt pans in coastal areas are "
            "classified as CRZ-I(B), permitting only salt extraction and natural gas "
            "exploration — effectively protecting them from most development.",
            "<b>Indian Wild Ass Sanctuary Act / Wildlife Protection Act 1972:</b> "
            "Governs the LRK, creating land-use restrictions that conflict with Agariya "
            "livelihoods.",
            "<b>Ramsar Convention:</b> While India has designated 82 Ramsar sites (as of "
            "2024), salt pans with significant bird populations but without formal "
            "Ramsar designation lack equivalent international conservation status.",
            "<b>FSSAI Food Safety Standards:</b> Mandates iodine content in edible "
            "salt and regulates packaging and labelling.",
            "<b>Forest Rights Act 2006:</b> Potentially applicable to Agariya customary "
            "rights within the sanctuary, though formal recognition proceedings have "
            "not been completed.",
        ]],

        sub_header("7.1  Land Tenure and Conflict", styles),
        body(
            "Salt pan land — particularly in major urban areas — is a focal point of "
            "conflict between productive use, conservation, and development. In Mumbai, "
            "the SCO owns much of the salt pan land while leasing it to salt producers. "
            "The Maharashtra Development Plan 2034 proposed opening up 1,781 acres of "
            "salt pans for urban development, while the Centre's 2024 approval of "
            "256-acre transfer to Maharashtra for Dharavi rehabilitation has renewed "
            "legal challenges from conservationists. In Andhra Pradesh, the 2000 "
            "Chinnaganjam police firing — in which two protesters died opposing a "
            "proposed 560-acre salt factory — illustrates the depth of community "
            "resistance to changes in salt land governance.",
            styles),
    ]

    # ══════════════════════════════════════════════════════
    # 8. BEST PRACTICES & RECOMMENDATIONS
    # ══════════════════════════════════════════════════════
    story += [
        PageBreak(),
        section_header("Best Practices and Policy Recommendations", styles, "8"),
        sp(4),

        sub_header("8.1  Production and Quality", styles),
        *[bullet(b, styles) for b in [
            "Mainstream <b>geo-membrane liner technology</b> in crystallisation ponds "
            "through SCO-subsidised loans to small and medium salt manufacturers.",
            "Establish <b>Model Salt Farms</b> in every salt-producing state to "
            "demonstrate integrated best practices in evaporation, harvesting, "
            "and iodisation.",
            "Create a <b>National Institute for Salt Technology</b> to coordinate R&D, "
            "skill development, and quality benchmarking.",
            "Integrate real-time <b>IMD weather alerts</b> with pan management "
            "protocols to minimise monsoon and cyclone losses.",
            "Expand <b>solar PV brine pump</b> subsidies to cover all states, "
            "not only SEWA-partnered areas in Gujarat.",
        ]],

        sub_header("8.2  Worker Welfare", styles),
        *[bullet(b, styles) for b in [
            "Urgently enact the <b>Salt Workers Welfare Bill</b> to create a national "
            "framework for registration, minimum wages, and social security.",
            "Extend <b>ESI and EPFO</b> coverage to all salt workers, including "
            "seasonal migrants, through simplified registration.",
            "Mandate <b>PPE provision</b> by pan operators as a licensing condition; "
            "SCO to supply subsidised kit.",
            "Require all salt works to provide <b>potable water, sanitation, "
            "rest sheds, and crèche facilities</b>.",
            "Scale mobile <b>health van services</b> to all major salt-producing districts.",
            "Formalise <b>Agariya land tenure</b> under Forest Rights Act provisions.",
        ]],

        sub_header("8.3  Ecological Conservation", styles),
        *[bullet(b, styles) for b in [
            "Designate ecologically significant salt pans as <b>Key Biodiversity "
            "Areas</b> and update municipal/state development plans to protect them.",
            "Establish <b>buffer zones</b> around Ramsar-designated saline lakes "
            "to restrict unregulated brine extraction.",
            "Implement a <b>Sambhar Lake Restoration Plan</b> addressing borewell "
            "abstraction, brine-level management, and avian disease surveillance.",
            "Adopt a <b>'Working Wetlands' framework</b> that formalises the dual "
            "productive-ecological role of human-made salt pans in national "
            "biodiversity accounting.",
            "Retain Mumbai salt pan CRZ-I(B) status and resist development "
            "encroachment given flood-buffer and flamingo habitat values.",
        ]],
    ]

    # ══════════════════════════════════════════════════════
    # 9. CONCLUSION
    # ══════════════════════════════════════════════════════
    story += [
        PageBreak(),
        section_header("Conclusion", styles, "9"),
        sp(4),
        body(
            "India's salt pan landscape is a palimpsest of history, ecology, and "
            "human endeavour. From the ancient sub-soil brine fields of the Little "
            "Rann of Kutch to the gleaming coastal pans of Thoothukudi, from "
            "Sambhar's flamingo-filled shallows to Mumbai's threatened urban wetlands, "
            "salt pans are far more than industrial sites — they are living heritage "
            "landscapes that sustain livelihoods, support migratory biodiversity, and "
            "buffer coastal communities against floods.",
            styles),
        body(
            "The sector faces a convergence of stressors: climate volatility, "
            "development pressure, persistent worker welfare deficits, and the "
            "absence of a coherent national legislative framework for the informal "
            "workforce. The good news is that solutions are well-understood. Geo-membrane "
            "technology, solar pumps, automated iodisation, and mobile health services "
            "have been piloted successfully. The Tamil Nadu Welfare Board, SEWA's Gujarat "
            "programmes, and SCO's Model Salt Farm initiative demonstrate what "
            "coordinated action can achieve.",
            styles),
        body(
            "What is needed is scale, political will, and institutional architecture: "
            "a national Salt Workers Welfare Act, a dedicated technology institute, "
            "and a formal 'Working Wetlands' policy that recognises the ecological "
            "services salt pans provide. India's third-place ranking in global salt "
            "production should be matched by first-place commitment to the human "
            "dignity of those who produce it and the ecological systems it sustains.",
            styles),
        sp(10),
        rule(CONTENT_W, ACCENT, 1.5),
        sp(8),
        body(
            "<b>Acknowledgements</b>",
            styles),
        body(
            "The authors gratefully acknowledge the open data resources of the "
            "Salt Commissioner's Organisation (SCO/DPIIT), the Indian Bureau of Mines "
            "(IBM), the Ramsar Sites Information Service (RSIS), the People's Archive "
            "of Rural India (PARI), Mongabay India, The Hindu, the Berkeley Journal of "
            "Sociology, and the Bombay Natural History Society (BNHS). "
            "Special thanks to the Agariya communities of the Little Rann of Kutch "
            "and the salt workers of Tamil Nadu and Andhra Pradesh whose labour and "
            "knowledge underpin this industry.",
            styles),
    ]

    # ══════════════════════════════════════════════════════
    # REFERENCES
    # ══════════════════════════════════════════════════════
    story += [
        PageBreak(),
        section_header("References", styles, ""),
        sp(6),
    ]

    refs = [
        ("IBM", "Indian Bureau of Mines (2022). <i>Indian Minerals Yearbook 2022 — Salt</i>. "
         "IBM, Government of India. https://ibm.gov.in/"),
        ("SCO", "Salt Commissioner's Organisation (2024). <i>Salient Features of Indian "
         "Salt Industry</i>. DPIIT, Ministry of Commerce and Industry. "
         "https://saltcomindia.gov.in/"),
        ("JMRA", "Chaudhary, P. et al. (2025). Performance evaluation of the salt industry "
         "in India with special reference to Gujarat. <i>Journal of Management Research "
         "and Analysis</i>, 11(4). https://jmra.in/archive/volume/11/issue/4/article/16057"),
        ("BJS", "Berkeley Journal of Sociology (2025). Salt 'Farming': Gendered Labour "
         "and Ecologies of migrant workers in Little Rann of Kutch. "
         "https://berkeleyjournal.org/2025/06/11/salt-farming/"),
        ("PARI", "People's Archive of Rural India (PARI). The Rani of Thoothukudi's salt pans. "
         "https://ruralindiaonline.org/article/the-rani-of-thoothukudis-salt-pans"),
        ("Mongabay", "Mongabay India (2024, March). Uncertain weather makes that pinch of salt "
         "dearer. https://india.mongabay.com/2024/03/uncertain-weather-makes-that-pinch-of-salt-dearer/"),
        ("Ramsar464", "Ramsar Sites Information Service (RSIS). Sambhar Lake — Ramsar site "
         "no. 464 (designated 23 March 1990). https://rsis.ramsar.org/ris/464"),
        ("Ramsar1210", "Ramsar Sites Information Service (RSIS). Point Calimere Wildlife and "
         "Bird Sanctuary — Ramsar site no. 1210 (designated 19 August 2002). "
         "https://rsis.ramsar.org/ris/1210"),
        ("EnvSociety", "Environment & Society Portal (2026). Between Salt and Water: The "
         "Environmental Crisis at Sambhar Lake, Rajasthan, India. "
         "https://www.environmentandsociety.org/arcadia/between-salt-and-water-environmental-"
         "crisis-sambhar-lake-rajasthan-india"),
        ("HansIndia", "The Hans India (2022, April). Sand mafia digging deep into salt lands at "
         "Chinaganjam. https://www.thehansindia.com/andhra-pradesh/sand-mafia-digging-deep-"
         "into-salt-lands-at-chinaganjam-736019"),
        ("Tata", "Tata Group / Tata Chemicals Ltd (n.d.). Chemicals With A Capital Sea. "
         "https://www.tata.com/newsroom/tata-chemicals-with-a-capital-sea"),
        ("Sahapedia", "Sahapedia (n.d.). In Search of White Gold: Salt Harvesting at "
         "Marakkanam. https://www.sahapedia.org/search-white-gold-salt-harvesting-marakkanam"),
        ("GeoJuris", "GeoJuris Today (2024). Salt Workers Welfare Bill — Legislative Status "
         "and Analysis. https://geojuristoday.in/"),
        ("NRSC", "NRSC/ISRO (n.d.). Salt Pan Atlas of India (Cartosat-2/3). "
         "https://www.nrsc.gov.in/nrscnew/resources_atlas_SaltPan.php"),
        ("CAT", "Conservation Action Trust (n.d.). How much of Mumbai's salt pans can be "
         "developed? https://cat.org.in/"),
        ("BNHS", "Bombay Natural History Society (BNHS) (2022). Flamingo Count Report, "
         "Thane Creek. BNHS, Mumbai."),
        ("LavanaGIS", "Gupta, A. & Srinivas, S. (2026). <i>Lavana GIS Dataset v1: Indian "
         "Salt Pan Geodatabase</i>. Lavana Project Research Initiative. "
         "https://github.com/ArnavGupta-codes/Lavana-Project-"),
        ("SEWA", "Self Employed Women's Association (SEWA) (2024). Solar Pump Initiative "
         "for Gujarat Salt Workers. https://www.sewa.org/"),
        ("FSSAI", "Food Safety and Standards Authority of India (FSSAI). IS 7224:2018 — "
         "Iodised Salt Specification. Government of India."),
        ("CSIR", "CSIR-CSMCRI (Central Salt and Marine Chemicals Research Institute). "
         "R&D on Geo-Membrane Liners and Solar-Assisted Evaporation. Bhavnagar, Gujarat."),
    ]

    ref_style = ParagraphStyle(
        "ref", parent=build_styles()["body"],
        fontSize=8.8, leftIndent=1.2*cm, firstLineIndent=-1.2*cm,
        spaceAfter=5, leading=13)

    for key, text in refs:
        story.append(Paragraph(f"[{key}] {text}", ref_style))

    # Build
    doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
    print(f"✅  PDF written to: {os.path.abspath(OUTPUT_PATH)}")


if __name__ == "__main__":
    build_pdf()
