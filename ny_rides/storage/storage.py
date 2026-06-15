from abc import ABC, abstractmethod
from pathlib import Path


class Storage(ABC):
    """
    Storage abstraction.

    Current implementation:
        - LocalStorage

    Future implementations:
        - S3Storage
        - GCSStorage
        - AzureBlobStorage
    """

    @abstractmethod
    def save(self, filename: str, content: bytes) -> Path:
        pass
