from pathlib import Path

from app.services.run_service import run_generate


def test_run_generate_output_structure():
    summary = run_generate(Path("configs/jobs/generate_outline.yaml"), dry_run=True)
    run_dir = Path(summary["run_dir"])
    assert run_dir.exists()
    assert (run_dir / "logs").exists()
    assert (run_dir / "exports").exists()
    assert (run_dir / "summary.json").exists()
