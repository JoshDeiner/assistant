.PHONY: run

streamlit-run:
	streamlit run app/streamlit_app.py --server.port 8500 --server.address 0.0.0.0 --server.headless true