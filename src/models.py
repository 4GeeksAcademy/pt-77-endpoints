from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    login: Mapped[str] = mapped_column(String(60), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)
    favorites: Mapped[list["Favorites"]] = relationship(back_populates="user_favorites")

    def serialize(self):
        return {
            "id": self.id,
            "login": self.login,
            # do not serialize the password, its a security breach
        }
    
class Favorites(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)

    # user id who favorited -- that is going to relate this table to the user table
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user_favorites: Mapped["User"] = relationship(back_populates="favorites")

    # character id if they faved a character store that id -- relate to the character table
    character_id: Mapped[int] = mapped_column(ForeignKey("characters.id"))
    fav_character: Mapped["Characters"] = relationship(back_populates="favorites")

    # planet id if they faved a planet store that id -- relate it to the planet table
    planet_id: Mapped[int] = mapped_column(ForeignKey("planets.id"))
    fav_planet: Mapped["Planets"] = relationship(back_populates="favorites")


    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "character_id": self.character_id,
            "planet_id": self.planet_id,
        }

class Characters(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(60), unique=True, nullable=False)
    eye_color: Mapped[str] = mapped_column(String(60),nullable=False)
    hair_color: Mapped[str] = mapped_column(String(60), nullable=False)
    favorites: Mapped[list["Favorites"]] = relationship(back_populates="fav_character")


    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "eye_color": self.eye_color,
            "hair_color": self.hair_color,
        }

class Planets(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(60), unique=True, nullable=False)
    climate: Mapped[str] = mapped_column(String(60),nullable=False)
    terrian: Mapped[str] = mapped_column(String(60), nullable=False)
    favorites: Mapped[list["Favorites"]] = relationship(back_populates="fav_planet")


    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "climate": self.name,
            "terrian": self.terrian
        }
