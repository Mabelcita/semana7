from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from .declarative_base import Base

class Receta(Base):
    __tablename__ = 'receta'

    id = Column(Integer, primary_key=True)
    nombre = Column(String)
    tiempoPreparacion = Column(String)
    personasBase = Column(Integer)
    caloriasPorcion = Column(Integer)
    instrucciones = Column(String)
    ingredientes = relationship('IngredienteReceta', cascade='all, delete, delete-orphan')