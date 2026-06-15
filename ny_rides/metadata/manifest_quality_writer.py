import json
import logging
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)


def write_manifest(
    report: dict,
    output_dir: str = "artifacts/quality",
) -> Path:
    """Write quality report as a JSON manifest.

    Args:
        report: Quality report dict produced by QualityValidator.validate()
        output_dir: Directory to save the manifest

    Returns:
        Path to the generated report file
    """
    timestamp = datetime.now()

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    manifest_path = (
        output_path / f"quality_report_{timestamp.strftime('%Y%m%d_%H%M%S')}.json"
    )

    logger.info("Writing quality report to %s", manifest_path)

    manifest_path.write_text(json.dumps(report, indent=2))

    logger.info("Quality report written successfully")

    return manifest_path
