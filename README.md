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
    streamlit run main.py
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

## 📘 Sample Usage

After launching the application, the sidebar on the left will appear where you can select the loan amount, annual interest rate, and loan term:

![Application sidebar](images/sidebar_default.png)

Below, you’ll also find options to analyze the loan with **prepayments**. You can choose prepayments over the entire loan period, with two available modes:
- fixed prepayment **without shortening the loan term**,
- fixed prepayment **that shortens the loan term**, keeping the monthly installment the same:

![Prepayment options](images/overpayment_full_term.png)

You can also define your own prepayments by creating a new set and giving it a name:

![Creating a prepayment set](images/custom_overpayment_menu.png)

Then, choose the type of prepayment you want to add:

![Selecting prepayment type](images/overpayment_type.png)

**One-time prepayment:**

![One-time prepayment](images/one_time_overpayment.png)

**Prepayments within a selected date range:**

![Range-based prepayments](images/range_overpayment.png)

**Prepayments over the entire loan term:**

![Full-term prepayments](images/full_term_overpayment.png)

You can also choose whether prepayments should:
- **reduce the monthly installment** (default), or
- **shorten the loan term**, keeping the installment unchanged:

![Prepayment strategy choice1](images/true_false_1.png)
![Prepayment strategy choice2](images/true_false_2.png)
![Prepayment strategy choice3](images/true_false_3.png)

New prepayments can be added to an existing set or to a newly created one:

![Adding to prepayment set](images/custom_overpayment_set_choose.png)

Below, the prepayment sets along with their individual entries will be displayed:

![Prepayment sets view 1](images/custom_overpayment_display.png)  
![Prepayment sets view 2](images/custom_overpayment_display_2.png)

You can delete individual prepayments or the entire set.

Finally, you can **calculate a loan summary** for the selected options:

![Calculating summary](images/calculate_button.png)

Loan details will appear in the center section of the screen:

![Loan details](images/loan_details.png)

Along with a comparison of:
- **without prepayments**:  
  ![No prepayments](images/loan_summary_no_overpayment.png)
- **with fixed prepayments**:  
  ![Fixed prepayments](images/loan_summary_constant_overpayment.png)
- **with custom prepayment sets**:  
  ![User-defined prepayments](images/loan_summary_custom_overpayment.png)

**Repayment schedules** for each option:

![Repayment schedule](images/loan_schedule.png)

Comparison charts showing:
- capital repayment speed:  
  ![Capital repayment speed](images/comparision_diagram.png)
- total cost for each option:  
  ![Total loan cost](images/total_cost_comparision_diagram.png)

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
    streamlit run main.py
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


## 📘 Przykładowe użycie

Po uruchomieniu aplikacji, z lewej strony pojawi się następujący sidebar, gdzie można wybrać kwotę kredytu, roczną stopę oprocentowania oraz okres kredytowania:

![Sidebar aplikacji](images/sidebar_default.png)

Poniżej pojawiają się również opcje analizy opłaty kredytu z **nadpłatami**. Masz do wyboru opcję nadpłaty w całym okresie kredytowania, rozpatrywaną w dwóch wariantach:
- nadpłacasz stałą kwotę **bez skracania okresu kredytowania**,
- nadpłacasz stale, **skracając okres kredytowania**, utrzymując wysokość raty:

![Opcje nadpłat](images/overpayment_full_term.png)

Możesz też dodać swoje własne nadpłaty, tworząc nowy zbiór i nadając mu nazwę:

![Tworzenie zbioru nadpłat](images/custom_overpayment_menu.png)

A następnie wybierając rodzaj nadpłaty, który chcesz dodać:

![Wybór rodzaju nadpłaty](images/overpayment_type.png)

**Jednorazowa nadpłata:**

![Jednorazowa nadpłata](images/one_time_overpayment.png)

**Nadpłaty w podanym zakresie dat:**

![Nadpłaty zakresowe](images/range_overpayment.png)

**Nadpłaty w całym okresie kredytowania:**

![Nadpłaty całookresowe](images/full_term_overpayment.png)

Możesz również określić, czy nadpłaty mają:
- **obniżać ratę kredytu** (domyślnie),
- czy **skrócić okres kredytowania**, pozostawiając ratę bez zmian (różny opis w zależnie od typu nadpłat):

![Wybór strategii nadpłat1](images/true_false_1.png)
![Wybór strategii nadpłat2](images/true_false_2.png)
![Wybór strategii nadpłat3](images/true_false_3.png)

Nowe nadpłaty możesz dodać do już istniejącego zbioru lub utworzyć nowy:

![Dodawanie do zbioru](images/custom_overpayment_set_choose.png)

Poniżej wyświetlone zostaną utworzone zbiory nadpłat wraz z ich zawartością:

![Zbiory nadpłat - widok 1](images/custom_overpayment_display.png)  
![Zbiory nadpłat - widok 2](images/custom_overpayment_display_2.png)

Możesz usuwać pojedyncze nadpłaty lub całe zbiory.

Na koniec możesz **obliczyć podsumowania kredytu** dla wybranych opcji:

![Obliczanie podsumowania](images/calculate_button.png)

W środkowej części ekranu pojawią się szczegóły dotyczące kredytu:

![Szczegóły kredytu](images/loan_details.png)

Wraz z porównaniem opcji:
- **bez nadpłat**:  
  ![Bez nadpłat](images/loan_summary_no_overpayment.png)
- **z nadpłatą stałą**:  
  ![Stała nadpłata](images/loan_summary_constant_overpayment.png)
- **z własnymi zbiorami nadpłat**:  
  ![Zbiory użytkownika](images/loan_summary_custom_overpayment.png)

**Harmonogramy spłat** dla każdej opcji:

![Harmonogram spłat](images/loan_schedule.png)

Wykresy porównujące:
- tempo spłaty kapitału:  
  ![Tempo spłaty](images/comparision_diagram.png)
- całkowity koszt kredytu:  
  ![Całkowity koszt](images/total_cost_comparision_diagram.png)
