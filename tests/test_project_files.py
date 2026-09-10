import importlib.util
from pathlib import Path

import yaml


ROOT = Path(__file__).parents[1]


def test_all_locale_files_are_valid_yaml():
    for locale_file in (ROOT / 'locales').glob('*.yml'):
        with locale_file.open(encoding='utf-8') as stream:
            assert isinstance(yaml.safe_load(stream), dict), locale_file


def test_integrity_migration_imports():
    migration_path = ROOT / 'database/migrations/2026_09_10_000000_add_integrity_indexes.py'
    spec = importlib.util.spec_from_file_location('integrity_migration', migration_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)


def test_compose_uses_one_shot_migration_and_private_database():
    with (ROOT / 'docker-compose.example.yml').open(encoding='utf-8') as stream:
        compose = yaml.safe_load(stream)

    assert compose['services']['bot']['depends_on']['migrate']['condition'] == 'service_completed_successfully'
    assert 'ports' not in compose['services']['db']
