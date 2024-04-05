import json
import platform

import nonebot
import psutil
from cpuinfo import get_cpu_info
from nonebot import on_command
from nonebot.adapters.onebot.v11 import MessageSegment
from nonebot.permission import SUPERUSER
from playwright.async_api import async_playwright
from liteyuki.utils import __NAME__, __VERSION__, load_from_yaml
from liteyuki.utils.htmlrender import template2image
from liteyuki.utils.language import Language, get_default_lang, get_user_lang
from liteyuki.utils.ly_typing import T_Bot, T_MessageEvent
from liteyuki.utils.resource import get_path
from liteyuki.utils.tools import convert_size

stats = on_command("stats", aliases={"状态"}, priority=5, permission=SUPERUSER)

config = load_from_yaml("config.yml")

protocol_names = {
        0: "iPad",
        1: "Android Phone",
        2: "Android Watch",
        3: "Mac",
        5: "iPad",
        6: "Android Pad",
}




@stats.handle()
async def _(bot: T_Bot, event: T_MessageEvent):
    ulang = get_user_lang(str(event.user_id))
    image = await template2image(
        get_path("templates/stats.html", abs_path=True),
        {
                "data": await get_stats_data(bot.self_id, ulang.lang_code)
        },
        debug=True
    )
    await stats.finish(MessageSegment.image(image))


async def get_bots_data(ulang: Language, self_id: "") -> list:
    bots_data = []
    for bot_id, bot in nonebot.get_bots().items():
        groups = 0
        friends = 0
        status = {}
        bot_name = bot_id
        version_info = {}
        try:
            bot_name = (await bot.get_login_info())["nickname"]
            groups = len(await bot.get_group_list())
            friends = len(await bot.get_friend_list())
            status = await bot.get_status()
            version_info = await bot.get_version_info()
        except Exception:
            pass

        statistics = status.get("stat", {})
        app_name = version_info.get("app_name", "UnknownImplementation")
        if app_name in ["Lagrange.OneBot", "LLOneBot", "Shamrock"]:
            icon = f"https://q.qlogo.cn/g?b=qq&nk={bot_id}&s=640"
        else:
            icon = "./img/liteyuki.png"
        bot_data = {
                "name": bot_name,
                "icon": icon,
                "id"  : bot_id,
                "tags": [
                        protocol_names.get(version_info.get("protocol_name"), "Online"),
                        f"{ulang.get('liteyuki.stats.groups')} {groups}",
                        f"{ulang.get('liteyuki.stats.friends')} {friends}",
                        f"{ulang.get('liteyuki.stats.sent')} {statistics.get('message_sent', 0)}",
                        f"{ulang.get('liteyuki.stats.received')} {statistics.get('message_received', 0)}",
                        app_name,

                ],
                "self": bot_id == self_id,  # 判断是否是自己
        }
        bots_data.append(bot_data)
    bots_data.append(
        {
                "name": "Liteyuki",
                "icon": "./img/liteyuki.png",
                "id"  : "liteyuki",
                "tags": [
                        f"{__NAME__} {__VERSION__}",
                        f"{ulang.get('liteyuki.stats.plugins')} {len(nonebot.get_loaded_plugins())}",
                        f"Nonebot {nonebot.__version__}",
                        f"{platform.python_implementation()} {platform.python_version()}",
                ]
        }
    )
    return bots_data


async def get_stats_data(self_id: str = None, lang: str = None):
    if self_id is None:
        self_id = list(nonebot.get_bots().keys())[0] if len(nonebot.get_bots()) > 0 else "liteyuki"
    if lang is None:
        ulang = get_default_lang()
    else:
        ulang = Language(lang)

    fake_device_info: dict = config.get("fake_device_info", {})

    mem_info = psutil.virtual_memory()
    mem_total = fake_device_info.get('mem', {}).get('total', mem_info.total)

    convert_size(mem_total, 1, False)
    mem_total_show = convert_size(mem_total, 1)  # 格式化带单位

    mem_used_bot = psutil.Process().memory_info().rss
    mem_used_bot_show = convert_size(mem_used_bot, 1)
    mem_used_other = mem_info.used - mem_used_bot
    mem_free = mem_total - mem_info.used
    mem_used_show = convert_size(mem_total - mem_used_bot - mem_used_other, 1)  # 计算已用格式化带单位

    swap_info = psutil.swap_memory()

    disk_data = []
    for disk in psutil.disk_partitions(all=True):
        disk_usage = psutil.disk_usage(disk.mountpoint)
        disk_total_show = convert_size(disk_usage.total, 1)
        disk_free_show = convert_size(disk_usage.free, 1)
        disk_data.append(
            {
                    "name"   : disk.device,
                    "total"  : disk_total_show,
                    "free"   : disk_free_show,
                    "percent": disk_usage.percent,
            }
        )

    cpu_info = get_cpu_info()
    if "AMD" in cpu_info.get("brand_raw", ""):
        brand = "AMD"
    elif "Intel" in cpu_info.get("brand_raw", ""):
        brand = "Intel"
    else:
        brand = "Unknown"

    if fake_device_info.get("cpu", {}).get("brand"):
        brand = fake_device_info.get("cpu", {}).get("brand")

    cpu_info = get_cpu_info()
    templ = {
            "cpu"        : [
                    {
                            "name" : "USED",
                            "value": psutil.cpu_percent(interval=1)
                    },
                    {
                            "name" : "FREE",
                            "value": 100 - psutil.cpu_percent(interval=1)
                    }
            ],
            "mem"        : [

                    {
                            "name" : "OTHER",
                            "value": mem_used_other
                    },
                    {
                            "name" : "FREE",
                            "value": mem_free
                    },
                    {
                            "name" : "BOT",
                            "value": mem_used_bot
                    },
            ],
            "swap"       : [
                    {
                            "name" : "USED",
                            "value": psutil.swap_memory().used
                    },
                    {
                            "name" : "FREE",
                            "value": psutil.swap_memory().free
                    }
            ],
            "disk"       : disk_data,  # list[{"name":"C", "total":100, "used":50, "free":50}]
            "bot"        : await get_bots_data(ulang, self_id),
            "cpuTags"    : [
                    f"{brand} {cpu_info.get('arch', 'Unknown')}",
                    f"{fake_device_info.get('cpu', {}).get('cores', psutil.cpu_count(logical=False))}C "
                    f"{fake_device_info.get('cpu', {}).get('logical_cores', psutil.cpu_count(logical=True))}T",
                    f"{fake_device_info.get('cpu', {}).get('frequency', psutil.cpu_freq().current) / 1000}GHz"
            ],
            "memTags"    : [
                    f"Bot {mem_used_bot_show}",
                    f"{ulang.get('main.monitor.used')} {mem_used_show}",
                    f"{ulang.get('main.monitor.total')} {mem_total_show}",
                    f"{ulang.get('main.monitor.free')} {convert_size(mem_free, 1)}",
            ],
            "swapTags"   : [
                    f"{ulang.get('main.monitor.used')} {convert_size(swap_info.used, 1)}",
                    f"{ulang.get('main.monitor.total')} {convert_size(swap_info.total, 1)}",
                    f"{ulang.get('main.monitor.free')} {convert_size(swap_info.free, 1)}",
            ],
            "cpu_trans"  : ulang.get("main.monitor.cpu"),
            "mem_trans"  : ulang.get("main.monitor.memory"),
            "swap_trans" : ulang.get("main.monitor.swap"),
            "used_trans" : ulang.get("main.monitor.used"),
            "free_trans" : ulang.get("main.monitor.free"),
            "total_trans": ulang.get("main.monitor.total"),
    }
    return templ