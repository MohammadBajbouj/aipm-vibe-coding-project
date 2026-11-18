"""Build the single, self-contained index.html (D30).

    python3 app/build.py

Reads app/data/alerts.json, runs the claim check (app/claim_check.py) and
renders every alert screen into app/template.html. The result is written to
index.html in the repo root. Re-run after any change to data, rules or
template. Python 3.9 standard library only.
"""

import json
from html import escape
from pathlib import Path

from claim_check import MATCH, MISMATCH, NOT_AVAILABLE, check_alert, warning_line

APP = Path(__file__).resolve().parent
ROOT = APP.parent
DATA_FILE = APP / "data" / "alerts.json"
TEMPLATE_FILE = APP / "template.html"
OUTPUT_FILE = ROOT / "index.html"

# Traffic light always with symbol + word (D15).
MARK_TEXT = {
    MATCH: "✓ matches",
    NOT_AVAILABLE: "⚠ not available",
    MISMATCH: "✗ mismatch",
}

MAX_PREVIOUS_DEVICES = 3  # D25

WEIGHT_LABELS = [("release", "Release"), ("block", "Block"), ("call", "Call")]


def load_alerts():
    return json.loads(DATA_FILE.read_text(encoding="utf-8"))["alerts"]


def format_amount(amount):
    return "€{:,.2f}".format(amount)


def render_row(alert):
    p = alert["payment"]
    aid = escape(alert["id"])
    return (
        '        <tr data-row="{id}">'
        '<td data-label="Alert"><strong>{id}</strong></td>'
        '<td data-label="Time">{time}</td>'
        '<td data-label="Merchant">{merchant}</td>'
        '<td data-label="Amount">{amount}</td>'
        '<td data-label="Status" class="status-cell">open</td>'
        '<td><button type="button" data-open="{id}" aria-label="Open alert {id}">Open</button></td>'
        "</tr>"
    ).format(
        id=aid,
        time=escape(p["time"]),
        merchant=escape(p["merchant"]),
        amount=escape(format_amount(p["amount_eur"])),
    )


def render_claims(alert, results):
    rows = []
    for claim, result in zip(alert["claims"], results):
        rows.append(
            '          <tr data-field="{field}" data-result="{result}">'
            '<td data-label="Copilot says">{claimed}</td>'
            '<td data-label="Record value">{record}</td>'
            '<td data-label="Claim check"><span class="mark mark-{result}">{mark}</span></td>'
            "</tr>".format(
                field=escape(claim["field"]),
                result=result,
                claimed=escape(claim["text"]),
                record=escape(claim["record_label"]),
                mark=MARK_TEXT[result],
            )
        )
    return "\n".join(rows)


def render_previous_devices(alert):
    """D13/D25: only when device data is missing - plain list, no matching, no marks."""
    device_missing = any(
        c["field"] == "device_known" and c.get("record") is None for c in alert["claims"]
    )
    devices = alert.get("previous_devices", [])[:MAX_PREVIOUS_DEVICES]
    if not device_missing or not devices:
        return ""
    items = "\n".join(
        "          <li>{name} – known since {since}</li>".format(
            name=escape(d["name"]), since=escape(d["known_since"])
        )
        for d in devices
    )
    return (
        '      <div class="previous-devices">\n'
        "        <h4>Device data not available – previous devices, not from this payment</h4>\n"
        "        <ul>\n{items}\n        </ul>\n"
        "      </div>"
    ).format(items=items)


def render_weights(alert):
    items = []
    weights = alert["suggestion_weights"]
    for key, label in WEIGHT_LABELS:
        value = int(weights[key])
        items.append(
            '          <li><span>{label}</span>'
            '<span class="bar" aria-hidden="true"><span style="width:{v}%"></span></span>'
            "<span>{v} %</span></li>".format(label=label, v=value)
        )
    return "\n".join(items)


