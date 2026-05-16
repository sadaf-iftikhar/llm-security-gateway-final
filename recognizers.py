from presidio_analyzer import PatternRecognizer, Pattern

def get_custom_recognizers():
    pak_phone = PatternRecognizer(
        supported_entity="PAK_PHONE",
        patterns=[
            Pattern("PAK_LOCAL", r"0[3][0-9]{2}[-\s]?[0-9]{7}", 0.85),
            Pattern("PAK_INTL", r"\+92[3][0-9]{9}", 0.90),
        ],
        context=["call", "contact", "number",
                 "phone", "whatsapp", "mobile", "reach me"]
    )

    api_key = PatternRecognizer(
        supported_entity="API_KEY",
        patterns=[
            Pattern("SK_KEY", r"sk-[a-zA-Z0-9]{20,}", 0.95),
            Pattern("BEARER", r"Bearer\s[a-zA-Z0-9\-._~+/]+=*", 0.90),
            Pattern("GENERIC", r"[a-zA-Z0-9]{32,}", 0.70),
        ],
        context=["key", "token", "secret",
                 "authorization", "api", "bearer", "credential"]
    )

    cnic = PatternRecognizer(
        supported_entity="PAK_CNIC",
        patterns=[
            Pattern("CNIC_DASH", r"[0-9]{5}-[0-9]{7}-[0-9]{1}", 0.95),
            Pattern("CNIC_PLAIN", r"[0-9]{13}", 0.70),
        ],
        context=["cnic", "identity", "id card",
                 "national", "nadra", "identification"]
    )

    internal_id = PatternRecognizer(
        supported_entity="INTERNAL_ID",
        patterns=[
            Pattern("STU_FAST", r"[A-Z]{2}[0-9]{2}-[A-Z]{3}-[0-9]{3}", 0.90),
            Pattern("STU_CUI", r"SP[0-9]{2}-[A-Z]{3}-[0-9]{3}", 0.90),
            Pattern("EMP_ID", r"EMP-[0-9]{4,6}", 0.80),
        ],
        context=["student", "registration", "roll",
                 "student id", "reg no", "enrollment",
                 "employee", "id", "number"]
    )

    email = PatternRecognizer(
        supported_entity="EMAIL_ADDRESS",
        patterns=[
            Pattern("EMAIL",
                    r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}",
                    0.85),
        ],
        context=["email", "mail", "contact", "send to",
                 "reach", "e-mail", "inbox", "gmail", "outlook"]
    )

    return [pak_phone, api_key, cnic, internal_id, email]