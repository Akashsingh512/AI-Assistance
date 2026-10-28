import webbrowser

class BrowserManager:
    @staticmethod
    def open_website(url_or_query: str) -> str:
        # Check if it looks like a URL
        if "." in url_or_query and " " not in url_or_query:
            url = url_or_query if url_or_query.startswith("http") else f"https://{url_or_query}"
            webbrowser.open(url)
            return f"Opened website: {url}"
        else:
            # Otherwise, treat as a search query
            search_url = f"https://www.google.com/search?q={url_or_query.replace(' ', '+')}"
            webbrowser.open(search_url)
            return f"Searched Google for: {url_or_query}"
