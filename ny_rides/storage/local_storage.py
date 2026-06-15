from pathlib import Path

from ny_rides.storage.storage import Storage

import logging
logger = logging.getLogger(__name__)

class LocalStorage(Storage):
    """"
    Local filesystem storage implementation.
    """
    def __init__(self, base_path: str):
        self.base_path = Path(base_path)

    def save(self, filename: str, content: bytes) -> Path:

        if not content:
            raise ValueError(
                f"Cannot save empty content for file {filename}"
            )

        self.base_path.mkdir(parents=True, exist_ok=True)

        destination = self.base_path / filename

        logger.info("Saving file %s", destination)

        try:
            destination.write_bytes(content)
            logger.info("Successfully saved file %s", destination)

            return destination

        except OSError:
            logger.exception("Failed to save file %s", destination)
            raise
