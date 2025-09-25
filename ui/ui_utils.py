from typing import Dict
from PySide6.QtWebEngineCore import (
    QWebEngineProfile,
    QWebEngineUrlRequestInfo,
    QWebEngineUrlRequestInterceptor,
)


class NoInternetProfile(QWebEngineProfile):
    """
    Custom QWebEngineProfile object that returns one with the default profile
    (off-the-record) and with internet access blocked.
    """

    def __init__(self):
        super().__init__()

        self.defaultProfile()
        self.interceptor = self.BlockedRequestInterceptor()
        self.setUrlRequestInterceptor(self.interceptor)

    class BlockedRequestInterceptor(QWebEngineUrlRequestInterceptor):
        """
        Custom class of QWebEngineUrlRequestInterceptor that sets a
        QWebEngineProfile to block any access to internet.
        """

        def interceptRequest(self, info: QWebEngineUrlRequestInfo):
            url = info.requestUrl()
            if url.scheme() in ["file", "data"]:
                # Allow local files and local data
                info.block(False)
            else:
                # Block all requests
                info.block(True)


update_decks_from_db: Dict[str, bool] = {}
