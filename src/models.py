from flask_sqlalchemy import SQLAlchemy
from typing import List, Optional
from datetime import datetime
from sqlalchemy import String, func, ForeignKey, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()

favorites = Table(
    "favorites",
    db.metadata,
    Column("id", db.Integer, primary_key=True),  
    Column("user_id", ForeignKey("user.id"), nullable=False),
    Column("character_id", ForeignKey("character.id"), nullable=True),
    Column("location_id", ForeignKey("location.id"), nullable=True)
)


class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    firstname: Mapped[str] = mapped_column(String(120), nullable=False)
    lastname: Mapped[str] = mapped_column(String(120), nullable=False)
    email: Mapped[str] = mapped_column(String(120), nullable=False)
    password: Mapped[str] = mapped_column(String(120), nullable=False)
    characters_like: Mapped[List["Character"]] = relationship(
        secondary=favorites,
        back_populates="users_characters_like",

    )
    locations_like: Mapped[List["Location"]] = relationship(
        secondary=favorites,
        back_populates="users_locations_like",

    )

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "email": self.email,
            "favorites": {
                "characters": [character.serialize() for character in self.characters_like],
                "locations": [location.serialize() for location in self.locations_like]
            }
        }


class Character(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    age: Mapped[Optional[int]] = mapped_column(nullable=True)
    birthdate: Mapped[str] = mapped_column(nullable=True)
    description: Mapped[str] = mapped_column(nullable=False)
    gender: Mapped[str] = mapped_column(String(60))
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    occupation: Mapped[str] = mapped_column(String(255))
    users_characters_like: Mapped[List["User"]] = relationship(
        secondary=favorites,
        back_populates="characters_like"
    )

    phrases: Mapped[List["Phrase"]] = relationship(
        back_populates="character"
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

    def serialize_complete(self):
        return {
            "id": self.id,
            "age": self.age,
            "birthdate": self.birthdate,
            "description": self.description,
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
    users_locations_like: Mapped[List["User"]] = relationship(
        secondary=favorites,
        back_populates="locations_like"
    )

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "image": self.image_path,
            "town": self.town,
            "use": self.use
        }
