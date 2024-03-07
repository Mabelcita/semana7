from src.logica.FachadaRecetario import FachadaRecetario
from src.modelo.ingrediente import Ingrediente
from src.modelo.ingrediente_receta import IngredienteReceta
from src.modelo.receta import Receta
from src.modelo.declarative_base import Session, engine, Base
import re

class LogicaRecetario():

    def __init__(self):
        Base.metadata.create_all(engine)
        self.session = Session()
        
        self.recetas = self.session.query(Receta).all()
        self.ingredientes = self.session.query(Ingrediente).all()
        self.ingredientes_recetas = self.session.query(IngredienteReceta).all()
        
    def dar_recetas(self):
        self.recetas = self.session.query(Receta).all()
        if (len(self.recetas) >= 1):
            recetas_ordenadas = sorted(self.recetas, key=lambda x: (x.nombre))
            recetas_ordenadas_lista =[]
            for receta in recetas_ordenadas:
                recetas_ordenadas_lista.append(
                    {
                    'nombre': receta.nombre,
                    'tiempoPreparacion': receta.tiempoPreparacion,
                    'personasBase': receta.personasBase,
                    'caloriasPorcion': receta.caloriasPorcion,
                    'instrucciones': receta.instrucciones
                    }
                )
            return recetas_ordenadas_lista
        else:
            return []
        
    def dar_ingredientes(self):
        self.ingredientes = self.session.query(Ingrediente).all()
        if(len(self.ingredientes) >= 1):
            ingredientes_ordenados = sorted(self.ingredientes, key=lambda x: (x.nombre, x.unidadMedida, x.sitioCompra))
            self.ingredientes_mock = []
            for ingrediente in ingredientes_ordenados:
                self.ingredientes_mock.append(
                    {
                    'nombre': ingrediente.nombre,
                    'unidad': ingrediente.unidadMedida,
                    'valor': ingrediente.valorUnidad,
                    'sitioCompra': ingrediente.sitioCompra
                }
                )
            return self.ingredientes_mock
        else:
            return []
    
    def crear_ingrediente(self, nombre, unidad, valor, sitioCompras):
        
        validacion = self.validar_crear_editar_ingrediente(nombre, unidad, valor, sitioCompras)

        if (validacion == ''):
            ingrediente = Ingrediente(nombre=nombre, unidadMedida=unidad, valorUnidad=valor, sitioCompra=sitioCompras)
            self.session.add(ingrediente)
            self.session.commit()
            return True
        else:
            return False

    def validar_crear_editar_ingrediente(self, nombre, unidad, valor, sitioCompra):
        valorInt = 0

        try:
            valorInt=int(valor)
        except:
            valorInt = 0
       
        if ((nombre == None or  nombre == '') or not isinstance(nombre, str) or len(nombre) > 255):
            return 'Nombre incorrecto'
        elif ((unidad == None or  unidad == '') or not isinstance(unidad, str) or len(unidad) > 255):
            return 'Unidad incorrecto'
        elif ((valorInt == None or  valorInt == '') or not isinstance(valorInt, int) or valorInt <= 0):
            return 'Valor incorrecto'
        elif ((sitioCompra == None or  sitioCompra == '') or not isinstance(sitioCompra, str) or len(sitioCompra) > 255):
            return 'Sitio de compra incorrecto'
        else:
            cantidad_ingredientes =  self.session.query(Ingrediente).count()
            if (cantidad_ingredientes==0):
                return ''
            
            existe_ingrediente  = self.session.query(Ingrediente).filter(Ingrediente.nombre == nombre, Ingrediente.unidadMedida == unidad).count()
            if (existe_ingrediente == 0):
                return ''
            else:
                return 'Ingrediente ya existe'

    def crear_receta(self, receta, tiempo, personas, calorias, preparacion):
        receta = Receta(nombre=receta, tiempoPreparacion=tiempo, personasBase=personas, caloriasPorcion=calorias, instrucciones=preparacion)
        self.session.add(receta)
        self.session.commit()
        return ''
    
    def validar_crear_editar_receta(self, id_receta, receta, tiempo, personas, calorias, preparacion):
        patron = re.compile(r"^(?:[0-9]+):([0-5][0-9]):([0-5][0-9])$")
        try:
            personasInt=int(personas)
        except:
            personasInt = 0

        try:
            caloriasInt=int(calorias)
        except:
            caloriasInt = 0

        if ((receta == None or  receta == '') or not isinstance(receta, str) or len(receta) > 255):
            return 'Nombre Invalido'
        elif (tiempo == None or  tiempo == '' or not isinstance(tiempo, str) or patron.match(tiempo) == None) :
            return 'Tiempo Preparacion Invalido'
        elif (personasInt == None or  personasInt == '' or personasInt <= 0) :
            return 'Numero de Personas Invalido'
        elif (caloriasInt == None or  caloriasInt == '' or caloriasInt <= 0) :
            return 'Calorias Porcion Invalido'
        elif (preparacion == None or  preparacion == '' or not isinstance(preparacion, str)) :
            return 'Instrucciones Receta Invalido'
        else:
            busqueda = self.session.query(Receta).filter(Receta.nombre == receta).count()
            if busqueda == 0:
                return ''
            else:
                return 'Receta ya existe'
    
    def dar_ingredientes_receta(self, id_receta):
        ingrediente_recetas_mostar = []
        ingredientes_recetas = self.session.query(IngredienteReceta).filter(IngredienteReceta.receta == (id_receta + 1)).all()
        for ingrediente in ingredientes_recetas:
            ingrediente_mostrar = self.session.query(Ingrediente).all()[ingrediente.ingrediente -1]
            ingrediente_recetas_mostar.append({
                'ingrediente': ingrediente_mostrar.nombre,
                'unidad': ingrediente_mostrar.unidadMedida,
                'cantidad': ingrediente.cantidad
            })
        
        ingredientes_receta_ordenados = sorted(ingrediente_recetas_mostar, key=lambda x: (x['ingrediente'], x['unidad'], x['cantidad']))

        return ingredientes_receta_ordenados
    
    def dar_receta(self, id_receta):
        receta = self.session.query(Receta).all()

        if (len(receta) < id_receta):
            return False
        else:
            receta_mock = ({
                    'nombre': receta[id_receta].nombre,
                    'tiempo': receta[id_receta].tiempoPreparacion,
                    'personas': receta[id_receta].personasBase,
                    'calorias': receta[id_receta].caloriasPorcion,
                    'preparacion': receta[id_receta].instrucciones
                    })
            return receta_mock
        
    def agregar_ingrediente_receta(self, receta, ingrediente, cantidad):

        ingrediente_busqueda = self.session.query(Ingrediente).filter(
            Ingrediente.nombre == ingrediente['nombre'],
            Ingrediente.sitioCompra == ingrediente['sitioCompra'],
            Ingrediente.unidadMedida == ingrediente['unidad'],
            Ingrediente.valorUnidad == ingrediente['valor']
        ).all()

        receta_busqueda =  self.session.query(Receta).filter(
            Receta.nombre == receta['nombre'],
            Receta.tiempoPreparacion == receta['tiempo'],
            Receta.personasBase == receta['personas'],
            Receta.caloriasPorcion == receta['calorias'],
            Receta.instrucciones == receta['preparacion']
        ).all()

        ingrediente_receta = IngredienteReceta(cantidad=cantidad, receta = receta_busqueda[0].id, ingrediente=ingrediente_busqueda[0].id)
        self.session.add(ingrediente_receta)
        self.session.commit()
        return True
        
    def validar_crear_editar_ingReceta(self, receta, ingrediente, cantidad):

        try:
            cantidadFloat=float(cantidad)
        except:
            cantidadFloat = 0.0


        self.ingredientes = self.session.query(Ingrediente).all()

        if (len(self.ingredientes)==0):
            return 'No existen ingredientes'
        
        ingredientes = self.session.query(Ingrediente).filter(
            Ingrediente.nombre == ingrediente['nombre'],
            Ingrediente.sitioCompra == ingrediente['sitioCompra'],
            Ingrediente.unidadMedida == ingrediente['unidad'],
            Ingrediente.valorUnidad == ingrediente['valor']
        ).all()

        if(len(ingredientes) == 0):
            return 'Ingrediente Invalido'
        
        if (cantidadFloat == None or cantidadFloat <= 0):
            return 'Cantidad invalido'
        
        return ''
        