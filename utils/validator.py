def validate_phone(phone):
    """
    This is added so the raw data that contains invalid phone number 
    will be automatically skipped
    """
    phone_str = str(phone).strip()
 
    if not phone_str.isdigit():
        return False
    
 
    if len(phone_str) != 10:
        return False
 
    if not phone_str.startswith("98"):
        return False
 
    return True

if __name__ == "__main__":
    print(validate_phone("9801234567"))  #it passes all validation tests.
    print(validate_phone("98123"))       #10 didits are not there
    print(validate_phone("9701234567"))  #fails the starts with 98 test
    print(validate_phone("980123456a"))  #the number is ivalid if letter is there