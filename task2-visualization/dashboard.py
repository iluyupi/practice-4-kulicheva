# =============================================================================
# ИТОГОВЫЙ ДАШБОРД — ФИНАНСОВЫЙ ПРОФИЛЬ ПРЕДПРИЯТИЯ
# =============================================================================
# Дисциплина: Проектно-технологическая практика
# Задание 2. Визуализация финансовых данных
#
# Автор:   [ФИО студента]
# Группа:  [номер группы]
# Дата:    [дата выполнения]
# Данные:  [название предприятия / демонстрационные данные]
#
# Что делает этот файл:
#   Компонует 4 графика из модулей 1–3 в единую фигуру 2×2.
#   Тема: финансовый профиль предприятия.
#
#   Панель A (верх-лево):  динамика выручки и прибыли
#   Панель B (верх-право): структура баланса (круговая)
#   Панель C (низ-лево):   динамика рентабельности
#   Панель D (низ-право):  коэффициенты ликвидности vs норматив
#
# Дашборд сохраняется в charts/dashboard.png
# =============================================================================

import os
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.patches as mpatches
import seaborn as sns

matplotlib.rcParams["font.sans-serif"] = ["Arial", "Liberation Sans", "DejaVu Sans"]
matplotlib.rcParams["axes.unicode_minus"] = False

os.makedirs("charts", exist_ok=True)


# =============================================================================
# БЛОК ДАННЫХ
# =============================================================================

# ┌─────────────────────────────────────────────────────────────────────────┐
# │  ИЗМЕНИТЕ ЗДЕСЬ: укажите путь к вашему файлу данных                    │
# └─────────────────────────────────────────────────────────────────────────┘
DATA_FILE = "data.xlsx"

df_results = pd.read_excel(DATA_FILE, sheet_name="results")
df_ratios  = pd.read_excel(DATA_FILE, sheet_name="ratios")
df_balance = pd.read_excel(DATA_FILE, sheet_name="balance")

years = df_results["year"].astype(str).tolist()


# =============================================================================
# СОЗДАНИЕ ФИГУРЫ 2×2
# =============================================================================

fig, axes = plt.subplots(2, 2, figsize=(16, 10))
ax_a, ax_b, ax_c, ax_d = axes[0, 0], axes[0, 1], axes[1, 0], axes[1, 1]

# ┌─────────────────────────────────────────────────────────────────────────┐
# │  ИЗМЕНИТЕ ЗДЕСЬ: общий заголовок дашборда                              │
# │  Укажите название предприятия и отчётный период                        │
# └─────────────────────────────────────────────────────────────────────────┘
fig.suptitle(
    "Финансовый профиль предприятия | 2022–2024",
    fontsize=16, fontweight="bold", y=1.01,
)


# =============================================================================
# ПАНЕЛЬ A. Динамика выручки и чистой прибыли
# =============================================================================

revenue    = df_results["revenue"].tolist()
net_profit = df_results["net_profit"].tolist()

ax_a.plot(years, revenue,
          marker="o", linewidth=2.5, markersize=7,
          color="#2E5090", label="Выручка")
ax_a.plot(years, net_profit,
          marker="s", linewidth=2.5, markersize=7,
          color="#E8844A", linestyle="--", label="Чистая прибыль")

for i, (r, n) in enumerate(zip(revenue, net_profit)):
    ax_a.annotate(f"{r:,}", xy=(i, r), ha="center", va="bottom",
                  fontsize=8, color="#2E5090")
    ax_a.annotate(f"{n:,}", xy=(i, n), ha="center", va="bottom",
                  fontsize=8, color="#E8844A")

# ┌─────────────────────────────────────────────────────────────────────────┐
# │  ИЗМЕНИТЕ ЗДЕСЬ: заголовок панели А                                    │
# └─────────────────────────────────────────────────────────────────────────┘
ax_a.set_title("А. Выручка и чистая прибыль, тыс. руб.",
               fontsize=11, fontweight="bold")
ax_a.set_xlabel("Год", fontsize=10)
ax_a.set_ylabel("Тыс. руб.", fontsize=10)
ax_a.legend(fontsize=9)
ax_a.grid(axis="y", linestyle="--", alpha=0.4)
ax_a.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:,.0f}"))


# =============================================================================
# ПАНЕЛЬ B. Структура баланса — круговая диаграмма (только активы)
# =============================================================================

assets = df_balance[df_balance["category"].str.contains("активы", case=False)]

# ┌─────────────────────────────────────────────────────────────────────────┐
# │  ИЗМЕНИТЕ ЗДЕСЬ: цвета срезов                                          │
# └─────────────────────────────────────────────────────────────────────────┘
colors_b = ["#2E5090", "#5B9BD5"]

