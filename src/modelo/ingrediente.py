from sqlalchemy import Column, Integer, String 
from sqlalchemy.orm import relationship

from .declarative_base import Base

class Ingrediente(Base):
    __tablename__ = 'ingrediente'

    id = Column(Integer, primary_key=True)
    nombre = Column(String)
    unidadMedida = Column(String)
    sitioCompra = Column(String)
    valorUnidad = Column(Integer)
    ingredientesRecetas = relationship('IngredienteReceta',cascade='all')
