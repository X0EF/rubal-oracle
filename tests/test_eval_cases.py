from __future__ import annotations

import json
import unittest
from pathlib import Path

from oracle.engine import (
    MemoryStore,
    commit,
    mirror,
    oracle_backfill,
    pre_llm_call,
    respond_track,
    revise,
    settle,
    slash,
)

_FIXTURES_DIR = Path(__file__).parent / "fixtures"
FIXTURES = json.loads((_FIXTURES_DIR / "cases.json").read_text(encoding="utf-8"))
_HACKATHON = json.loads(
    (_FIXTURES_DIR / "hackathon_use_case.json").read_text(encoding="utf-8")
)
_ALL_CASES = FIXTURES["cases"] + _HACKATHON["cases"]
CASES = {c["id"]: c for c in _ALL_CASES}
DEFAULT_NOW = FIXTURES["now"]

SYNTHETIC = {
    "settle-git-success-from-class": {
        "setup": ["capture-git-ship-with-class"],
        "then": "settle-git-success",
    }
}


def _run_case(case: dict, store: MemoryStore, sources_override=None):
    now = case.get("now", DEFAULT_NOW)
    sources = sources_override if sources_override is not None else case.get("sources", {})
    surface = case["surface"]
    if surface == "tool":
        tool = case["tool"]
        args = dict(case.get("input") or {})
        if args.get("id") == "$last_id":
            args["id"] = store.last_id
        if tool == "oracle_commit":
            return commit(args, sources=sources, store=store, now=now)
        if tool == "oracle_settle":
            return settle(args, sources=sources, store=store, now=now)
        if tool == "oracle_revise":
            return revise(args, store=store, now=now)
        if tool == "oracle_mirror":
            return mirror(store)
        if tool == "oracle_respond_track":
            return respond_track(args, sources=sources, store=store, now=now)
        if tool == "oracle_backfill":
            return oracle_backfill(args, sources=sources, store=store)
        raise AssertionError(f"unknown tool {tool}")
    if surface == "pre_llm_call":
        state = case.get("state") or {}
        return pre_llm_call(
            case["input"],
            store=store,
            now=now,
            slipping=bool(state.get("slipping")),
            decision_point=bool(state.get("decision_point")),
            receptive=state.get("receptive") if "receptive" in state else True,
        )
    if surface == "slash":
        return slash(case["raw_args"], store=store, sources=sources, now=now)
    raise AssertionError(f"unknown surface {surface}")


def _apply_setup(setup_ids: list, store: MemoryStore) -> None:
    for sid in setup_ids:
        if sid in SYNTHETIC:
            spec = SYNTHETIC[sid]
            _apply_setup(spec["setup"], store)
            then = CASES[spec["then"]]
            _run_case(then, store, sources_override=then.get("sources"))
            continue
        prior = CASES[sid]
        _apply_setup(prior.get("setup") or [], store)
        _run_case(prior, store)


