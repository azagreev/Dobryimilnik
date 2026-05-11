from pathlib import Path

MIGRATION_PATH = Path("alembic/versions/0001_create_domain_schemas.py")


def test_baseline_migration_creates_only_phase_one_domain_schemas() -> None:
    migration = MIGRATION_PATH.read_text(encoding="utf-8")

    for schema in ("catalog", "orders", "users", "content"):
        assert f"CREATE SCHEMA IF NOT EXISTS {schema}" in migration

    assert "staging" not in migration
    assert "INSERT INTO" not in migration
    assert "op.bulk_insert" not in migration


def test_baseline_migration_is_reversible() -> None:
    migration = MIGRATION_PATH.read_text(encoding="utf-8")

    assert "def upgrade()" in migration
    assert "def downgrade()" in migration
    assert "DROP SCHEMA IF EXISTS" in migration
    assert "public\" CASCADE" not in migration
