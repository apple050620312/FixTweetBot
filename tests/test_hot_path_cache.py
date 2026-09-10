from src import hot_path_cache


def test_cache_evicts_least_recently_used_item():
    cache = hot_path_cache.TTLCache(max_size=2, ttl=60)
    cache.set('first', 1)
    cache.set('second', 2)
    cache.set('third', 3)

    assert cache.get('first') is hot_path_cache.MISSING
    assert cache.get('second') == 2
    assert cache.get('third') == 3


def test_cache_expires_items(monkeypatch):
    now = 100.0
    monkeypatch.setattr(hot_path_cache.time, 'monotonic', lambda: now)
    cache = hot_path_cache.TTLCache(max_size=2, ttl=5)
    cache.set('key', 'value')
    now = 106.0

    assert cache.get('key') is hot_path_cache.MISSING


def test_guild_invalidation_only_removes_matching_keys():
    cache = hot_path_cache.TTLCache(max_size=4, ttl=60)
    cache.set((10, 'member'), True)
    cache.set((11, 'member'), False)
    cache.pop_guild(10)

    assert cache.get((10, 'member')) is hot_path_cache.MISSING
    assert cache.get((11, 'member')) is False
