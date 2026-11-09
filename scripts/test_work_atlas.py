"""Data-contract checks for the profile graph; no third-party dependencies."""

import copy
import json
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET

from work_atlas import TOOLS, build_atlas, model


class WorkAtlasTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.snapshot = json.loads((Path(__file__).resolve().parents[1] / "assets/profile-data.json").read_text())
        cls.graph = model(cls.snapshot)
        cls.nodes = {node["id"]: node for node in cls.graph["nodes"]}

    def test_every_project_is_represented_and_forks_are_excluded(self):
        expected = {r["name"] for r in self.snapshot["repositories"]
                    if not r["fork"] and r["name"] != self.snapshot["user"]}
        actual = {n["name"] for n in self.nodes.values() if n["kind"] == "repository"}
        self.assertEqual(expected, actual)
        self.assertEqual(len(actual), self.graph["summary"]["repositories"])

    def test_relationships_have_real_endpoints_and_documented_tools(self):
        edges = self.graph["edges"]
        self.assertEqual(len(edges), len({e["id"] for e in edges}))
        self.assertEqual(len(edges), self.graph["summary"]["connections"])
        for edge in edges:
            self.assertIn(edge["source"], self.nodes)
            self.assertIn(edge["target"], self.nodes)
            if edge["kind"] == "tool":
                repo = self.nodes[edge["target"]]["name"]
                tool = self.nodes[edge["source"]]["name"]
                self.assertIn(tool, TOOLS[repo])
                self.assertTrue(edge["evidence"])
                self.assertTrue(edge["url"].endswith("#readme"))

    def test_exactly_one_primary_language_link_per_repository(self):
        for node in self.nodes.values():
            if node["kind"] == "repository":
                links = [e for e in self.graph["edges"] if e["target"] == node["id"] and e["kind"] == "language"]
                self.assertEqual(len(links), 1)
                language = self.nodes[links[0]["source"]]["name"]
                self.assertEqual(language, node["language"] or "No language detected")

    def test_future_repositories_do_not_gain_invented_frameworks(self):
        snapshot = copy.deepcopy(self.snapshot)
        snapshot["repositories"].append({"name": "a-new-rust-project", "language": "Rust", "fork": False})
        graph = model(snapshot)
        project = next(n for n in graph["nodes"] if n["id"] == "repo:a-new-rust-project")
        self.assertEqual(project["group"], "other")
        links = [e for e in graph["edges"] if e["target"] == project["id"]]
        self.assertEqual([e["kind"] for e in links], ["language"])

    def test_optional_redis_is_identified(self):
        edge = next(e for e in self.graph["edges"]
                    if e["source"] == "tool:Redis" and e["target"] == "repo:URLShortener")
        self.assertTrue(edge["optional"])
        self.assertIn("Optional", edge["evidence"])

    def test_exports_are_deterministic_and_standalone(self):
        files = build_atlas(self.snapshot)
        self.assertEqual(files, build_atlas(self.snapshot))
        root = ET.fromstring(files["work-atlas.svg"])
        self.assertEqual(len(root.findall(".//*[@data-node]")), len(self.nodes))
        self.assertNotIn("<script", files["work-atlas.svg"])
        self.assertNotIn("__ATLAS_", files["work-atlas.html"])
        self.assertNotIn('<script src=', files["work-atlas.html"])


if __name__ == "__main__":
    unittest.main()
