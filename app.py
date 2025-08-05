# This script is intended to be run in a local environment with Streamlit installed.
# Please install dependencies using: pip install streamlit qrcode reportlab pillow

import qrcode
import uuid
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A5, landscape
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader
import streamlit as st

# Load logo path (ensure this file exists in the same directory)
logo_path = "FIESTA_HUB_LOGO.jpg"

st.set_page_config(page_title="Fiesta Hub | Ticket Generator", layout="centered")
st.title("🎟️ Colour Splash 3.0 Ticket Generator")
st.write("Enter your details below to generate your event ticket.")

with st.form("ticket_form"):
    name = st.text_input("Full Name", max_chars=40)
    mpesa_code = st.text_input("M-Pesa Code", max_chars=15)
    submitted = st.form_submit_button("Generate Ticket")

if submitted:
    if not name or not mpesa_code:
        st.warning("Please enter both your name and M-Pesa code.")
    else:
        event_date = "24 AUGUST 2025"
        venue = "Canaville Resort, Jujafarm"
        ticket_id = str(uuid.uuid4())[:8].upper()

        # Generate QR code
        qr_data = f"Ticket for {name} | ID: {ticket_id}"
        qr_img = qrcode.make(qr_data)
        qr_buffer = BytesIO()
        qr_img.save(qr_buffer)
        qr_buffer.seek(0)
        qr_reader = ImageReader(qr_buffer)

        # Create PDF
        pdf_buffer = BytesIO()
        c = canvas.Canvas(pdf_buffer, pagesize=landscape(A5))
        width, height = landscape(A5)

        c.setFillColorRGB(0.95, 0.95, 0.95)
        c.rect(0, 0, width, height, fill=True, stroke=False)

        try:
            logo = ImageReader(logo_path)
            c.drawImage(logo, 20*mm, height - 40*mm, width=40*mm, preserveAspectRatio=True, mask='auto')
        except Exception as e:
            c.setFont("Helvetica", 10)
            c.drawString(20*mm, height - 20*mm, f"[Logo missing: {e}]")

        c.setFont("Helvetica-Bold", 16)
        c.drawString(70*mm, height - 20*mm, "Fiesta Hub Presents")
        c.setFont("Helvetica-Bold", 24)
        c.drawString(70*mm, height - 30*mm, "COLOUR SPLASH 3.0")
        c.setFont("Helvetica", 14)
        c.drawString(70*mm, height - 40*mm, f"Date: {event_date}")
        c.drawString(70*mm, height - 50*mm, f"Venue: {venue}")

        c.setFont("Helvetica-Bold", 16)
        c.drawString(20*mm, 40*mm, f"Admit: {name}")
        c.setFont("Helvetica", 12)
        c.drawString(20*mm, 32*mm, f"Ticket ID: {ticket_id}")
        c.drawString(20*mm, 26*mm, f"M-Pesa Code: {mpesa_code}")

        c.drawImage(qr_reader, width - 50*mm, 20*mm, width=30*mm, preserveAspectRatio=True, mask='auto')
        c.save()

        pdf_buffer.seek(0)

        st.success("✅ Ticket generated successfully!")
        st.download_button(
            label="📥 Download Ticket (PDF)",
            data=pdf_buffer,
            file_name=f"Ticket_{name.replace(' ', '_')}.pdf",
            mime="application/pdf"
        )
