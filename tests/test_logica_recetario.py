import unittest

from src.logica.logica_recetario import LogicaRecetario
from src.modelo.ingrediente import Ingrediente
from src.modelo.ingrediente_receta import IngredienteReceta
from src.modelo.receta import Receta
from src.modelo.declarative_base import Session
from faker import Faker
from faker_food import FoodProvider
from faker.providers import company
from sqlalchemy import asc, desc

import re

class LogicaRecetarioTestCase(unittest.TestCase):

     def setUp(self):
          self.logica = LogicaRecetario()
          self.session = Session()
          self.fake = Faker()
          self.fake.add_provider(FoodProvider)
          Faker.seed(15)

     def tearDown(self):
          '''Abre la sesión'''
          self.session = Session()

          '''Consulta todos los ingredientes'''
          busqueda = self.session.query(Ingrediente).all()

          '''Borra todos los ingredientes'''
          for ingrediente in busqueda:
               self.session.delete(ingrediente)

          '''Consulta todos las recetas'''
          busqueda = self.session.query(Receta).all()

          '''Borra todos las recetas'''
          for receta in busqueda:
               self.session.delete(receta)

          self.session.commit()
          self.session.close()

     def test_dar_recetas_lista_vacia(self):
          self.logica.recetas = []
          self.assertEqual(self.logica.dar_recetas(), [])

     def test_dar_recetas_lista_un_registro(self):
          receta = Receta(nombre = self.fake.unique.dish(),
                         tiempoPreparacion =str(self.fake.time_object())[0:8],
                         personasBase = self.fake.random_int(1,6),
                         caloriasPorcion = self.fake.random_int(100, 2500),
                         instrucciones = self.fake.paragraph(nb_sentences=5, variable_nb_sentences=False))
          self.session.add(receta)
          self.session.commit()
          self.assertEqual(len(self.logica.dar_recetas()), 1)
     
     def test_dar_recetas_lista_multiples_registros(self):
          for i in range(0,10):
               receta = Receta(nombre = self.fake.unique.dish(),
                         tiempoPreparacion =str(self.fake.time_object())[0:8],
                         personasBase = self.fake.random_int(1,6),
                         caloriasPorcion = self.fake.random_int(100, 2500),
                         instrucciones = self.fake.paragraph(nb_sentences=5, variable_nb_sentences=False))
               self.session.add(receta)
               self.session.commit()    
          self.assertEqual(len(self.logica.dar_recetas()), 10)

     def test_dar_recetas_lista_en_orden_alfabetico(self):
          for i in range(0,10):
               receta = Receta(nombre = self.fake.unique.dish(),
                         tiempoPreparacion =str(self.fake.time_object())[0:8],
                         personasBase = self.fake.random_int(1,6),
                         caloriasPorcion = self.fake.random_int(100, 2500),
                         instrucciones = self.fake.paragraph(nb_sentences=5, variable_nb_sentences=False))
               self.session.add(receta)
               self.session.commit()
          receta =self.session.query(Receta).order_by(asc(Receta.nombre)).first()
          self.assertEqual(self.logica.dar_recetas()[0]["nombre"], receta.nombre) 
          receta =self.session.query(Receta).order_by(desc(Receta.nombre)).first()
          self.assertEqual(self.logica.dar_recetas()[len(self.logica.dar_recetas())-1]["nombre"], receta.nombre)

     def test_dar_ingredientes_lista_vacia(self):
          self.logica.ingredientes = []
          self.assertEqual(self.logica.dar_ingredientes(), [])

     def test_dar_ingredientes_lista_un_registro(self):
          ingrediente =Ingrediente(
                         nombre = self.fake.unique.ingredient(),
                         unidadMedida = self.fake.metric_measurement(),
                         sitioCompra =  self.fake.company(),
                         valorUnidad = self.fake.random_int(100, 250000)
                    )
          self.session.add(ingrediente)
          self.session.commit()
          self.assertEqual(len(self.logica.dar_ingredientes()), 1)

     def test_dar_ingredientes_lista_multiples_registros(self):
          for i in range(0,7):
               ingrediente =Ingrediente(
                         nombre = self.fake.unique.ingredient(),
                         unidadMedida = self.fake.metric_measurement(),
                         sitioCompra =  self.fake.company(),
                         valorUnidad = self.fake.random_int(100, 250000)
                    )
               self.session.add(ingrediente)
               self.session.commit()
          self.assertEqual(len(self.logica.dar_ingredientes()), 7)

     def test_dar_ingredientes_lista_en_orden_alfabetico_nombre(self):
          for i in range(0,10):
               ingrediente =Ingrediente(
                         nombre = self.fake.unique.ingredient(),
                         unidadMedida = self.fake.metric_measurement(),
                         sitioCompra =  self.fake.company(),
                         valorUnidad = self.fake.random_int(100, 250000)
                    )
               self.session.add(ingrediente)
               self.session.commit()
          ingrediente =self.session.query(Ingrediente).order_by(asc(Ingrediente.nombre)).first()
          self.assertEqual(self.logica.dar_ingredientes()[0]["nombre"], ingrediente.nombre) 
          ingrediente =self.session.query(Ingrediente).order_by(desc(Ingrediente.nombre)).first()
          self.assertEqual(self.logica.dar_ingredientes()[len(self.logica.dar_ingredientes())-1]["nombre"], ingrediente.nombre)

     
     def test_dar_ingredientes_lista_en_orden_alfabetico_nombre_unidad(self):
          for i in range(0,10):
               ingrediente =Ingrediente(
                         nombre = self.fake.unique.ingredient(),
                         unidadMedida = self.fake.metric_measurement(),
                         sitioCompra =  self.fake.company(),
                         valorUnidad = self.fake.random_int(100, 250000)
                    )
               self.session.add(ingrediente)
               self.session.commit()
          ingrediente =self.session.query(Ingrediente).order_by(Ingrediente.nombre.asc(), Ingrediente.unidadMedida.asc()).first()
          self.assertEqual(self.logica.dar_ingredientes()[0]["unidad"], ingrediente.unidadMedida) 
          ingrediente =self.session.query(Ingrediente).order_by(Ingrediente.nombre.desc(), Ingrediente.unidadMedida.desc()).first()
          self.assertEqual(self.logica.dar_ingredientes()[len(self.logica.dar_ingredientes())-1]["unidad"], ingrediente.unidadMedida)

     def test_dar_ingredientes_lista_en_orden_alfabetico_nombre_unidad_sitio(self):
          for i in range(0,10):
               ingrediente =Ingrediente(
                         nombre = self.fake.unique.ingredient(),
                         unidadMedida = self.fake.metric_measurement(),
                         sitioCompra =  self.fake.company(),
                         valorUnidad = self.fake.random_int(100, 250000)
                    )
               self.session.add(ingrediente)
               self.session.commit()
          ingrediente =self.session.query(Ingrediente).order_by(Ingrediente.nombre.asc(), Ingrediente.unidadMedida.asc(), Ingrediente.sitioCompra.asc() ).first()
          self.assertEqual(self.logica.dar_ingredientes()[0]["sitioCompra"], ingrediente.sitioCompra) 
          ingrediente =self.session.query(Ingrediente).order_by(Ingrediente.nombre.desc(), Ingrediente.unidadMedida.desc(), Ingrediente.sitioCompra.desc() ).first()
          self.assertEqual(self.logica.dar_ingredientes()[len(self.logica.dar_ingredientes())-1]["sitioCompra"], ingrediente.sitioCompra)

     def test_crear_ingrediente_nombre_invalido(self):
          nombre_nulo = None
          nombre_vacio = ''
          self.assertEqual(self.logica.crear_ingrediente(nombre_nulo,'',0,''), False)
          self.assertEqual(self.logica.crear_ingrediente(nombre_vacio,'',0,''), False)

     def test_crear_ingrediente_nombre_no_string(self):
          nombre = 12345
          self.assertEqual(self.logica.crear_ingrediente(nombre,'',0,''), False)

     def test_crear_ingrediente_nombre_numero_caracteres(self):
          nombre = 'hola' * 255
          self.assertEqual(self.logica.crear_ingrediente(nombre,'',0,''), False)

     def test_crear_ingrediente_unidad_invalido(self):
          unidad_nulo = None
          unidad_vacio = ''
          self.assertEqual(self.logica.crear_ingrediente('Arroz', unidad_nulo,0,''), False)
          self.assertEqual(self.logica.crear_ingrediente('Ajo', unidad_vacio,0,''), False)
     
     def test_crear_ingrediente_unidad_no_string(self):
          unidad = 12345
          self.assertEqual(self.logica.crear_ingrediente('Arroz', unidad ,0,''), False)

     def test_crear_ingrediente_unidad_numero_caracteres(self):
          unidad = 'kilo' * 255
          self.assertEqual(self.logica.crear_ingrediente('Arroz', unidad,0,''), False)
     
     def test_crear_ingrediente_valor_invalido(self):
          valor_nulo = None
          valor_vacio = ''
          self.assertEqual(self.logica.crear_ingrediente('Arroz', 'libra',valor_nulo,''), False)
          self.assertEqual(self.logica.crear_ingrediente('Ajo', 'libra',valor_vacio,''), False)

     def test_crear_ingrediente_valor_no_entero(self):
          valor = '12345'
          self.assertEqual(self.logica.crear_ingrediente('Arroz', 'libra' ,valor,''), False)

     def test_crear_ingrediente_valor_mayor_cero(self):
          valor = 0
          self.assertEqual(self.logica.crear_ingrediente('Arroz', 'libra' ,valor,''), False)

     def test_crear_ingrediente_sitio_compra_invalido(self):
         sitio_compra_nulo = None
         sitio_compra_vacio = ''
         self.assertEqual(self.logica.crear_ingrediente('Arroz', 'libra' ,1234,sitio_compra_nulo), False)
         self.assertEqual(self.logica.crear_ingrediente('Arroz', 'libra' ,345,sitio_compra_vacio), False)

     def test_crear_ingrediente_sitio_compra_no_string(self):
         sitio_compra = {}
         self.assertEqual(self.logica.crear_ingrediente('Arroz', 'libra' ,1234, sitio_compra), False)

     def test_crear_ingrediente_sitio_compra_numero_caracteres(self):
         sitio_compra = 'Exito' * 255
         self.assertEqual(self.logica.crear_ingrediente('Arroz', 'Libra',657,sitio_compra), False)

     def test_validar_crear_ingrediente_cuando_no_hay_registros_ingredientes(self):
         self.logica.ingredientes = []
         self.assertEqual(self.logica.validar_crear_editar_ingrediente('Tomate chonto', 'libra',  5000, 'Fruver El mejor'), '')

     def test_validar_crear_ingrediente_cuando_hay_ingredientes_igual_nombre_diferente_unidad(self):
          nombre = self.fake.unique.ingredient()
          self.assertEqual(self.logica.crear_ingrediente(nombre, self.fake.unique.metric_measurement(), str(self.fake.random_int(100, 250000)), self.fake.company()), True)
          unidad =self.fake.unique.metric_measurement()
          self.assertEqual(self.logica.validar_crear_editar_ingrediente(nombre, unidad, str(self.fake.random_int(100, 250000)), self.fake.company()), '')
          self.assertEqual(self.logica.crear_ingrediente(nombre, unidad, str(self.fake.random_int(100, 250000)), self.fake.company()), True)
    
     def test_validar_crear_ingrediente_cuando_hay_ingredientes_igual_nombre_igual_unidad(self):
          nombre = self.fake.unique.ingredient()
          unidad = self.fake.metric_measurement()
          self.logica.crear_ingrediente(nombre, unidad, self.fake.random_int(100, 250000), self.fake.company())
          self.assertEqual(self.logica.validar_crear_editar_ingrediente(nombre, unidad, self.fake.random_int(100, 250000), self.fake.company()), 'Ingrediente ya existe')

     def test_crear_ingrediente_exitosamente(self):
          self.assertEqual(self.logica.crear_ingrediente(self.fake.unique.ingredient(),self.fake.metric_measurement(),str(self.fake.random_int(100, 250000)), self.fake.company()), True)

     def test_crear_ingrediente_fallido(self):
          nombre = self.fake.unique.ingredient()
          unidad = self.fake.metric_measurement()
          self.assertEqual(self.logica.crear_ingrediente(nombre, unidad, str(self.fake.random_int(100, 250000)), self.fake.company()), True)
          self.assertEqual(self.logica.crear_ingrediente(nombre, unidad, str(self.fake.random_int(100, 250000)), self.fake.company()), False)

     def test_verificar_almacenamiento_crear_ingrediente(self):
          nombre = self.fake.unique.ingredient()
          unidad = self.fake.metric_measurement()
          valor = str(self.fake.random_int(100, 250000))
          sitioCompra = self.fake.company()

          self.logica.crear_ingrediente(nombre,unidad,valor,sitioCompra)
     
          ingredientes_resultado= []
          resultado_ingrediente = self.session.query(Ingrediente).all()
     
          for ingrediente in resultado_ingrediente:
                ingredientes_resultado.append({
                         'nombre':ingrediente.nombre,
                         'unidad': ingrediente.unidadMedida,
                         'valor': str(ingrediente.valorUnidad),
                         'sitioCompra': ingrediente.sitioCompra
                    }
                )         
          self.assertIn({'nombre':  nombre,'unidad':unidad,'valor': valor,'sitioCompra':  sitioCompra} ,ingredientes_resultado)
          

     def test_verificar_almacenamiento_crear_ingrediente_persistencia_data(self):
          nombre = self.fake.unique.ingredient()
          unidad = self.fake.metric_measurement()
          valor = str(self.fake.random_int(100, 250000))
          sitioCompra = self.fake.company()
          self.logica.crear_ingrediente(nombre,unidad,valor,sitioCompra)
          resultado_ingrediente = self.session.query(Ingrediente).filter(Ingrediente.nombre == nombre and Ingrediente.unidadMedida == unidad and Ingrediente.valorUnidad == valor and Ingrediente.sitioCompra == sitioCompra).first()
          self.assertEqual(resultado_ingrediente.nombre, nombre)
          self.assertEqual(resultado_ingrediente.unidadMedida, unidad)
          self.assertEqual(resultado_ingrediente.valorUnidad, int(valor))
          self.assertEqual(resultado_ingrediente.sitioCompra, sitioCompra)

     def test_validar_receta_nombre_invalido(self):
          nombre_nulo = None
          nombre_vacio = ''
          self.assertEqual(self.logica.validar_crear_editar_receta(0, nombre_nulo, ' ', ' ', ' ', ' '), "Nombre Invalido")
          self.assertEqual(self.logica.validar_crear_editar_receta(0, nombre_vacio, ' ', ' ', ' ', ' '), "Nombre Invalido")

     def test_validar_receta_nombre_numero_caracteres(self):
          nombre = 'hola' * 255
          self.assertEqual(self.logica.validar_crear_editar_receta(0, nombre, ' ', ' ', ' ', ' '), "Nombre Invalido")

     def test_validar_receta_nombre_no_string(self):
          nombre = 123
          self.assertEqual(self.logica.validar_crear_editar_receta(0, nombre, ' ', ' ', ' ', ' '), "Nombre Invalido")

     def test_validar_receta_tiempo_preparacion_invalido(self):
          tiempo_nulo = None
          tiempo_vacio = ''
          self.assertEqual(self.logica.validar_crear_editar_receta(0, 'Ajiaco', tiempo_nulo, ' ', ' ', ' '), "Tiempo Preparacion Invalido")
          self.assertEqual(self.logica.validar_crear_editar_receta(0, 'Ajiaco', tiempo_vacio, ' ', ' ', ' '), "Tiempo Preparacion Invalido")

     def test_validar_receta_tiempo_preparacion_formato_invalido(self):
          tiempo='24'
          self.assertEqual(self.logica.validar_crear_editar_receta(0, 'Ajiaco', tiempo, ' ', ' ', ' '), "Tiempo Preparacion Invalido")

     def test_validar_receta_tiempo_preparacion_minutos_invalidos(self):
          tiempo='24:70:00'
          self.assertEqual(self.logica.validar_crear_editar_receta(0, 'Ajiaco', tiempo, ' ', ' ', ' '), "Tiempo Preparacion Invalido")

     def test_validar_receta_tiempo_preparacion_segundos_invalidos(self):
          tiempo='24:40:99'
          self.assertEqual(self.logica.validar_crear_editar_receta(0, 'Ajiaco', tiempo, ' ', ' ', ' '), "Tiempo Preparacion Invalido")

     def test_validar_receta_tiempo_preparacion_no_string(self):
          tiempo=123
          self.assertEqual(self.logica.validar_crear_editar_receta(0, 'Ajiaco', tiempo, ' ', ' ', ' '), "Tiempo Preparacion Invalido")

     def test_validar_receta_numero_personas_invalido(self):
          personas_nulo = None
          personas_vacio = ''
          self.assertEqual(self.logica.validar_crear_editar_receta(0, 'Ajiaco', '01:00:00', personas_nulo, ' ', ' '), "Numero de Personas Invalido")
          self.assertEqual(self.logica.validar_crear_editar_receta(0, 'Ajiaco', '01:00:00', personas_vacio, ' ', ' '), "Numero de Personas Invalido")

     def test_validar_receta_numero_personas_mayor_cero(self):
          personas = '0'
          self.assertEqual(self.logica.validar_crear_editar_receta(0, 'Ajiaco', '01:00:00', personas, ' ', ' '), "Numero de Personas Invalido")

     def test_validar_receta_numero_personas_tipo_entero(self):
          personas = 'a'
          self.assertEqual(self.logica.validar_crear_editar_receta(0, 'Ajiaco', '01:00:00', personas, ' ', ' '), "Numero de Personas Invalido")

     def test_validar_receta_calorias_invalido(self):
          calorias_nulo = None
          calorias_vacio = ''
          self.assertEqual(self.logica.validar_crear_editar_receta(0, 'Ajiaco', '01:00:00', '1', calorias_nulo, ' '), "Calorias Porcion Invalido")
          self.assertEqual(self.logica.validar_crear_editar_receta(0, 'Ajiaco', '01:00:00', '1', calorias_vacio, ' '), "Calorias Porcion Invalido")

     def test_validar_receta_calorias_mayor_cero(self):
          calorias = '0'
          self.assertEqual(self.logica.validar_crear_editar_receta(0, 'Ajiaco', '01:00:00', '1', calorias, ' '), "Calorias Porcion Invalido")

     def test_validar_receta_calorias_tipo_entero(self):
          calorias = 'a'
          self.assertEqual(self.logica.validar_crear_editar_receta(0, 'Ajiaco', '01:00:00', '1', calorias, ' '), "Calorias Porcion Invalido")

     def test_validar_receta_instrucciones_invalido(self):
          instrucciones_nulo = None
          instrucciones_vacio = ''
          self.assertEqual(self.logica.validar_crear_editar_receta(0, 'Ajiaco', '01:00:00', '1', '1', instrucciones_nulo ), "Instrucciones Receta Invalido")
          self.assertEqual(self.logica.validar_crear_editar_receta(0, 'Ajiaco', '01:00:00', '1', '1', instrucciones_vacio), "Instrucciones Receta Invalido")

     def test_validar_receta_instrucciones_tipo_string(self):
          instrucciones = 123
          self.assertEqual(self.logica.validar_crear_editar_receta(0, 'Ajiaco', '01:00:00', '1', '1', instrucciones ), "Instrucciones Receta Invalido")

     def test_crear_receta(self):
        self.assertEqual(self.logica.crear_receta( self.fake.unique.dish(),str(self.fake.time_object())[0:8], self.fake.random_int(1,6), self.fake.random_int(100, 2500), self.fake.paragraph(nb_sentences=5, variable_nb_sentences=False)) , '')

     def test_crear_receta_repetida(self):
        nombre= self.fake.unique.dish()
        self.logica.crear_receta(nombre,str(self.fake.time_object())[0:8], self.fake.random_int(1,6), self.fake.random_int(100, 2500), self.fake.paragraph(nb_sentences=5, variable_nb_sentences=False))
        receta_id = self.session.query(Receta).filter(Receta.nombre == nombre).first().id
        self.assertEqual(self.logica.validar_crear_editar_receta(receta_id, nombre,str(self.fake.time_object())[0:8], self.fake.random_int(1,6), self.fake.random_int(100, 2500), self.fake.paragraph(nb_sentences=5, variable_nb_sentences=False)), "Receta ya existe")

     def test_verificar_almacenamiento_crear_receta(self):
        nombre= self.fake.unique.dish()
        instrucciones = self.fake.paragraph(nb_sentences=5, variable_nb_sentences=False)
        self.logica.crear_receta( nombre,str(self.fake.time_object())[0:8], self.fake.random_int(1,6), self.fake.random_int(100, 2500), instrucciones)
        self.session = Session()
        receta = self.session.query(Receta).filter(Receta.nombre == nombre).first()
        self.assertEqual(receta.nombre, nombre)
        self.assertEqual(receta.instrucciones, instrucciones)
        
     def test_verificar_lista_ingredientes_receta_vacia(self):
          receta = Receta(nombre = self.fake.unique.dish(),
                         tiempoPreparacion =str(self.fake.time_object())[0:8],
                         personasBase = self.fake.random_int(1,6),
                         caloriasPorcion = self.fake.random_int(100, 2500),
                         instrucciones = self.fake.paragraph(nb_sentences=5, variable_nb_sentences=False)
                         )
          self.session.add(receta)
          self.session.commit()

          self.assertListEqual(self.logica.dar_ingredientes_receta(receta.id),[])
     
     def test_verificar_lista_ingredientes_receta_un_ingrediente(self):
          receta = Receta(
                    nombre = self.fake.unique.dish(),
                    tiempoPreparacion =str(self.fake.time_object())[0:8],
                    personasBase = self.fake.random_int(1,6),
                    caloriasPorcion = self.fake.random_int(100, 2500),
                    instrucciones = self.fake.paragraph(nb_sentences=5, variable_nb_sentences=False)
                    )
          self.session.add(receta)
          self.session.commit()

          ingrediente = Ingrediente(
               nombre = self.fake.unique.ingredient(),
               unidadMedida = self.fake.metric_measurement(),
               sitioCompra =  self.fake.company(),
               valorUnidad = self.fake.random_int(100, 250000)
               )
          self.session.add(ingrediente)
          self.session.commit()

          ingredeintes_guardados = self.session.query(Ingrediente).all()
          recetas_guardadas = self.session.query(Receta).all()

          ingrediente_receta = IngredienteReceta(
               cantidad=self.fake.random_int(0, 2000),
               receta=(recetas_guardadas[0].id),
               ingrediente=(ingredeintes_guardados[0].id)
          )

          self.session.add(ingrediente_receta)
          self.session.commit()

          ingredientes_receta = self.logica.dar_ingredientes_receta(recetas_guardadas[0].id -1)

          self.assertEqual(len(ingredientes_receta),1)
          
          
     
     def test_verificar_lista_ingredientes_receta_varios_ingredientes(self):
          receta = Receta(nombre = self.fake.unique.dish(),
                         tiempoPreparacion =str(self.fake.time_object())[0:8],
                         personasBase = self.fake.random_int(1,6),
                         caloriasPorcion = self.fake.random_int(100, 2500),
                         instrucciones = self.fake.paragraph(nb_sentences=5, variable_nb_sentences=False)
                         )
          self.session.add(receta)
          self.session.commit()

          for i in range(0,10):
               ingrediente = Ingrediente(
                    nombre = self.fake.unique.ingredient(),
                    unidadMedida = self.fake.metric_measurement(),
                    sitioCompra =  self.fake.company(),
                    valorUnidad = self.fake.random_int(100, 250000)
               )
               self.session.add(ingrediente)
               self.session.commit()

          ingredientes = self.session.query(Ingrediente).all()
          recetas_guardadas = self.session.query(Receta).all()   

          for i in range(0,10):
               ingrediente_receta = IngredienteReceta(
                    cantidad=self.fake.random_int(0, 2000),
                    receta=receta.id,
                    ingrediente=ingredientes[i].id
               )

               self.session.add(ingrediente_receta)
               self.session.commit()
          
          

          ingredientes_receta = self.logica.dar_ingredientes_receta(recetas_guardadas[0].id - 1)

          self.assertEqual(len(ingredientes_receta),10)

     def test_verificar_lista_ingredientes_receta_varios_ingredientes_organizados_nombre(self):
          receta = Receta(nombre = self.fake.unique.dish(),
                         tiempoPreparacion =str(self.fake.time_object())[0:8],
                         personasBase = self.fake.random_int(1,6),
                         caloriasPorcion = self.fake.random_int(100, 2500),
                         instrucciones = self.fake.paragraph(nb_sentences=5, variable_nb_sentences=False)
                         )
          self.session.add(receta)
          self.session.commit()

          for i in range(0,10):
               ingrediente = Ingrediente(
                    nombre = self.fake.unique.ingredient(),
                    unidadMedida = self.fake.metric_measurement(),
                    sitioCompra =  self.fake.company(),
                    valorUnidad = self.fake.random_int(100, 250000)
               )
               self.session.add(ingrediente)
               self.session.commit()

          recetas_guardadas = self.session.query(Receta).all()
          ingredientes = self.session.query(Ingrediente).all()
          
          for i in range(0,10):
               ingrediente_receta = IngredienteReceta(
                    cantidad=self.fake.random_int(0, 2000),
                    receta=recetas_guardadas[0].id,
                    ingrediente= ingredientes[i].id
               )
               self.session.add(ingrediente_receta)
               self.session.commit()
          
          ingredientes_receta= sorted(ingredientes, key=lambda x: x.nombre)

          self.assertEqual(self.logica.dar_ingredientes_receta(recetas_guardadas[0].id - 1)[0]['ingrediente'], ingredientes_receta[0].nombre)
          self.assertEqual(self.logica.dar_ingredientes_receta(recetas_guardadas[0].id - 1)[1]['ingrediente'], ingredientes_receta[1].nombre)
          self.assertEqual(self.logica.dar_ingredientes_receta(recetas_guardadas[0].id - 1)[2]['ingrediente'], ingredientes_receta[2].nombre)
          self.assertEqual(self.logica.dar_ingredientes_receta(recetas_guardadas[0].id - 1)[3]['ingrediente'], ingredientes_receta[3].nombre)
          self.assertEqual(self.logica.dar_ingredientes_receta(recetas_guardadas[0].id - 1)[4]['ingrediente'], ingredientes_receta[4].nombre)
          self.assertEqual(self.logica.dar_ingredientes_receta(recetas_guardadas[0].id - 1)[5]['ingrediente'], ingredientes_receta[5].nombre)
          self.assertEqual(self.logica.dar_ingredientes_receta(recetas_guardadas[0].id - 1)[6]['ingrediente'], ingredientes_receta[6].nombre)
          self.assertEqual(self.logica.dar_ingredientes_receta(recetas_guardadas[0].id - 1)[7]['ingrediente'], ingredientes_receta[7].nombre)
          self.assertEqual(self.logica.dar_ingredientes_receta(recetas_guardadas[0].id - 1)[8]['ingrediente'], ingredientes_receta[8].nombre)
          self.assertEqual(self.logica.dar_ingredientes_receta(recetas_guardadas[0].id - 1)[9]['ingrediente'], ingredientes_receta[9].nombre)
     
     def test_verificar_lista_ingredientes_receta_varios_ingredientes_organizados_nombre_unidad(self):
          receta = Receta(nombre = self.fake.unique.dish(),
                         tiempoPreparacion =str(self.fake.time_object())[0:8],
                         personasBase = self.fake.random_int(1,6),
                         caloriasPorcion = self.fake.random_int(100, 2500),
                         instrucciones = self.fake.paragraph(nb_sentences=5, variable_nb_sentences=False)
                         )
          self.session.add(receta)
          self.session.commit()

          for i in range(0,10):
               ingrediente = Ingrediente(
                    nombre = self.fake.unique.ingredient(),
                    unidadMedida = self.fake.metric_measurement(),
                    sitioCompra =  self.fake.company(),
                    valorUnidad = self.fake.random_int(100, 250000)
               )
               self.session.add(ingrediente)
               self.session.commit()

          recetas_guardadas = self.session.query(Receta).all()
          ingredientes = self.session.query(Ingrediente).all()

          ingredientes_recetas_guardadas = []
          
          for i in range(0,10):
               ingrediente_receta = IngredienteReceta(
                    cantidad=self.fake.random_int(0, 2000),
                    receta=recetas_guardadas[0].id,
                    ingrediente= ingredientes[i].id
               )
               ingredientes_recetas_guardadas.append({
                    'ingrediente': ingredientes[i].nombre,
                    'unidad': ingredientes[i].unidadMedida,
                    'cantidad': ingrediente_receta.cantidad
               })
               self.session.add(ingrediente_receta)
               self.session.commit()

          
          ingredientes_receta_ordenadas= sorted(ingredientes_recetas_guardadas, key=lambda x: (x['ingrediente'], x['cantidad']))

          self.assertEqual(self.logica.dar_ingredientes_receta(recetas_guardadas[0].id - 1)[0]['cantidad'], ingredientes_receta_ordenadas[0]['cantidad'])
          self.assertEqual(self.logica.dar_ingredientes_receta(recetas_guardadas[0].id - 1)[1]['cantidad'], ingredientes_receta_ordenadas[1]['cantidad'])
          self.assertEqual(self.logica.dar_ingredientes_receta(recetas_guardadas[0].id - 1)[2]['cantidad'], ingredientes_receta_ordenadas[2]['cantidad'])
          self.assertEqual(self.logica.dar_ingredientes_receta(recetas_guardadas[0].id - 1)[3]['cantidad'], ingredientes_receta_ordenadas[3]['cantidad'])
          self.assertEqual(self.logica.dar_ingredientes_receta(recetas_guardadas[0].id - 1)[4]['cantidad'], ingredientes_receta_ordenadas[4]['cantidad'])
          self.assertEqual(self.logica.dar_ingredientes_receta(recetas_guardadas[0].id - 1)[5]['cantidad'], ingredientes_receta_ordenadas[5]['cantidad'])
          self.assertEqual(self.logica.dar_ingredientes_receta(recetas_guardadas[0].id - 1)[6]['cantidad'], ingredientes_receta_ordenadas[6]['cantidad'])
          self.assertEqual(self.logica.dar_ingredientes_receta(recetas_guardadas[0].id - 1)[7]['cantidad'], ingredientes_receta_ordenadas[7]['cantidad'])
          self.assertEqual(self.logica.dar_ingredientes_receta(recetas_guardadas[0].id - 1)[8]['cantidad'], ingredientes_receta_ordenadas[8]['cantidad'])
          self.assertEqual(self.logica.dar_ingredientes_receta(recetas_guardadas[0].id - 1)[9]['cantidad'], ingredientes_receta_ordenadas[9]['cantidad'])
     
     def test_verificar_lista_ingredientes_receta_varios_ingredientes_organizados_nombre_unidad_cantidad(self):
          receta = Receta(nombre = self.fake.unique.dish(),
                         tiempoPreparacion =str(self.fake.time_object())[0:8],
                         personasBase = self.fake.random_int(1,6),
                         caloriasPorcion = self.fake.random_int(100, 2500),
                         instrucciones = self.fake.paragraph(nb_sentences=5, variable_nb_sentences=False)
                         )
          self.session.add(receta)
          self.session.commit()

          for i in range(0,10):
               ingrediente = Ingrediente(
                    nombre = 'Cebolla',
                    unidadMedida = self.fake.metric_measurement(),
                    sitioCompra =  self.fake.company(),
                    valorUnidad = self.fake.random_int(100, 250000)
               )
               self.session.add(ingrediente)
               self.session.commit()

          recetas_guardadas = self.session.query(Receta).all()
          ingredientes = self.session.query(Ingrediente).all()

          ingredientes_recetas_guardadas = []
          
          for i in range(0,10):
               
               ingrediente_receta = IngredienteReceta(
                    cantidad=self.fake.random_int(0, 2000),
                    receta=recetas_guardadas[0].id,
                    ingrediente= ingredientes[i].id
               )
               ingredientes_recetas_guardadas.append({
                    'ingrediente': ingredientes[1].nombre,
                    'unidad': ingredientes[i].unidadMedida,
                    'cantidad': ingrediente_receta.cantidad
               })
               
               self.session.add(ingrediente_receta)
               self.session.commit()

          
          ingredientes_receta_ordenadas= sorted(ingredientes_recetas_guardadas, key=lambda x: (x['ingrediente'], x['unidad'], x['cantidad']))

          self.assertEqual(self.logica.dar_ingredientes_receta(recetas_guardadas[0].id - 1)[0]['unidad'], ingredientes_receta_ordenadas[0]['unidad'])
          self.assertEqual(self.logica.dar_ingredientes_receta(recetas_guardadas[0].id - 1)[1]['unidad'], ingredientes_receta_ordenadas[1]['unidad'])
          self.assertEqual(self.logica.dar_ingredientes_receta(recetas_guardadas[0].id - 1)[2]['unidad'], ingredientes_receta_ordenadas[2]['unidad'])
          self.assertEqual(self.logica.dar_ingredientes_receta(recetas_guardadas[0].id - 1)[3]['unidad'], ingredientes_receta_ordenadas[3]['unidad'])
          self.assertEqual(self.logica.dar_ingredientes_receta(recetas_guardadas[0].id - 1)[4]['unidad'], ingredientes_receta_ordenadas[4]['unidad'])
          self.assertEqual(self.logica.dar_ingredientes_receta(recetas_guardadas[0].id - 1)[5]['unidad'], ingredientes_receta_ordenadas[5]['unidad'])
          self.assertEqual(self.logica.dar_ingredientes_receta(recetas_guardadas[0].id - 1)[6]['unidad'], ingredientes_receta_ordenadas[6]['unidad'])
          self.assertEqual(self.logica.dar_ingredientes_receta(recetas_guardadas[0].id - 1)[7]['unidad'], ingredientes_receta_ordenadas[7]['unidad'])
          self.assertEqual(self.logica.dar_ingredientes_receta(recetas_guardadas[0].id - 1)[8]['unidad'], ingredientes_receta_ordenadas[8]['unidad'])
          self.assertEqual(self.logica.dar_ingredientes_receta(recetas_guardadas[0].id - 1)[9]['unidad'], ingredientes_receta_ordenadas[9]['unidad'])


     def test_dar_receta_id_invalido(self):
          for i in range(0,10):
               receta = Receta(
                    nombre = self.fake.unique.dish(),
                         tiempoPreparacion =str(self.fake.time_object())[0:8],
                         personasBase = self.fake.random_int(1,6),
                         caloriasPorcion = self.fake.random_int(100, 2500),
                         instrucciones = self.fake.paragraph(nb_sentences=5, variable_nb_sentences=False)
               )

               self.session.add(receta)
               self.session.commit()
          
          self.assertEqual(self.logica.dar_receta(id_receta= 11), False)

     def test_dar_receta_id_valido(self):
          for i in range(0,10):
               receta = Receta(
                    nombre = self.fake.unique.dish(),
                         tiempoPreparacion =str(self.fake.time_object())[0:8],
                         personasBase = self.fake.random_int(1,6),
                         caloriasPorcion = self.fake.random_int(100, 2500),
                         instrucciones = self.fake.paragraph(nb_sentences=5, variable_nb_sentences=False)
               )

               self.session.add(receta)
               self.session.commit()
          receta_mostrar = self.session.query(Receta).all()[8]
          self.assertEqual(self.logica.dar_receta(8)['nombre'], receta_mostrar.nombre)
          self.assertEqual(self.logica.dar_receta(8)['tiempo'], receta_mostrar.tiempoPreparacion)
          self.assertEqual(self.logica.dar_receta(8)['personas'], receta_mostrar.personasBase)
          self.assertEqual(self.logica.dar_receta(8)['calorias'], receta_mostrar.caloriasPorcion)
          self.assertEqual(self.logica.dar_receta(8)['preparacion'], receta_mostrar.instrucciones)

     def test_validar_crear_editar_ingrediente_receta_lista_ingrediente_vacia(self):

          receta = Receta(
                    nombre = self.fake.unique.dish(),
                         tiempoPreparacion =str(self.fake.time_object())[0:8],
                         personasBase = self.fake.random_int(1,6),
                         caloriasPorcion = self.fake.random_int(100, 2500),
                         instrucciones = self.fake.paragraph(nb_sentences=5, variable_nb_sentences=False)
               )

          self.session.add(receta)
          self.session.commit()

          receta_seleccionada = ({
                    'nombre': receta.nombre,
                    'tiempo': receta.tiempoPreparacion,
                    'personas': receta.personasBase,
                    'calorias': receta.caloriasPorcion,
                    'preparacion': receta.instrucciones
                    })

          self.assertEqual(self.logica.validar_crear_editar_ingReceta(receta_seleccionada, None, None ), 'No existen ingredientes')

     def test_validar_crear_editar_ingrediente_receta_lista_ingredientes(self):

          receta = Receta(
                    nombre = self.fake.unique.dish(),
                         tiempoPreparacion =str(self.fake.time_object())[0:8],
                         personasBase = self.fake.random_int(1,6),
                         caloriasPorcion = self.fake.random_int(100, 2500),
                         instrucciones = self.fake.paragraph(nb_sentences=5, variable_nb_sentences=False)
               )

          self.session.add(receta)
          self.session.commit()

          receta_seleccionada = ({
                    'nombre': receta.nombre,
                    'tiempo': receta.tiempoPreparacion,
                    'personas': receta.personasBase,
                    'calorias': receta.caloriasPorcion,
                    'preparacion': receta.instrucciones
                    })

          for i in range(0,10):
               ingrediente =Ingrediente(
                         nombre = self.fake.unique.ingredient(),
                         unidadMedida = self.fake.metric_measurement(),
                         sitioCompra =  self.fake.company(),
                         valorUnidad = self.fake.random_int(100, 250000)
                    )
               self.session.add(ingrediente)
               self.session.commit()

          ingrediente_falso =(
                    {
                    'nombre': self.fake.unique.ingredient(),
                    'unidad': self.fake.metric_measurement(),
                    'valor': self.fake.company(),
                    'sitioCompra': self.fake.random_int(100, 250000)
                }
                )

          self.assertEqual(self.logica.validar_crear_editar_ingReceta(receta_seleccionada, ingrediente_falso, None ), 'Ingrediente Invalido')

     def test_validar_crear_editar_ingrediente_receta_cantidad_vacio(self):

          receta = Receta(
                    nombre = self.fake.unique.dish(),
                         tiempoPreparacion =str(self.fake.time_object())[0:8],
                         personasBase = self.fake.random_int(1,6),
                         caloriasPorcion = self.fake.random_int(100, 2500),
                         instrucciones = self.fake.paragraph(nb_sentences=5, variable_nb_sentences=False)
               )

          self.session.add(receta)
          self.session.commit()

          receta_seleccionada = ({
                    'nombre': receta.nombre,
                    'tiempo': receta.tiempoPreparacion,
                    'personas': receta.personasBase,
                    'calorias': receta.caloriasPorcion,
                    'preparacion': receta.instrucciones
                    })

          for i in range(0,10):
               ingrediente =Ingrediente(
                         nombre = self.fake.unique.ingredient(),
                         unidadMedida = self.fake.metric_measurement(),
                         sitioCompra =  self.fake.company(),
                         valorUnidad = self.fake.random_int(100, 250000)
                    )
               self.session.add(ingrediente)
               self.session.commit()

          ingredientes = self.session.query(Ingrediente).all()[8]

          ingrediente_valido =(
                    {
                    'nombre': ingredientes.nombre,
                    'unidad': ingredientes.unidadMedida,
                    'valor': ingredientes.valorUnidad,
                    'sitioCompra': ingredientes.sitioCompra
                }
                )

          self.assertEqual(self.logica.validar_crear_editar_ingReceta(receta_seleccionada, ingrediente_valido, None ), 'Cantidad invalido')

     def test_validar_crear_editar_ingrediente_receta_cantidad_invalido(self):
          
          receta = Receta(
                    nombre = self.fake.unique.dish(),
                         tiempoPreparacion =str(self.fake.time_object())[0:8],
                         personasBase = self.fake.random_int(1,6),
                         caloriasPorcion = self.fake.random_int(100, 2500),
                         instrucciones = self.fake.paragraph(nb_sentences=5, variable_nb_sentences=False)
               )

          self.session.add(receta)
          self.session.commit()

          receta_seleccionada = ({
                    'nombre': receta.nombre,
                    'tiempo': receta.tiempoPreparacion,
                    'personas': receta.personasBase,
                    'calorias': receta.caloriasPorcion,
                    'preparacion': receta.instrucciones
                    })

          for i in range(0,10):
               ingrediente =Ingrediente(
                         nombre = self.fake.unique.ingredient(),
                         unidadMedida = self.fake.metric_measurement(),
                         sitioCompra =  self.fake.company(),
                         valorUnidad = self.fake.random_int(100, 250000)
                    )
               self.session.add(ingrediente)
               self.session.commit()

          ingredientes = self.session.query(Ingrediente).all()[8]

          ingrediente_valido =(
                    {
                    'nombre': ingredientes.nombre,
                    'unidad': ingredientes.unidadMedida,
                    'valor': ingredientes.valorUnidad,
                    'sitioCompra': ingredientes.sitioCompra
                }
                )

          self.assertEqual(self.logica.validar_crear_editar_ingReceta(receta_seleccionada, ingrediente_valido, 0 ), 'Cantidad invalido')


     
     def test_validar_crear_editar_ingrediente_receta_cantidad_tipo_invalido(self):
          
          receta = Receta(
                    nombre = self.fake.unique.dish(),
                         tiempoPreparacion =str(self.fake.time_object())[0:8],
                         personasBase = self.fake.random_int(1,6),
                         caloriasPorcion = self.fake.random_int(100, 2500),
                         instrucciones = self.fake.paragraph(nb_sentences=5, variable_nb_sentences=False)
               )

          self.session.add(receta)
          self.session.commit()

          receta_seleccionada = ({
                    'nombre': receta.nombre,
                    'tiempo': receta.tiempoPreparacion,
                    'personas': receta.personasBase,
                    'calorias': receta.caloriasPorcion,
                    'preparacion': receta.instrucciones
                    })

          for i in range(0,10):
               ingrediente =Ingrediente(
                         nombre = self.fake.unique.ingredient(),
                         unidadMedida = self.fake.metric_measurement(),
                         sitioCompra =  self.fake.company(),
                         valorUnidad = self.fake.random_int(100, 250000)
                    )
               self.session.add(ingrediente)
               self.session.commit()

          ingredientes = self.session.query(Ingrediente).all()[8]

          ingrediente_valido =(
                    {
                    'nombre': ingredientes.nombre,
                    'unidad': ingredientes.unidadMedida,
                    'valor': ingredientes.valorUnidad,
                    'sitioCompra': ingredientes.sitioCompra
                }
                )

          self.assertEqual(self.logica.validar_crear_editar_ingReceta(receta_seleccionada, ingrediente_valido, 'str' ), 'Cantidad invalido')

     def test_validar_agregar_ingrediente_receta(self):
          
          receta = Receta(
                    nombre = self.fake.unique.dish(),
                         tiempoPreparacion =str(self.fake.time_object())[0:8],
                         personasBase = self.fake.random_int(1,6),
                         caloriasPorcion = self.fake.random_int(100, 2500),
                         instrucciones = self.fake.paragraph(nb_sentences=5, variable_nb_sentences=False)
               )

          self.session.add(receta)
          self.session.commit()

          receta_seleccionada = ({
                    'nombre': receta.nombre,
                    'tiempo': receta.tiempoPreparacion,
                    'personas': receta.personasBase,
                    'calorias': receta.caloriasPorcion,
                    'preparacion': receta.instrucciones
                    })

          for i in range(0,10):
               ingrediente =Ingrediente(
                         nombre = self.fake.unique.ingredient(),
                         unidadMedida = self.fake.metric_measurement(),
                         sitioCompra =  self.fake.company(),
                         valorUnidad = self.fake.random_int(100, 250000)
                    )
               self.session.add(ingrediente)
               self.session.commit()

          ingredientes = self.session.query(Ingrediente).all()[8]

          ingrediente_valido =(
                    {
                    'nombre': ingredientes.nombre,
                    'unidad': ingredientes.unidadMedida,
                    'valor': ingredientes.valorUnidad,
                    'sitioCompra': ingredientes.sitioCompra
                }
                )

          self.assertEqual(self.logica.validar_crear_editar_ingReceta(receta_seleccionada, ingrediente_valido, 3.0 ), '')


     def test_guardar_ingrediente_receta_persistencia(self):
          receta = Receta(
                    nombre = self.fake.unique.dish(),
                         tiempoPreparacion =str(self.fake.time_object())[0:8],
                         personasBase = self.fake.random_int(1,6),
                         caloriasPorcion = self.fake.random_int(100, 2500),
                         instrucciones = self.fake.paragraph(nb_sentences=5, variable_nb_sentences=False)
               )

          self.session.add(receta)
          self.session.commit()

          receta_seleccionada = ({
                    'nombre': receta.nombre,
                    'tiempo': receta.tiempoPreparacion,
                    'personas': receta.personasBase,
                    'calorias': receta.caloriasPorcion,
                    'preparacion': receta.instrucciones
                    })

          for i in range(0,10):
               ingrediente =Ingrediente(
                         nombre = self.fake.unique.ingredient(),
                         unidadMedida = self.fake.metric_measurement(),
                         sitioCompra =  self.fake.company(),
                         valorUnidad = self.fake.random_int(100, 250000)
                    )
               self.session.add(ingrediente)
               self.session.commit()

          ingredientes = self.session.query(Ingrediente).all()[8]

          ingrediente_valido =(
                    {
                    'nombre': ingredientes.nombre,
                    'unidad': ingredientes.unidadMedida,
                    'valor': ingredientes.valorUnidad,
                    'sitioCompra': ingredientes.sitioCompra
                }
                )
          
          self.assertEqual(self.logica.agregar_ingrediente_receta(receta_seleccionada, ingrediente_valido,150.0), True)
          
          ingredientes_receta = self.session.query(IngredienteReceta).filter(IngredienteReceta.cantidad == 150.0, IngredienteReceta.receta == 1).all()

          self.assertEqual(len(ingredientes_receta), 0)
