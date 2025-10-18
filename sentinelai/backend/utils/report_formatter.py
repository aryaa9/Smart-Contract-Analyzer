import json

def format_report(raw_report):
    """Flatten nested dicts for clean JSON export."""
    return json.dumps(raw_report, indent=2)
