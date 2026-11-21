import importlib.util
from pathlib import Path
import unittest

SCRIPT=Path(__file__).resolve().parents[1]/'scripts'/'validate_reference.py'
spec=importlib.util.spec_from_file_location('validate_reference',SCRIPT)
mod=importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

class ReferenceIntegrityTest(unittest.TestCase):
    def test_immutable_benchmark_is_intact(self):
        self.assertEqual([],mod.check())
    def test_benchmark_manifest_is_not_empty(self):
        self.assertGreater((mod.REF/'REFERENCE_MANIFEST.json').stat().st_size,200)

if __name__=='__main__': unittest.main()
