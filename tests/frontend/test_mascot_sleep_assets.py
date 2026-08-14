"""Regression checks for the registered KitCode sleep sprite frames."""

from __future__ import annotations

import unittest
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[2]
MASCOTS = ROOT / "public" / "mascots"


class SleepSpriteRegistrationTests(unittest.TestCase):
    def test_all_sleep_frames_share_one_pose_box_and_ground_anchor(self) -> None:
        """The entire sleep sequence must not zoom or drift between drawings."""
        for index in range(1, 9):
            with Image.open(MASCOTS / f"kit-sleep-{index:02d}.webp") as image:
                rgba = image.convert("RGBA")
                self.assertEqual(rgba.size, (512, 512))
                bbox = rgba.getchannel("A").getbbox()

            self.assertIsNotNone(bbox, f"sleep frame {index} has visible art")
            assert bbox is not None
            visible_height = bbox[3] - bbox[1]
            self.assertGreaterEqual(visible_height, 359, f"sleep frame {index}")
            self.assertLessEqual(visible_height, 361, f"sleep frame {index}")
            self.assertGreaterEqual(bbox[3], 483, f"sleep frame {index}")
            self.assertLessEqual(bbox[3], 485, f"sleep frame {index}")


if __name__ == "__main__":
    unittest.main()
