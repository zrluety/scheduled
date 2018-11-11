import os

from scheduled.utils import load_profile

TEST_DIR = os.path.dirname(os.path.dirname(__file__))
RESOURCES_DIR = os.path.join(os.path.dirname(TEST_DIR), 'resources')
ASSETMARK_STATEMENT = os.path.join(RESOURCES_DIR, '2015Q1 6073-ModernAuto.pdf')

def test_resources_dir_is_found():
    assert os.path.exists(RESOURCES_DIR)

def test_assetmark_pdf_is_found():
    assert os.path.exists(ASSETMARK_STATEMENT)

def test_assetmark_profile_exists():
    profile = load_profile('AssetMark')
    assert profile is not None


