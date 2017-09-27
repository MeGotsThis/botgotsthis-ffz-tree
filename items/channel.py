from typing import Iterable, Mapping, Optional

from lib.data import ChatCommand

from .. import channel


def filterMessage() -> Iterable[ChatCommand]:
    return []


def commands() -> Mapping[str, Optional[ChatCommand]]:
    if not hasattr(commands, 'commands'):
        setattr(commands, 'commands', {
            '!tree': channel.commandTree,
            }
        )
    return getattr(commands, 'commands')


def commandsStartWith() -> Mapping[str, Optional[ChatCommand]]:
    if not hasattr(commandsStartWith, 'commands'):
        setattr(commandsStartWith, 'commands', {
            '!tree-': channel.commandTreeLong,
            }
        )
    return getattr(commandsStartWith, 'commands')


def processNoCommand() -> Iterable[ChatCommand]:
    return []
