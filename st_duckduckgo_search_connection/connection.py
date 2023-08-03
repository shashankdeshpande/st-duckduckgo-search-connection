import pandas as pd
from duckduckgo_search import DDGS
from typing import Union, Optional, Literal
from streamlit.runtime.caching import cache_data
from streamlit.connections import ExperimentalBaseConnection

SEARCH_TYPES = Literal["text", "news", "images", "videos"]

class DuckDuckGoSearchConnection(ExperimentalBaseConnection[DDGS]):
    """A connection to a DuckDuckGo search using duckduckgo_search package

    Reference: https://pypi.org/project/duckduckgo-search/

    It handles following types of search methods - 
    - Text: Perform a text search and retrieve a list of search results.
    - News: Perform a news search and retrieve a list of news articles related to the query.
    - Image:  Perform an image search and retrieve a list of image URLs.
    - Video: Perform a video search and retrieve a list of video results.
    """

    def __init__(self, connection_name: str = "default", **kwargs) -> None:
        super().__init__(connection_name, **kwargs)

    def _connect(self, **kwargs) -> DDGS:
        """Method to initialize DDGS"""

        ddgs = DDGS(**kwargs)
        return ddgs
    
    @property
    def ddgs(self):
        """Method to get instance of DDGS"""

        return self._instance
    
    def query(
        self,
        search_term: str,
        search_type: SEARCH_TYPES = "text",
        ttl: Optional[Union[int, None]] = 3600,
        **kwargs
        ) -> pd.DataFrame:
        """Method to perform duckduckgo search

        Args:
            search_term: search term
            search_type: text, news, images, videos. Defaults to text
            ttl: Time to live in seconds. Defaults to 3600
        """
        
        @cache_data(ttl=ttl)
        def _search_text(search_term, **kwargs) -> pd.DataFrame:
            """
            Text search: Wraps ddgs.text() method
            Reference: https://github.com/deedy5/duckduckgo_search#1-text---text-search-by-duckduckgocom
            """
            results = self.ddgs.text(keywords=search_term, **kwargs)
            return pd.DataFrame(results)
        
        @cache_data(ttl=ttl)
        def _search_news(search_term, **kwargs) -> pd.DataFrame:
            """
            News search: Wraps ddgs.news() method
            Reference: https://github.com/deedy5/duckduckgo_search#5-news---news-search-by-duckduckgocom
            """
            results = self.ddgs.news(keywords=search_term, **kwargs)
            return pd.DataFrame(results)
        
        @cache_data(ttl=ttl)
        def _search_images(search_term, **kwargs) -> pd.DataFrame:
            """
            Image search: Wraps ddgs.images() method
            Reference: https://github.com/deedy5/duckduckgo_search#3-images---image-search-by-duckduckgocom
            """
            results = self.ddgs.images(keywords=search_term, **kwargs)
            return pd.DataFrame(results)
        
        @cache_data(ttl=ttl)
        def _search_videos(search_term, **kwargs) -> pd.DataFrame:
            """
            Video search: Wraps ddgs.videos() method
            Reference: https://github.com/deedy5/duckduckgo_search#4-videos---video-search-by-duckduckgocom
            """
            results = self.ddgs.videos(keywords=search_term, **kwargs)
            return pd.DataFrame(results)
        
        if search_type == "text":
            return _search_text(search_term, **kwargs)
        elif search_type == "news":
            return _search_news(search_term, **kwargs)
        elif search_type == "images":
            return _search_images(search_term, **kwargs)
        elif search_type == "videos":
            return _search_videos(search_term, **kwargs)
        raise ValueError(f"{search_type} is not a valid value for `search_type=`.")