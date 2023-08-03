import streamlit as st
from st_duckduckgo_search_connection import DuckDuckGoSearchConnection

ADVANCE_PARAMS_MAPPING = {
    "text": {"search_term":"your-search-term","search_type":"text","region":"wt-wt", "safesearch":"Off", "timelimit":"y", "backend":"api"},
    "news": {"search_term":"your-search-term","search_type":"news","region":"wt-wt", "safesearch":"Off", "timelimit":"y"},
    "images": {"search_term":"your-search-term","search_type":"images","region":"wt-wt","safesearch":"Off","size":None,"color":"Monochrome","type_image":None,"layout":None,"license_image":None},
    "videos": {"search_term":"your-search-term","search_type":"videos","region":"wt-wt","safesearch":"Off","timelimit":"w","resolution":"high","duration":"medium"},
}
prefix = ",\n"+" "*16
DICT_TO_PARAMS = lambda x: prefix.lstrip(",")+prefix.join([f"""{k}={f'"{v}"' if isinstance(v, str) else v}""" for k,v in x.items()])

LINKS_MAPPING = {
    "text": "https://github.com/deedy5/duckduckgo_search#1-text---text-search-by-duckduckgocom",
    "news": "https://github.com/deedy5/duckduckgo_search#5-news---news-search-by-duckduckgocom",
    "images": "https://github.com/deedy5/duckduckgo_search#3-images---image-search-by-duckduckgocom",
    "videos": "https://github.com/deedy5/duckduckgo_search#4-videos---video-search-by-duckduckgocom"
}
URL_COLS = ["href","image","thumbnail","url","href","content","embed_url"]


st.set_page_config(
    page_title="DuckDuckGoSearch Connection",
    page_icon="https://duckduckgo.com/assets/logo_header.v109.svg",
    menu_items={"About":"""
        Demo app showcasing usage of DuckDuckGoSearchConnection.
        Developed by [Shashank Deshpande](https://www.linkedin.com/in/shashank-deshpande/)
        """
    }
)
st.title("DuckDuckGo Search Connection")
st.write("This is a demo app that presents basic use of DuckDuckGoSearchConnection")
st.write("""
[![view source code ](https://img.shields.io/badge/view%20source%20code-gray?logo=github)](https://github.com/shashankdeshpande/st-duckduckgo-search-connection)
""")


# User inputs
search_term = st.text_input(
    label="Search",
    placeholder='🔍 enter your search term here'
    )
search_type = st.radio(
    label="Search type",
    options=["text","news","images","videos"],
    format_func=lambda x: "default" if x=="text" else x,
    horizontal=True
    )
st.divider()
    
if search_term:
    conn = st.experimental_connection("ddg-search", type=DuckDuckGoSearchConnection)
    df = conn.query(search_term, search_type)

    st.write("#### Code snippet")
    code_snippet = f"""
            from st_duckduckgo_search_connection import DuckDuckGoSearchConnection

            conn = st.experimental_connection("web_search", type=DuckDuckGoSearchConnection)
            df = conn.query("{search_term}"{f''', search_type="{search_type}"''' if search_type!="text" else ""})
        """
    
    st.code(code_snippet, language="python")
    with st.expander("**View advance configuration options 🚀**"):
        st.write("Using proxy, headers and timeout")
        st.code("""
            conn = st.experimental_connection(
                "connection-name",
                type=DuckDuckGoSearchConnection,
                proxies="socks5://localhost:9150",
                headers={
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
                    "Referer": "https://duckduckgo.com/"
                },
                timeout=30
                )
        """, language="python")
        st.write("Additional parameters for search")

        st.code(f"""
            df = conn.query({DICT_TO_PARAMS(ADVANCE_PARAMS_MAPPING[search_type])}
                )
        """, language="python")

        st.info(f"[click here]({LINKS_MAPPING[search_type]}) for more details", icon="💡")
    st.write("##### Search results")

    current_url_cols = set(df.columns).intersection(URL_COLS)
    column_config = {col:st.column_config.LinkColumn(col) for col in current_url_cols}
    st.dataframe(df, column_config=column_config)

    # To preview search results
    if search_type in ["images","videos"]:
        with st.expander("**Preview search results**", expanded=True):
            count = st.select_slider(
                label=f"Top {search_type} to retrieve",
                options=range(1, min(21, df.shape[0])),
                value=min(6, df.shape[0])
            )
            st.write(f"Showing top {count} {search_type} from search results")
            st.warning("Some links might be broken")
            preview_df = df.head(count)

            if search_type == "videos":
                for video_url in preview_df['content']:
                    st.video(video_url)
            else:
                st.image(
                    image=preview_df['image'].tolist(),
                    caption=preview_df['title'].tolist(),
                    width=330)
else:
    st.warning("Enter search term to continue")

