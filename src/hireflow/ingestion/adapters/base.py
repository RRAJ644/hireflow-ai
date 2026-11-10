
from abc import ABC, abstractmethod
from typing import Any


class BaseATSAdapter(ABC):

    @abstractmethod
    async def fetch_jobs(self, board_token: str) -> list[dict[str, Any]]:
        """
        Fetch all published jobs from a company's ATS board.

        Args:
            board_token: Provider-specific company board identifier.

        Returns:
            A list of raw job dictionaries from the ATS provider.
        """
        raise NotImplementedError
