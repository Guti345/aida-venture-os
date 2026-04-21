import pytest


def test_list_startups_returns_10(client):
    resp = client.get("/startups")
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) >= 10, f"Expected >=10 startups, got {len(data)}"


def test_get_startup_by_name(client):
    resp = client.get("/startups", params={"name": "FinStack"})
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) >= 1
    assert any(s["name"] == "FinStack" for s in data)


def test_metrics_latest_has_arr(client):
    resp = client.get("/startups/FinStack/metrics/latest")
    assert resp.status_code == 200
    data = resp.json()
    assert "ARR" in data, f"ARR not found in latest metrics: {list(data.keys())}"


def test_percentile_returns_result(client):
    resp = client.get(
        "/startups/FinStack/percentile",
        params={
            "metric_name": "ARR",
            "segment_sector": "SaaS",
            "segment_stage": "seed",
            "segment_geography": "US",
        },
    )
    assert resp.status_code == 200
    data = resp.json()
    assert "percentile_position" in data
    assert 0 <= data["percentile_position"] <= 100


def test_ingest_metrics(client, auth_headers):
    payload = {
        "startup_name": "FinStack",
        "period_date": "2025-01-01",
        "arr_usd": 520000,
        "mrr_usd": 43000,
        "runway_months": 16,
    }
    resp = client.post("/startups/ingest-metrics", json=payload, headers=auth_headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["metrics_saved"] == 3
    assert data["startup_name"] == "FinStack"
