import argparse
from datetime import datetime
import importlib.util
import json
from pathlib import Path
import platform
import socket
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "host_facts.py"
SPEC = importlib.util.spec_from_file_location("host_facts", SCRIPT)
host_facts = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(host_facts)


class HostFactsTests(unittest.TestCase):
    def test_real_local_observations(self):
        facts = host_facts.collect_facts()
        self.assertEqual(facts["hostname_hint"], socket.gethostname())
        self.assertEqual(facts["os"]["system"], platform.system())
        self.assertEqual(facts["status"], "observed")
        self.assertEqual(facts["execution_scope"], "local-process-host")
        self.assertIsNotNone(datetime.fromisoformat(facts["observed_at_utc"]).tzinfo)

    def test_discovery_does_not_confirm_binding(self):
        for label in (None, "work-linux-01"):
            facts = host_facts.collect_facts(label)
            self.assertEqual(facts["proposed_host_id"], label)
            self.assertIs(facts["host_binding_confirmed"], False)

    def test_tool_presence_is_boolean_not_command_output(self):
        tools = host_facts.collect_facts()["tools_on_path"]
        self.assertEqual(set(tools), set(host_facts.TOOLS))
        self.assertTrue(all(type(value) is bool for value in tools.values()))

    def test_rejects_unsafe_or_ambiguous_labels(self):
        for label in ("", "../host", "/host", "-host", "a b", "Host", "é", "a" * 64):
            with self.subTest(label=label), self.assertRaises(argparse.ArgumentTypeError):
                host_facts.collect_facts(label)

    def test_cli_json_from_unrelated_directory_without_files(self):
        with tempfile.TemporaryDirectory() as directory:
            result = subprocess.run(
                [sys.executable, str(SCRIPT), "--host-id", "test-host"],
                cwd=directory, capture_output=True, text=True, check=True,
            )
            facts = json.loads(result.stdout)
            self.assertEqual(facts["proposed_host_id"], "test-host")
            self.assertEqual(result.stderr, "")
            self.assertEqual(list(Path(directory).iterdir()), [])

    def test_cli_invalid_label_fails_without_json(self):
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "--host-id", "../host"],
            capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, "")


if __name__ == "__main__":
    unittest.main()