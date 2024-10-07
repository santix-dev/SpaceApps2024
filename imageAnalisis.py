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

    def distintasFuentes(self,coo1=[-31.537657, -68.530436],coo2=[-31.533055, -68.536174],coo3=[-31.538011, -68.515829]):

        area_de_california = ee.Geometry.Polygon(
            [[[-124.48, 32.53], [-124.48, 42.01], [-114.13, 42.01], [-114.13, 32.53]]]
            # # coordenadas
            # [[coo1,coo2,coo3]]
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
        print(f"Temperatura: {temperatura} °C")
        print(f"Humedad relativa (punto de rocío): {humedad_punto_rocio_celsius} °C")
        print(f"Humedad relativa: {humedad_relativa_porcentaje:.2f}%")
        print(f"Radiación solar: {radiacion_solar} W/m²")
        print(f"Velocidad del viento (u, v): {viento_u} m/s, {viento_v} m/s")
        print(f"Precipitaciones: {precipitaciones} mm")
        print(f"Evapotranspiración: {evapotranspiracion} kg/m²/8 días")


if __name__ == "__main__":
    a = DatosClimaticos()

