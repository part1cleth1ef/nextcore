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

from abc import ABC
from logging import getLogger
from typing import TYPE_CHECKING

from ...route import Route
from ..abstract_client import AbstractHTTPClient

if TYPE_CHECKING:
    from typing import Final

    from discord_typings import GetGatewayBotData, GetGatewayData

    from ...authentication import BotAuthentication

logger = getLogger(__name__)

__all__: Final[tuple[str, ...]] = ("GatewayHTTPWrappers",)


class GatewayHTTPWrappers(AbstractHTTPClient, ABC):
    """HTTP wrappers for gateway API endpoints.

    This is an abstract base class that should not be used directly.
    """

    __slots__ = ()

    async def get_gateway(self) -> GetGatewayData:
        """Gets gateway connection info.

        Read the `documentation <https://discord.dev/topics/gateway#get-gateway>`__ for more info.

        **Example usage:**

        .. code-block:: python

            gateway_info = await http_client.get_gateway()

        Returns
        -------
        discord_typings.GetGatewayData
            The gateway info.
        """
        route = Route("GET", "/gateway", ignore_global=True)
        r = await self._request(route, rate_limit_key=None)

        # TODO: Make this verify the payload from discord?
        return await r.json()  # type: ignore [no-any-return]

    async def get_gateway_bot(
        self,
        authentication: BotAuthentication,
        *,
        bucket_priority: int = 0,
        global_priority: int = 0,
        wait: bool = True,
    ) -> GetGatewayBotData:
        """Gets gateway connection information.

        Read the `documentation <https://discord.dev/topics/gateway#gateway-get-gateway-bot>`__

        **Example usage:**

        .. code-block:: python

            bot_info = await http_client.get_gateway_bot(token)

        Parameters
        ----------
        authentication:
            Authentication info.
        global_priority:
            The priority of the request for the global rate-limiter.
        bucket_priority:
            The priority of the request for the bucket rate-limiter.
        wait:
            Wait when rate limited.

            This will raise :exc:`RateLimitedError` if set to :data:`False` and you are rate limited.

        Raises
        ------
        RateLimitedError
            You are rate limited, and ``wait`` was set to :data:`False`

        Returns
        -------
        discord_typings.GetGatewayBotData
            Gateway connection info.
        """
        route = Route("GET", "/gateway/bot")
        r = await self._request(
            route,
            rate_limit_key=authentication.rate_limit_key,
            headers={"Authorization": str(authentication)},
            bucket_priority=bucket_priority,
            global_priority=global_priority,
            wait=wait,
        )

        # TODO: Make this verify the payload from discord?
        return await r.json()  # type: ignore [no-any-return]
