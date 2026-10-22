"""Regression checks for the map's identity, aliases, and lineage rules."""

import json
import unittest
from pathlib import Path

from field_map_curation import NAMED_BRANCHES, RELATED_PEERS, SAME_EVENT, SEQUELS, VISIBLE_ALIASES, audit_near_duplicates, audit_shared_first_statements, audit_shared_roots, audit_visible_aliases, norm
from field_map_taxonomy import LANES


ROOT = Path(__file__).resolve().parents[1]


class FieldMapCurationTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        page = (ROOT / "public/field-emergence-explorer.html").read_text()
        cls.events = json.loads(page.split("const D=", 1)[1].split(";\nconst REDIRECTS=", 1)[0])
        cls.edges = json.loads(page.split("const EDGES=", 1)[1].split(";\n", 1)[0])
        cls.by_id = {e["pid"]: e for e in cls.events}
        cls.raw = json.loads((ROOT / "public/field-emergence-milestones.json").read_text())["events"]

    def test_every_shared_source_root_has_an_identity_decision(self):
        audit_shared_roots([{"id": e["eventId"], "pid": e.get("pid", e["eventId"])} for e in self.raw])
        self.assertEqual(len(self.events), len(self.raw) - len(SAME_EVENT))
        for duplicate, primary in SAME_EVENT.items():
            self.assertNotIn(duplicate, self.by_id)
            self.assertIn(duplicate, self.by_id[primary]["mergedPids"])

    def test_same_period_name_overlaps_are_reviewed(self):
        raw_map = []
        for event in self.raw:
            pid = event.get("pid", event["eventId"])
            mapped = self.by_id.get(pid)
            if mapped:
                raw_map.append({"pid": pid, "name": mapped["name"], "y": mapped["y"]})
        # The build itself checks the full pre-merge set; here we check the
        # published result remains free of unreviewed near duplicates.
        audit_near_duplicates(raw_map)
        audit_shared_first_statements(self.events)

    def test_merged_moonshine_has_both_sources_and_milestones(self):
        moonshine = self.by_id["P036"]
        self.assertEqual(moonshine["name"], "Monstrous moonshine")
        self.assertEqual(set(moonshine["sourceIds"]), {"E44", "QC55", "WC37"})
        self.assertTrue(any(m["y"] == 1979 for m in moonshine["ms"]))
        self.assertTrue(any(m["y"] == 1992 for m in moonshine["ms"]))

    def test_measure_rigidity_overlap_is_one_event(self):
        event = self.by_id["P079"]
        self.assertNotIn("P329", self.by_id)
        self.assertEqual(set(event["sourceIds"]), {"B13", "WC47"})
        self.assertTrue(any("Littlewood" in m["l"] for m in event["ms"]))

    def test_conjecture_and_solution_stay_distinct_and_connected(self):
        edge_pairs = {(a, b) for a, b, _ in self.edges}
        for pair in SEQUELS:
            self.assertIn(pair[0], self.by_id)
            self.assertIn(pair[1], self.by_id)
            self.assertIn(pair, edge_pairs)

    def test_named_lineage_without_broad_name_false_positive(self):
        edge_pairs = {(a, b) for a, b, _ in self.edges}
        self.assertIn(("P026", "P058"), edge_pairs)
        self.assertFalse(("P399", "P026") in edge_pairs, "Differential Galois theory is not a Langlands precursor")
        self.assertIn(("P036", "P550"), edge_pairs)
        self.assertIn(("P036", "P274"), edge_pairs)

    def test_explicit_field_context_is_separate_and_visible(self):
        links = {(a, b): kind for a, b, kind in self.edges}
        for pair in [("P004", "P254"), ("P007", "P251"), ("P012", "P396"), ("P021", "P211")]:
            self.assertEqual(links[pair], "context")
        for pair in NAMED_BRANCHES:
            self.assertIn(links[pair], {"feeds", "named", "same"})
            self.assertLessEqual(self.by_id[pair[0]]["y"], self.by_id[pair[1]]["y"])
            if self.by_id[pair[0]]["y"] == self.by_id[pair[1]]["y"]:
                self.assertEqual(links[pair], "same")
        for a, b in RELATED_PEERS:
            self.assertEqual(links.get((a, b)), "same")
        for a, b, kind in self.edges:
            outgoing = [r for r in self.by_id[a]["rel"]["a"] if r["p"] == b]
            incoming = [r for r in self.by_id[b]["rel"]["b"] if r["p"] == a]
            if kind == "same":
                self.assertTrue(any(r["p"] == b for r in self.by_id[a]["rel"]["s"]))
                self.assertTrue(any(r["p"] == a for r in self.by_id[b]["rel"]["s"]))
            else:
                self.assertTrue(any(r["t"] == kind for r in outgoing), (a, b, kind))
                self.assertTrue(any(r["t"] == kind for r in incoming), (a, b, kind))

    def test_all_events_have_a_reviewed_field_lane_and_unlinked_disposition(self):
        self.assertTrue(all(e["cl"] in LANES for e in self.events))
        self.assertFalse(any(e["cl"] == "Other fields" for e in self.events))
        self.assertEqual(self.by_id["P004"]["cl"], "Graph theory")
        self.assertEqual(self.by_id["P249"]["cl"], "Information & cryptography")
        self.assertEqual(self.by_id["P307"]["cl"], "Number theory")
        incident = {pid for a, b, _ in self.edges for pid in (a, b)}
        remaining = {e["pid"] for e in self.events if e["pid"] not in incident}
        reviewed = json.loads((ROOT / "data/collection/field-map-unlinked-review.json").read_text())
        self.assertEqual(remaining, {item["pid"] for item in reviewed["remaining"]})
        self.assertTrue(all(item["reason"] for item in reviewed["remaining"]))

    def test_aliases_are_displayed_only_when_relevant(self):
        audit_visible_aliases(self.events)
        self.assertEqual(sum(len(e["aliases"]) for e in self.events), 46)
        langlands = self.by_id["P026"]
        self.assertEqual(langlands["aliases"], [])
        self.assertIn("Langlands conjectures", langlands["searchTerms"])
        self.assertEqual(self.by_id["P405"]["aliases"], ["multi-valued logic"])
        self.assertEqual(self.by_id["P127"]["aliases"], [])  # Ptolemy's theorem is not the Almagest
        for event in self.events:
            terms = [norm(a) for a in event["aliases"]]
            self.assertEqual(event["aliases"], VISIBLE_ALIASES.get(event["pid"], []))
            self.assertEqual(len(terms), len(set(terms)))
            self.assertNotIn(norm(event["name"]), terms)

    def test_no_dangling_links_or_stale_merged_dates(self):
        for a, b, _ in self.edges:
            self.assertIn(a, self.by_id)
            self.assertIn(b, self.by_id)
        for event in self.events:
            if event["mergedPids"]:
                self.assertEqual(event["y"], event["shown"]["conceptual"]["y"])

    def test_dates_do_not_promote_precursors_to_main_events(self):
        perelman = self.by_id["P045"]
        self.assertEqual(perelman["y"], 2002)
        self.assertTrue(any(m["r"] == "precursor" and m["y"] == 1982 for m in perelman["ms"]))
        self.assertTrue(any(m["r"] == "first_statement" and m["y"] == 2002 for m in perelman["ms"]))

    def test_p_adic_hodge_theory_bridges_earlier_and_later_work(self):
        event = self.by_id["P557"]
        self.assertEqual(event["y"], 1982)
        self.assertEqual(event["cl"], "Number theory")
        links = {(a, b) for a, b, _ in self.edges}
        self.assertIn(("P023", "P557"), links)
        self.assertIn(("P557", "P303"), links)
        self.assertIn(("P557", "P542"), links)

    def test_focused_subject_additions_are_sourced_and_connected(self):
        additions = json.loads((ROOT / "data/collection/field-map-focused-additions.json").read_text())["entries"]
        links = {(a, b) for a, b, _ in self.edges}
        for addition in additions:
            record = addition["record"]
            event = self.by_id[record["pid"]]
            self.assertNotEqual(event["cl"], "Other fields")
            self.assertEqual(event["y"], record["derivedDates"]["conceptual"]["start"])
            self.assertTrue(any((event["pid"] in (a, b)) for a, b in links))
            for milestone in record["milestones"]:
                self.assertTrue(all(source["url"].startswith("https://") for source in milestone["evidence"]))
            for link in addition["links"]:
                self.assertIn((link["from"], link["to"]), links)


if __name__ == "__main__":
    unittest.main()
