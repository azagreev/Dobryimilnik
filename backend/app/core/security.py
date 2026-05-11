def redact_secret(value: str | None) -> str | None:
    if value is None:
        return None
    return "***"
