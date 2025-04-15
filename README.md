# Mortgage Calculator

A web application to calculate loan repayment schedules with support for overpayments. Built using Python, `streamlit`,
`pandas`, `numpy_financial`, and `matplotlib`.

👉 [Polish version below](#kalkulator-kredytowy)

## ⚙️ Features

- Loan monthly payment calculation
- Handles overpayments (one-time, periodic, full-term)
- Generates visual amortization schedule
- Interactive UI built with Streamlit
- Summary of total loan cost and interest

## 🚀 Run Locally

### Option 1: Streamlit (Local)

```bash
    pip install -r requirements.txt
    streamlit run dashboard.py
```

### Option 2: Docker image

1. Build Docker image:
   ```bash
   docker build -t mortgage-calculator .
   ```
2. Run container:
    ```bash
    docker run -p 8080:8080 mortgage-calculator
    ```

The app will be available at http://localhost:8080

## 🧪 Tests

Unit tests are written using `pytest`:

```bash
  pytest tests.py
```

## 📦 Requirements

Install dependencies with:

```bash
  pip install -r requirements.txt
```

## 🐳 Note

The .venv folder is excluded via .dockerignore – the local virtual environment is not copied into the Docker image.

# Kalkulator Kredytowy

Aplikacja webowa do obliczania harmonogramu spłat kredytu z uwzględnieniem nadpłat. Wykonana w Pythonie przy użyciu
`streamlit`, `pandas`, `numpy_financial` i `matplotlib`.

## ⚙️ Funkcjonalności

- Obliczanie miesięcznej raty kredytu
- Obsługa nadpłat (jednorazowych, zakresowych, stałych)
- Interfejs w Streamlit
- Wykres harmonogramu spłat
- Podsumowanie kosztów i odsetek

## 🚀 Uruchamianie

### Opcja 1: Streamlit (Localnie)

```bash
    pip install -r requirements.txt
    streamlit run dashboard.py
```

### Opcja 2: Docker

1. Zbuduj obraz Dockera:
   ```bash
   docker build -t mortgage-calculator .
   ```
2. Uruchom kontener:
    ```bash
    docker run -p 8080:8080 mortgage-calculator
    ```

Aplikacja będzie dostępna pod http://localhost:8080

## 🧪 Testy

Testy jednostkowe uruchomisz przy użyciu `pytest`

```bash
  pytest tests.py
```

## 📦 Wymagania

Wszystkie biblioteki znajdują się w pliku `requirements.txt`:

```bash
  pip install -r requirements.txt
```

## 🐳 Uwaga

Folder `.venv` jest ignorowany dzięki `.dockerignore` – nie trafia do obrazu Dockera.
