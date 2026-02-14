# Topsis-Sarishti-102317212

A professional Python package and web service implementing the **Technique for Order of Preference by Similarity to Ideal Solution (TOPSIS)** for Multi-Criteria Decision Making (MCDM).

---

## 1. Methodology

The project follows a structured data science pipeline to ensure accurate results and professional delivery:

1. **Data Collection**  
   Accepts CSV files containing alternatives and multiple criteria.

2. **Pre-processing**  
   - Validates minimum 3 columns  
   - Ensures all criteria columns are numeric  
   - Validates weights and impacts length  

3. **Model Application**  
   - Normalizes decision matrix  
   - Applies weights  
   - Determines ideal best and worst  
   - Calculates Euclidean distance  

4. **Result Analysis**  
   Generates:
   - TOPSIS Score  
   - Final Rank  

---

## 2. Live Links

- **PyPI Package:** [https://pypi.org/project/Topsis-Sarishti-102317212/](https://pypi.org/project/Topsis-Sarishti-102317212/1.0.0/)
- **GitHub Repository:** [https://github.com/Sarishti845/Topsis-Sarishti-102317212](https://github.com/Sarishti845/Topsis-Sarishti-102317212)

---

## 3. Features & Interface

The project provides two interfaces:

---

### 🔹 Command Line Interface (CLI)

Run directly from terminal:

```bash
topsis data.csv "1,1,1,1" "+,+,-,+" result.csv
