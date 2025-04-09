import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Simple Sales Summary", layout="centered")
st.title("📊 Sales Summary + Q&A")

# Hardcoded CSV path
file_path = "orders.csv"

if os.path.exists(file_path):
    try:
        df = pd.read_csv(file_path)

        # Validate required columns
        required_cols = ['State', 'Category', 'Sub-Category', 'Sales', 'Profit']
        if not all(col in df.columns for col in required_cols):
            st.error("The dataset must include 'State', 'Category', 'Sub-Category', 'Sales', and 'Profit' columns.")
        else:
            # Generate simple summary using pandas
            top_state_sales = df.groupby('State')['Sales'].sum().idxmax()
            top_state_profit = df.groupby('State')['Profit'].sum().idxmax()

            top_cat_sales = df.groupby('Category')['Sales'].sum().idxmax()
            top_cat_profit = df.groupby('Category')['Profit'].sum().idxmax()

            top_subcat_sales = df.groupby('Sub-Category')['Sales'].sum().idxmax()
            top_subcat_profit = df.groupby('Sub-Category')['Profit'].sum().idxmax()

            st.subheader("📌 Summary (Based on Sales & Profit)")
            st.markdown(f"""
                - 🏆 **Top State by Sales**: {top_state_sales}  
                - 💰 **Top State by Profit**: {top_state_profit}  
                - 📦 **Top Category by Sales**: {top_cat_sales}  
                - 📈 **Top Category by Profit**: {top_cat_profit}  
                - 🔍 **Top Sub-Category by Sales**: {top_subcat_sales}  
                - 💼 **Top Sub-Category by Profit**: {top_subcat_profit}
            """)

            # Simple Q&A chatbot
            st.subheader("💬 Ask a Question About the Data")
            question = st.text_input("Example: Top 3 states by sales")

            if question:
                q = question.lower()

                try:
                    if "top" in q and "state" in q:
                        n = int([word for word in q.split() if word.isdigit()][0])
                        top_states = df.groupby('State')['Sales'].sum().sort_values(ascending=False).head(n)
                        result = "\n".join([f"{i+1}. {state}: ${val:,.2f}" for i, (state, val) in enumerate(top_states.items())])
                        st.text(f"Top {n} states by sales:\n{result}")

                    elif "lowest" in q and "sub" in q:
                        bottom_subs = df.groupby('Sub-Category')['Sales'].sum().sort_values().head(5)
                        result = "\n".join([f"{i+1}. {sub}: ${val:,.2f}" for i, (sub, val) in enumerate(bottom_subs.items())])
                        st.text("Lowest 5 Sub-Categories by Sales:\n" + result)

                    elif "average sales by category" in q:
                        avg_sales = df.groupby('Category')['Sales'].mean()
                        result = "\n".join([f"{cat}: ${val:,.2f}" for cat, val in avg_sales.items()])
                        st.text("Average Sales by Category:\n" + result)

                    elif "average profit" in q:
                        avg_profit = df['Profit'].mean()
                        st.text(f"Average profit: ${avg_profit:,.2f}")

                    else:
                        st.info("Try something like:\n- Top 3 states by sales\n- Lowest sub category by sales\n- Average sales by category")
                except Exception as e:
                    st.error(f"Could not answer the question: {e}")

    except Exception as e:
        st.error(f"Error reading file: {e}")
else:
    st.error("❌ File not found at the specified path.")
