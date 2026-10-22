import argparse
import json
from pathlib import Path
from .engine import certify
from .report import html_report, csv_report

parser = argparse.ArgumentParser(description='Validate a cumulative payment certificate')
parser.add_argument('input', type=Path)
parser.add_argument('--html', type=Path, help='Write standalone review report')
parser.add_argument('--csv', type=Path, help='Write spreadsheet-safe line details')
args = parser.parse_args()
try:
    payload = json.loads(args.input.read_text(encoding='utf-8'))
    result = certify(**payload)
    for path, contents in ((args.html, html_report(result)), (args.csv, csv_report(result))):
        if path:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(contents, encoding='utf-8')
    print(json.dumps(result, indent=2))
except (ValueError, KeyError, TypeError) as exc:
    parser.exit(2, f'Invalid certificate: {exc}\n')
