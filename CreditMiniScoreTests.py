import unittest
from CreditMiniScore import Business, Loan

class TestCreditMiniScore(unittest.TestCase):
    # Emulate a business with a perfect payment history and more than sufficient assets to repay a loan.
    def test_max_credit_score(self):
        b = Business('test', 'test-owner', 5, 1, [Loan(1, 1, [0])])
        self.assertEqual(Business.MAX_CREDIT, b.credit_mini_score())
        self.assertEqual(1., b.p_value())

    # Emulate a business with no credibility.
    def test_min_credit_score(self):
        b = Business('test', 'test-owner', 0, 1, [])
        self.assertEqual(Business.MIN_CREDIT, b.credit_mini_score())
        self.assertEqual(0., b.p_value())

if __name__ == '__main__':
    unittest.main()
