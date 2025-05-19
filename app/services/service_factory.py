from .bitcoin_chart_service import BitcoinChartService
from .bitcoin_data_service import BitcoinDataService
from .yfinance_service import YFinanceService


class ServiceFactory:

    """Factory to create services dynamically based on a service type or command."""

    @staticmethod
    def create_service(service_name, **kwargs):
        service_map = {
            "bitcoin_chart": BitcoinChartService,
            "bitcoin_data": BitcoinDataService,
            "asset_service": YFinanceService
        }

        service_class = service_map.get(service_name)
        if not service_class:
            raise ValueError(f"Unknown service requested: {service_name}")

        return service_class(**kwargs)