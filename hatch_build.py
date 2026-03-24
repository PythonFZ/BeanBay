"""Hatch custom build hook -- builds the React frontend into the Python package."""

import os
import subprocess
from pathlib import Path

from hatchling.builders.hooks.plugin.interface import BuildHookInterface


class CustomBuildHook(BuildHookInterface):
    """Build the frontend with bun and place output in src/beanbay/static/."""

    def initialize(self, version: str, build_data: dict) -> None:
        """Run the frontend build if static assets are not already present.

        Parameters
        ----------
        version : str
            The resolved package version string.
        build_data : dict
            Mutable mapping of build metadata.
        """
        root = Path(self.root)
        static_dir = root / "src" / "beanbay" / "static"
        manifest = static_dir / ".vite" / "manifest.json"

        if manifest.is_file():
            return

        frontend_dir = root / "frontend"
        if not frontend_dir.is_dir():
            return

        env = {**os.environ, "VITE_APP_VERSION": version}
        subprocess.run(["bun", "install"], cwd=frontend_dir, check=True, env=env)
        subprocess.run(
            [
                "bun",
                "run",
                "--",
                "vite",
                "build",
                "--outDir",
                str(static_dir),
                "--emptyOutDir",
            ],
            cwd=frontend_dir,
            check=True,
            env=env,
        )
