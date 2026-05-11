from app.core.errors import DomainError
from app.core.logging import configure_logging
from app.core.pagination import PageParams
from app.core.schemas import TimestampedModel
from app.core.security import redact_secret


def test_core_scaffold_helpers_are_usable() -> None:
    configure_logging()

    assert PageParams().limit == 50
    assert redact_secret("secret") == "***"
    assert redact_secret(None) is None
    assert TimestampedModel().created_at.tzinfo is not None
    assert issubclass(DomainError, Exception)
