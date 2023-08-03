# Streamlit DuckDuckGo Search Connection

## Demo App
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://duckduckgo-search-connection.streamlit.app/)
## Setup
Basic
```python
from st_duckduckgo_search_connection import DuckDuckGoSearchConnection
conn = st.experimental_connection("connection-name", type=DuckDuckGoSearchConnection)
```
Advance - configuration of proxy, headers, timeout
```python
from st_duckduckgo_search_connection import DuckDuckGoSearchConnection
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
```

## Sample Usage
*Default search*
```python
df = conn.query("search-term")
```
*Supported search types*
- news
- images
- videos

```python
df = conn.query("search-term", search_type="news") #images|videos
```
*For advance search parameters, refer - https://pypi.org/project/duckduckgo-search/*