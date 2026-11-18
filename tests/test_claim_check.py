"""Automated check of the claim-check logic (D9, D19, D32).

Runs without a browser and without Node.js:
    python3 -m unittest discover -s tests -v
"""

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "app"))

from claim_check import (  # noqa: E402
    MATCH,
    MISMATCH,
    NOT_AVAILABLE,
    check_alert,
    check_claim,
    warning_line,
)

ALERTS_FILE = ROOT / "app" / "data" / "alerts.json"


def load_alert(alert_id):
    data = json.loads(ALERTS_FILE.read_text(encoding="utf-8"))
    for alert in data["alerts"]:
        if alert["id"] == alert_id:
            return alert
    raise AssertionError("Alert {} not found in alerts.json".format(alert_id))


class ClaimRules(unittest.TestCase):
    """The 4 rule cases of D19."""

    def test_yesno_different_is_mismatch(self):
        claim = {"type": "yesno", "claimed": False, "record": True}
        self.assertEqual(check_claim(claim), MISMATCH)

    def test_number_more_than_25_percent_away_is_mismatch(self):
        claim = {"type": "number", "claimed": 6.0, "record": 2.1}
        self.assertEqual(check_claim(claim), MISMATCH)

    def test_missing_record_is_not_available(self):
        claim = {"type": "yesno", "claimed": False, "record": None}
        self.assertEqual(check_claim(claim), NOT_AVAILABLE)

    def test_otherwise_match(self):
        self.assertEqual(check_claim({"type": "yesno", "claimed": True, "record": True}), MATCH)
        self.assertEqual(check_claim({"type": "number", "claimed": 4.0, "record": 4.2}), MATCH)

    def test_exactly_25_percent_is_still_match(self):
        # D19 says "more than 25 %" - exactly 25 % is not a mismatch.
        self.assertEqual(check_claim({"type": "number", "claimed": 5.0, "record": 4.0}), MATCH)


class AlertA1042(unittest.TestCase):
    """Acceptance row 2: A-1042 shows ✗ for "new device" and "6 times"."""

    def test_new_device_and_6_times_are_mismatch(self):
        alert = load_alert("A-1042")
        results = dict(zip((c["field"] for c in alert["claims"]), check_alert(alert)))
        self.assertEqual(results["device_known"], MISMATCH)
        self.assertEqual(results["amount_vs_average"], MISMATCH)

    def test_warning_line_says_2_of_3_not_confirmed(self):
        alert = load_alert("A-1042")
        self.assertIn("2 of 3 not confirmed", warning_line(check_alert(alert)))


class GeneratedHtml(unittest.TestCase):
    """The shipped index.html shows what the rules say (D30, handover 04 step 2)."""

    INDEX_FILE = ROOT / "index.html"

    def setUp(self):
        self.assertTrue(self.INDEX_FILE.exists(), "index.html missing - run: python3 app/build.py")
        self.html = self.INDEX_FILE.read_text(encoding="utf-8")

    def test_index_html_is_up_to_date(self):
        import build  # app/ is on sys.path

        self.assertEqual(
            self.html, build.render(),
            "index.html is out of date - run: python3 app/build.py",
        )

    def test_a1042_shows_both_mismatch_marks(self):
        start = self.html.index('id="alert-A-1042"')
        section = self.html[start:self.html.index("</section>", start)]
        for field in ("device_known", "amount_vs_average"):
            self.assertRegex(
                section,
                r'data-field="{}" data-result="mismatch">.*?✗ mismatch'.format(field),
            )


    def test_no_status_before_the_analysts_click(self):
        # Acceptance row 3 (D14): the generated page starts with every alert open.
        import re

        cells = re.findall(r'<td [^>]*class="status-cell">(.*?)</td>', self.html)
        self.assertEqual(cells, ["open", "open", "open"])


