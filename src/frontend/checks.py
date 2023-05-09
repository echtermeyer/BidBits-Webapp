# TODO: Check if fields are not empty and user with password exists in database.
# Used when clicking on Login-Submit. 
def check_valid_login(username, password):
    if not username or not password:
        return "Error: All fields must be filled.", True
    else:
        return "Login successful", False 


# TODO: Check if fields are not empty and user with password exists in database.
# Used when clicking on Login-Submit. 
def check_valid_registration(username, email, firstname, lastname, address, phone, password, confirm_password):
    if not all([username, email, firstname, lastname, address, phone, password, confirm_password]):
        return "Error: All fields must be filled.", True

    # Assuming a phone number consists of only digits 
    if not phone.isdigit():
        return "Error: Phone number must be a digit number", True

    if password != confirm_password:
        return "Error: Passwords must be identical", True

    return "Registration successful", False 