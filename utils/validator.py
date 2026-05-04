def validate_phone(phone):
    phone_str = str(phone).strip()

    if not phone_str.isdigit():
        return False

    if len(phone_str) != 10:
        return False

    if not phone_str.startswith("98"):
        return False

    return True


def validate_name(name):
    name_str = str(name).strip()

    # empty or pandas missing value
    if not name_str or name_str.lower() in ("nan", "<na>"):
        return False

    # whitespace only — shouldn't reach here after preprocessing but safety net
    if not name_str.replace(" ", ""):
        return False

    # all digits
    if name_str.isdigit():
        return False

    # too short to be a real name
    if len(name_str) < 2:
        return False

    return True


def validate_business_name(business_name):
    biz_str = str(business_name).strip()

    if not biz_str or biz_str.lower() == "nan":
        return False

    if not biz_str.replace(" ", ""):
        return False

    if biz_str.isdigit():
        return False

    if len(biz_str) < 2:
        return False

    return True


def validate_message_length(message, max_length=160):
    return len(message) <= max_length