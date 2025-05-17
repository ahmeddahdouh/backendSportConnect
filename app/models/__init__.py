from flask_sqlalchemy import SQLAlchemy

from .user import User
from .event import Event
from .sport import Sport
from .channel import Channel
from .channel_member import ChannelMember
from .message import Message

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
