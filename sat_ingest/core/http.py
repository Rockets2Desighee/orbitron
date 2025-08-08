import httpx
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

_DEFAULT_TIMEOUT = httpx.Timeout(30.0)

class HttpClient:
    """Shared HTTP client with retries and timeouts."""

    def __init__(self, headers: dict | None = None):
        self._client = httpx.Client(headers=headers or {}, timeout=_DEFAULT_TIMEOUT)

    @retry(stop=stop_after_attempt(5), wait=wait_exponential(multiplier=0.5, max=10),
           retry=retry_if_exception_type((httpx.ConnectError, httpx.ReadError, httpx.RemoteProtocolError)))
    def get(self, url: str, **kwargs) -> httpx.Response:
        resp = self._client.get(url, **kwargs)
        resp.raise_for_status()
        return resp

    @retry(stop=stop_after_attempt(5), wait=wait_exponential(multiplier=0.5, max=10),
           retry=retry_if_exception_type((httpx.ConnectError, httpx.ReadError, httpx.RemoteProtocolError)))
    def post(self, url: str, json: dict, **kwargs) -> httpx.Response:
        resp = self._client.post(url, json=json, **kwargs)
        resp.raise_for_status()
        return resp

    def stream_download(self, url: str, dest_path: str, chunk_size: int = 1024 * 1024):
        with self._client.stream("GET", url) as r:
            r.raise_for_status()
            with open(dest_path, "wb") as f:
                for chunk in r.iter_bytes(chunk_size=chunk_size):
                    f.write(chunk)