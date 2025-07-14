import streamlit as st
import streamlit.components.v1 as components
import urllib.parse

st.set_page_config(layout="wide")
st.title("📊 Tableau Dashboard Embed (filters shown in URL but not applied)")

# UI filters
regions = st.multiselect("Select Region(s):", ["East", "West", "Central", "South"])
categories = st.multiselect("Select Category(s):", ["Furniture", "Office Supplies", "Technology"])

# Build query params
params = {}
if regions:
    params["Region"] = ",".join(regions)
if categories:
    params["Category"] = ",".join(categories)

query_string = urllib.parse.urlencode(params)

# Base Tableau embed URL
base_url = "https://prod-useast-b.online.tableau.com/t/nylanalytics/views/Book1_test_17521798367410/Dashboard1"
embed_url = f"{base_url}?{query_string}" if query_string else base_url

# Show the URL being used (for demo purposes)
st.markdown("**🔗 Tableau Embed URL:**")
st.code(embed_url, language="text")

# HTML with <tableau-viz> and dynamic URL
html_code = f"""
<!DOCTYPE html>
<html>
  <head>
    <script type='module' src='https://prod-useast-b.online.tableau.com/javascripts/api/tableau.embedding.3.latest.min.js'></script>
    <style>
      .scroll-container {{
        width: 100%;
        overflow-x: auto;
      }}

      tableau-viz {{
        min-width: 900px;
        height: 900px;
        display: block;
      }}
    </style>
  </head>
  <body>
    <div class="scroll-container">
      <tableau-viz
        id='tableau-viz'
        src='{embed_url}'
        toolbar='bottom'
        hide-tabs>
      </tableau-viz>
    </div>
  </body>
</html>
"""

components.html(html_code, height=950, scrolling=True)