def render_view(alert):
    p = alert["payment"]
    aid = escape(alert["id"])
    results = check_alert(alert)
    funds = "yes" if alert["funds_available"] else "no"
    # R3: orange warning style only when a reason is ✗ or ⚠; neutral when all ✓.
    all_confirmed = all(r == MATCH for r in results)
    warning_class = "warning-line warning-line-ok" if all_confirmed else "warning-line"
    return """  <section class="alert-view" data-alert="{id}" id="alert-{id}" hidden aria-labelledby="title-{id}">
    <button type="button" class="back" data-back>← Back to alert list</button>

    <div class="card">
      <h2 id="title-{id}" tabindex="-1">Alert {id}</h2>
      <p class="status-line">Status: <span data-status-for="{id}">open – no decision yet</span></p>
      <dl class="details">
        <dt>Time</dt><dd>{time}</dd>
        <dt>Amount</dt><dd>{amount}</dd>
        <dt>Merchant</dt><dd>{merchant}</dd>
        <dt>Country</dt><dd>{country}</dd>
        <dt>Channel</dt><dd>{channel}</dd>
        <dt>Customer</dt><dd>{customer}</dd>
        <dt>Funds available</dt><dd>{funds}</dd>
        <dt>Assigned analyst</dt><dd>{analyst}</dd>
      </dl>
    </div>

    <div class="card">
      <h3>Copilot's reasons <span class="badge badge-mock">mocked</span></h3>
      <table class="claims stack">
        <thead><tr><th>Copilot says</th><th>Record value</th><th>Claim check</th></tr></thead>
        <tbody>
{claims}
        </tbody>
      </table>
{previous_devices}
    </div>

    <div class="card">
      <h3>Suggestion – non-binding <span class="badge badge-mock">mocked weights</span></h3>
      <p class="{warning_class}">{warning}</p>
      <ul class="weights">
{weights}
      </ul>
      <p class="hint">The suggestion never sets a status. Only the analyst's decision does.</p>
    </div>

    <div class="card decision-card" data-decision-for="{id}" data-analyst="{analyst}">
      <h3>Your decision</h3>
      <div class="decision-form">
        <div class="decision-buttons" role="group" aria-label="Decision for alert {id}">
          <button type="button" data-choice="release" aria-pressed="false">Release payment</button>
          <button type="button" data-choice="block" aria-pressed="false">Block card</button>
          <button type="button" data-choice="call" aria-pressed="false">Call customer</button>
        </div>
        <p class="error" role="alert" data-error="choice" hidden>⚠ Please choose release, block or call</p>
        <label for="reason-{id}">Short reason</label>
        <textarea id="reason-{id}" rows="2" maxlength="200" data-reason aria-describedby="reason-error-{id}"></textarea>
        <p class="error" role="alert" id="reason-error-{id}" data-error="reason" hidden>⚠ Please enter a reason</p>
        <button type="button" class="primary" data-save>Save decision</button>
        <p class="hint">A saved decision is final and cannot be edited.</p>
      </div>
      <div class="decision-result" role="status" tabindex="-1" hidden></div>
    </div>
  </section>""".format(
        id=aid,
        time=escape(p["time"]),
        amount=escape(format_amount(p["amount_eur"])),
        merchant=escape(p["merchant"]),
        country=escape(p["country"]),
        channel=escape(p["channel"]),
        customer=escape(alert["customer_id"]),
        funds=funds,
        analyst=escape(alert["assigned_analyst_id"]),
        claims=render_claims(alert, results),
        previous_devices=render_previous_devices(alert),
        warning=escape(warning_line(results)),
        warning_class=warning_class,
        weights=render_weights(alert),
    )


def render():
    """Return the full HTML page as a string (used by build and by the test)."""
    alerts = load_alerts()
    template = TEMPLATE_FILE.read_text(encoding="utf-8")
    page = template.replace("{{ALERT_ROWS}}", "\n".join(render_row(a) for a in alerts))
    page = page.replace("{{ALERT_VIEWS}}", "\n\n".join(render_view(a) for a in alerts))
    return page


def main():
    OUTPUT_FILE.write_text(render(), encoding="utf-8")
    print("Wrote {} ({} alerts)".format(OUTPUT_FILE.relative_to(ROOT), len(load_alerts())))


if __name__ == "__main__":
    main()
