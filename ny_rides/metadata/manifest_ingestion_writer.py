import json
import logging
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)


def write_manifest(
    results,
    output_dir: str = "artifacts/ingestion",
) -> Path:
    """Write manifest with download results and metadata.

    Args:
        results: List of DownloadResult objects
        output_dir: Directory to save the manifest

    Returns:
        Path to the generated manifest file
    """
    timestamp = datetime.now()

    manifest = {
        "execution_timestamp": timestamp.isoformat(),
        "requested_files": len(results),
        "successful_files": sum(1 for r in results if r.success),
        "failed_files": sum(1 for r in results if not r.success),
        "files": [
            {
                "file_name": r.file_name,
                "success": r.success,
                "error": r.error_message,
            }
            for r in results
        ],
    }

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    manifest_path = output_path / f"manifest_{timestamp.strftime('%Y%m%d_%H%M%S')}.json"

    logger.info("Writing manifest to %s", manifest_path)

    manifest_path.write_text(json.dumps(manifest, indent=2))

    logger.info("Manifest written successfully")

    return manifest_path