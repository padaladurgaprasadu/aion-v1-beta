import urllib.request
import json
import urllib.parse
from backend.utils.logger import get_logger

logger = get_logger("AiON_Visuals")

def get_wiki_image(query: str) -> str:
    """
    Searches Wikipedia for the query and returns the URL of the main thumbnail/image
    associated with the primary article.
    """
    if not query:
        return None
        
    try:
        # First search for the article to get the exact title
        search_url = f"https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch={urllib.parse.quote(query)}&utf8=&format=json"
        req = urllib.request.Request(search_url, headers={'User-Agent': 'AiON/1.0 (https://aion.ai; contact@aion.ai)'})
        
        with urllib.request.urlopen(req) as response:
            search_data = json.loads(response.read().decode())
            
        if not search_data.get('query', {}).get('search'):
            return None
            
        title = search_data['query']['search'][0]['title']
        
        # Then fetch the original image for that exact title
        img_url = f"https://en.wikipedia.org/w/api.php?action=query&prop=pageimages&format=json&piprop=original&titles={urllib.parse.quote(title)}"
        req2 = urllib.request.Request(img_url, headers={'User-Agent': 'AiON/1.0 (https://aion.ai; contact@aion.ai)'})
        
        with urllib.request.urlopen(req2) as response:
            img_data = json.loads(response.read().decode())
            
        pages = img_data.get('query', {}).get('pages', {})
        for page_id, page_info in pages.items():
            if 'original' in page_info:
                return page_info['original']['source']
                
        return None
    except Exception as e:
        logger.error(f"Visuals: Failed to fetch Wiki image for {query} - {e}")
        return None
