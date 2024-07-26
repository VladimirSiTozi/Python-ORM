from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(
        Integer,
        primary_key=True,
    )
    name = Column(
        String(100), # models.CharField(max_length=100)
        nullable=False,
    )
    ingredients = Column(
        Text,
        nullable=False,
    )
    instructions = Column(
        Text,
        nullable=False
    )
    chef_id = Column(
        Integer,
        ForeignKey('chefs.id')
    )

    chef = relationship(
        "Chef",
        back_populates="recipe",
        # foreign_keys=['chef_id']  # if there are more than one relationship in the model
    )


# 7. Model Chef 8. Extend the Recipe Model
class Chef(Base):
    __tablename__ = 'chefs'

    id = Column(
        Integer,
        primary_key=True
    )
    name = Column(
        String(100),
        nullable=False
    )

    recipe = relationship(
        "Recipe",
        back_populates="chef"
    )



