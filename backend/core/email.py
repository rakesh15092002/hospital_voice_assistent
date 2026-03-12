# core/email.py

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from core.config import settings


def send_appointment_email(
    to_email: str,
    patient_name: str,
    doctor_name: str,
    doctor_specialization: str,
    slot_start: str,
    slot_end: str,
    appointment_id: int,
) -> bool:
    """Send appointment confirmation email to patient"""
    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = f"Appointment Confirmed - City Hospital (ID: #{appointment_id})"
        msg["From"] = settings.EMAIL_USER
        msg["To"] = to_email

        html = f"""
        <html>
        <body style="font-family: Arial, sans-serif; max-width: 600px; margin: auto; padding: 20px;">
            <div style="background-color: #0077b6; padding: 20px; border-radius: 8px 8px 0 0;">
                <h1 style="color: white; margin: 0;">🏥 City Hospital</h1>
                <p style="color: #caf0f8; margin: 5px 0;">Appointment Confirmation</p>
            </div>
            <div style="background-color: #f8f9fa; padding: 30px; border-radius: 0 0 8px 8px;">
                <p>Dear <strong>{patient_name}</strong>,</p>
                <p>Your appointment has been successfully booked. Here are your details:</p>
                <div style="background-color: white; padding: 20px; border-radius: 8px; border-left: 4px solid #0077b6; margin: 20px 0;">
                    <table style="width: 100%;">
                        <tr>
                            <td style="padding: 8px 0; color: #666;">Appointment ID</td>
                            <td style="padding: 8px 0;"><strong>#{appointment_id}</strong></td>
                        </tr>
                        <tr>
                            <td style="padding: 8px 0; color: #666;">Doctor</td>
                            <td style="padding: 8px 0;"><strong>Dr. {doctor_name}</strong></td>
                        </tr>
                        <tr>
                            <td style="padding: 8px 0; color: #666;">Specialization</td>
                            <td style="padding: 8px 0;"><strong>{doctor_specialization}</strong></td>
                        </tr>
                        <tr>
                            <td style="padding: 8px 0; color: #666;">Date & Time</td>
                            <td style="padding: 8px 0;"><strong>{slot_start}</strong></td>
                        </tr>
                        <tr>
                            <td style="padding: 8px 0; color: #666;">End Time</td>
                            <td style="padding: 8px 0;"><strong>{slot_end}</strong></td>
                        </tr>
                    </table>
                </div>
                <div style="background-color: #fff3cd; padding: 15px; border-radius: 8px; margin: 20px 0;">
                    <p style="margin: 0;">⚠️ <strong>Important:</strong> Please arrive 10 minutes before your appointment time.</p>
                </div>
                <p>For emergencies, call: <strong>108</strong></p>
                <p>Hospital Address: <strong>123 Main Street</strong></p>
                <hr style="border: none; border-top: 1px solid #dee2e6; margin: 20px 0;">
                <p style="color: #666; font-size: 12px;">This is an automated email from City Hospital Voice Assistant. Please do not reply.</p>
            </div>
        </body>
        </html>
        """

        msg.attach(MIMEText(html, "html"))

        with smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT) as server:
            server.starttls()
            server.login(settings.EMAIL_USER, settings.EMAIL_PASSWORD)
            server.sendmail(settings.EMAIL_USER, to_email, msg.as_string())

        print(f"[EMAIL SENT] Appointment #{appointment_id} confirmation sent to {to_email}")
        return True

    except Exception as e:
        print(f"[EMAIL ERROR] {e}")
        return False