Deployment quick guide

1. From project root, run:

```
streamlit run main.py
```

2. Ensure `Data/` contains your CSVs (e.g. `data_unificada.csv` or `data_demo_ok.csv`).

3. If you want email notifications configure env vars:

- SMTP_HOST
- SMTP_PORT
- SMTP_USER
- SMTP_PASS
- FROM_EMAIL (optional)

4. For Streamlit Cloud set Main file to `main.py`.

5. If you need to recover archived app versions, they are in `/archive`.
