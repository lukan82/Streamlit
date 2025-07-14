import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load the data
df = pd.read_csv("orders.csv")

# --- Get and clean query parameters ---
query_params = st.query_params

def clean_filter(param):
    raw = query_params.get(param, [])

    # If it was split character by character (e.g., 'South' → ['S','o','u','t','h'])
    if len(raw) > 1 and all(len(r) == 1 for r in raw):
        combined = ''.join(raw)
        return [] if combined.upper() == "ALL" else [combined]

    # Comma-separated values like ['South,East']
    if len(raw) == 1 and ',' in raw[0]:
        values = [v.strip() for v in raw[0].split(',')]
        return [] if "ALL" in [v.upper() for v in values] else values

    # Normal case
    if raw and raw[0].strip().upper() == "ALL":
        return []
    return [r.strip() for r in raw if r.strip()]

region_filters = clean_filter("Region")
category_filters = clean_filter("Category")

# --- Filter the data ---
filtered_df = df.copy()
if region_filters:
    filtered_df = filtered_df[filtered_df["Region"].isin(region_filters)]
if category_filters:
    filtered_df = filtered_df[filtered_df["Category"].isin(category_filters)]

# --- Format sales nicely ---
def format_currency(val):
    if val >= 1_000_000:
        return f"${val/1_000_000:.1f}M"
    elif val >= 1_000:
        return f"${val/1_000:.1f}K"
    else:
        return f"${val:.0f}"

# --- Dashboard Title ---
st.markdown("<h1 style='font-size: 40px;'>📊 Sales Dashboard</h1>", unsafe_allow_html=True)

# --- Filter Summary Display ---
region_display = ", ".join(region_filters) if region_filters else "All"
category_display = ", ".join(category_filters) if category_filters else "All"
st.success(f"Filtered by: Region = {region_display} | Category = {category_display}")

# --- Layout Charts Side by Side ---
col1, spacer, col2 = st.columns([5, 1, 5])

# --- Chart 1: Sales by Region ---
with col1:
    st.markdown("### Sales by Region")
    if not filtered_df.empty:
        region_sales = filtered_df.groupby("Region")["Sales"].sum().sort_values()
        fig1, ax1 = plt.subplots(figsize=(6, 4))
        bars = ax1.barh(region_sales.index, region_sales.values, color="#4C72B0")
        ax1.set_xlabel("Sales", fontsize=12)
        ax1.set_ylabel("Region", fontsize=12)
        ax1.tick_params(labelsize=11)

        for bar in bars:
            width = bar.get_width()
            ax1.text(width + 0.02 * region_sales.max(), bar.get_y() + bar.get_height()/2,
                     format_currency(width), va='center', fontsize=11, fontweight='bold')

        plt.tight_layout()
        st.pyplot(fig1)
    else:
        st.warning("No data for selected Region filters.")

# --- Chart 2: Sales by Category ---
with col2:
    st.markdown("### Sales by Category")
    if not filtered_df.empty:
        category_sales = filtered_df.groupby("Category")["Sales"].sum().sort_values()
        fig2, ax2 = plt.subplots(figsize=(6, 4))
        bars = ax2.barh(category_sales.index, category_sales.values, color="#DD8452")
        ax2.set_xlabel("Sales", fontsize=12)
        ax2.set_ylabel("Category", fontsize=12)
        ax2.tick_params(labelsize=11)

        for bar in bars:
            width = bar.get_width()
            ax2.text(width + 0.02 * category_sales.max(), bar.get_y() + bar.get_height()/2,
                     format_currency(width), va='center', fontsize=11, fontweight='bold')

        plt.tight_layout()
        st.pyplot(fig2)
    else:
        st.warning("No data for selected Category filters.")









