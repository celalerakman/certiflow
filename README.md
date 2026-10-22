# CertiFlow

Payment certificate calculations with cumulative quantities, measured evidence,
retention and previous-payment reconciliation.

The approved quantity is the minimum of contract, claimed and measured quantities.
Current-period quantities and held quantities remain visible on each BOQ line.
Amounts use Decimal with explicit half-up rounding. Negative net due is preserved
as a credit; cumulative quantity regression is rejected.

## Run

Python 3.11 or newer; no external packages.

```sh
python -m certiflow examples/certificate.json --html runtime/certificate.html --csv runtime/certificate.csv
python -m unittest discover -s tests -v
```

Open the generated HTML file in a browser. CSV text cells are protected against
formula interpretation. HTML output escapes untrusted text.

## Calculation conventions

Each certificate uses one currency. Quantities are cumulative in the BOQ item's
unit. Retention is deducted before tax. Earlier certified net amounts are deducted
from cumulative net. Variation pricing, advance recovery and retention caps are
outside the current calculation model.

`engine.py` contains the calculation rules, `report.py` contains report formatting,
and `__main__.py` provides file input/output. Cash forecasts and earned-value
indicators are available as library functions.
