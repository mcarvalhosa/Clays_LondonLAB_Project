# Clays LondonLAB Project

End-to-end analytics & pricing pipeline for Clays.

---

## 📂 Folder Structure

```
Clays_LondonLAB_Project/
├── data/
│   ├── raw/          ← original CSV exports & safety parquet copies
│   └── processed/    ← cleaned, feature-engineered & master dataset
├── code/
│   ├── 1_ingest/       ← data cleaning & feature engineering pipeline
│   ├── models/       ← clustering & prediction code
│   ├── optimize/     ← pricing optimization scripts
│   └── dashboard/    ← dashboard & reporting code
├── notebooks/        ← EDA and experiment notebooks
├── outputs/          ← HTML reports, figures, presentations
├── .gitignore
└── README.md
```

---

## 🛠️ Setup

1. **Clone the repository**:
   ```
   git clone https://github.com/mcarvalhosa/Clays_LondonLAB_Project.git
   cd Clays_LondonLAB_Project
   ```

2. **Create & activate a virtual environment**:
   ```
   python -m venv .venv
   # Activate the virtualenv:
   # - Windows:
   .venv\Scripts\activate
   # - Mac/Linux:
   source .venv/bin/activate
   ```

3. **Install dependencies**:
   ```
   pip install -r code/ingest/requirements.txt
   ```

---

## ▶️ Running the Pipeline

1. **Go to the ingest folder**:
   ```
   cd code/ingest
   ```

2. **Run the cleaning and feature engineering pipeline**:
   ```
   python run_ingest.py
   ```

3. **Outputs** (like the Master Dataset) will be written to:
   ```
   data/processed/
   ```

4. **Reports** (like the Data Quality HTML) will be written to:
   ```
   outputs/
   ```

---

## 🧮 Git Best Practices

- Always **pull** before starting new work:
  ```
  git pull origin main
  ```
- **Create a new branch** when starting a feature:
  ```
  git checkout -b feat/your-feature
  ```
- **Commit often** with clear, short messages:
  ```
  git commit -m "feat: add clustering pipeline"
  ```
- **Push and open a pull request** for review:
  ```
  git push origin main
  ```

---

# 📣 Important!

**Never commit raw or processed data files!**  
The folders `data/raw/`, `data/processed/`, and `outputs/` are automatically ignored via `.gitignore`.

