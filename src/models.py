from flask_sqlalchemy import SQLAlchemy
from typing import List, Optional
from datetime import datetime
from sqlalchemy import String, func, ForeignKey, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()

favorites = Table(
    "favorites",
    db.metadata,
    Column("user_id", ForeignKey("user.id")),
    Column("character_id", ForeignKey("character.id")),
    Column("location_id", ForeignKey("location.id"))
)


class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    firstname: Mapped[str] = mapped_column(String(120), nullable=False)
    lastname: Mapped[str] = mapped_column(String(120), nullable=False)
    email: Mapped[str] = mapped_column(String(120), nullable=False)
    characters_like: Mapped[List["Character"]
                            ] = relationship(secondary=favorites)
    locations_like: Mapped[List["Location"]
                           ] = relationship(secondary=favorites)

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "email": self.email,
            "favorites": {
                "characters": [character.name for character in self.characters_like],
                "locations": [location.name for location in self.locations_like]
            }
        }


class Character(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    age: Mapped[Optional[int]] = mapped_column(nullable=True)
    birthdate: Mapped[datetime] = mapped_column(server_default=func.now())
    gender: Mapped[str] = mapped_column(String(60))
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    occupation: Mapped[str] = mapped_column(String(255))
    phrases: Mapped[List["Phrase"]] = relationship(
        back_populates="character", cascade="all, delete-orphan"
    )
    status: Mapped[str] = mapped_column(String(120), nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "age": self.age,
            "birthdate": self.birthdate,
            "gender": self.gender,
            "name": self.name,
            "occupation": self.occupation,
            "phrases": [phrase.serialize() for phrase in self.phrases],
            "status": self.status
        }


class Phrase(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(String(500), nullable=False)
    character_id: Mapped[int] = mapped_column(ForeignKey("character.id"))
    character: Mapped["Character"] = relationship(back_populates="phrases")

    def serialize(self):
        return self.text


class Location(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    image_path: Mapped[str] = mapped_column(String(255), nullable=False)
    town: Mapped[str] = mapped_column(String(255), nullable=False)
    use: Mapped[str] = mapped_column(String(255), nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "image": self.image_path,
            "town": self.town,
            "use": self.use
        }
