# The MIT License (MIT)
# Copyright (c) 2021-present nextcore developers
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

from __future__ import annotations

from abc import ABC, abstractmethod
from logging import getLogger
from typing import TYPE_CHECKING

from ..route import Route

if TYPE_CHECKING:
    from typing import Any, Final

    from aiohttp import ClientResponse

logger = getLogger(__name__)

__all__: Final[tuple[str, ...]] = ("AbstractHTTPClient",)


class AbstractHTTPClient(ABC):
    """Abstract base class for HTTP clients.

    This defines :meth:`AbstractHTTPClient._request` for HTTP endpoint wrappers to use.
    """

    __slots__ = ()

    @abstractmethod
    async def _request(
        self,
        route: Route,
        rate_limit_key: str | None,
        *,
        headers: dict[str, str] | None = None,
        bucket_priority: int = 0,
        global_priority: int = 0,
        wait: bool = True,
        **kwargs: Any,
    ) -> ClientResponse:
        ...
