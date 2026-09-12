def test_vendored_protocol_matches_recorded_digests(protocol_root, load_json, sha256):
    source = load_json(protocol_root / "source.json")
    for item in source["files"]:
        assert sha256(protocol_root / "v1" / item["path"]) == item["sha256"]
