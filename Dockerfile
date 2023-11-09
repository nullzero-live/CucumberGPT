# Use a specific digest for reproducibility
FROM python:3.10-slim@sha256:digest_here

# Create a non-root user to run the application
RUN useradd -m appuser

WORKDIR /app

COPY requirements.txt .

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"


RUN pip install --no-cache-dir -r requirements.txt

COPY . .

USER appuser

EXPOSE 8501

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]

#Application is run on Streamlit front end.
CMD ["streamlit", "run", "frontend/streamlit_app.py"]
