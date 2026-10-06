import os
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setStrokeColor(colors.HexColor('#1f2f54'))
        self.setLineWidth(0.75)
        # Top banner line on pages > 1
        if self._pageNumber > 1:
            self.line(40, 800, 555, 800)
            self.setFont("Helvetica-Bold", 8)
            self.setFillColor(colors.HexColor('#2563eb'))
            self.drawString(40, 806, "ZAGROS VITOSHA BULGARIA EOOD")
            self.setFont("Helvetica", 8)
            self.setFillColor(colors.HexColor('#64748b'))
            self.drawRightString(555, 806, "CORPORATE PROFILE & COMMODITY MATRIX")

        # Bottom footer line on all pages
        self.line(40, 42, 555, 42)
        self.setFont("Helvetica", 7.5)
        self.setFillColor(colors.HexColor('#64748b'))
        self.drawString(40, 30, "UIC/EIK: 208619412 | VAT: BG208619412 | Sofia, Republic of Bulgaria | Zvbulgaria@gmail.com")
        self.drawRightString(555, 30, f"Page {self._pageNumber} of {page_count}")
        self.restoreState()

def build_pdf(filename="zagros-vitosha-company-profile.pdf"):
    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        leftMargin=40,
        rightMargin=40,
        topMargin=48,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()
    
    # Custom Corporate Styles
    c_navy = colors.HexColor('#09152e')
    c_blue = colors.HexColor('#1e4bb5')
    c_gold = colors.HexColor('#d97706')
    c_text = colors.HexColor('#1e293b')
    c_light = colors.HexColor('#f8fafc')

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=c_navy
    )

    subtitle_style = ParagraphStyle(
        'DocSub',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=c_gold
    )

    h1_style = ParagraphStyle(
        'SectionH1',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=c_navy,
        spaceBefore=14,
        spaceAfter=6
    )

    body_style = ParagraphStyle(
        'BodyDark',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=c_text
    )

    bullet_style = ParagraphStyle(
        'BulletText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=c_text,
        leftIndent=12
    )

    story = []

    # ---------------- PAGE 1: COVER & EXECUTIVE SUMMARY ----------------
    story.append(Spacer(1, 15))
    story.append(Paragraph("ZAGROS VITOSHA BULGARIA EOOD", subtitle_style))
    story.append(Spacer(1, 4))
    story.append(Paragraph("CORPORATE PROFILE & COMMERCIAL COMMODITY SPECIFICATION", title_style))
    story.append(Spacer(1, 8))
    
    meta_table_data = [
        [
            Paragraph("<b>Legal Entity:</b> Zagros Vitosha Bulgaria EOOD", body_style),
            Paragraph("<b>Commercial Register EIK:</b> 208619412", body_style)
        ],
        [
            Paragraph("<b>Registered VAT ID:</b> BG208619412", body_style),
            Paragraph("<b>Headquarters:</b> Sofia Center, Sofia 1000, Bulgaria", body_style)
        ],
        [
            Paragraph("<b>Core Activities:</b> International Polymer & Commodity Trade", body_style),
            Paragraph("<b>Logistics Corridors:</b> Ports of Varna, Burgas, Mersin & Inland DAP", body_style)
        ]
    ]
    meta_table = Table(meta_table_data, colWidths=[255, 260])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f1f5f9')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#cbd5e1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0')),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 14))

    story.append(Paragraph("1. Executive Corporate Summary", h1_style))
    story.append(Paragraph(
        "Zagros Vitosha Bulgaria EOOD is a Bulgarian registered corporate trading and international sourcing entity headquartered in Sofia. The company operates as a reliable cross-border bridge between primary petrochemical manufacturers and industrial processors across Bulgaria, Romania, Serbia, Greece, and Turkey.",
        body_style
    ))
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "We specialize in full container load (FCL) maritime dispatches of virgin polymers (HDPE, LDPE, PP, S-PVC K67), direct paving bitumen, and industrial fasteners. With established relationships with tier-1 global maritime lines (MSC, Maersk, Arkas), we ensure secured delivery to the Ports of Varna and Burgas with guaranteed 14 to 21 free demurrage days, bonded warehousing, and inland delivery (DAP) directly to manufacturing facilities.",
        body_style
    ))
    story.append(Spacer(1, 12))

    story.append(Paragraph("2. Strategic Advantages & Commercial Capabilities", h1_style))
    capabilities = [
        "<b>Virgin Prime Quality:</b> Strictly prime grade virgin resins with certified Melt Flow Index (MFI) and density properties.",
        "<b>Origin Transparency:</b> Specific manufacturer mill and country of origin are confirmed per proforma invoice and documented on official batch COA and Certificate of Origin.",
        "<b>Multi-Modal Logistics:</b> Flexible maritime terms (CIF / CFR Port of Varna / Burgas) combined with inland trucking (DAP) across Bulgarian industrial zones and regional Balkan markets.",
        "<b>Extended Port Free Days:</b> 14 to 21 days free demurrage / detention guaranteed on shipping documents to provide seamless customs clearance.",
        "<b>Quality Verification:</b> Manufacturer Batch Certificate of Analysis (COA) provided with shipping documents; independent third-party inspection (SGS / Bureau Veritas) available upon buyer request."
    ]
    for cap in capabilities:
        story.append(Paragraph(f"• {cap}", bullet_style))
        story.append(Spacer(1, 3))

    story.append(PageBreak())

    # ---------------- PAGE 2: COMMODITY SPECIFICATION MATRIX ----------------
    story.append(Spacer(1, 10))
    story.append(Paragraph("3. Core Petrochemical & Polymer Grades", h1_style))
    story.append(Paragraph("Technical baseline parameters for export dispatches. Detailed batch COA provided upon cargo booking.", body_style))
    story.append(Spacer(1, 8))

    spec_data = [
        ["Commodity", "Typical Grades", "MFI / Property", "Standard Packaging", "Key Applications"],
        [
            "HDPE Resin\n(High Density)",
            "Film Grade 5110 / F7000\nPipe Grade PE100 Black\nBlow Molding 0035",
            "0.05 - 0.12 g/10min\n0.22 - 0.28 g/10min\nDensity: 0.952 - 0.960",
            "25 kg PP valve bags,\n1,375 kg shrink-wrapped\npallets (24.75 MT / 40' HC)",
            "High-strength shopping bags, pressure water/gas pipes, rigid industrial containers."
        ],
        [
            "LDPE Resin\n(Low Density)",
            "Heavy Film 2420H / 020\nGeneral Film 2102",
            "1.9 - 2.2 g/10min\nDensity: 0.923 - 0.926",
            "25 kg bags on pallets\n(24.75 MT / 40' HC)",
            "Heavy agricultural greenhouse film, shrink bundling, industrial wrapping."
        ],
        [
            "Polypropylene\n(PP Granules)",
            "Raffia V30S / T30S\nInjection Z30S / HP500N\nFiber / Yarn Grade",
            "2.8 - 3.5 g/10min (Raffia)\n12 - 25 g/10min (Injection)\nDensity: 0.900 - 0.905",
            "25 kg PP bags, palletized\nwith UV stretch hood",
            "Woven sacks, FIBC jumbo big bags, strapping bands, thin-wall food containers."
        ],
        [
            "Suspension PVC\n(S-PVC Resin)",
            "Grade K67 / SG-5\nGrade K58 / SG-7",
            "K-Value: 66 - 68\nBulk Density: >= 0.54\nVolatiles: <= 0.30%",
            "25 kg multi-layer kraft\ncomposite valve bags",
            "Rigid window and door profiles, technical conduits, pressure pipes, siding panels."
        ],
        [
            "Bitumen / Asphalt\n(Paving Grade)",
            "Penetration 60/70\nPenetration 80/100",
            "Penetration @ 25C: 60-70\nSoftening Point: 49 - 56 C\nDuctility: >= 100 cm",
            "180 kg new steel drums\nor 1,000 kg meltable bags",
            "Highway asphalt paving, waterproofing membranes, bridge mastic roofing."
        ],
        [
            "Industrial Fasteners\n(Standard Hardware)",
            "DIN 933, DIN 934, DIN 7981\nClass 4.8 / 8.8 / 10.9",
            "Zinc plated (Cr3+ RoHS)\nHot dip galvanized",
            "25 kg reinforced carton\nboxes on Euro-pallets",
            "PVC profile steel reinforcing, construction framework, industrial assembly."
        ]
    ]

    spec_table = Table(spec_data, colWidths=[80, 110, 105, 105, 115])
    spec_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_navy),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 8),
        ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
        ('FONTSIZE', (0,1), (-1,-1), 7.5),
        ('LEADING', (0,0), (-1,-1), 9.5),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#f8fafc')])
    ]))
    story.append(spec_table)

    story.append(PageBreak())

    # ---------------- PAGE 3: LOGISTICS, INCOTERMS & CONTACTS ----------------
    story.append(Spacer(1, 10))
    story.append(Paragraph("4. Maritime Corridors, Inland Trucking & Incoterms 2020", h1_style))
    story.append(Paragraph(
        "Zagros Vitosha Bulgaria EOOD manages end-to-end logistics operations from primary loading ports to final delivery points across Southeastern Europe:",
        body_style
    ))
    story.append(Spacer(1, 6))

    ports_data = [
        ["Logistics Hub", "Service Scope & Delivery Terms", "Transit / Features"],
        [
            "Port of Varna\n(Varna-West / East)",
            "Primary Bulgarian maritime discharge hub. Ocean FCL containers cleared or transshipped directly to industrial zones in Sofia, Plovdiv, Ruse, and Asenovgrad.",
            "• 14–21 Free Demurrage Days\n• Direct customs warehouse\n• Fast highway road transit"
        ],
        [
            "Port of Burgas\n(BMF Port Burgas)",
            "Deep-sea handling terminal serving central and southeastern Bulgaria and regional transit routes.",
            "• Rail and highway connections\n• Dedicated bulk container handling"
        ],
        [
            "Port of Mersin\n(Mersin Free Zone)",
            "Major Eastern Mediterranean petrochemical port. Bonded warehousing, high-frequency feeder sailings, and rapid transshipment.",
            "• Free Zone storage facilities\n• Frequent container departures"
        ],
        [
            "Inland Trucking (DAP)\nBulgaria & Balkans",
            "Door-to-door delivery with standard 24 MT tilt trailers and tautliners directly to buyer factory gates in Bulgaria, Romania (Bucharest), and Northern Greece.",
            "• Incoterms: DAP / CPT\n• Full CMR transit insurance\n• Timed delivery scheduling"
        ]
    ]

    ports_table = Table(ports_data, colWidths=[105, 270, 140])
    ports_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_blue),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 8),
        ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
        ('FONTSIZE', (0,1), (-1,-1), 8),
        ('LEADING', (0,0), (-1,-1), 10.5),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#f8fafc')])
    ]))
    story.append(ports_table)
    story.append(Spacer(1, 14))

    story.append(Paragraph("5. Commercial Terms & Direct Executive Contacts", h1_style))
    
    contacts_data = [
        [
            Paragraph("<b>Commercial Framework</b><br/>"
                      "• <b>Incoterms 2020:</b> CIF, CFR, DAP, FCA<br/>"
                      "• <b>Payment Methods:</b> Confirmed Irrevocable L/C at sight, CAD, T/T<br/>"
                      "• <b>Documentation:</b> Bill of Lading, Invoice, Packing List, Batch COA, Origin Certificate, CMR (for DAP)<br/>"
                      "• <b>Inspection:</b> SGS / BV available on request", body_style),
            Paragraph("<b>Direct Trade & Executive Desk</b><br/>"
                      "<b>Managing Director (Executive Desk):</b><br/>"
                      "• Phone / WhatsApp: +359 87 794 4353<br/><br/>"
                      "<b>Head of Commercial & Export:</b><br/>"
                      "• Phone / WhatsApp: +359 88 970 0004<br/><br/>"
                      "<b>Corporate Email:</b> Zvbulgaria@gmail.com<br/>"
                      "<b>Registered Office:</b> Sofia Center, Sofia 1000, Bulgaria", body_style)
        ]
    ]

    contact_table = Table(contacts_data, colWidths=[255, 260])
    contact_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f8fafc')),
        ('BOX', (0,0), (-1,-1), 1, c_navy),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(contact_table)

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"PDF generated successfully: {filename}")

if __name__ == "__main__":
    build_pdf()