ax_b.pie(
    assets["value"],
    labels=assets["category"],
    autopct="%1.1f%%",
    colors=colors_b,
    startangle=90,
    pctdistance=0.75,
    textprops={"fontsize": 9},
)

# ┌─────────────────────────────────────────────────────────────────────────┐
# │  ИЗМЕНИТЕ ЗДЕСЬ: заголовок панели B — укажите год                      │
# └─────────────────────────────────────────────────────────────────────────┘
ax_b.set_title("Б. Структура активов на 31.12.2024",
               fontsize=11, fontweight="bold")


# =============================================================================
# ПАНЕЛЬ C. Динамика рентабельности
# =============================================================================

df_prof = df_ratios[["year", "roa", "roe", "ros"]].copy()
for col in ["roa", "roe", "ros"]:
    df_prof[col] = (df_prof[col] * 100).round(1)

df_long = df_prof.melt(id_vars="year", var_name="ind", value_name="val")
label_map = {"roa": "ROA", "roe": "ROE", "ros": "ROS"}
df_long["ind"] = df_long["ind"].map(label_map)
palette_c = {"ROA": "#2E5090", "ROE": "#E8844A", "ROS": "#A8D08D"}

sns.lineplot(data=df_long, x="year", y="val",
             hue="ind", palette=palette_c,
             marker="o", markersize=7, linewidth=2,
             ax=ax_c)

ax_c.set_xticks(df_ratios["year"].tolist())
ax_c.set_xticklabels(years, fontsize=10)

# ┌─────────────────────────────────────────────────────────────────────────┐
# │  ИЗМЕНИТЕ ЗДЕСЬ: заголовок панели C                                    │
# └─────────────────────────────────────────────────────────────────────────┘
ax_c.set_title("В. Рентабельность, %",
               fontsize=11, fontweight="bold")
ax_c.set_xlabel("Год", fontsize=10)
ax_c.set_ylabel("%", fontsize=10)
ax_c.legend(title="", fontsize=9)
ax_c.grid(axis="y", linestyle="--", alpha=0.4)


# =============================================================================
# ПАНЕЛЬ D. Коэффициенты ликвидности vs норматив
# =============================================================================

last = df_ratios[df_ratios["year"] == df_ratios["year"].max()].iloc[0]

liq_labels = ["Текущая", "Быстрая", "Абс."]
liq_values = [last["current_ratio"], last["quick_ratio"], 0.18]

# ┌─────────────────────────────────────────────────────────────────────────┐
# │  ИЗМЕНИТЕ ЗДЕСЬ: нормативы и фактическое значение абс. ликвидности     │
# └─────────────────────────────────────────────────────────────────────────┘
liq_norms  = [2.0, 1.0, 0.2]

colors_d = ["#A8D08D" if v >= n else "#FF7C7C"
            for v, n in zip(liq_values, liq_norms)]

bars_d = ax_d.bar(liq_labels, liq_values, color=colors_d, width=0.4, zorder=3)

for bar, norm in zip(bars_d, liq_norms):
    x = bar.get_x()
    w = bar.get_width()
    ax_d.hlines(norm, x, x + w,
                colors="#CC2222", linewidths=2, linestyles="--", zorder=4)
    h = bar.get_height()
    ax_d.text(bar.get_x() + w / 2, h + 0.03,
              f"{h:.2f}", ha="center", va="bottom", fontsize=9, fontweight="bold")

patch_ok  = mpatches.Patch(color="#A8D08D", label="≥ норматива")
patch_bad = mpatches.Patch(color="#FF7C7C", label="< норматива")
ax_d.legend(handles=[patch_ok, patch_bad], fontsize=8, loc="upper right")

# ┌─────────────────────────────────────────────────────────────────────────┐
# │  ИЗМЕНИТЕ ЗДЕСЬ: заголовок панели D — укажите год                      │
# └─────────────────────────────────────────────────────────────────────────┘
ax_d.set_title("Г. Ликвидность vs норматив (2024)",
               fontsize=11, fontweight="bold")
ax_d.set_ylabel("Значение", fontsize=10)
ax_d.grid(axis="y", linestyle="--", alpha=0.4, zorder=0)


# =============================================================================
# СОХРАНЕНИЕ
# =============================================================================

plt.tight_layout()
plt.savefig("charts/dashboard.png", dpi=150, bbox_inches="tight")
plt.show()
print("Дашборд сохранён: charts/dashboard.png")

# ┌─────────────────────────────────────────────────────────────────────────┐
# │  ВАШ ВЫВОД ПО ДАШБОРДУ:                                                │
# │  Напишите 3–5 предложений — общий финансовый портрет предприятия       │
# │  на основе четырёх панелей дашборда.                                   │
# └─────────────────────────────────────────────────────────────────────────┘
# ВЫВОД: ...
