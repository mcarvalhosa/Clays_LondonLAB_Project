# Clays LondonLAB Project

End-to-end analytics & pricing pipeline for Clays.

---

## 🧮 Git Best Practices

- Before anything, always make sure to **go to the repo folder**:
  ```
   cd Clays_LondonLAB_Project
  ```

- Always **pull** before starting new work to make sure your branch is up to date:
  ```
   git checkout main
   git pull origin main
   git checkout *your_name/featurename*
   git merge main  

  ```
- **Add your changes** before committing:
  ```
  git add .
  ```
- **Commit often** with clear, short messages:
  ```
  git commit -m "what_you_did"
  ```
- **Push and open a pull request** for review:
  ```
  git push 
  ```

- **Open a Pull Request on GitHub** to merge into main

---

## 📂 Folder Structure

```
Clays_LondonLAB_Project/
├── data/
│   ├── raw/            ← original CSV exports & safety parquet copies
│   └── processed/      ← cleaned, feature-engineered & master dataset
├── code/
│   ├── 1_ingest/       ← data cleaning & feature engineering pipeline
│   ├── 2_models/       ← clustering & prediction code
│   ├── 3_optimize/     ← pricing optimization scripts
│   └── final_model/    ← dashboard & reporting code
├── outputs/            ← HTML reports, figures, presentations
├── .gitignore
├── README.md
└── requirements.txt
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

# 📣 Important!

**Never commit raw or processed data files!**  
The folders `data/raw/`, `data/processed/`, and `outputs/` are automatically ignored via `.gitignore`.