# gpd.read_file('maps/data/russia.geojson')

# if gdf is not None:
#     # Преобразуем столбцы с типом Timestamp в строки
#     for col in gdf.columns:
#         if col  == 'created_at':  # Проверяем, является ли столбец временной меткой
#             gdf[col] = gdf[col].astype(str)  # Преобразуем в строку
#         if col == 'updated_at':  # Проверяем, является ли столбец временной меткой
#             gdf[col] = gdf[col].astype(str)  # Преобразуем в строку


import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import geopandas as gpd
import pandas as pd

# Загрузка геоданных о регионах России
# gdf = gpd.read_file("maps/data/russia.geojson")  # Замените на путь к вашему GeoJSON файлу
gdf = gpd.read_file("maps/data/gadm41_RUS_1.json")

# Создание Dash приложения
app = dash.Dash(__name__)

# Создание фигуры с картой
fig = px.choropleth(gdf,
                    geojson=gdf.geometry.__geo_interface__,
                    locations=gdf.index,
                    # color='10',  # Укажите столбец для цветовой шкалы
                    hover_name='NAME_1',  # Укажите столбец для отображения имени региона
                    title='Интерактивная карта России')

# Обновление макета карты
fig.update_geos(fitbounds="locations", visible=False)

# Определение макета приложения
app.layout = html.Div([
    dcc.Graph(id='map', figure=fig),
    html.Div(id='output-container')
])

# Обработчик кликов по регионам
@app.callback(
    Output('output-container', 'children'),
    Input('map', 'clickData')
)
def display_click_data(clickData):
    if clickData:
        region_name = clickData['points'][0]['hovertext']  # Получение имени региона из всплывающей подсказки
        # Здесь можно добавить дополнительные данные о регионе, если они есть в gdf
        return f'Вы выбрали регион: {region_name}'
    return 'Нажмите на регион для получения информации.'

# Запуск приложения
if __name__ == '__main__':
    app.run_server(debug=True)
