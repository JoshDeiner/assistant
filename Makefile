.PHONY: run validate-btc streamlit-run

validate-btc:
	python -m app.streamlit.streamlit_validator --file_path btc_data.csv --service_name bitcoin_chart

streamlit-run:
	streamlit run app/streamlit/streamlit_orchestrator.py --server.port 8500 --server.address 0.0.0.0 --server.headless true