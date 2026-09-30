import copy
import unittest
from model import load, calculate, validate


class UltimateTests(unittest.TestCase):
    def setUp(self): self.a=load()
    def test_revision_changes_amortization(self):
        self.assertGreater(calculate(self.a)['amortization'],calculate(self.a,'prior')['amortization'])
    def test_every_sensitivity_rolls_forward(self):
        for h in range(101):
            m=calculate(self.a,haircut=h/100)
            self.assertAlmostEqual(m['rollforward_error'],0)
            self.assertGreaterEqual(m['closing_content_asset'],-1e-10)
            self.assertLessEqual(m['amortization']+m['illustrative_write_down'],m['available_cost']+1e-10)
    def test_zero_revenue_writes_off_asset(self):
        self.a['current_revenue']=0
        m=calculate(self.a,haircut=1)
        self.assertEqual(m['amortization'],0); self.assertEqual(m['closing_content_asset'],0)
        self.assertEqual(m['illustrative_write_down'],45)
    def test_no_future_revenue_amortizes_remaining_cost(self):
        m=calculate(self.a,haircut=1)
        self.assertEqual(m['closing_content_asset'],0)
    def test_break_even_threshold(self):
        threshold=calculate(self.a)['break_even_future_revenue']
        total=sum(r['prior_future_revenue'] for r in self.a['windows'])
        m=calculate(self.a,revision='prior',haircut=1-threshold/total)
        self.assertAlmostEqual(m['recoverability_headroom'],0)
    def test_invalid_and_duplicate(self):
        self.a['windows'].append(copy.deepcopy(self.a['windows'][0]))
        with self.assertRaises(ValueError):validate(self.a)
    def test_historical_actuals_not_rewritten(self):
        a=copy.deepcopy(self.a); calculate(a,haircut=0.55)
        self.assertEqual(a,self.a)


if __name__=='__main__':unittest.main()
