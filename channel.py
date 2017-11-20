import itertools
from contextlib import suppress
from datetime import timedelta
from typing import Dict, Optional, Set  # noqa: F401

import bot
from lib.data import ChatCommandArgs
from lib.helper import chat, timeout
from lib.helper.chat import min_args, permission_feature


@permission_feature(('broadcaster', None), ('moderator', 'modtree'))
async def commandTree(args: ChatCommandArgs) -> bool:
    if not await args.data.ffz_load_broadcaster_emotes(args.chat.channel):
        return False
    emotes: Optional[Dict[int, str]]
    emotes = await args.data.ffz_get_broadcaster_emotes(args.chat.channel)
    if emotes is None:
        return False
    ffzEmotes: Set[str] = set(emotes.values())
    if 'Neck2' not in ffzEmotes or 'Neck3' not in ffzEmotes:
        return False

    count: int = 2
    rep: str = 'Neck1'
    # If below generate a ValueError or IndexError,
    # only the above line gets used
    if len(args.message) <= 2:
        try:
            count = int(args.message[1])
        except ValueError:
            rep = args.message[1]
        except IndexError:
            pass
    else:
        with suppress(ValueError, IndexError):
            rep = args.message[1]
            count = int(args.message[2])
    if rep == 'Neck1' and 'Neck1' not in ffzEmotes:
        return False
    return await process_tree(args, rep, count)


@permission_feature(('broadcaster', None), ('moderator', 'modtree'))
@min_args(2)
async def commandTreeLong(args: ChatCommandArgs) -> bool:
    if not await args.data.ffz_load_broadcaster_emotes(args.chat.channel):
        return False
    emotes: Optional[Dict[int, str]]
    emotes = await args.data.ffz_get_broadcaster_emotes(args.chat.channel)
    if emotes is None:
        return False
    ffzEmotes: Set[str] = set(emotes.values())
    if 'Neck2' not in ffzEmotes or 'Neck3' not in ffzEmotes:
        return False

    count: int = 2
    with suppress(ValueError, IndexError):
        count = int(args.message.command.split('tree-')[1])
    return await process_tree(args, args.message.query, count)


async def process_tree(args: ChatCommandArgs,
                       repetition: str,
                       count: int) -> bool:
    if not args.permissions.broadcaster:
        count = min(count, 5)

        cooldown: timedelta = timedelta(
            seconds=bot.config.spamModeratorCooldown)
        if chat.inCooldown(args, cooldown, 'modPyramid'):
            return False
    elif not args.permissions.globalModerator:
        count = min(count, 20)
    messages: itertools.chain[str] = itertools.chain(
        (repetition,),
        ('Neck2',) * count,
        ('Neck3',)
        )
    if args.permissions.chatModerator:
        await timeout.record_timeout(
            args.chat, args.nick, repetition, str(args.message), 'pyramid')
    args.chat.send(messages, -1)
    return True
