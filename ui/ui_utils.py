from PySide6.QtWebEngineCore import (
    QWebEngineProfile,
    QWebEngineUrlRequestInfo,
    QWebEngineUrlRequestInterceptor,
)

from PySide6.QtCore import QObject

from abc import ABC, ABCMeta, abstractmethod


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


# class _ABQObjectMeta(type(QObject), ABCMeta):
#     pass


class QABCMeta(ABCMeta, type(QObject)):
    """A metaclass that can be used for abstract QObject-derived classes."""

    pass


class DeckUpdReciever(ABC, metaclass=QABCMeta):
    @abstractmethod
    def decks_updated_reciever(self) -> None:
        pass


class DeckUpdEmitter(ABC, metaclass=QABCMeta):
    @abstractmethod
    def decks_updated_emitter(self) -> None:
        pass


class ProblemsUpdEmitter(ABC, metaclass=QABCMeta):
    @abstractmethod
    def problems_updated_emitter(self) -> None:
        pass


class ProblemsUpdReciever(ABC, metaclass=QABCMeta):
    @abstractmethod
    def problems_updated_reciever(self) -> None:
        pass


class TagsUpdEmitter(ABC, metaclass=QABCMeta):
    @abstractmethod
    def tags_updated_emitter(self) -> None:
        pass


class TagsUpdReciever(ABC, metaclass=QABCMeta):
    @abstractmethod
    def tags_updated_reciever(self) -> None:
        pass

# TODO: Distinguish between emitters and propagators!
