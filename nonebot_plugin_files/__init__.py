# -*- coding: utf-8 -*-
import asyncio
from typing import TYPE_CHECKING, Dict, Type

from nonebot import get_driver, logger, on_shell_command
from nonebot.adapters.onebot.v11 import (
    Bot,
    Event,
    GroupMessageEvent,
    MessageEvent,
    PrivateMessageEvent,
)
from nonebot.params import ShellCommandArgs
from nonebot.permission import SUPERUSER
from nonebot.rule import ArgumentParser, Namespace, Rule

from .core import walk_group
from .handlers import (
    Aria2DownloadHandler,
    BaseDownloadHandler,
    FTPUploadHandler,
    LogFileHandler,
    MockHandler,
    WebDavUploadHandler,
)

if TYPE_CHECKING:
    from .abc import BaseHandler
driver = get_driver()
config = driver.config

handlers_t: Dict[str, Type["BaseHandler"]] = {
    "download": BaseDownloadHandler,
    "aria2": Aria2DownloadHandler,
    "ftp": FTPUploadHandler,
    "webdav": WebDavUploadHandler,
    "log": LogFileHandler,
    "test": MockHandler,
}

parser = ArgumentParser()
parser.add_argument("-g", "--group", type=int)
parser.add_argument("-t", "--type", nargs="+")  # ftp webdave aria2


async def check_bot(bot: Bot, event: Event) -> bool:
    return True if event.self_id in config.SYNC_ALLOW_BOTS else False


matcher = on_shell_command(
    "同步", rule=Rule(check_bot), permission=SUPERUSER, parser=parser
)


@matcher.handle()
async def hanlde_sync(
    bot: Bot, event: MessageEvent, args: Namespace = ShellCommandArgs()
):
    logger.debug("handle sync")
    group_id = args.group
    if not group_id and isinstance(event, PrivateMessageEvent):
        # await matcher.finish("参数错误")
        logger.error(f"私聊的时候需要 -g")
    if not group_id and isinstance(event, GroupMessageEvent):
        group_id = event.group_id
    try:
        if not args.type:
            handlers = [BaseDownloadHandler(config)]
        else:
            handlers = [handlers_t[t](config) for t in args.type]
        logger.debug(f"using handlers {handlers}")
        await walk_group(bot, group_id, handlers, config.storage_path)
    except KeyError as e:
        logger.error(f"wrong handler type: {e}")
    except Exception:
        raise
    else:
        # await matcher.send(event, "同步完成")
        logger.debug(f"同步群{group_id} 文件完成")
    finally:
        # 无论如何都要close
        await asyncio.gather(
            *(asyncio.create_task(handler.close()) for handler in handlers)
        )