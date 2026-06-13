# =============================================================================
# МОДУЛЬ 1. БАЗОВЫЕ ГРАФИКИ — MATPLOTLIB
# =============================================================================
# Дисциплина: Проектно-технологическая практика
# Задание 2. Визуализация финансовых данных
#
# Автор:   Иванова Ирина Сергеевна
# Группа:  ЭК-21
# Дата:    13.06.2026
# Данные:  ООО "Энергомонтаж"
#
# Что делает этот файл:
#   График 1 — линейный: динамика выручки и чистой прибыли
#   График 2 — столбчатый: структура выручки (себестоимость + валовая прибыль)
#   График 3 — круговые: структура активов и пассивов баланса
# =============================================================================

import os
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

matplotlib.rcParams["font.sans-serif"] = ["Arial", "Liberation Sans", "DejaVu Sans"]
matplotlib.rcParams["axes.unicode_minus"] = False

os.makedirs("charts", exist_ok=True)

DATA_FILE = "data.xlsx"

df_results = pd.read_excel(DATA_FILE, sheet_name="results")
df_balance = pd.read_excel(DATA_FILE, sheet_name="balance")

print("Данные загружены")


# =============================================================================
# ГРАФИК 1. Выручка и чистая прибыль
# =============================================================================

fig1, ax1 = plt.subplots(figsize=(10, 5))

years = df_results["year"].astype(str).tolist()
revenue = df_results["revenue"].tolist()
net_profit = df_results["net_profit"].tolist()

ax1.plot(years, revenue, marker="o", linewidth=2.5,
         color="#2E5090", label="Выручка")

ax1.plot(years, net_profit, marker="s", linewidth=2.5,
         linestyle="--", color="#E8844A", label="Чистая прибыль")

for i, (r, n) in enumerate(zip(revenue, net_profit)):
    ax1.annotate(f"{r:,.0f}", (i, r), ha="center", fontsize=9)
    ax1.annotate(f"{n:,.0f}", (i, n), ha="center", fontsize=9)

ax1.set_title("Динамика выручки и чистой прибыли", fontweight="bold")
ax1.set_xlabel("Год")
ax1.set_ylabel("Тыс. руб.")
ax1.legend()
ax1.grid(alpha=0.3)

plt.tight_layout()
plt.savefig("charts/m1_revenue_trend.png", dpi=150)
plt.show()

# ВЫВОД:
# Выручка предприятия растет в течение периода.
# Однако в 2025 году наблюдается отрицательная чистая прибыль.
# Это указывает на рост затрат и снижение эффективности.


# =============================================================================
# ГРАФИК 2. Структура выручки
# =============================================================================

fig2, ax2 = plt.subplots(figsize=(10, 5))

x = range(len(years))
cost = df_results["cost"].tolist()
gross = df_results["gross_profit"].tolist()

ax2.bar(x, cost, label="Себестоимость", color="#5B8DB8")
ax2.bar(x, gross, bottom=cost, label="Валовая прибыль", color="#A8D08D")

ax2.set_xticks(list(x))
ax2.set_xticklabels(years)

ax2.set_title("Структура выручки предприятия", fontweight="bold")
ax2.set_xlabel("Год")
ax2.set_ylabel("Тыс. руб.")
ax2.legend()
ax2.grid(axis="y", alpha=0.3)

plt.tight_layout()
plt.savefig("charts/m1_cost_structure.png", dpi=150)
plt.show()

# ВЫВОД:
# Себестоимость занимает основную долю выручки.
# Валовая прибыль нестабильна по годам.
# Это говорит о давлении затрат.

# =============================================================================
# ГРАФИК 3. Структура баланса — круговые диаграммы
# =============================================================================

fig3, (ax3a, ax3b) = plt.subplots(1, 2, figsize=(12, 6))

df_balance["category"] = df_balance["category"].astype(str).str.strip()

assets = df_balance[df_balance["category"].isin([
    "Внеоборотные активы",
    "Оборотные активы"
])]

liabilities = df_balance[df_balance["category"].isin([
    "Собственный капитал",
    "Долгосрочные обязательства",
    "Краткосрочные обязательства"
])]

if assets.empty or liabilities.empty:
    raise ValueError("Баланс пустой — проверь data.xlsx")

ax3a.pie(
    assets["value"],
    labels=assets["category"],
    autopct="%1.1f%%",
    startangle=90
)
ax3a.set_title("Активы")

ax3b.pie(
    liabilities["value"],
    labels=liabilities["category"],
    autopct="%1.1f%%",
    startangle=90
)
ax3b.set_title("Пассивы")

fig3.suptitle("Структура баланса")

plt.tight_layout()

plt.savefig("charts/m1_balance_structure.png", dpi=150)
plt.show()

print("График 3 сохранён")