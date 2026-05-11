from importlib import import_module


DOMAINS = ("catalog", "orders", "users", "content", "analytics")
MODULES = ("api", "service", "repository", "models")


def test_domain_modules_are_importable() -> None:
    for domain in DOMAINS:
        for module in MODULES:
            import_module(f"app.domains.{domain}.{module}")