def _assert_expect(test: unittest.TestCase, result, expect: dict, store: MemoryStore) -> None:
    if "ok" in expect:
        test.assertIs(result["ok"], expect["ok"])
    if "refused" in expect:
        test.assertIs(result.get("refused"), expect["refused"])
    if "saved" in expect:
        saved = bool(store.commitments)
        if expect["saved"]:
            test.assertTrue(saved)
            test.assertIs(result.get("ok"), True)
        else:
            test.assertFalse(saved)
    if "code" in expect:
        test.assertEqual(result.get("code"), expect["code"])
    if "how_to_make_saveable_contains" in expect:
        blob = (result.get("how_to_make_saveable") or result.get("reason") or "")
        test.assertIn(expect["how_to_make_saveable_contains"].lower(), blob.lower())
    if "commitment.status" in expect:
        c = result.get("commitment") or store.commitments[-1]
        test.assertEqual(c["status"], expect["commitment.status"])
    if "commitment.settler.kind" in expect:
        c = result.get("commitment") or store.commitments[-1]
        test.assertEqual(c["settler"]["kind"], expect["commitment.settler.kind"])
    if "forecast.probability" in expect:
        f = result.get("forecast") or store.forecasts[-1]
        test.assertEqual(f.get("probability"), expect["forecast.probability"])
    if "forecast.uncertainty" in expect:
        f = result.get("forecast") or store.forecasts[-1]
        test.assertEqual(f.get("uncertainty"), expect["forecast.uncertainty"])
    if "forecast.comparisons" in expect:
        f = result.get("forecast") or store.forecasts[-1]
        test.assertEqual(f.get("comparisons"), expect["forecast.comparisons"])
    if "forecast.comparisons_len" in expect:
        f = result.get("forecast") or store.forecasts[-1]
        test.assertEqual(len(f.get("comparisons") or []), expect["forecast.comparisons_len"])
    if "forecast.reasons_mention" in expect:
        f = result.get("forecast") or store.forecasts[-1]
        reasons = " ".join(f.get("reasons") or [])
        test.assertIn(expect["forecast.reasons_mention"].lower(), reasons.lower())
    if "action_block" in expect:
        blocked = isinstance(result, dict) and result.get("action") == "block"
        test.assertFalse(blocked)
        test.assertIs(expect["action_block"], False)
    if "has_context" in expect:
        ctx = (result or {}).get("context") if isinstance(result, dict) else None
        test.assertIs(bool(ctx), expect["has_context"])
    if "context_contains" in expect:
        ctx = (result or {}).get("context") if isinstance(result, dict) else ""
        for needle in expect["context_contains"]:
            test.assertIn(needle.lower(), ctx.lower())
    if "offer_subtract" in expect:
        ctx = ((result or {}).get("context") if isinstance(result, dict) else "") or ""
        test.assertIs("subtract" in ctx.lower(), expect["offer_subtract"])
    if "outcome" in expect:
        test.assertEqual(result.get("outcome"), expect["outcome"])
    if "not_outcome" in expect:
        test.assertNotEqual(result.get("outcome"), expect["not_outcome"])
    if "original.status" in expect:
        test.assertEqual(store.commitments[0]["status"], expect["original.status"])
    if "original.success_criteria_unchanged" in expect:
        test.assertEqual(
            store.commitments[0]["success_criteria"],
            CASES["capture-git-ship-no-class"]["input"]["success_criteria"],
        )
    if "revision.status" in expect:
        test.assertEqual(store.commitments[-1]["status"], expect["revision.status"])
    if "revision.original_id" in expect:
        test.assertEqual(store.commitments[-1]["original_id"], store.commitments[0]["id"])
    if "n_resolved_numeric" in expect:
        test.assertEqual(result.get("n_resolved_numeric"), expect["n_resolved_numeric"])
    if "brier" in expect:
        test.assertAlmostEqual(result.get("brier"), expect["brier"])
    if "claims_calibration" in expect:
        test.assertIs(result.get("claims_calibration"), expect["claims_calibration"])
    if "count" in expect:
        test.assertEqual(result.get("count"), expect["count"])
    if "declined" in expect:
        test.assertIs(result.get("declined"), expect["declined"])
    if "text_contains" in expect:
        text = result if isinstance(result, str) else json.dumps(result)
        for needle in expect["text_contains"]:
            test.assertIn(needle.lower(), text.lower())


def _make_test(case_id: str):
    def test(self):
        case = CASES[case_id]
        store = MemoryStore()
        _apply_setup(case.get("setup") or [], store)
        result = _run_case(case, store)
        _assert_expect(self, result, case["expect"], store)

    test.__name__ = f"test_{case_id.replace('-', '_')}"
    test.__doc__ = case_id
    return test


class EvalCases(unittest.TestCase):
    pass


for _cid in [c["id"] for c in _ALL_CASES]:
    setattr(EvalCases, f"test_{_cid.replace('-', '_')}", _make_test(_cid))


if __name__ == "__main__":
    unittest.main()
