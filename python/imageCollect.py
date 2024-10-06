import ee
import geopandas as gpd
from datetime import datetime, timedelta
class DatosClimaticos:
    def __init__(self):
        # Autenticar con tu cuenta de Earth Engine
        ee.Authenticate()
        ee.Initialize(project='ee-santigimenez20020817')
        self.__datos=self.distintasFuentes()
        return

    def distintasFuentes(self,coordenadas=[[[-124.48, 32.53], [-124.48, 42.01], [-114.13, 42.01], [-114.13, 32.53]]]):

        area_de_california = ee.Geometry.Polygon(
            [[[-124.48, 32.53], [-124.48, 42.01], [-114.13, 42.01], [-114.13, 32.53]]]
        )

        # Filtrar por el rango de fechas
        # fecha_hoy = datetime.today().strftime('%Y-%m-%d')
        fecha_hoy = (datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d')
        fecha_ayer = (datetime.today() - timedelta(days=2)).strftime('%Y-%m-%d')
        # print(fecha_ayer,"  ",fecha_hoy)
        # return
        fecha_inicio = '2024-01-01'
        fecha_fin = '2024-09-20'
        

        # Colección de temperatura (ECMWF ERA5 Land)
        coleccion_temperatura = ee.ImageCollection('ECMWF/ERA5_LAND/HOURLY').select('temperature_2m')\
            .filterDate(fecha_inicio, fecha_fin).filterBounds(area_de_california)

        # Colección de humedad relativa (ECMWF ERA5 Land)
        coleccion_humedad = ee.ImageCollection('ECMWF/ERA5_LAND/HOURLY').select('dewpoint_temperature_2m')\
            .filterDate(fecha_inicio, fecha_fin).filterBounds(area_de_california)

        # Colección de radiación solar (ECMWF ERA5 Land - superficie)
        coleccion_radiacion = ee.ImageCollection('ECMWF/ERA5_LAND/HOURLY').select('surface_solar_radiation_downwards')\
            .filterDate(fecha_inicio, fecha_fin).filterBounds(area_de_california)

        # Colección de viento (ECMWF ERA5 Land)
        coleccion_viento = ee.ImageCollection('ECMWF/ERA5_LAND/HOURLY').select(['u_component_of_wind_10m', 'v_component_of_wind_10m'])\
            .filterDate(fecha_inicio, fecha_fin).filterBounds(area_de_california)

        # Colección de precipitaciones (CHIRPS Daily)
        coleccion_precipitacion = ee.ImageCollection('UCSB-CHG/CHIRPS/DAILY').select('precipitation')\
            .filterDate(fecha_inicio, fecha_fin).filterBounds(area_de_california)

        # Colección de evapotranspiración (MODIS)
        coleccion_evapotranspiracion = ee.ImageCollection('MODIS/061/MOD16A2').select('ET')\
            .filterDate(fecha_inicio, fecha_fin).filterBounds(area_de_california)

        # Obtener promedios
        media_temperatura = coleccion_temperatura.mean()
        media_humedad = coleccion_humedad.mean()
        media_radiacion = coleccion_radiacion.mean()
        media_viento = coleccion_viento.mean()
        media_precipitacion = coleccion_precipitacion.mean()
        media_evapotranspiracion = coleccion_evapotranspiracion.mean()

        # Reducir las colecciones para obtener valores promedios sobre el área de interés
        datos_temperatura = media_temperatura.reduceRegion(reducer=ee.Reducer.mean(), geometry=area_de_california, scale=9000)
        datos_humedad = media_humedad.reduceRegion(reducer=ee.Reducer.mean(), geometry=area_de_california, scale=9000)
        datos_radiacion = media_radiacion.reduceRegion(reducer=ee.Reducer.mean(), geometry=area_de_california, scale=9000)
        datos_viento = media_viento.reduceRegion(reducer=ee.Reducer.mean(), geometry=area_de_california, scale=9000)
        datos_precipitacion = media_precipitacion.reduceRegion(reducer=ee.Reducer.mean(), geometry=area_de_california, scale=5000)
        datos_evapotranspiracion = media_evapotranspiracion.reduceRegion(reducer=ee.Reducer.mean(), geometry=area_de_california, scale=500)

        # Guardar los datos en variables individuales
        temperatura = datos_temperatura.get('temperature_2m').getInfo()  # Kelvin
        humedad_relativa = datos_humedad.get('dewpoint_temperature_2m').getInfo()  # Kelvin
        radiacion_solar = datos_radiacion.get('surface_solar_radiation_downwards').getInfo()  # W/m²
        viento_u = datos_viento.get('u_component_of_wind_10m').getInfo()  # m/s
        viento_v = datos_viento.get('v_component_of_wind_10m').getInfo()  # m/s
        precipitaciones = datos_precipitacion.get('precipitation').getInfo()  # mm
        evapotranspiracion = datos_evapotranspiracion.get('ET').getInfo()  # kg/m²/8 días
        temperatura = datos_temperatura.get('temperature_2m').getInfo() - 273.15  # Convertir de Kelvin a °C
        punto_rocio = datos_humedad.get('dewpoint_temperature_2m').getInfo() - 273.15  # Convertir de Kelvin a °C

        # Calcular la presión de vapor actual (e) a partir del punto de rocío
        e = 6.11 * 10**((7.5 * punto_rocio) / (punto_rocio + 237.3))

        # Calcular la presión de vapor de saturación (es) a partir de la temperatura actual
        e_s = 6.11 * 10**((7.5 * temperatura) / (temperatura + 237.3))

        # Calcular la humedad relativa (HR)
        if e_s > 0:  # Asegurarse de que la presión de vapor de saturación no sea cero
            humedad_relativa_porcentaje = 100 * (e / e_s)
        else:
            humedad_relativa_porcentaje = 0  # Manejar el caso donde no hay datos

        # Imprimir el resultado
        # print(f"Humedad relativa: {humedad_relativa_porcentaje:.2f}%")
        # Convertir la temperatura a Celsius
        temperatura_celsius = temperatura - 273.15
        humedad_punto_rocio_celsius = humedad_relativa - 273.15
        arreglo = {
            "temperatura": {
                "valor": temperatura_celsius,
                "unidad": "°C"
            },
            "humedad relativa": {
                "valor": humedad_punto_rocio_celsius,
                "unidad": "°C"
            }
        }
        print(f"Temperatura: {temperatura_celsius} °C")
        print(f"Humedad relativa (punto de rocío): {humedad_punto_rocio_celsius} °C")
        print(f"Radiación solar: {radiacion_solar} W/m²")
        print(f"Velocidad del viento (u, v): {viento_u} m/s, {viento_v} m/s")
        print(f"Precipitaciones: {precipitaciones} mm")
        print(f"Evapotranspiración: {evapotranspiracion} kg/m²/8 días")

        # Imprimir los resultados
        # print("Temperatura (K): ", datos_temperatura.getInfo())
        # print("Humedad relativa (punto de rocío, K): ", datos_humedad.getInfo())
        # print("Radiación solar (W/m^2): ", datos_radiacion.getInfo())
        # print("Viento (u y v en m/s): ", datos_viento.getInfo())
        # print("Precipitaciones (mm): ", datos_precipitacion.getInfo())
        # print("Evapotranspiración (kg/m^2/8 días): ", datos_evapotranspiracion.getInfo())


if __name__ == "__main__":
    a = DatosClimaticos()

# class DatosClimaticos:
#     def __init__(self):
#         # Autenticar con tu cuenta de Earth Engine
#         ee.Authenticate()
#         ee.Initialize(project='ee-santigimenez20020817')
#         self.distintasFuentes()
#         return
#         # Definir el área de interés usando coordenadas
#         self.area_de_interes = ee.Geometry.Polygon(
#             [[[-69.0, -32.0], [-69.0, -33.0], [-68.0, -33.0], [-68.0, -32.0]]]
#         )

#         # Cargar la colección de datos climáticos (ejemplo: MODIS)
#         self.imagenes = ee.ImageCollection('MODIS/061/MOD11A2').filterDate('2023-01-01', '2023-12-31')

#         # Filtrar la colección por el área de interés
#         self.imagenes_en_area = self.imagenes.filterBounds(self.area_de_interes)

#         # Extraer los datos y convertirlos en GeoDataFrame
#         self.extraer_datos()

#     def extraer_datos(self):
#         # Definir la lista de variables
#         variables = {
#             'temperatura': 'LST_Day_1km',
#             'humedad': 'humidity',  # Cambiar según la colección de datos
#             'radiacion': 'solar_radiation',  # Cambiar según la colección de datos
#             'viento': 'wind_speed',  # Cambiar según la colección de datos
#             'precipitaciones': 'precipitation',  # Cambiar según la colección de datos
#             'evapotranspiracion': 'evapotranspiracion'  # Cambiar según la colección de datos
#         }

#         # Inicializar un diccionario para almacenar los datos
#         datos = {}

#         # Extraer el promedio de cada variable
#         for nombre, banda in variables.items():
#             imagen_media = self.imagenes_en_area.select(banda).mean()
#             datos[nombre] = imagen_media.reduceRegion(
#                 reducer=ee.Reducer.mean(),
#                 geometry=self.area_de_interes,
#                 scale=30,
#                 maxPixels=1e13
#             ).getInfo()  # Obtener información

#         # Convertir los datos a un GeoDataFrame
#         self.datos_geopandas(datos)

#     def datos_geopandas(self, datos):
#         # Crear un DataFrame de pandas a partir de los datos
#         df = gpd.GeoDataFrame([datos])
        
#         # Agregar geometría (opcional, si quieres un punto en el GeoDataFrame)
#         df['geometry'] = gpd.points_from_xy([-68.5], [-32.5])  # Cambia a las coordenadas del centro de tu área

#         # Definir el sistema de referencia (CRS)
#         df.set_crs(epsg=4326, inplace=True)

#         # Ahora puedes analizar tus datos usando GeoPandas
#         print(df)
#     def distintasFuentes(self):



#         # # Definir el área de interés (California)
#         area_de_california = ee.Geometry.Polygon(
#             [[[-124.48, 32.53], [-124.48, 42.01], [-114.13, 42.01], [-114.13, 32.53]]]
#         )

#         # # Cargar una colección de imágenes climáticas (ejemplo: ERA5 para temperatura)
#         # coleccion_temperatura = ee.ImageCollection('ECMWF/ERA5_LAND/HOURLY')\
#         #     .select('temperature_2m')\
#         #     .filterDate('2023-01-01', '2023-12-31')\
#         #     .filterBounds(area_de_california)

#         # # Extraer datos de temperatura promedio para California
#         # media_temperatura = coleccion_temperatura.mean()

#         # # Obtener los valores en un formato legible
#         # datos_temperatura = media_temperatura.reduceRegion(
#         #     reducer=ee.Reducer.mean(),
#         #     geometry=area_de_california,
#         #     scale=10000,  # Ajusta la escala según la resolución de los datos
#         #     maxPixels=1e13
#         # )

#         # print(datos_temperatura.getInfo())
#         # Cargar colecciones de diferentes variables


#         area_de_california = ee.Geometry.Polygon(
#             [[[-124.48, 32.53], [-124.48, 42.01], [-114.13, 42.01], [-114.13, 32.53]]]
#         )

#         # Filtrar por el rango de fechas
#         fecha_inicio = '2023-01-01'
#         fecha_fin = '2023-12-31'

#         # Colección de temperatura (ECMWF ERA5 Land)
#         coleccion_temperatura = ee.ImageCollection('ECMWF/ERA5_LAND/HOURLY').select('temperature_2m')\
#             .filterDate(fecha_inicio, fecha_fin).filterBounds(area_de_california)

#         # Colección de humedad relativa (ECMWF ERA5 Land)
#         coleccion_humedad = ee.ImageCollection('ECMWF/ERA5_LAND/HOURLY').select('dewpoint_temperature_2m')\
#             .filterDate(fecha_inicio, fecha_fin).filterBounds(area_de_california)

#         # Colección de radiación solar (NASA/POWER)
#         coleccion_radiacion = ee.ImageCollection('NASA/POWER/SOLAR_DAILY').select('ALLSKY_SFC_SW_DWN')\
#             .filterDate(fecha_inicio, fecha_fin).filterBounds(area_de_california)

#         # Colección de viento (ECMWF ERA5 Land)
#         coleccion_viento = ee.ImageCollection('ECMWF/ERA5_LAND/HOURLY').select(['u_component_of_wind_10m', 'v_component_of_wind_10m'])\
#             .filterDate(fecha_inicio, fecha_fin).filterBounds(area_de_california)

#         # Colección de precipitaciones (CHIRPS Daily)
#         coleccion_precipitacion = ee.ImageCollection('UCSB-CHG/CHIRPS/DAILY').select('precipitation')\
#             .filterDate(fecha_inicio, fecha_fin).filterBounds(area_de_california)

#         # Colección de evapotranspiración (MODIS)
#         coleccion_evapotranspiracion = ee.ImageCollection('MODIS/061/MOD16A2').select('ET')\
#             .filterDate(fecha_inicio, fecha_fin).filterBounds(area_de_california)

#         # Obtener promedios
#         media_temperatura = coleccion_temperatura.mean()
#         media_humedad = coleccion_humedad.mean()
#         media_radiacion = coleccion_radiacion.mean()
#         media_viento = coleccion_viento.mean()
#         media_precipitacion = coleccion_precipitacion.mean()
#         media_evapotranspiracion = coleccion_evapotranspiracion.mean()

#         # Reducir las colecciones para obtener valores promedios sobre el área de interés
#         datos_temperatura = media_temperatura.reduceRegion(reducer=ee.Reducer.mean(), geometry=area_de_california, scale=9000)
#         datos_humedad = media_humedad.reduceRegion(reducer=ee.Reducer.mean(), geometry=area_de_california, scale=9000)
#         datos_radiacion = media_radiacion.reduceRegion(reducer=ee.Reducer.mean(), geometry=area_de_california, scale=9000)
#         datos_viento = media_viento.reduceRegion(reducer=ee.Reducer.mean(), geometry=area_de_california, scale=9000)
#         datos_precipitacion = media_precipitacion.reduceRegion(reducer=ee.Reducer.mean(), geometry=area_de_california, scale=5000)
#         datos_evapotranspiracion = media_evapotranspiracion.reduceRegion(reducer=ee.Reducer.mean(), geometry=area_de_california, scale=500)

#         # Imprimir los resultados
#         print("Temperatura (K): ", datos_temperatura.getInfo())
#         print("Humedad relativa (punto de rocío, K): ", datos_humedad.getInfo())
#         print("Radiación solar (W/m^2): ", datos_radiacion.getInfo())
#         print("Viento (u y v en m/s): ", datos_viento.getInfo())
#         print("Precipitaciones (mm): ", datos_precipitacion.getInfo())
#         print("Evapotranspiración (kg/m^2/8 días): ", datos_evapotranspiracion.getInfo())



# # Crear una instancia de la clase
# # datos_climaticos = DatosClimaticos()


# if __name__=="__main__":
#     # ee.Authenticate()
#     # ee.Initialize(project='ee-santigimenez20020817')

#     # # Probar si funciona la autenticación mostrando información sobre un ImageCollection
#     # collection = ee.ImageCollection('LANDSAT/LC08/C02/T1_L2').first()
#     # print(collection.getInfo())

#     a=DatosClimaticos()