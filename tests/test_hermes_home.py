from __future__ import annotations

import os
import unittest
from pathlib import Path
from unittest.mock import patch

from oracle import hermes_home as hm


class HermesHome(unittest.TestCase):
  def test_fallback_uses_hermes_home_env(self):
      with patch.object(hm, "__name__", hm.__name__):
          with patch.dict(
              "sys.modules",
              {"hermes_constants": None},
              clear=False,
          ):
              # Force ImportError path inside hermes_home()
              original_import = __builtins__.__import__ if hasattr(__builtins__, "__import__") else __import__

              def block_hermes_constants(name, *args, **kwargs):
                  if name == "hermes_constants":
                      raise ImportError("test")
                  return original_import(name, *args, **kwargs)

              with patch.dict(os.environ, {"HERMES_HOME": "/tmp/hermes-test"}, clear=False):
                  with patch("builtins.__import__", side_effect=block_hermes_constants):
                      self.assertEqual(hm.hermes_home(), Path("/tmp/hermes-test"))


if __name__ == "__main__":
    unittest.main()