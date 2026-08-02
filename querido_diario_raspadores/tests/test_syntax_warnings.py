import warnings
from pathlib import Path


def test_gazette_modules_compile_without_syntax_warnings():
    package_dir = Path(__file__).parents[1] / "gazette"

    with warnings.catch_warnings():
        warnings.simplefilter("error", SyntaxWarning)
        for source_path in package_dir.rglob("*.py"):
            compile(source_path.read_bytes(), source_path, "exec")
