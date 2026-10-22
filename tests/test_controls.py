import unittest
from decimal import Decimal
from certiflow.engine import certify, cash_forecast, earned_value, number


def item(**updates):
    return dict(code='C1', contract_quantity='100', previous_quantity='20',
                claimed_quantity='90', measured_quantity='80', unit_rate='10.05', **updates)


class CertificateTests(unittest.TestCase):
    def test_measurement_limits_claim_and_previous_payment_is_deducted(self):
        result = certify([item()], previous_net='100')
        self.assertEqual(result['lines'][0]['approved_quantity'], '80')
        self.assertEqual(result['lines'][0]['held_quantity'], '10')
        self.assertEqual(result['net_due'], '816.56')

    def test_overpayment_produces_credit(self):
        self.assertEqual(certify([item()], previous_net='1000')['net_due'], '-83.44')

    def test_duplicate_items_rejected(self):
        with self.assertRaises(ValueError):
            certify([item(), item()])

    def test_quantity_regression_rejected(self):
        row = item()
        row['measured_quantity'] = '10'
        with self.assertRaises(ValueError):
            certify([row])

    def test_non_finite_negative_and_invalid_rates_rejected(self):
        for value in ('NaN', 'Infinity', '-1', 'abc'):
            with self.subTest(value=value), self.assertRaises(ValueError):
                number(value)
        with self.assertRaises(ValueError):
            certify([item()], retention='1.01')

    def test_half_cent_rounds_up(self):
        row = item()
        row.update(contract_quantity='1', previous_quantity='0', claimed_quantity='1',
                   measured_quantity='1', unit_rate='0.005')
        self.assertEqual(certify([row], retention=0, tax=0)['gross'], '0.01')

    def test_forecast_keeps_deficit_and_undefined_ratios(self):
        result = cash_forecast(10, [{'period':'M1','inflow':0,'outflow':20}])
        self.assertTrue(result[0]['shortfall'])
        self.assertIsNone(earned_value(0, 10, 0)['cpi'])


if __name__ == '__main__':
    unittest.main()
