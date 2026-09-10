import pytest

from src.sharding import shard_options


def test_sharding_is_automatic_without_assignment():
    assert shard_options({}) == {}


def test_shard_assignment_is_parsed_and_trimmed():
    assert shard_options({'SHARD_COUNT': '50', 'SHARD_IDS': '0, 7,49'}) == {
        'shard_count': 50,
        'shard_ids': [0, 7, 49],
    }


@pytest.mark.parametrize(
    'environment',
    [
        {'SHARD_IDS': '1'},
        {'SHARD_COUNT': '0'},
        {'SHARD_COUNT': '2', 'SHARD_IDS': '2'},
        {'SHARD_COUNT': '2', 'SHARD_IDS': '1,1'},
    ],
)
def test_invalid_shard_assignment_fails_fast(environment):
    with pytest.raises((RuntimeError, ValueError)):
        shard_options(environment)
