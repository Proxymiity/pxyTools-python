import requests as www


class HTTPCacheInterface:
    __slots__ = ("base", "token", "ingress", "api", "name", "requests", "get_requests")

    def __init__(self, base: str, token: str, name=None):
        self.base = base
        self.token = token
        self.ingress = base + "/ingress"
        self.api = base + "/api"
        self.name = name or "http_cache_interface"
        self.requests = 0
        self.get_requests = 0

    def cached(self, url: str):
        return _cached(self, url)

    def cache(self, url: str):
        print(f"[{self.name}] Backend download for {url}")
        rq = www.get(self.api, params={"token": self.token, "url": url, "create": True})
        self.get_requests += 1
        rj = rq.json()
        return {"cached": rj["cached"], "url": rj["url"]}


class MDCacheInterface:
    __slots__ = ("base", "token", "ingress", "api", "name", "requests", "get_requests")

    def __init__(self, base: str, token: str, name=None):
        self.base = base
        self.token = token
        self.ingress = base + "/ingress"
        self.api = base + "/api"
        self.name = name or "md_cache_interface"
        self.requests = 0
        self.get_requests = 0

    def cached(self, url: str):
        return _cached(self, url)

    def cache(self, url: str):
        print(f"[{self.name}] Backend download for {url}")
        rq = www.get(self.ingress, params={"token": self.token, "url": url})
        self.get_requests += 1
        rj = rq.json()
        rj["md_url"] = rj.pop("url")
        cached_url = rj.pop("api_response")["url"]
        return {**rj, "url": cached_url}


def _cached(self, url):
    print(f"[{self.name}] Backend request for {url}")
    rq = www.get(self.api, params={"token": self.token, "url": url})
    self.requests += 1
    rj = rq.json()
    return {"cached": rj["cached"], "url": rj["url"]}
