import os
import time
from datetime import datetime
from io import BytesIO

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm, inch
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer,
    HRFlowable, Frame, PageTemplate, BaseDocTemplate
)
from reportlab.graphics.shapes import Drawing, Rect, Line, String
from reportlab.graphics import renderPDF

from app.config import settings


INVOICES_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "invoices")

BRAND_DARK = colors.HexColor("#0d2137")
BRAND_BLUE = colors.HexColor("#1565c0")
BRAND_RED = colors.HexColor("#c62828")
BRAND_GOLD = colors.HexColor("#f9a825")
BRAND_LIGHT = colors.HexColor("#f0f4f8")
BRAND_GRAY = colors.HexColor("#64748b")
WHITE = colors.white


def generate_invoice_pdf(payment_id: int, member_code: str, member_name: str, member_phone: str, amount: float, payment_date) -> BytesIO:
    """Generate invoice PDF in memory and return as BytesIO buffer."""
    buffer = BytesIO()
    
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        topMargin=30 * mm,
        bottomMargin=25 * mm,
        leftMargin=25 * mm,
        rightMargin=25 * mm,
    )

    elements = _build_invoice_elements(payment_id, member_code, member_name, member_phone, amount, payment_date)
    doc.build(elements)
    
    buffer.seek(0)
    return buffer


def generate_invoice(payment_id: int, member_code: str, member_name: str, member_phone: str, amount: float, payment_date) -> str:
    """Generate invoice and save to disk (for local development). Returns URL."""
    os.makedirs(INVOICES_DIR, exist_ok=True)

    filename = f"invoice_{payment_id}_{int(time.time())}.pdf"
    filepath = os.path.join(INVOICES_DIR, filename)

    doc = SimpleDocTemplate(
        filepath,
        pagesize=A4,
        topMargin=30 * mm,
        bottomMargin=25 * mm,
        leftMargin=25 * mm,
        rightMargin=25 * mm,
    )

    elements = _build_invoice_elements(payment_id, member_code, member_name, member_phone, amount, payment_date)
    doc.build(elements)

    # Return API endpoint URL instead of static file URL
    invoice_url = f"{settings.BASE_URL}/subscriptions/{payment_id}/invoice"
    return invoice_url


