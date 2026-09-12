def test_incremental_fixture_preserves_manual_fields(run_validator, profile_fixture, load_json):
    before = profile_fixture / "before/profile/modules/pkg.core.json"
    after = profile_fixture / "after/profile/modules/pkg.core.json"

    result = run_validator(profile_fixture / "after/profile")

    assert result.returncode == 0
    assert load_json(after)["manual"] == load_json(before)["manual"]


def test_profile_rejects_manifest_module_map_drift(
    run_validator, profile_fixture, load_json, write_json, copy_fixture
):
    profile = copy_fixture(profile_fixture / "after/profile")
    manifest = load_json(profile / "manifest.json")
    manifest["profile_files"]["modules"]["pkg.missing"] = "modules/pkg.missing.json"
    write_json(profile / "manifest.json", manifest)

    result = run_validator(profile)

    assert result.returncode == 4
    assert "pkg.missing" in result.stderr


def test_profile_rejects_facet_unknown_module(run_validator, profile_fixture, load_json, write_json, copy_fixture):
    profile = copy_fixture(profile_fixture / "after/profile")
    facet_path = profile / "facets/users.json"
    facet = load_json(facet_path)
    facet["featured_modules"].append("pkg.missing")
    write_json(facet_path, facet)

    result = run_validator(profile)

    assert result.returncode == 4
    assert "pkg.missing" in result.stderr


def test_profile_rejects_malformed_changed_scopes(run_validator, profile_fixture, load_json, write_json, copy_fixture):
    profile = copy_fixture(profile_fixture / "after/profile")
    manifest_path = profile / "manifest.json"
    manifest = load_json(manifest_path)
    manifest["changed_scopes"] = "oops"
    write_json(manifest_path, manifest)

    result = run_validator(profile)

    assert result.returncode == 4
    assert "not of type 'object'" in result.stderr
    assert "Traceback" not in result.stderr


def test_profile_rejects_malformed_before_profile_files(
    run_validator, profile_fixture, load_json, write_json, copy_fixture
):
    profile = copy_fixture(profile_fixture)
    before = profile / "before/profile"
    after = profile / "after/profile"
    manifest_path = before / "manifest.json"
    manifest = load_json(manifest_path)
    manifest["profile_files"] = "oops"
    write_json(manifest_path, manifest)

    result = run_validator(after, "--before-profile", str(before))

    assert result.returncode == 4
    assert "profile_files" in result.stderr
    assert "Traceback" not in result.stderr


def test_incremental_fixture_rejects_manual_field_changes(
    run_validator, profile_fixture, load_json, write_json, copy_fixture
):
    profile = copy_fixture(profile_fixture)
    before = profile / "before/profile"
    after = profile / "after/profile"
    module_path = after / "modules/pkg.core.json"
    module = load_json(module_path)
    module["manual"]["notes"] = "Tampered note."
    write_json(module_path, module)

    result = run_validator(after, "--before-profile", str(before))

    assert result.returncode == 4
    assert "pkg.core" in result.stderr
    assert "manual" in result.stderr
    assert "preserved" in result.stderr


def test_result_option_validates_transient_result(
    run_validator, profile_fixture, load_json, write_json, tmp_path
):
    result_path = tmp_path / "completion-result.json"
    write_json(
        result_path,
        {
            "$schema": "urn:mountainash:textbook-skills:completion-result:1",
            "invocation_id": "test-invocation",
            "skill": {
                "name": "package-documentation-profile",
                "version": "1.0.0",
                "source_revision": "0" * 40,
                "digest": "sha256:" + "0" * 64,
            },
            "stage": "profile",
            "capability": "package-profile.generate",
            "behavior": "full",
            "status": "success",
            "execution": {
                "provider": "test",
                "model": "test",
                "attempts": 1,
                "input_tokens": None,
                "output_tokens": None,
                "cost": None,
            },
            "inputs": [],
            "outputs": [],
            "targets": {"requested_modules": [], "effective_modules": []},
            "warnings": [],
            "metrics": {
                "modules_discovered": 2,
                "modules_profiled": 2,
                "facets_written": 2,
            },
            "preserved": [],
        },
    )

    result = run_validator(
        profile_fixture / "after/profile", "--result", str(result_path)
    )

    assert result.returncode == 0
    assert result_path.is_file()
    assert load_json(result_path)["status"] == "success"
