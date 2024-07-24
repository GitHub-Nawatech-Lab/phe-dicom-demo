run:
	uvicorn main:app --reload --port 8080 --log-level debug --timeout-keep-alive 30