def _build_invoice_elements(payment_id: int, member_code: str, member_name: str, member_phone: str, amount: float, payment_date) -> list:
    """Build the invoice PDF elements (shared between file and memory generation)."""
    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        "InvoiceTitle",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=28,
        textColor=BRAND_DARK,
        spaceAfter=0,
        alignment=TA_LEFT,
        leading=34,
    )
    subtitle_style = ParagraphStyle(
        "InvoiceSubtitle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=10,
        textColor=BRAND_GRAY,
        spaceAfter=0,
        alignment=TA_LEFT,
        letterSpacing=2,
    )
    heading_style = ParagraphStyle(
        "SectionHeading",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=11,
        textColor=BRAND_DARK,
        spaceBefore=20,
        spaceAfter=8,
        textTransform="uppercase",
    )
    label_style = ParagraphStyle(
        "Label",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9,
        textColor=BRAND_GRAY,
    )
    value_style = ParagraphStyle(
        "Value",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=10,
        textColor=BRAND_DARK,
    )
    amount_style = ParagraphStyle(
        "Amount",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=22,
        textColor=BRAND_BLUE,
        alignment=TA_RIGHT,
    )
    footer_style = ParagraphStyle(
        "Footer",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8,
        textColor=BRAND_GRAY,
        alignment=TA_CENTER,
    )

    elements = []

    # === HEADER SECTION ===
    # Brand bar
    header_data = [
        [
            Paragraph("MARVEL FITNESS", ParagraphStyle(
                "BrandName", parent=styles["Normal"],
                fontName="Helvetica-Bold", fontSize=20, textColor=BRAND_DARK,
            )),
            Paragraph("INVOICE", ParagraphStyle(
                "InvoiceTag", parent=styles["Normal"],
                fontName="Helvetica-Bold", fontSize=14, textColor=BRAND_BLUE,
                alignment=TA_RIGHT,
            )),
        ],
        [
            Paragraph("Gym Management System", ParagraphStyle(
                "BrandSub", parent=styles["Normal"],
                fontName="Helvetica", fontSize=8, textColor=BRAND_GRAY,
            )),
            Paragraph(f"#{payment_id:05d}", ParagraphStyle(
                "InvoiceNum", parent=styles["Normal"],
                fontName="Helvetica-Bold", fontSize=10, textColor=BRAND_GRAY,
                alignment=TA_RIGHT,
            )),
        ],
    ]
    header_table = Table(header_data, colWidths=[300, 160])
    header_table.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
    ]))
    elements.append(header_table)
    elements.append(Spacer(1, 4))

    # Red accent line
    elements.append(HRFlowable(
        width="100%", thickness=3, color=BRAND_RED,
        spaceBefore=4, spaceAfter=20,
    ))

    # === INVOICE META ===
    meta_data = [
        [
            Paragraph("Date Issued", label_style),
            Paragraph("Payment Date", label_style),
            Paragraph("Status", label_style),
        ],
        [
            Paragraph(datetime.utcnow().strftime("%d %b %Y"), value_style),
            Paragraph(payment_date.strftime("%d %b %Y"), value_style),
            Paragraph("PAID", ParagraphStyle(
                "Paid", parent=styles["Normal"],
                fontName="Helvetica-Bold", fontSize=10, textColor=colors.HexColor("#2e7d32"),
            )),
        ],
    ]
    meta_table = Table(meta_data, colWidths=[153, 153, 154])
    meta_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), BRAND_LIGHT),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("LEFTPADDING", (0, 0), (-1, -1), 12),
        ("ROUNDEDCORNERS", [6, 6, 6, 6]),
    ]))
    elements.append(meta_table)
    elements.append(Spacer(1, 20))

    # === MEMBER DETAILS ===
    elements.append(Paragraph("BILLED TO", heading_style))

    member_data = [
        [
            Paragraph("Member ID", label_style),
            Paragraph(member_code, value_style),
        ],
        [
            Paragraph("Name", label_style),
            Paragraph(member_name, value_style),
        ],
        [
            Paragraph("Phone", label_style),
            Paragraph(member_phone, value_style),
        ],
    ]
    member_table = Table(member_data, colWidths=[120, 340])
    member_table.setStyle(TableStyle([
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LINEBELOW", (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
    ]))
    elements.append(member_table)
    elements.append(Spacer(1, 20))

    # === PAYMENT BREAKDOWN ===
    elements.append(Paragraph("PAYMENT DETAILS", heading_style))

    payment_data = [
        [
            Paragraph("Description", ParagraphStyle(
                "TH", parent=styles["Normal"],
                fontName="Helvetica-Bold", fontSize=9, textColor=WHITE,
            )),
            Paragraph("Amount", ParagraphStyle(
                "THR", parent=styles["Normal"],
                fontName="Helvetica-Bold", fontSize=9, textColor=WHITE,
                alignment=TA_RIGHT,
            )),
        ],
        [
            Paragraph("Gym Membership Payment", ParagraphStyle(
                "TD", parent=styles["Normal"],
                fontName="Helvetica", fontSize=10, textColor=BRAND_DARK,
            )),
            Paragraph(f"Rs. {amount:,.2f}", ParagraphStyle(
                "TDR", parent=styles["Normal"],
                fontName="Helvetica", fontSize=10, textColor=BRAND_DARK,
                alignment=TA_RIGHT,
            )),
        ],
    ]
    payment_table = Table(payment_data, colWidths=[340, 120])
    payment_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), BRAND_DARK),
        ("TOPPADDING", (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
        ("LEFTPADDING", (0, 0), (-1, -1), 12),
        ("RIGHTPADDING", (0, 0), (-1, -1), 12),
        ("LINEBELOW", (0, 1), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
    ]))
    elements.append(payment_table)
    elements.append(Spacer(1, 4))

    # Total row
    total_data = [
        [
            Paragraph("TOTAL", ParagraphStyle(
                "TotalLabel", parent=styles["Normal"],
                fontName="Helvetica-Bold", fontSize=12, textColor=BRAND_DARK,
            )),
            Paragraph(f"Rs. {amount:,.2f}", ParagraphStyle(
                "TotalValue", parent=styles["Normal"],
                fontName="Helvetica-Bold", fontSize=16, textColor=BRAND_BLUE,
                alignment=TA_RIGHT,
            )),
        ],
    ]
    total_table = Table(total_data, colWidths=[340, 120])
    total_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), BRAND_LIGHT),
        ("TOPPADDING", (0, 0), (-1, -1), 12),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
        ("LEFTPADDING", (0, 0), (-1, -1), 12),
        ("RIGHTPADDING", (0, 0), (-1, -1), 12),
    ]))
    elements.append(total_table)
    elements.append(Spacer(1, 30))

    # === FOOTER ===
    elements.append(HRFlowable(
        width="100%", thickness=0.5, color=colors.HexColor("#e2e8f0"),
        spaceBefore=0, spaceAfter=12,
    ))
    elements.append(Paragraph(
        "Thank you for being a part of Marvel Fitness!",
        ParagraphStyle("ThankYou", parent=styles["Normal"],
                       fontName="Helvetica-Bold", fontSize=11,
                       textColor=BRAND_DARK, alignment=TA_CENTER, spaceAfter=6),
    ))
    elements.append(Paragraph(
        "This is a system-generated invoice. No signature required.",
        footer_style,
    ))
    elements.append(Paragraph(
        f"Generated on {datetime.utcnow().strftime('%d %b %Y at %H:%M UTC')}",
        footer_style,
    ))

    return elements
