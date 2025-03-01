import re

def validate_registration_data(data):
    required_fields = [
        "first_name",
        "last_name",
        "dob",
        "gender",
        "email",
        "phone_number",
        "street_address",
        "city",
        "state",
        "postal_code",
        "country",
        "password",
        "confirm_password"
    ]

    for field in required_fields:
        if field not in data or not data[field]:
            return False, f"{field} is required."

    # Additional validations can go here (e.g., email format, password strength, etc.)
    return True, "Valid data."

def validate_email_format(email):
    """
    Validates if the email is in a valid format.
    """
    email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(email_regex, email) is not None

def validate_password_strength(password):
    """
    Validates if the password is strong enough.
    A strong password should:
    - Be at least 8 characters long
    - Contain at least one digit
    - Contain at least one letter
    """
    if len(password) < 8:
        return False, "Password must be at least 8 characters long."
    if not any(char.isdigit() for char in password):
        return False, "Password must contain at least one digit."
    if not any(char.isalpha() for char in password):
        return False, "Password must contain at least one letter."
    return True, ""
