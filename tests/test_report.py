import unittest
from certiflow.engine import certify
from certiflow.report import html_report, csv_report

class Reports(unittest.TestCase):
    def test_escape(self):
        row=dict(code='<script>',contract_quantity=1,previous_quantity=0,claimed_quantity=1,measured_quantity=1,unit_rate=1)
        result=certify([row])
        self.assertNotIn('<script>',html_report(result))
        self.assertIn('&lt;script&gt;',html_report(result))
        result['lines'][0]['code']='=1+1'
        self.assertIn("'=1+1",csv_report(result))
