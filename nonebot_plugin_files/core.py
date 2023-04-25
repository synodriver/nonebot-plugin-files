import asyncio
from os.path import join
from typing import List

from nonebot import logger
from nonebot.adapters.onebot.v11 import Bot
from nonebot.exception import ActionFailed

from .abc import BaseHandler
from .models import FileUrlResponse, GroupFileResponse


async def walk_file(
    bot: Bot,
    group_id: int,
    file_id: str,
    file_name: str,
    busid: int,
    current_path,
    handlers: List[BaseHandler],
):
    logger.debug(f"walk_file {current_path} ")
    try:
        data = FileUrlResponse.parse_obj(
            await bot.get_group_file_url(
                group_id=group_id, file_id=file_id, bus_id=busid
            )
        )
        tasks = (
            asyncio.create_task(handler(data.url, file_name, current_path))
            for handler in handlers
        )
        await asyncio.gather(*tasks)
    except ActionFailed as e:
        logger.error(f"{e}: file was baned by tx: {join(current_path, file_name)}")
    except Exception as e:
        logger.error(
            f"exception during downloading {join(current_path, file_name)} : {e}"
        )


async def walk_folder(
    bot: Bot,
    group_id: int,
    folder_id: str,
    folder_name: str,
    current_path,
    handlers: List[BaseHandler],
):
    """遍历文件夹"""
    data = GroupFileResponse.parse_obj(
        await bot.get_group_files_by_folder(group_id=group_id, folder_id=folder_id)
    )
    for file in data.files:
        await walk_file(
            bot,
            group_id,
            file.file_id,
            file.file_name,
            file.busid,
            current_path,
            handlers,
        )
    for folder in data.folders:
        await walk_folder(
            bot,
            group_id,
            folder.folder_id,
            folder.folder_name,
            join(current_path, folder.folder_name),
            handlers,
        )


async def walk_group(
    bot: Bot, group_id: int, handlers: List[BaseHandler], storage_path: str
):
    """

    :param bot:
    :param group_id: 群号
    :param handlers: 下载器
    :param storage_path: 本机存储根目录
    :return:
    """
    logger.debug(f"walk_group {storage_path}")
    data = GroupFileResponse.parse_obj(
        await bot.get_group_root_files(group_id=group_id)
    )
    for file in data.files:
        await walk_file(
            bot,
            group_id,
            file.file_id,
            file.file_name,
            file.busid,
            join(storage_path, str(group_id)),
            handlers,
        )
    for folder in data.folders:
        await walk_folder(
            bot,
            group_id,
            folder.folder_id,
            folder.folder_name,
            join(storage_path, str(group_id), folder.folder_name),
            handlers,
        )
