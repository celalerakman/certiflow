"""Escaped, standalone project controls report."""
import csv
from html import escape
import io


def html_report(result, title='Payment certificate review'):
    def cell(value):
        return escape(str(value))
    rows = ''.join('<tr>' + ''.join(f'<td>{cell(row[key])}</td>' for key in
                   ('code', 'approved_quantity', 'period_quantity', 'held_quantity',
                    'cumulative_gross', 'period_gross')) + '</tr>' for row in result['lines'])
    cards = ''.join(f'<article><span>{cell(label)}</span><strong>{cell(result[key])}</strong></article>'
                    for label, key in [('Cumulative gross','gross'), ('Retention','retention'),
                                       ('Tax','tax'), ('Current net due','net_due')])
    return '''<!doctype html><html lang="en"><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>''' + cell(title) + '''</title>
<style>body{font:16px/1.6 system-ui;background:#eff3f7;color:#142538;margin:0;padding:5vw}
main{max-width:1180px;margin:auto}header{border-top:6px solid #148175;padding:24px 0}
small,span{color:#526779}h1{font-size:clamp(28px,4vw,44px);margin:8px 0}
.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:16px}
article{background:white;padding:24px;border-radius:12px}strong{display:block;font-size:28px}
.table{overflow:auto;margin-top:24px;background:white;border-radius:12px}
table{border-collapse:collapse;width:100%;text-align:right;white-space:nowrap}
th,td{padding:16px;border-bottom:1px solid #e0e7ed}th:first-child,td:first-child{text-align:left}
footer{margin-top:24px;font-size:14px}@media print{body{background:white;padding:0}}</style>
<main><header><small>CERTIFLOW / PROJECT CONTROLS</small><h1>''' + cell(title) + '''</h1>
<p>Cumulative quantities, measured evidence and transparent deductions.</p></header>
<section class="cards">''' + cards + '''</section><section class="table"><table>
<thead><tr><th>BOQ item</th><th>Approved cumulative</th><th>Current quantity</th>
<th>Held quantity</th><th>Cumulative gross</th><th>Current gross</th></tr></thead>
<tbody>''' + rows + '''</tbody></table></section><footer>Example calculation.
One currency per certificate. Quantities use each BOQ item's declared unit.
Tax is applied after retention. Negative due represents a credit.</footer></main></html>'''


def csv_report(result):
    output = io.StringIO(newline='')
    fields = ('code', 'approved_quantity', 'period_quantity', 'held_quantity',
              'cumulative_gross', 'period_gross')
    writer = csv.DictWriter(output, fields)
    writer.writeheader()
    for row in result['lines']:
        safe = {key: ("'" + str(value) if str(value).lstrip().startswith(('=', '+', '-', '@'))
                      else value) for key, value in row.items()}
        writer.writerow(safe)
    return output.getvalue()
