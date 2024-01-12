"""log.py"""

from dataclasses import dataclass
import re
from typing import Any, Dict, Optional, Union

REGEX_TIMESTAMP = r"(?P<timestamp>\d{2}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}\.\d{3})"
REGEX_LEVEL = r"(?P<level>\w+)"
REGEX_COORDINATES = r"(?P<coordinates>(\d+,?){3})"
REGEX_MESSAGE = r"(?P<message>.*)"
REGEX_STEAMID = r"(?P<steam_id>\d{1,19})"
REGEX_USERNAME = r"(?P<username>.+)"
REGEX_CONTAINER = r"(?P<container>\w+)"
REGEX_ACTION = r"(?P<action>.+)"


@dataclass
class Base:
    """Base"""
    timestamp: str

    @staticmethod
    def from_dict(t: type, parsed_data: dict[str, str]) -> Any:
        """Generic Dataclass"""
        return t(**parsed_data)


@dataclass
class Chat(Base):
    """Chat"""
    level: str
    message: str
    NAME = "chat"
    PARSER = re.compile(f"""
        \\[{REGEX_TIMESTAMP}\\]
        \\[{REGEX_LEVEL}\\]\\s
        {REGEX_MESSAGE}\\.""", re.X)


@dataclass
class Admin(Base):
    """Admin"""
    level: Optional[str]
    message: str
    NAME = "admin"
    PARSER = re.compile(f"""
        \\[{REGEX_TIMESTAMP}\\]\\s?
        (\\[{REGEX_LEVEL}\\])?\\s
        {REGEX_MESSAGE}\\.""", re.X)


@dataclass
class DebugServer(Base):
    """DebugServer"""
    level: str
    message: str
    type: str
    unix_timestamp: str
    coordinates: str
    NAME = "DebugLog-server"
    PARSER = re.compile(f"""
       \\[{REGEX_TIMESTAMP}\\]\\s*
       {REGEX_LEVEL}\\s*:\\s
       (?P<type>\\w+)\\s*,\\s
       (?P<unix_timestamp>\\d+)>\\s
       {REGEX_COORDINATES}>\\s
       {REGEX_MESSAGE}\\.""", re.X)


@dataclass
class Pvp(Base):
    """Pvp"""
    level: Optional[str]
    usertype: str
    username: str
    coordinates: Optional[str]
    action: str
    NAME = "pvp"
    PARSER = re.compile(f"""
        \\[{REGEX_TIMESTAMP}\\]
        (\\[{REGEX_LEVEL}\\])?
        \\s(?P<usertype>\\w+)\\s
        "{REGEX_USERNAME}"\\s
        (\\({REGEX_COORDINATES}\\)\\s)?
        {REGEX_ACTION}\\.""", re.X)


@dataclass
class User(Base):
    """User"""
    steam_id: Optional[str]
    username: Optional[str]
    message: str
    NAME = "user"
    PARSER = re.compile(f"""
        \\[{REGEX_TIMESTAMP}\\]\\s
        ({REGEX_STEAMID}\\s
        "{REGEX_USERNAME}"\\s)?
        {REGEX_MESSAGE}\\.""", re.X)


@dataclass
class Cmd(Base):
    """Cmd"""
    steam_id: str
    username: str
    coordinates: str
    action: str
    NAME = "cmd"
    PARSER = re.compile(f"""\\[
       {REGEX_TIMESTAMP}\\]\\s
       {REGEX_STEAMID}\\s
       "{REGEX_USERNAME}"\\s
       {REGEX_ACTION}\\s@\\s
       {REGEX_COORDINATES}\\.""", re.X)


@dataclass
class Map(Base):
    """Map"""
    steam_id: str
    username: str
    coordinates: str
    action: str
    NAME = "map"
    PARSER = re.compile(f"""
        \\[{REGEX_TIMESTAMP}\\]\\s
        {REGEX_STEAMID}\\s
        "{REGEX_USERNAME}"\\s
        {REGEX_ACTION}\\sat\\s
        {REGEX_COORDINATES}\\.""", re.X)


@dataclass
class PerkLog(Base):
    """PerkLog"""
    steam_id: str
    username: str
    message: str
    coordinates: str
    hours_survived: str
    NAME = "PerkLog"
    PARSER = re.compile(f"""
        \\[{REGEX_TIMESTAMP}\\]\\s
        \\[{REGEX_STEAMID}\\]
        \\[{REGEX_USERNAME}\\]
        \\[{REGEX_COORDINATES}\\]
        \\[{REGEX_MESSAGE}\\]
        \\[(?P<hours_survived>.+)\\]\\.""", re.X)


@dataclass
class Item(Base):
    """Item"""
    steam_id: str
    username: str
    coordinates: str
    container: str
    inventory_change: str
    items: Optional[str]
    NAME = "item"
    PARSER = re.compile(f"""
        \\[{REGEX_TIMESTAMP}\\]\\s
        {REGEX_STEAMID}\\s
        "{REGEX_USERNAME}"\\s
        {REGEX_CONTAINER}\\s
        (?P<inventory_change>(\\+|-)\\d+)\\s
        {REGEX_COORDINATES}
        (\\s\\[(?P<items>.*)\\])?\\.""", re.X)


@dataclass
class ClientAction(Base):
    """ClientAction"""
    steam_id: str
    username: str
    coordinates: str
    container: str
    action: str
    NAME = "ClientActionLog"
    PARSER = re.compile(f"""
        \\[{REGEX_TIMESTAMP}\\]\\s
        \\[{REGEX_STEAMID}\\]
        \\[{REGEX_ACTION}\\]
        \\[{REGEX_USERNAME}\\]
        \\[{REGEX_COORDINATES}\\]
        \\[{REGEX_CONTAINER}\\]\\.""", re.X)


LogVar = Union[ClientAction, Item, PerkLog, Map,
               Cmd, User, Pvp, DebugServer, Admin, Chat]

FACTORY: Dict[str, type[LogVar]] = {
    DebugServer.NAME: DebugServer,
    Chat.NAME: Chat,
    Pvp.NAME: Pvp,
    Cmd.NAME: Cmd,
    PerkLog.NAME: PerkLog,
    Admin.NAME: Admin,
    Item.NAME: Item,
    ClientAction.NAME: ClientAction,
    Map.NAME: Map,
    User.NAME: User
}
