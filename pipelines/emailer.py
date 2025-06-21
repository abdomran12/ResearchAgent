
import os
import smtplib
import ssl
from email.message import EmailMessage
from datetime import datetime

def log(msg):
    print(f"[emailer] {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {msg}")

def send_email_with_report(sender_email, receiver_email, password, report_path):
    msg = EmailMessage()
    msg['Subject'] = f"Weekly AI Research Report - {datetime.now().strftime('%Y-%m-%d')}"
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg.set_content("Attached is this week's AI research report with summaries and ideas.")

    with open(report_path, 'rb') as f:
        file_data = f.read()
        file_name = os.path.basename(report_path)
    msg.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=file_name)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(sender_email, password)
        smtp.send_message(msg)
    log(f"Report sent to {receiver_email}")

if __name__ == "__main__":
    # These should be set via environment variables for security
    sender = os.getenv("AGENT_SENDER_EMAIL")
    receiver = os.getenv("AGENT_RECEIVER_EMAIL")
    pwd = os.getenv("AGENT_EMAIL_PASSWORD")
    report = "outputs/weekly_report_" + datetime.now().strftime('%Y%m%d') + ".docx"

    if os.path.exists(report):
        send_email_with_report(sender, receiver, pwd, report)
    else:
        log("No report found to send.")
