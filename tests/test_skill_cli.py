from __future__ import annotations

import os
import shutil
import subprocess
import tarfile
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
        self.assertIn("alibaba-java-guidelines", self.run_cli("list").stdout)
        self.assertIn("alibaba-java-guidelines", self.run_cli("search", "阿里巴巴").stdout)
        self.assertIn("没有找到 Skill", self.run_cli("search", "missing-query").stdout)

    def test_unknown_skill_is_rejected(self):
        result = self.run_cli("install", "not-registered", expected=1)
        self.assertIn("找不到 Skill", result.stderr)

    def test_install_update_and_uninstall_user_skill(self):
        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory)
            destination = home / ".agents" / "skills" / "alibaba-java-guidelines"

            self.run_cli("install", "alibaba-java-guidelines", "--target", "codex", home=home)
            self.assertTrue((destination / "SKILL.md").is_file())
            self.assertTrue((destination / "references" / "mysql.md").is_file())

            duplicate = self.run_cli(
                "install", "alibaba-java-guidelines", "--target", "codex", home=home, expected=1
            )
            self.assertIn("目标已存在", duplicate.stderr)

            self.run_cli("update", "alibaba-java-guidelines", "--target", "codex", home=home)
            self.run_cli(
                "uninstall", "alibaba-java-guidelines", "--target", "codex", "--yes", home=home
            )
            self.assertFalse(destination.exists())

    def test_install_all_project_targets(self):
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            self.run_cli(
                "install",
                "alibaba-java-guidelines",
                "--target",
                "all",
                "--scope",
                "project",
                "--project-dir",
                str(project),
            )
            relative = "skills/alibaba-java-guidelines/SKILL.md"
            self.assertTrue((project / ".agents" / relative).is_file())
            self.assertTrue((project / ".claude" / relative).is_file())
            self.assertTrue((project / ".dsh" / relative).is_file())

    def test_global_cli_downloads_skill_from_remote_repository(self):
        with tempfile.TemporaryDirectory() as directory:
            sandbox = Path(directory)
            remote = sandbox / "remote"
            remote.mkdir()
            shutil.copy2(ROOT / "registry.json", remote / "registry.json")

            archive = remote / "repository.tar.gz"
            skill_name = "alibaba-java-guidelines"
            with tarfile.open(archive, "w:gz") as bundle:
                bundle.add(
                    ROOT / "skills" / skill_name,
                    arcname=f"skill-hub-main/skills/{skill_name}",
                )

            home = sandbox / "home"
            bin_dir = home / ".local" / "bin"
            home.mkdir()
            env = os.environ.copy()
            env.update(
                {
                    "HOME": str(home),
                    "SKILL_HUB_BIN_DIR": str(bin_dir),
                    "SKILL_HUB_CLI_URL": CLI.as_uri(),
                    "SKILL_HUB_REGISTRY_URL": (remote / "registry.json").as_uri(),
                    "SKILL_HUB_ARCHIVE_URL": archive.as_uri(),
                }
            )

            bootstrap = subprocess.run(
                ["bash", str(ROOT / "scripts" / "install-cli.sh")],
                cwd=sandbox,
                env=env,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(0, bootstrap.returncode, bootstrap.stderr)

            installed_cli = bin_dir / "skill"
            self.assertTrue(installed_cli.is_file())
            result = subprocess.run(
                [str(installed_cli), "install", skill_name, "--target", "codex"],
                cwd=sandbox,
                env=env,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(0, result.returncode, result.stderr)
            installed_skill = home / ".agents" / "skills" / skill_name
            self.assertTrue((installed_skill / "SKILL.md").is_file())
            self.assertTrue((installed_skill / "references" / "mysql.md").is_file())


if __name__ == "__main__":
    unittest.main()
