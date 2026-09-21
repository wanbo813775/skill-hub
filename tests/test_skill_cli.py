from __future__ import annotations

import os
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
CLI = ROOT / "scripts" / "skill"


class SkillCliTest(unittest.TestCase):
    def run_cli(self, *args: str, home: Path | None = None, expected: int = 0):
        env = os.environ.copy()
        if home is not None:
            env["HOME"] = str(home)
        result = subprocess.run(
            [str(CLI), *args],
            cwd=ROOT,
            env=env,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(expected, result.returncode, result.stderr)
        return result

    def test_validate_and_search(self):
        self.assertIn("校验通过", self.run_cli("validate").stdout)
        self.assertIn("spring-boot-review", self.run_cli("search", "spring").stdout)
        self.assertIn("没有找到 Skill", self.run_cli("search", "missing-query").stdout)

    def test_install_update_and_uninstall_user_skill(self):
        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory)
            destination = home / ".agents" / "skills" / "spring-boot-review"

            self.run_cli("install", "spring-boot-review", "--target", "codex", home=home)
            self.assertTrue((destination / "SKILL.md").is_file())

            duplicate = self.run_cli(
                "install", "spring-boot-review", "--target", "codex", home=home, expected=1
            )
            self.assertIn("目标已存在", duplicate.stderr)

            self.run_cli("update", "spring-boot-review", "--target", "codex", home=home)
            self.run_cli(
                "uninstall", "spring-boot-review", "--target", "codex", "--yes", home=home
            )
            self.assertFalse(destination.exists())

    def test_install_all_project_targets(self):
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            self.run_cli(
                "install",
                "spring-boot-review",
                "--target",
                "all",
                "--scope",
                "project",
                "--project-dir",
                str(project),
            )
            self.assertTrue((project / ".agents/skills/spring-boot-review/SKILL.md").is_file())
            self.assertTrue((project / ".claude/skills/spring-boot-review/SKILL.md").is_file())
            self.assertTrue((project / ".dsh/skills/spring-boot-review/SKILL.md").is_file())


if __name__ == "__main__":
    unittest.main()
