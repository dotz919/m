from pyrogram.errors import ChannelPrivate, UserNotParticipant
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from config import PLAYLIST_IMG_URL, PRIVATE_BOT_MODE, adminlist, MUST_JOIN
from strings import get_string
from ZeebMusic import app
from ZeebMusic.core.call import Yukki
from ZeebMusic.misc import SUDOERS
from ZeebMusic.platforms import youtube
from ZeebMusic.utils.database import (
    get_assistant,
    get_cmode,
    get_lang,
    get_playmode,
    get_playtype,
    is_active_chat,
    is_commanddelete_on,
    is_maintenance,
    is_served_private_chat,
)
from ZeebMusic.utils.inline import botplaylist_markup

# FIX MUST_JOIN jika kosong
try:
    MUST_JOIN
except NameError:
    MUST_JOIN = None


links = {}


def PlayWrapper(command):
    async def wrapper(client, message):
        language = await get_lang(message.chat.id)
        _ = get_string(language)

        # jika anonymous admin
        if message.sender_chat:
            upl = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="How to Fix ?",
                            callback_data="AnonymousAdmin",
                        )
                    ]
                ]
            )
            return await message.reply_text(_["general_4"], reply_markup=upl)

        # FORCE SUB / MUST JOIN CHECK
        if MUST_JOIN:
            try:
                await app.get_chat_member(MUST_JOIN, message.from_user.id)
            except UserNotParticipant:
                link = await app.export_chat_invite_link(MUST_JOIN)
                kontol = InlineKeyboardMarkup(
                    [
                        [InlineKeyboardButton("➕ Gabung Dulu", url=link)]
                    ]
                )
                return await message.reply_text(
                    _["force_sub"].format(message.from_user.mention),
                    reply_markup=kontol,
                )

        # Maintenance mode
        if await is_maintenance() is False:
            if message.from_user.id not in SUDOERS:
                return

        # Private bot mode
        if PRIVATE_BOT_MODE:
            if not await is_served_private_chat(message.chat.id):
                await message.reply_text(
                    "**PRIVATE MUSIC BOT**\n\nOnly For Authorized chats. Ask my owner to allow your chat first."
                )
                return await app.leave_chat(message.chat.id)

        # delete command
        if await is_commanddelete_on(message.chat.id):
            try:
                await message.delete()
            except Exception:
                pass

        # Detection
        audio_telegram = (
            (message.reply_to_message.audio or message.reply_to_message.voice)
            if message.reply_to_message
            else None
        )

        video_telegram = (
            (message.reply_to_message.video or message.reply_to_message.document)
            if message.reply_to_message
            else None
        )

        url = await youtube.url(message)

        # jika tidak ada audio/video/url
        if audio_telegram is None and video_telegram is None and url is None:
            if len(message.command) < 2:
                if "stream" in message.command:
                    return await message.reply_text(_["str_1"])
                buttons = botplaylist_markup(_)
                return await message.reply_photo(
                    photo=PLAYLIST_IMG_URL,
                    caption=_["playlist_1"],
                    reply_markup=InlineKeyboardMarkup(buttons),
                )

        # channel mode
        if message.command[0][0] == "c":
            chat_id = await get_cmode(message.chat.id)
            if chat_id is None:
                return await message.reply_text(_["setting_12"])
            try:
                chat = await app.get_chat(chat_id)
            except Exception:
                return await message.reply_text(_["cplay_4"])
            channel = chat.title
        else:
            chat_id = message.chat.id
            channel = None

        # check voice chat active
        try:
            is_call_active = (await app.get_chat(chat_id)).is_call_active
            if not is_call_active:
                return await message.reply_text(
                    "**No active voice chat found**\n\nPlease start a voicechat first."
                )
        except Exception:
            pass

        # mode play
        playmode = await get_playmode(message.chat.id)
        playty = await get_playtype(message.chat.id)

        # permission check
        if playty != "Everyone":
            if message.from_user.id not in SUDOERS:
                admins = adminlist.get(message.chat.id)
                if not admins:
                    return await message.reply_text(_["admin_18"])
                if message.from_user.id not in admins:
                    return await message.reply_text(_["play_4"])

        # detect video mode
        if message.command[0][0] == "v":
            video = True
        else:
            if "-v" in message.text:
                video = True
            else:
                video = True if message.command[0][1] == "v" else None

        # force play
        if message.command[0][-1] == "e":
            if not await is_active_chat(chat_id):
                return await message.reply_text(_["play_18"])
            fplay = True
        else:
            fplay = None

        # check assistant join VC
        if await is_active_chat(chat_id):
            userbot = await get_assistant(message.chat.id)
            try:
                call_participants_id = [
                    member.chat.id
                    async for member in userbot.get_call_members(chat_id)
                    if member.chat
                ]

                if not call_participants_id or userbot.id not in call_participants_id:
                    await Yukki.stop_stream(chat_id)

            except ChannelPrivate:
                pass

        # execute command real
        return await command(
            client,
            message,
            _,
            chat_id,
            video,
            channel,
            playmode,
            url,
            fplay,
        )

    return wrapper
