import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mlxtend.frequent_patterns import apriori, association_rules
import warnings
import os

warnings.filterwarnings("ignore")

FILE_NAME = "data_penjualan.csv"

def load_data(file_name):

    if not os.path.exists(file_name):
        raise FileNotFoundError(f"{file_name} tidak ditemukan")

    df = pd.read_csv(file_name)

    df["tgl_transaksi"] = pd.to_datetime(
        df["tgl_transaksi"],
        dayfirst=True
    )

    return df

def prepare_daily_sales(df):

    daily = (
        df.groupby(
            ["tgl_transaksi", "nama_produk"],
            as_index=False
        )["total_nilai"]
        .sum()
    )

    daily = daily.sort_values(
        ["nama_produk", "tgl_transaksi"]
    )

    return daily

def calculate_moving_average(daily):

    daily["ma_3"] = (
        daily.groupby("nama_produk")["total_nilai"]
        .transform(
            lambda x:
            x.rolling(3, min_periods=1).mean()
        )
    )

    return daily

def calculate_rising_streak(series):

    diff = series.diff()

    streak = 0
    max_streak = 0

    for val in diff:

        if val > 0:
            streak += 1

        else:
            streak = 0

        if streak > max_streak:
            max_streak = streak

    return max_streak

def get_rising_star(daily):

    results = []

    grouped = daily.groupby("nama_produk")

    for product, group in grouped:

        ma_values = group["ma_3"]

        streak = calculate_rising_streak(ma_values)

        first = ma_values.iloc[0]

        if first == 0:
            first = 1

        last = ma_values.iloc[-1]

        growth = ((last / first) - 1) * 100

        results.append({
            "nama_produk": product,
            "max_streak_days": streak,
            "growth_percentage": round(growth, 2)
        })

    result_df = pd.DataFrame(results)

    result_df = result_df.sort_values(
        ["max_streak_days", "growth_percentage"],
        ascending=False
    )

    return result_df.head(18)

def market_basket_analysis(df, rising_star):

    basket = pd.crosstab(
        df["nomor_struk"],
        df["nama_produk"]
    )

    basket = basket > 0

    frequent_itemsets = apriori(
        basket,
        min_support=0.01,
        use_colnames=True
    )

    rules = association_rules(
        frequent_itemsets,
        metric="lift",
        min_threshold=1.2
    )

    rising_products = set(
        rising_star["nama_produk"]
    )

    def contains_star(items):

        return not set(items).isdisjoint(
            rising_products
        )

    filtered = rules[
        (
            rules["antecedents"].apply(contains_star)
            |
            rules["consequents"].apply(contains_star)
        )
        &
        (rules["lift"] >= 2)
    ]

    return filtered.sort_values(
        "lift",
        ascending=False
    )

def export_excel(rising_star, packaging):

    with pd.ExcelWriter(
        "retail_insight.xlsx",
        engine="openpyxl"
    ) as writer:

        rising_star.to_excel(
            writer,
            sheet_name="Rising Star",
            index=False
        )

        packaging.to_excel(
            writer,
            sheet_name="Potential Packaging",
            index=False
        )

def create_chart(
    daily,
    products,
    chart_type,
    filename
):

    plt.style.use("ggplot")

    fig, ax = plt.subplots(
        figsize=(15, 8)
    )

    fig.patch.set_facecolor("#EAEAEA")

    ax.set_facecolor("#F2F2F2")

    colors = [
        "#16a085",
        "#d35400",
        "#7f8c8d",
        "#e84393",
        "#6ab04c",
        "#f1c40f",
        "#8e6e53",
        "#636e72"
    ]

    for idx, product in enumerate(products):

        product_data = daily[
            daily["nama_produk"] == product
        ]

        if chart_type == "actual":

            y = product_data["total_nilai"]

            title = (
                "ANALISIS PENJUALAN PRODUK RISING STAR (Nilai Pertumbuhan Asli)"
            )

            ylabel = "Total Nilai Penjualan"

            marker = "o"

        else:

            base = (
                product_data["total_nilai"]
                .iloc[0]
            )

            if base == 0:
                base = 1

            y = (
                product_data["total_nilai"]
                / base
            ) * 100

            title = (
                "ANALISIS PERTUMBUHAN RELATIF PRODUK RISING STAR"
            )

            ylabel = "Index Pertumbuhan (Base 100)"

            marker = "s"

            ax.axhline(
                100,
                color="black",
                linestyle="--",
                linewidth=1.2,
                alpha=0.6
            )

        ax.plot(
            product_data["tgl_transaksi"],
            y,
            label=product,
            color=colors[idx % len(colors)],
            linewidth=2.5,
            marker=marker,
            markersize=5
        )

    ax.set_title(
        title,
        loc="left",
        fontsize=17,
        fontweight="bold",
        pad=20
    )

    ax.set_ylabel(
        ylabel,
        fontsize=12
    )

    ax.grid(
        True,
        linestyle=":",
        alpha=0.6
    )

    ax.legend(
        bbox_to_anchor=(1.01, 0.5),
        loc="center left",
        frameon=True,
        shadow=True
    )

    plt.tight_layout()

    plt.savefig(
        filename,
        dpi=300,
        bbox_inches="tight"
    )

    plt.show()

def main():

    df = load_data(FILE_NAME)

    print(
        f"Jumlah data: {len(df):,}"
    )

    daily = prepare_daily_sales(df)

    daily = calculate_moving_average(daily)

    rising_star = get_rising_star(daily)

    print("\n===== RISING STAR =====")

    print(
        rising_star.to_string(index=False)
    )

    packaging = market_basket_analysis(
        df,
        rising_star
    )

    export_excel(
        rising_star,
        packaging
    )

    print(
        "\n[OK] retail_insight.xlsx berhasil dibuat"
    )

    top_sales = (
        df.groupby("nama_produk")["total_nilai"]
        .sum()
        .nlargest(3)
        .index
        .tolist()
    )

    top_rising = (
        rising_star["nama_produk"]
        .head(5)
        .tolist()
    )

    products_plot = list(
        dict.fromkeys(
            top_rising + top_sales
        )
    )

    create_chart(
        daily,
        products_plot,
        "actual",
        "rising_star_actual.png"
    )

    create_chart(
        daily,
        products_plot,
        "index",
        "rising_star_index.png"
    )

if __name__ == "__main__":
    main()