
import httpx


from hireflow.db.enums import ATSProvider
from hireflow.ingestion.adapters.base import BaseATSAdapter
from hireflow.ingestion.adapters.greenhouse import GreenhouseAdapter
from hireflow.ingestion.adapters.lever import LeverAdapter
from hireflow.ingestion.adapters.ashby import AshbyAdapter


def get_adapter(provider: ATSProvider, client: httpx.AsyncClient) -> BaseATSAdapter:
    adapters = {
        ATSProvider.GREENHOUSE: GreenhouseAdapter,
        ATSProvider.LEVER: LeverAdapter,
        ATSProvider.ASHBY: AshbyAdapter,
    }

    adapter_class = adapters.get(provider)

    if adapter_class is None:
        raise ValueError(f"Unsupported ATS provider: {provider}")

    return adapter_class(client)
