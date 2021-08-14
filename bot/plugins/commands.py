#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) @AlbertEinsteinTG

from pyrogram import filters, Client
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from bot import Translation # pylint: disable=import-error
from bot.database import Database # pylint: disable=import-error

db = Database()

@Client.on_message(filters.command(["start"]) & filters.private, group=1)
async def start(bot, update):
    
    try:
        file_uid = update.command[1]
    except IndexError:
        file_uid = False
    
    if file_uid:
        file_id, file_name, file_caption, file_type = await db.get_file(file_uid)
        
        if (file_id or file_type) == None:
            return
        
        caption = file_caption if file_caption != ("" or None) else ("<code>" + file_name + "</code>")
        
        if file_type == "document":
        
            await bot.send_document(
                chat_id=update.chat.id,
                document = file_id,
                caption = caption,
                parse_mode="html",
                reply_to_message_id=update.message_id,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton
                                (
                                    'Developers', url="https://t.me/CrazyBotsz"
                                )
                        ]
                    ]
                )
            )

        elif file_type == "video":
        
            await bot.send_video(
                chat_id=update.chat.id,
                video = file_id,
                caption = caption,
                parse_mode="html",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton
                                (
                                    'Developers', url="https://t.me/CrazyBotsz"
                                )
                        ]
                    ]
                )
            )
            
        elif file_type == "audio":
        
            await bot.send_audio(
                chat_id=update.chat.id,
                audio = file_id,
                caption = caption,
                parse_mode="html",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton
                                (
                                    'Developers', url="https://t.me/CrazyBotsz"
                                )
                        ]
                    ]
                )
            )

        else:
            print(file_type)
        
        return

    buttons = [[
        InlineKeyboardButton('Developers', url='https://t.me/CrazyBotsz'),
        InlineKeyboardButton('Source Code 🧾', url ='https://github.com/CrazyBotsz/Adv-Auto-Filter-Bot-V2')
    ],[
        InlineKeyboardButton('Support 🛠', url='https://t.me/CrazyBotszGrp')
    ],[
        InlineKeyboardButton('Help ⚙', callback_data="help")
    ]]
    
    reply_markup = InlineKeyboardMarkup(buttons)
    
    await bot.send_message(
        chat_id=update.chat.id,
        text=Translation.START_TEXT.format(
                update.from_user.first_name),
        reply_markup=reply_markup,
        parse_mode="html",
        reply_to_message_id=update.message_id
    )


@Client.on_message(filters.command(["help"]) & filters.private, group=1)
async def help(bot, update):
    buttons = [[
        InlineKeyboardButton('Home ⚡', callback_data='start'),
        InlineKeyboardButton('About 🚩', callback_data='about')
    ],[
        InlineKeyboardButton('Close 🔐', callback_data='close')
    ]]
    
    reply_markup = InlineKeyboardMarkup(buttons)
    
    await bot.send_message(
        chat_id=update.chat.id,
        text=Translation.HELP_TEXT,
        reply_markup=reply_markup,
        parse_mode="html",
        reply_to_message_id=update.message_id
    )


@Client.on_message(filters.command(["about"]) & filters.private, group=1)
async def about(bot, update):
    
    buttons = [[
        InlineKeyboardButton('Home ⚡', callback_data='start'),
        InlineKeyboardButton('Close 🔐', callback_data='close')
    ]]
    reply_markup = InlineKeyboardMarkup(buttons)
    
    await bot.send_message(
        chat_id=update.chat.id,
        text=Translation.ABOUT_TEXT,
        reply_markup=reply_markup,
        disable_web_page_preview=True,
        parse_mode="html",
        reply_to_message_id=update.message_id
    )
import logging
logger = logging.getLogger(__name__)

import datetime
from ..config import Config
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import UserNotParticipant, ChatAdminRequired, UsernameNotOccupied


@Client.on_message(filters.private & filters.incoming)
async def force_sub(c, m):
    if Config.FORCE_SUB:
        try:
            chat = await c.get_chat_member(Config.FORCE_SUB, m.from_user.id)
            if chat.status=='kicked':
                return await m.reply_text('Hai you are kicked from my updates channel. So, you are not able to use me',  quote=True)

        except UserNotParticipant:
            button = [[
                InlineKeyboardButton('join Updates channel', url=f'https://t.me/testchanel369{Config.FORCE_SUB}')
                ],[
                InlineKeyboardButton('🔄 Refresh 🔄', url=f'https://t.me/NewConverter_Bot?start')
            ]]
            markup = InlineKeyboardMarkup(button)
            return await m.reply_text(text="Hey join in my updates channel to use me.", parse_mode='markdown', reply_markup=markup, quote=True)

        except ChatAdminRequired:
            logger.warning(f"Make me admin in @{Config.FORCE_SUB}")
            if m.from_user.id in Config.AUTH_USERS:
                return await m.reply_text(f"Make me admin in @{Config.FORCE_SUB}")

        except UsernameNotOccupied:
            logger.warning("The forcesub username was Incorrect. Please give the correct username.")
            if m.from_user.id in Config.AUTH_USERS:
                return await m.reply_text("The forcesub username was Incorrect. Please give the correct username.")

        except Exception as e:
            if "belongs to a user" in str(e):
                logger.warning("Forcesub username must be a channel username Not yours or any other users username")
                if m.from_user.id in Config.AUTH_USERS:
                    return await m.reply_text("Forcesub username must be a channel username Not yours or any other users username")
            logger.error(e)
            return await m.reply_text("Some thing went wrong. Try again and if same issue occur contact [Owner](https://t.me/AswanthVK)", disable_web_page_preview=True, quote=True)

    await m.continue_propagation()
