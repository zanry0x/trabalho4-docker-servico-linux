FROM python:3.13-slim

WORKDIR /app

RUN addgroup --system appgroup && adduser --system --ingroup appgroup --uid 10001 appuser

COPY app.py .

RUN chown appuser:appgroup /app/app.py

USER appuser

EXPOSE 8080

ENV PORT=8080
ENV LOG_LEVEL=INFO

CMD ["python", "app.py"]