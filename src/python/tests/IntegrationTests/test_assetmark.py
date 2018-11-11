import os

from manager import TEST_DATA_DIR
from scheduled.utils import load_profile


def test_assetmark_pdf_is_found():
    ASSETMARK_STATEMENT = os.path.join(TEST_DATA_DIR, '2015Q1 6073-ModernAuto.pdf')
    assert os.path.exists(ASSETMARK_STATEMENT)

def test_assetmark_profile_exists():
    profile = load_profile('AssetMark')
    assert profile is not None


