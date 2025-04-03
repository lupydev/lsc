import re


def validate_names(value):
    if not re.match(r"^[a-zA-Z\s]*$", value):
        raise ValueError(
            "El nombre y/o apellido solo pueden contener letras y espacios."
        )
    return value.strip().title()
