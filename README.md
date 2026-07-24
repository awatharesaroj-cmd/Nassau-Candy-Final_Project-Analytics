# Nassau-Candy-Final_Project-Analytics
# 🍬 Nassau Candy Distributor
## Factory Reallocation & Shipping Optimization Analytics

![Power BI](https://img.shields.io/badge/PowerBI-F2C811?style=for-the-badge&logo=powerbi&logoColor=black)
![Excel](https://img.shields.io/badge/Excel-217346?style=for-the-badge&logo=microsoft-excel&logoColor=white)
![DAX](https://img.shields.io/badge/DAX-0078D4?style=for-the-badge&logo=microsoft&logoColor=white)

---

## 📌 Project Overview

This project presents a comprehensive **data analytics solution** 
for Nassau Candy Distributor, focusing on:
- 🏭 Factory performance analysis
- 🚚 Shipping optimization
- 📦 Product profitability insights
- 🎯 What-If scenario simulation

Built using **Microsoft Power BI Desktop** as part of 
the Unified Mentor Data Analytics Program.

---

## 🎯 Problem Statement

Nassau Candy currently assigns products to factories using 
static rules and legacy processes. This leads to:
- Suboptimal shipping distances
- High lead times for certain regions
- Margin erosion due to logistics inefficiencies

---

## 📊 Dashboard Pages

| Page | Description |
|------|-------------|
| 1️⃣ Executive Summary | KPIs, Sales trends, Division breakdown |
| 2️⃣ Factory Performance | Map, Sales & Lead Time by Factory |
| 3️⃣ Shipping Analysis | Speed categories, Regional performance |
| 4️⃣ Product Analytics | Top products, Margin analysis |
| 5️⃣ What-If Analysis | Lead time reduction simulator |

---

## 🔢 Key Metrics

| Metric | Value |
|--------|-------|
| Total Sales | 138K |
| Total Orders | 8K |
| Profit Margin | 66.1% |
| Avg Lead Time | 5.32 days |
| Slow Shipments | 71.14% |

---

## 🛠️ Tools & Technologies

- **Microsoft Power BI Desktop** — Dashboard & visualization
- **Power Query Editor** — Data cleaning & transformation
- **DAX** — Measures & calculations
- **Excel** — Raw data source
- **Star Schema** — Data modeling approach

---

## 📁 Project Structure


---

## 🧮 DAX Measures Created

```dax
Total Sales = SUM(Nassau_Candy_Distributor[Sales])
Total Profit = SUM(Nassau_Candy_Distributor[Gross Profit])
Profit Margin % = DIVIDE([Total Profit], [Total Sales], 0)
Avg Lead Time = AVERAGE(Nassau_Candy_Distributor[Lead Time (Days)])
Slow Shipments = COUNTROWS(FILTER(...Speed = "Slow"))
Simulated Lead Time = [Avg Lead Time] * (1 - MIN('Lead Time Reduction'[Lead Time Reduction]))
Simulated Profit = [Total Profit] * (1 + MIN(...) * 0.3)
```

---

## 🏭 Factory Performance Summary

| Factory | Total Sales | Avg Lead Time |
|---------|-------------|---------------|
| Wicked Choccy's | 54K | 5.4 days |
| Lot's O' Nuts | 47K | 5.3 days |
| Secret Factory | 8K | 5.0 days |
| The Other Factory | 1K | 5.1 days |
| Sugar Shack | 0K | 5.8 days |

---

## 💡 Key Findings

- ✅ Wicked Choccy's leads with 54K in sales
- ✅ Sugar Shack needs urgent reallocation
- ✅ 71.14% of shipments are slow (Standard Class)
- ✅ Everlasting Gobstopper has highest margin (80%)
- ✅ 20% lead time reduction = +5.6K additional profit

---

## 📈 What-If Analysis Results

| Reduction | Simulated Lead Time | Simulated Profit |
|-----------|--------------------|--------------------|
| 0% | 5.32 days | 91.51K |
| 10% | 4.79 days | 94.3K |
| 20% | 4.26 days | 97.1K |
| 30% | 3.72 days | 99.9K |
| 50% | 2.66 days | 105.2K |

---

## 🚀 How to Use

1. Download `Nassau_Candy_Project_Final.pbix`
2. Open with **Power BI Desktop** (free download)
3. Explore all 5 dashboard pages
4. Use slicers to filter by Division, Region, Ship Mode
5. Move the **Lead Time Reduction slider** on Page 5
   to simulate profit improvements

---

## 👤 Author

**Saroj**
Data Analytics Student
Unified Mentor Program — July 2026

---

## 📜 License

This project is for educational purposes as part of
the Unified Mentor Data Analytics Program.
