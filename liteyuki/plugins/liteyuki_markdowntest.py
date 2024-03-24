import nonebot
from nonebot import on_command
from nonebot.params import CommandArg
from nonebot.permission import SUPERUSER
from nonebot.plugin import PluginMetadata

from liteyuki.utils.ly_typing import T_Bot, T_MessageEvent, v11
from liteyuki.utils.message import send_markdown

md_test = on_command("mdts", aliases={"会话md"}, permission=SUPERUSER)
md_group = on_command("mdg", aliases={"群md"}, permission=SUPERUSER)
md_conv = on_command("md", block=False, permission=SUPERUSER)

placeholder = {
        "&#91;": "[",
        "&#93;": "]",
        "&amp;": "&",
        "&#44;": ",",
        "\n"   : r"\n",
        "\""   : r'\\\"'
}


@md_test.handle()
async def _(bot: T_Bot, event: T_MessageEvent, arg: v11.Message = CommandArg()):
    await send_markdown(
        str(arg),
        bot,
        message_type=event.message_type,
        session_id=event.user_id if event.message_type == "private" else event.group_id
    )


ignore_msg_ids = []
last_sent = None


@md_conv.handle()
async def _(bot: v11.Bot, event: T_MessageEvent, arg: v11.Message = CommandArg()):
    if str(event.user_id) == str(bot.self_id) and str(bot.self_id) in ["2751454815"]:
        nonebot.logger.info("开始处理：%s" % str(event.message_id))

        data = await send_markdown(str(arg), bot, message_type=event.message_type,
                                   session_id=event.user_id if event.message_type == "private" else event.group_id)
        await bot.delete_msg(message_id=event.message_id)


__author__ = "snowykami"
__plugin_meta__ = PluginMetadata(
    name="轻雪Markdown测试",
    description="用于测试Markdown的插件",
    usage="",
    homepage="https://github.com/snowykami/LiteyukiBot",
    extra={
            "liteyuki": True,
    }
)
