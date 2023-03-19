from app import db
from typing import List
from typing import Optional
from sqlalchemy import String, Integer, ForeignKey, Identity
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship


class Emoji(db.Model):
    __tablename__ = "emojis"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    emoji: Mapped[str] = mapped_column(String(30))

    user: Mapped["User"] = relationship(back_populates="emoji")

    def __repr__(self) -> str:
        return f"Emoji(id={self.id!r}, emoji={self.emoji!r})"


class User(db.Model):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    emoji_id: Mapped[int] = mapped_column(ForeignKey("emojis.id"), nullable=True)
    emoji: Mapped["Emoji"] = relationship(back_populates="user")

    # Level_User associations
    levels: Mapped[List["Level"]] = relationship(
        secondary="levels_users", back_populates="users", viewonly=True
    )
    level_associations: Mapped[List["Level_User"]] = relationship(
        back_populates="user", viewonly=True
    )

    # Answer associations
    calcs: Mapped[List["Calc"]] = relationship(
        secondary="answers", back_populates="users", viewonly=True
    )
    calc_associations: Mapped[List["Answer"]] = relationship(back_populates="user")

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, emoji={self.emoji_id!r})"


class Level(db.Model):
    __tablename__ = "levels"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    # Level_User associations
    users: Mapped[List["User"]] = relationship(
        secondary="levels_users", back_populates="levels", viewonly=True
    )
    user_associations: Mapped[List["Level_User"]] = relationship(back_populates="level")

    # Level_Calc associations
    calcs: Mapped[List["Calc"]] = relationship(
        secondary="levels_calcs", back_populates="levels", viewonly=True
    )
    calc_associations: Mapped[List["Level_Calc"]] = relationship(back_populates="level")

    def __repr__(self) -> str:
        return f"Level(id={self.id!r})"


class Level_User(db.Model):
    __tablename__ = "levels_users"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    level_id: Mapped[int] = mapped_column(ForeignKey("levels.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    level: Mapped["Level"] = relationship(back_populates="user_associations")
    user: Mapped["User"] = relationship(back_populates="level_associations")

    def __repr__(self) -> str:
        return f"Level_User(id={self.id!r}, level_id={self.level_id!r}, user_id={self.user_id!r})"


class Game(db.Model):
    __tablename__ = "games"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(60))

    def __repr__(self) -> str:
        return f"Game(id={self.id!r}, name={self.name!r})"


class Calc(db.Model):
    __tablename__ = "calcs"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    multiplier: Mapped[int] = mapped_column(Integer)
    multiplicand: Mapped[int] = mapped_column(Integer)

    # Level_Calc associations
    levels: Mapped[List["Level"]] = relationship(
        secondary="levels_calcs", back_populates="calcs", viewonly=True
    )
    level_associations: Mapped[List["Level_Calc"]] = relationship(back_populates="calc")

    # Answer associations
    users: Mapped[List["User"]] = relationship(
        secondary="answers", back_populates="calcs", viewonly=True
    )
    user_associations: Mapped[List["Answer"]] = relationship(back_populates="calc")

    def __repr__(self) -> str:
        return f"Calc(id={self.id!r}, multiplier={self.multiplier!r}, multiplicand={self.multiplicand!r})"


class Level_Calc(db.Model):
    __tablename__ = "levels_calcs"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    level_id: Mapped[int] = mapped_column(ForeignKey("levels.id"))
    calc_id: Mapped[int] = mapped_column(ForeignKey("calcs.id"))

    level: Mapped["Level"] = relationship(back_populates="calc_associations")
    calc: Mapped["Calc"] = relationship(back_populates="level_associations")

    def __repr__(self) -> str:
        return f"Level_Calc(id={self.id!r}, level_id={self.level_id!r}, calc_id={self.user_id!r})"


class Answer(db.Model):
    __tablename__ = "answers"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    calc_id: Mapped[int] = mapped_column(ForeignKey("calcs.id"))
    game_id: Mapped[int] = mapped_column(ForeignKey("games.id"))

    right_answer: Mapped[str] = mapped_column(String(10))
    datetime: Mapped[str] = mapped_column(String(30))

    user: Mapped["User"] = relationship(back_populates="calc_associations")
    calc: Mapped["Calc"] = relationship(back_populates="user_associations")

    def __repr__(self) -> str:
        return f"Answers(id={self.id!r}, user_id={self.user_id!r}, calc_id={self.calc_id!r})"


# arvo yksi lasku
# - 2 laskua ei voi olla peräkkäin - views.py
# - vain level_calcin laskut - user_level_calcs()
# - ei niitä laskuja, joista löytyy väh. 3 answeria
