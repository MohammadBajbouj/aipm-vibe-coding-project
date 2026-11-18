"""Claim check (D19) - the only place the rules exist.

Each copilot reason is a structured claim (field + claimed value) that is
compared with the record value of the same field:

- record value missing                        -> NOT_AVAILABLE (⚠)
- yes/no fact, claimed differs from record     -> MISMATCH (✗)
- number more than 25 % away from the record   -> MISMATCH (✗)
  (distance measured relative to the record value; record 0 -> any other
  claimed number is a mismatch)
- otherwise                                    -> MATCH (✓)

Python 3.9 standard library only (D30).
"""

MATCH = "match"
NOT_AVAILABLE = "not_available"
MISMATCH = "mismatch"

NUMBER_TOLERANCE = 0.25  # D19: more than 25 % away = mismatch


def check_claim(claim):
    """Return MATCH, NOT_AVAILABLE or MISMATCH for one claim dict."""
    record = claim.get("record")
    claimed = claim.get("claimed")

    if record is None:
        return NOT_AVAILABLE

    if claim["type"] == "yesno":
        return MATCH if claimed == record else MISMATCH

    if claim["type"] == "number":
        if record == 0:
            return MATCH if claimed == 0 else MISMATCH
        distance = abs(claimed - record) / abs(record)
        return MISMATCH if distance > NUMBER_TOLERANCE else MATCH

    raise ValueError("Unknown claim type: {!r}".format(claim["type"]))


def check_alert(alert):
    """Return the list of results, one per claim, in the alert's order."""
    return [check_claim(claim) for claim in alert["claims"]]


def warning_line(results):
    """Warning line above the suggestion (D22), derived from the results."""
    total = len(results)
    mismatches = results.count(MISMATCH)
    missing = results.count(NOT_AVAILABLE)
    parts = []
    if mismatches:
        parts.append("{} of {} not confirmed by the records".format(mismatches, total))
    if missing:
        parts.append("{} of {} could not be checked (record not available)".format(missing, total))
    if not parts:
        parts.append("all {} confirmed by the records".format(total))
    return "Based on the copilot's reasons – " + "; ".join(parts)
