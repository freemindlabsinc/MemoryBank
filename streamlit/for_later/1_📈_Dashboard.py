import streamlit as st
import pandas as pd
import altair as alt
from urllib.error import URLError

st.set_page_config(page_title="Dashboard", page_icon="📈", 
                   layout="wide", initial_sidebar_state="expanded",
                   menu_items={
                        'Get Help': 'https://www.extremelycoolapp.com/help',
                        'Report a bug': "https://www.extremelycoolapp.com/bug",
                        'About': "# This is a header. This is an *extremely* cool app!"
                   })

st.markdown("# DataFrame DemoX")
st.sidebar.header("DataFrame DemoY")
st.write(
    """This demo shows how to use `st.write` to visualize Pandas DataFrames.
(Data courtesy of the [UN Data Explorer](http://data.un.org/Explorer.aspx).)"""
)


@st.cache_data
def get_UN_data():
    AWS_BUCKET_URL = "http://streamlit-demo-data.s3-us-west-2.amazonaws.com"
    df = pd.read_csv(AWS_BUCKET_URL + "/agri.csv.gz")
    return df.set_index("Region")


try:
    df = get_UN_data()
    countries = st.multiselect(
        "Choose countries", list(df.index), ["China", "United States of America"]
    )
    if not countries:
        st.error("Please select at least one country.")
    else:
        data = df.loc[countries]
        data /= 1000000.0
        tmp = data.sort_index()
        st.write("### Gross Agricultural Production ($B)", tmp)

    
        data = data.T.reset_index()
        data = pd.melt(data, id_vars=["index"]).rename(
            columns={"index": "year", "value": "Gross Agricultural Product ($B)"}
        )
        chart = (
            alt.Chart(data)
            .mark_area(opacity=0.3)
            .encode(
                x="year:T",
                y=alt.Y("Gross Agricultural Product ($B):Q", stack=None),
                color="Region:N",
            )
        )
        st.altair_chart(chart, use_container_width=True)
except URLError as e:
    st.error(
        """
        **This demo requires internet access.**
        Connection error: %s
    """
        % e.reason
    )