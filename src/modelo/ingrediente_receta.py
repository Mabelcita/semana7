from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship

from .declarative_base import Base

class IngredienteReceta(Base):
    __tablename__ = 'ingrediente_receta'

    id = Column(Integer, primary_key=True)
    cantidad = Column(Float)
    receta = Column(Integer, ForeignKey('receta.id'))
    ingrediente =  Column(Integer, ForeignKey('ingrediente.id'))