class States(unittest.TestCase):
    """Round 2 states (D23 b, D24, D25). The tests prove the texts are in the
    page; that JavaScript shows them at the right moment is a manual check."""

    def setUp(self):
        self.html = (ROOT / "index.html").read_text(encoding="utf-8")

    def section(self, alert_id):
        start = self.html.index('id="alert-{}"'.format(alert_id))
        return self.html[start:self.html.index("</section>", start)]

    def test_empty_list_message_present_and_hidden_at_start(self):
        self.assertRegex(self.html, r'id="empty-message" role="status" hidden>.*No open alerts')

    def test_please_enter_a_reason_for_every_alert(self):
        self.assertEqual(self.html.count("Please enter a reason"), 3)

    def test_reload_note_visible(self):
        self.assertRegex(
            self.html,
            r'<p class="demo-note">Demo – decisions are lost when the page is reloaded\.</p>',
        )

    def test_a1044_shows_previous_devices_label_and_list(self):
        section = self.section("A-1044")
        self.assertIn("previous devices, not from this payment", section)
        self.assertEqual(section.count("known since"), 2)
        # No marks on the devices list (D25).
        devices = section[section.index('class="previous-devices"'):]
        devices = devices[:devices.index("</div>")]
        self.assertNotIn("mark", devices)

    def test_previous_devices_only_when_device_data_missing(self):
        for alert_id in ("A-1042", "A-1043"):
            self.assertNotIn("previous devices", self.section(alert_id))


class PhoneAndKeyboard(unittest.TestCase):
    """D26 - only the building blocks can be checked here; the look at
    390 px and the Tab order are checked by a person in Chrome and on a phone."""

    def setUp(self):
        self.html = (ROOT / "index.html").read_text(encoding="utf-8")

    def test_viewport_and_phone_layout_rule(self):
        self.assertIn('name="viewport" content="width=device-width, initial-scale=1"', self.html)
        self.assertIn("@media (max-width: 600px)", self.html)

    def test_every_table_cell_has_a_label_for_the_stacked_layout(self):
        import re

        cells = re.findall(r"<td( [^>]*)?>", self.html)
        labelled = [c for c in cells if "data-label" in (c or "")]
        # 3 list cells without label = the Open buttons; all others labelled.
        self.assertEqual(len(cells) - len(labelled), 3)

    def test_visible_focus_outline(self):
        self.assertIn("button:focus-visible, textarea:focus-visible { outline: 3px solid", self.html)

    def test_decision_controls_are_real_buttons_and_textarea(self):
        # Native <button>/<textarea> are reachable with Tab without extra code.
        self.assertEqual(self.html.count('<button type="button" data-choice='), 9)
        self.assertEqual(self.html.count("<textarea "), 3)
        self.assertEqual(self.html.count('<button type="button" class="primary" data-save>'), 3)


class M4Fixes(unittest.TestCase):
    """M4.1 review fixes R1-R3 (handover 07, approved by Mohammad (AI PM) in chat)."""

    def setUp(self):
        self.html = (ROOT / "index.html").read_text(encoding="utf-8")

    def section(self, alert_id):
        start = self.html.index('id="alert-{}"'.format(alert_id))
        return self.html[start:self.html.index("</section>", start)]

    def test_r1_list_heading_is_alerts(self):
        self.assertIn('<h2 id="list-title" tabindex="-1">Alerts</h2>', self.html)
        self.assertNotIn(">Open alerts<", self.html)

    def test_r2_selected_choice_has_symbol_not_colour_only(self):
        self.assertIn('button[aria-pressed="true"]::before { content: "✓ "', self.html)

    def test_r3_warning_line_neutral_only_when_all_confirmed(self):
        self.assertIn('class="warning-line warning-line-ok"', self.section("A-1043"))
        for alert_id in ("A-1042", "A-1044"):
            self.assertIn('<p class="warning-line">', self.section(alert_id))


if __name__ == "__main__":
    unittest.main()
