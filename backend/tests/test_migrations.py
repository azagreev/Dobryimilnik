from pathlib import Path

BASELINE_MIGRATION_PATH = Path("alembic/versions/0001_create_domain_schemas.py")
IMPORT_STAGING_MIGRATION_PATH = Path("alembic/versions/0002_create_import_staging.py")


def test_baseline_migration_creates_only_phase_one_domain_schemas() -> None:
    migration = BASELINE_MIGRATION_PATH.read_text(encoding="utf-8")

    for schema in ("catalog", "orders", "users", "content"):
        assert f"CREATE SCHEMA IF NOT EXISTS {schema}" in migration

    assert "staging" not in migration
    assert "INSERT INTO" not in migration
    assert "op.bulk_insert" not in migration


def test_baseline_migration_is_reversible() -> None:
    migration = BASELINE_MIGRATION_PATH.read_text(encoding="utf-8")

    assert "def upgrade()" in migration
    assert "def downgrade()" in migration
    assert "DROP SCHEMA IF EXISTS" in migration
    assert "public\" CASCADE" not in migration


def test_import_staging_migration_creates_required_tables() -> None:
    migration = IMPORT_STAGING_MIGRATION_PATH.read_text(encoding="utf-8")

    assert 'CREATE SCHEMA IF NOT EXISTS staging' in migration
    for table in ("import_batches", "import_rows", "source_mappings", "import_errors"):
        assert f'"{table}"' in migration

    assert "catalog." not in migration
    assert "orders." not in migration
    assert "users." not in migration
    assert "content." not in migration


def test_import_staging_migration_preserves_source_identity_uniqueness() -> None:
    migration = IMPORT_STAGING_MIGRATION_PATH.read_text(encoding="utf-8")

    assert "uq_source_mappings_source_system_entity_type_source_id" in migration
    assert '"source_system"' in migration
    assert '"entity_type"' in migration
    assert '"source_id"' in migration


def test_import_staging_migration_downgrade_only_drops_staging_objects() -> None:
    migration = IMPORT_STAGING_MIGRATION_PATH.read_text(encoding="utf-8")

    assert 'op.drop_table("import_errors", schema="staging")' in migration
    assert 'op.drop_table("source_mappings", schema="staging")' in migration
    assert 'op.drop_table("import_rows", schema="staging")' in migration
    assert 'op.drop_table("import_batches", schema="staging")' in migration
    assert 'DROP SCHEMA IF EXISTS staging' in migration
    assert "DROP SCHEMA IF EXISTS catalog" not in migration
