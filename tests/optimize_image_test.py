import pytest
import shutil

from pathlib import Path
from hooks.optimize_image import main


@pytest.mark.parametrize(
    ("image",), (("test.png",), ("test.svg",),),
)
def test_compress_png(image, tmpdir):
    path = Path(tmpdir) / image
    test_file = Path(__file__).parent / image
    shutil.copy(test_file, path)

    assert main((str(path),)) == 0
    assert test_file.stat().st_size > path.stat().st_size
