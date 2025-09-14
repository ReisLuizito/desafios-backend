import re
from typing import List
from app.schemas import ValidationError

RE_UPPER = re.compile(r"[A-Z]")
RE_LOWER = re.compile(r"[a-z]")
RE_DIGIT = re.compile(r"\d")
RE_SPECIAL = re.compile(r"[^A-Za-z0-9]")

def validate_password(pw: str) -> List[ValidationError]:
    errors: List[ValidationError] = []

    if len(pw) < 8:
        errors.append(ValidationError(code="length", message="A senha deve ter pelo menos 8 caracteres."))

    if RE_UPPER.search(pw) is None:
        errors.append(ValidationError(code="uppercase", message="A senha deve conter ao menos uma letra maiúscula."))

    if RE_LOWER.search(pw) is None:
        errors.append(ValidationError(code="lowercase", message="A senha deve conter ao menos uma letra minúscula."))

    if RE_DIGIT.search(pw) is None:
        errors.append(ValidationError(code="digit", message="A senha deve conter ao menos um dígito numérico."))

    if RE_SPECIAL.search(pw) is None:
        errors.append(ValidationError(code="special", message="A senha deve conter ao menos um caractere especial."))

    return errors
