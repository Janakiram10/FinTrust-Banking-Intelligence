from src.generate_data import build

def test_referential_integrity():
    t = build("test")
    assert t["accounts"].customer_id.isin(t["customers"].customer_id).all()
    assert t["transactions"].account_id.isin(t["accounts"].account_id).all()
    assert t["loans"].customer_id.isin(t["customers"].customer_id).all()
    assert t["loan_payments"].loan_id.isin(t["loans"].loan_id).all()
    assert t["monthly_balances"].account_id.isin(t["accounts"].account_id).all()

def test_business_ranges():
    t = build("test")
    assert t["transactions"].amount.gt(0).all()
    assert t["transactions"].risk_score.between(0, 1).all()
    assert t["loans"].outstanding_amount.le(t["loans"].principal_amount).all()
    assert t["customers"].age.between(18, 78).all()

def test_generator_is_deterministic():
    left, right = build("test"), build("test")
    assert left["transactions"].equals(right["transactions"])
    assert left["loan_payments"].equals(right["loan_payments"])

def test_monthly_snapshot_grain():
    t = build("test")
    assert not t["monthly_balances"].duplicated(["snapshot_date","account_id"]).any()
