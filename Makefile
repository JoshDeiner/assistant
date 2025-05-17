.PHONY: run

streamlit-run:
	streamlit run test.py --server.port 8501 --server.address 0.0.0.0 --server.headless true