import os
from fpdf import FPDF
from datetime import datetime


def clean(text: str) -> str:
    return (text
        .replace("\u2014", "-")
        .replace("\u2013", "-")
        .replace("\u2264", "<=")
        .replace("\u2265", ">=")
        .replace("\u00b2", "2")
        .replace("\u00b0", " deg")
    )


class NoteStackReport(FPDF):
    def header(self):
        self.set_font("Helvetica", "B", 14)
        self.set_text_color(26, 18, 8)
        self.cell(0, 10, "NoteStack", ln=False)
        self.set_font("Helvetica", "", 9)
        self.set_text_color(139, 107, 72)
        self.cell(0, 10, "Reverse Sensory Formulation Engine", ln=True, align="R")
        self.set_draw_color(221, 213, 191)
        self.line(10, 20, 200, 20)
        self.ln(4)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "", 8)
        self.set_text_color(155, 139, 114)
        self.cell(0, 10, "Built by Drashti Patel  |  B.Tech Food Processing Technology  |  ADIT, CVMU", align="C")


def generate_pdf(category: str, formulation: dict, predicted_scores: dict,
                 target_scores: dict, confidence_pct: float,
                 residual_error: float, compliance: dict) -> bytes:

    pdf = NoteStackReport()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Title block
    pdf.set_font("Helvetica", "B", 18)
    pdf.set_text_color(26, 18, 8)
    pdf.cell(0, 10, "Formulation Report", ln=True)
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(107, 92, 72)
    pdf.cell(0, 6, f"Category: {category.capitalize()}   |   Generated: {datetime.now().strftime('%d %b %Y, %H:%M')}", ln=True)
    pdf.ln(6)

    # Confidence banner
    if confidence_pct >= 85:
        r, g, b = 58, 107, 42
        br, bg, bb = 238, 245, 235
    elif confidence_pct >= 65:
        r, g, b = 122, 92, 16
        br, bg, bb = 253, 244, 220
    else:
        r, g, b = 122, 32, 32
        br, bg, bb = 253, 240, 240

    pdf.set_fill_color(br, bg, bb)
    pdf.set_draw_color(br, bg, bb)
    pdf.rect(10, pdf.get_y(), 190, 12, "F")
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(r, g, b)
    msg = "High confidence" if confidence_pct >= 85 else "Moderate confidence" if confidence_pct >= 65 else "Low confidence"
    pdf.cell(0, 12, f"  Confidence: {confidence_pct}%   |   {msg}   |   Residual error: {residual_error}", ln=True)
    pdf.ln(6)

    def section_title(title):
        pdf.set_font("Helvetica", "B", 9)
        pdf.set_text_color(139, 107, 72)
        pdf.set_draw_color(221, 213, 191)
        pdf.cell(0, 6, clean(title.upper()), ln=True)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(3)

    # Ingredient ratios
    section_title("Ingredient ratios")
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_text_color(155, 139, 114)
    pdf.cell(120, 7, "INGREDIENT", border=0)
    pdf.cell(60, 7, "AMOUNT", align="R", ln=True)
    pdf.set_draw_color(240, 232, 208)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())

    for i, (k, v) in enumerate(formulation.items()):
        label = k.replace("_pct", " %").replace("_", " ").title()
        if i % 2 == 0:
            pdf.set_fill_color(250, 248, 243)
            pdf.rect(10, pdf.get_y(), 190, 7, "F")
        pdf.set_font("Helvetica", "", 10)
        pdf.set_text_color(61, 51, 38)
        pdf.cell(120, 7, f"  {clean(label)}")
        pdf.set_font("Helvetica", "B", 10)
        pdf.set_text_color(139, 69, 19)
        pdf.cell(60, 7, f"{v}%", align="R", ln=True)

    pdf.ln(6)

    # Sensory scores
    section_title("Sensory profile - target vs predicted")
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_text_color(155, 139, 114)
    pdf.cell(90, 7, "ATTRIBUTE")
    pdf.cell(50, 7, "TARGET", align="C")
    pdf.cell(50, 7, "PREDICTED", align="R", ln=True)
    pdf.set_draw_color(240, 232, 208)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())

    for i, (k, v) in enumerate(predicted_scores.items()):
        targ = target_scores.get(k, "-")
        label = k.replace("_", " ").title()
        if i % 2 == 0:
            pdf.set_fill_color(250, 248, 243)
            pdf.rect(10, pdf.get_y(), 190, 7, "F")
        pdf.set_font("Helvetica", "", 10)
        pdf.set_text_color(61, 51, 38)
        pdf.cell(90, 7, f"  {clean(label)}")
        pdf.set_text_color(107, 92, 72)
        pdf.cell(50, 7, str(targ), align="C")
        pdf.set_font("Helvetica", "B", 10)
        pdf.set_text_color(26, 18, 8)
        pdf.cell(50, 7, str(v), align="R", ln=True)

    pdf.ln(6)

    # FSSAI compliance
    section_title("FSSAI compliance")
    status = compliance.get("status", "UNKNOWN")
    if status == "COMPLIANT":
        sc_r, sc_g, sc_b = 58, 107, 42
    elif status == "ADVISORY":
        sc_r, sc_g, sc_b = 122, 92, 16
    else:
        sc_r, sc_g, sc_b = 122, 32, 32

    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(sc_r, sc_g, sc_b)
    pdf.cell(0, 7, f"Status: {status}", ln=True)
    pdf.ln(2)

    def compliance_items(items, dot_r, dot_g, dot_b):
        for item in items:
            pdf.set_fill_color(dot_r, dot_g, dot_b)
            x, y = pdf.get_x(), pdf.get_y()
            pdf.ellipse(x + 2, y + 3.5, 2.5, 2.5, "F")
            pdf.set_x(x + 7)
            pdf.set_font("Helvetica", "", 9)
            pdf.set_text_color(61, 51, 38)
            pdf.multi_cell(183, 5, clean(item))
            pdf.ln(1)

    compliance_items(compliance.get("passed", []), 58, 107, 42)
    compliance_items(compliance.get("warnings", []), 201, 160, 48)
    compliance_items(compliance.get("flags", []), 192, 48, 48)

    return bytes(pdf.output())