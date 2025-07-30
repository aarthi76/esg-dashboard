# esg-dashboard
An ESG data dashboard built using Financial Modeling Prep API and Power BI.

ESG-Dashboard/
    ├── data/          # For CSVs
    ├── scripts/       # For Python files
    ├── dashboard/     # For Power BI/Tableau files
    └── README.md
# ESG Dashboard – Real-Time ESG Insights

A real-time **Environmental, Social, and Governance (ESG) Dashboard** that uses data from the **Financial Modeling Prep (FMP) API** to visualize ESG performance across companies and industries.  
This project combines **Python (for data fetching & cleaning)** with **Power BI/Tableau (for interactive dashboards)**.

---

## **Table of Contents**
1. [Project Overview](#project-overview)
2. [Features](#features)
3. [Data Source](#data-source)
4. [Tech Stack](#tech-stack)
5. [Installation & Setup](#installation--setup)
6. [How to Use](#how-to-use)
7. [Dashboard Preview](#dashboard-preview)
8. [Future Improvements](#future-improvements)
9. [License](#license)

---

## **Project Overview**
The ESG Dashboard provides a simple way to:
- Track **real-time ESG ratings** for companies.
- Compare **Environmental, Social, and Governance pillars**.
- Analyze industry trends and highlight ESG leaders/laggards.

---

## **Features**
- Fetch real-time ESG data using the **Financial Modeling Prep API**.
- Export **clean CSV datasets** for dashboarding.
- Interactive **visualizations**:  
  - Top companies by ESG score.  
  - ESG score breakdown by sector.  
  - Correlation heatmaps for E, S, G pillars.
- Modular Python script that can be easily extended.

---

## **Data Source**
- **[Financial Modeling Prep API](https://financialmodelingprep.com/developer/docs/)**  
  - Provides real-time ESG ratings at a company level.
  - API Endpoint used:  
    ```
    https://financialmodelingprep.com/api/v4/esg-environmental-social-governance-data-ratings
    ```

---

## **Tech Stack**
- **Python 3.10+**
  - `requests`, `pandas` (for data pulling and cleaning)
- **Power BI / Tableau** for visualization
- **GitHub** for version control

---

## **Installation & Setup**

### **1. Clone the Repository**
```bash
git clone https://github.com/YOUR_USERNAME/esg-dashboard.git
cd esg-dashboard
