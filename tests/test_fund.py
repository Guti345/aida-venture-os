import pytest


def test_fund_exists(client):
    resp = client.get("/fund")
    assert resp.status_code == 200
    data = resp.json()
    assert data["name"] == "AIDA Ventures Fund I"


def test_simulate_quick_returns_moic(client, auth_headers):
    resp = client.get("/fund/simulate/quick", params={"scenario_label": "base"}, headers=auth_headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["moic_p50"] > 0


def test_simulate_custom_high_scenario(client, auth_headers):
    low = client.get(
        "/fund/simulate/quick",
        params={"scenario_label": "base", "pct_winners": 0.1},
        headers=auth_headers,
    )
    high = client.get(
        "/fund/simulate/quick",
        params={"scenario_label": "base", "pct_winners": 0.5},
        headers=auth_headers,
    )
    assert low.status_code == 200
    assert high.status_code == 200
    assert high.json()["moic_p50"] > low.json()["moic_p50"]
