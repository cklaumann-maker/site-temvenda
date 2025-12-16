from datetime import date

from app.finance_service import build_forecast_for_day, parse_month_code


def test_parse_month_code():
    year, month = parse_month_code("12-25")
    assert year == 2025
    assert month == 12


def test_forecast_weekday():
    # Terça-feira 2025-03-04
    d = date(2025, 3, 4)
    f = build_forecast_for_day(d)
    assert f["money"] == 13334.00
    assert f["pix"] == 6010.11
    assert f["card"] == 15706.20
    assert f["convenio"] == 179.11


def test_forecast_monday():
    # Segunda-feira 2025-03-03
    d = date(2025, 3, 3)
    f = build_forecast_for_day(d)
    assert f["money"] == 29296.30
    assert f["pix"] == 13204.89
    assert f["card"] == 34508.30
    assert f["convenio"] == 393.52


def test_forecast_weekend_zero():
    # Domingo
    d = date(2025, 3, 2)
    f = build_forecast_for_day(d)
    assert f["money"] == 0
    assert f["pix"] == 0
    assert f["card"] == 0
    assert f["convenio"] == 0


