# 1. Koristimo zvaničnu i laganu Python sliku
FROM python:3.11-slim

# 2. Postavljamo environment varijable
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3. Postavljamo radni direktorijum unutar kontejnera
WORKDIR /code

# 4. Kopiramo requirements i instaliramo zavisnosti
COPY src/requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# 5. Kopiramo ostatak aplikacije (sada kopiramo ceo src jer imamo i app podfolder)
COPY src/ /code/src/

# 6. Kreiramo ne-privilegovanog korisnika iz bezbednosnih razloga
RUN useradd -u 8888 appuser && chown -R appuser:appuser /code
USER appuser

# 7. Otvaramo port 8000
EXPOSE 8000

# 8. Komanda za pokretanje aplikacije (Uvicorn)
CMD ["uvicorn", "src.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
