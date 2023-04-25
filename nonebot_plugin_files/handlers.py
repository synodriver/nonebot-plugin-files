# -*- coding: utf-8 -*-
from os import mkdir
from os.path import exists, join, split

import aiofiles
import aiohttp
from nonebot import logger

try:
    import aioaria2
except ImportError:
    aioaria2 = None
try:
    import aioftp
except ImportError:
    aioftp = None
try:
    from aiowebdav.client import Client as WebDavClient
except ImportError:
    aiowebdav = None

from .abc import BaseHandler


def ensure_path(current_path: str):
    """
    Make sure that path exists. If not, create one
    :param current_path:
    :return:
    """
    split_result = split(current_path)
    temp = ""
    for chunk in split_result:
        temp = join(temp, chunk)
        if not exists(temp):
            mkdir(temp)


class MockHandler(BaseHandler):
    """
    调试用的下载器
    """

    async def __call__(self, file_url: str, file_name: str, current_path: str):
        logger.info(rf"found file: {current_path} / {file_name}")

    async def close(self):
        logger.info(f"Mock handler closed")


class BaseDownloadHandler(BaseHandler):
    def __init__(self, config):
        super().__init__(config)
        self.client_session = aiohttp.ClientSession(
            headers={"User-Agent": "QQ/8.2.0.1296 CFNetwork/1126", "Net-Type": "Wifi"}
        )
        self.chunk_size = 60

    async def _iter_content(self, reader):
        while chunk := await reader.read(self.chunk_size):
            yield chunk

    async def __call__(self, file_url: str, file_name: str, current_path: str):
        logger.info(current_path)
        ensure_path(current_path)
        async with aiofiles.open(join(current_path, file_name), "wb") as f:
            async with self.client_session.get(file_url) as resp:
                async for chunk in self._iter_content(resp.content):
                    await f.write(chunk)

    async def close(self):
        await self.client_session.close()


class LogFileHandler(BaseHandler):
    """
    记录文件url 但是不下载
    """

    def __init__(self, config):
        super().__init__(config)

    async def __call__(self, file_url: str, file_name: str, current_path: str):
        # todo 记录到数据库
        pass

    async def close(self):
        pass


class Aria2DownloadHandler(BaseHandler):
    def __init__(self, config):
        assert aioaria2 is not None
        super().__init__(config)
        self.aria2 = aioaria2.Aria2HttpClient(
            config.aria2_url, token=config.aria2_token
        )

    async def __call__(self, file_url: str, file_name: str, current_path: str):
        await self.aria2.addUri(
            [file_url],
            options={
                "dir": current_path,
                "header": [
                    "User-Agent: QQ/8.2.0.1296 CFNetwork/1126",
                    "Net-Type: Wifi",
                ],
                "out": file_name,
            },
        )

    async def close(self):
        await self.aria2.close()


class FTPUploadHandler(BaseHandler):
    def __init__(self, config):
        assert aioftp is not None
        super().__init__(config)
        self.client_session = aiohttp.ClientSession(
            headers={"User-Agent": "QQ/8.2.0.1296 CFNetwork/1126", "Net-Type": "Wifi"}
        )
        self.chunk_size = 60
        self.ftp = aioftp.Client()
        self._connected = False

    async def _connect(self):
        # await self.ftp.context
        assert not self._connected
        await self.ftp.connect(self.config.ftp_host, self.config.ftp_port or 21)
        await self.ftp.login(
            self.config.ftp_user, self.config.ftp_password, self.config.ftp_account
        )
        self._connected = True

    async def _iter_content(self, reader):
        while chunk := await reader.read(self.chunk_size):
            yield chunk

    async def __call__(self, file_url: str, file_name: str, current_path: str):
        if not self._connected:
            await self._connect()
        async with self.ftp.upload_stream(
            join(self.config.ftp_root, current_path)
        ) as stream:
            async with self.client_session.get(file_url) as resp:
                async for chunk in self._iter_content(resp.content):
                    await stream.write(chunk)

    async def close(self):
        await self.ftp.quit()


class WebDavUploadHandler(BaseHandler):
    def __init__(self, config):
        assert aiowebdav is not None
        super().__init__(config)
        self.client_session = aiohttp.ClientSession(
            headers={"User-Agent": "QQ/8.2.0.1296 CFNetwork/1126", "Net-Type": "Wifi"}
        )
        self.chunk_size = 60
        self.webdav = WebDavClient(
            {
                "webdav_hostname": config.webdav_hostname,
                "webdav_login": config.webdav_login,
                "webdav_password": config.webdav_password,
                "webdav_root": config.webdav_root,
            }
        )

    async def _iter_content(self, reader):
        while chunk := await reader.read(self.chunk_size):
            yield chunk

    async def __call__(self, file_url: str, file_name: str, current_path: str):
        async with self.client_session.get(file_url) as resp:
            await self.webdav.upload_iter(
                self._iter_content(resp.content), join(current_path, file_name)
            )

    async def close(self):
        await self.client_session.close()
        await self.webdav.close()
