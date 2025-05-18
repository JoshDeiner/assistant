
# 📈 **Streamlit Bitcoin Chart Viewer – Service Refactoring Guide**

## 🎯 **Objective**

Refactor the existing Streamlit application to:

* Rename the generic `ChartService` to **`BitcoinChartService`** for clarity.
* Restrict its current responsibility to Bitcoin-related chart visualization.
* Keep the architecture extensible by enforcing a clear **BaseService abstraction**.
* Ensure the application remains modular and follows clean design principles.

---

## 📝 **Instructions for Code Updates**

---

### 1️⃣ **Update `BaseService` to Be Abstract**

Create or update `app/services/base_service.py`:

```python
from abc import ABC, abstractmethod

class BaseService(ABC):
    @abstractmethod
    def name(self):
        """Return the unique name of the service."""
        pass

    @abstractmethod
    def run(self):
        """Main execution logic for the service in Streamlit."""
        pass
```

---

### 2️⃣ **Rename `ChartService` to `BitcoinChartService`**

Update or create `app/services/bitcoin_chart_service.py`:

```python
import streamlit as st
import pandas as pd
from app.services.base_service import BaseService

class BitcoinChartService(BaseService):
    def name(self):
        return "Bitcoin Chart Service"
    
    def run(self):
        st.header("📈 Bitcoin Chart Viewer")

        file_path = st.text_input("CSV File Path", "btc_data.csv")
        title = st.text_input("Chart Title", "Bitcoin Weekly Data Mapped")
        chart_type = st.selectbox("Chart Type", ["Line", "Area", "Bar"])

        if st.button("Generate Chart"):
            try:
                df = pd.read_csv(file_path)
                if "Date" in df.columns:
                    df["Date"] = pd.to_datetime(df["Date"])
                    df = df.set_index("Date")

                y_columns = [col for col in df.columns if col != "Date"]
                selected_columns = st.multiselect("Select Columns to Plot", y_columns, default=y_columns[:1])

                if selected_columns:
                    if chart_type == "Line":
                        st.line_chart(df[selected_columns])
                    elif chart_type == "Area":
                        st.area_chart(df[selected_columns])
                    elif chart_type == "Bar":
                        st.bar_chart(df[selected_columns])

            except Exception as e:
                st.error(f"Error: {e}")
```

---

### 3️⃣ **Update Service Registration in `main.py`**

```python
from app.services.bitcoin_chart_service import BitcoinChartService
from app.service_registry import ServiceRegistry
from app.client import StreamlitClient

if __name__ == "__main__":
    registry = ServiceRegistry()
    registry.register(BitcoinChartService())

    app = StreamlitClient(registry)
    app.run()
```

---

### 📚 **Optional Enhancements**

* Create a new `ChartService` in the future to handle other financial instruments (e.g., Ethereum, Stocks).
* Introduce a **configuration system** (YAML or JSON) to dynamically enable/disable services.
* Implement **dynamic service discovery** by scanning the `services/` directory automatically.
* Add a **service metadata system** so each service can describe its purpose and expected inputs.

---

## ✅ **Expected Outcome**

* Clear and specific class responsibility (`BitcoinChartService` is only for Bitcoin charts).
* Easy future expansion through the `BaseService` abstraction.
* Clean, readable, and maintainable code structure.
