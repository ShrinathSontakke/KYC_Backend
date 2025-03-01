from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

def send_purchase_email(recipient_email, license_type, validity_period):
    """Send an email notification when a user purchases a license."""
    
    subject = "License Purchase Confirmation"
    
    # Load HTML template
    html_content = render_to_string("license_purchase.html", {
        "license_type": license_type,
        "validity_period": validity_period,
    })

    text_content = strip_tags(html_content)  # Fallback plain text

    email = EmailMultiAlternatives(subject, text_content, "pratyakshakyc@gmail.com", [recipient_email])
    email.attach_alternative(html_content, "text/html")
    email.send()

def send_license_assignment_email(recipient_email, license_type, assigned_at, initiator_email):
    """Send an email notification when a license is assigned."""
    
    subject = "You Have Been Assigned a License"
    
    # Load HTML template
    html_content = render_to_string("license_assigned.html", {
        "license_type": license_type,
        "assigned_at": assigned_at.strftime('%Y-%m-%d %H:%M:%S'),
        "initiator_email": initiator_email,
    })

    text_content = strip_tags(html_content)  # Fallback plain text

    email = EmailMultiAlternatives(subject, text_content, "pratyakshakyc@gmail.com", [recipient_email])
    email.attach_alternative(html_content, "text/html")
    email.send()