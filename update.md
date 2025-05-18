Here’s a focused `README.md` that directly instructs an LLM (or developer) to create and use the Service Factory pattern.

# 🏗️ **Service Factory Pattern for Dynamic Streamlit Clients**

## 📚 **Objective**

Implement a **Service Factory** to dynamically create and inject services into the `StreamlitClient` based on a requested service name or identifier.

This promotes modularity, decouples service creation from business logic, and supports dynamic behavior driven by external systems (e.g., LLM function calls).

---

## ✅ **Part 1: Create the `ServiceFactory` Class**

* Define a `ServiceFactory` class responsible for instantiating services.
* It should:

  * Maintain a **mapping** of service names to their corresponding service classes.
  * Accept **dynamic parameters** for service instantiation.
  * Raise an error if an unknown service is requested.

---

### 📄 **Example Implementation (`service_factory.py`):**

```python
from services.bitcoin_chart_service import BitcoinChartService
from services.schema_inspector_service import SchemaInspectorService

class ServiceFactory:
    """Factory to create services dynamically based on a service type or command."""

    @staticmethod
    def create_service(service_name, **kwargs):
        service_map = {
            "bitcoin_chart": BitcoinChartService,
            "schema_inspector": SchemaInspectorService,
            # Add new services here as needed
        }

        service_class = service_map.get(service_name)
        if not service_class:
            raise ValueError(f"Unknown service requested: {service_name}")

        return service_class(**kwargs)
```

---

### 📌 **Key Design Notes:**

* The `service_map` centralizes available services.
* Additional keyword arguments (`**kwargs`) allow passing configuration or initialization data to services.
* Raising `ValueError` ensures invalid service requests are properly handled.

---

### 📦 **Usage Example:**

```python
from service_factory import ServiceFactory
from streamlit_client import StreamlitClient

# Create a service dynamically
service = ServiceFactory.create_service(
    "bitcoin_chart",
    default_file_path="btc_data.csv",
    default_chart_title="Bitcoin Price Chart"
)

# Pass the service to the Streamlit client
client = StreamlitClient(service)
client.run()
```

---

## 🚀 **Benefits of Using a Service Factory**

* ✅ Clean separation between service creation and application logic.
* ✅ Easy to add or remove services in one place (`service_map`).
* ✅ Supports dynamic, runtime decisions for which service to load.

---

> **Note:** Ensure that all service classes implement a common interface like `BaseService` to maintain consistency and compatibility with `StreamlitClient`.
