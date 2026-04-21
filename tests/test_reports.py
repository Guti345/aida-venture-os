import pytest

_LP_REQUIRED_FIELDS = {"fund_moic_current", "fund_irr_current", "portfolio_companies", "narrative_summary"}


def test_lp_summary_structure(client, auth_headers):
    resp = client.get("/reports/lp-summary", headers=auth_headers)
    assert resp.status_code == 200
    data = resp.json()
    missing = _LP_REQUIRED_FIELDS - set(data.keys())
    assert not missing, f"Missing fields in lp-summary: {missing}"


def test_portfolio_snapshot_has_all_active(client, auth_headers):
    resp = client.get("/reports/portfolio-snapshot", headers=auth_headers)
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) >= 5, f"Expected >=5 portfolio items, got {len(data)}"
