import pandas as pd
from conda_index.index.convert_cache import db_path
from dash import Dash, Input, Output, html, dcc, dash_table
import dash_bootstrap_components as dbc
import plotly.express as px
import numpy as np
from app import app
from apps.maps.map_figure import mapFigure, convert_crs
import plotly.graph_objects as go
from pyproj import Transformer


# regions = pd.read_parquet("apps/maps/data/russia_regions.parquet")
regions = pd.read_parquet("russia_regions.parquet")

def convert_lon_lat_to_xy(lon, lat):
    transformer = Transformer.from_crs("EPSG:4326", "EPSG:32646", always_xy=True)
    # Преобразование в UTM (метры)
    x, y = transformer.transform(lon, lat)
    return (x,y)

layout = [

    html.Div(
        style={'display': 'flex',
               'justifyContent': 'center',
               'alignItems': 'center',
               # 'height': '100vh'
               },
        children =[
        dcc.Graph(
            id = 'mapka',
            figure = russia_map
        )
        ]
    ),
    html.Div(
        id='regions_pizza_container_div',
        style={'display': 'none'}  # По умолчанию невидимый
    ),

    html.Div(
        id='output-container_div'
    )

]

# Обработчик кликов по регионам
@app.callback(
    [
        Output('regions_pizza_container_div', 'style'),
        Output('regions_pizza_container_div', 'children'),
        Output('mapka', 'figure')
     ]    ,
    Input('mapka', 'clickData')
)
def display_click_data(clickdata_input):
    if clickdata_input:
        region_name = russia_map.data[clickdata_input['points'][0]['curveNumber']].name
        df = marc4_cls.read_region_pizza(region_name)[0]
        df_years = marc4_cls.read_region_pizza(region_name)[1]
        fig_kv = px.pie(
            df,
            names='Кто2',
            values='Вес, т',
            title=f'{region_name}, период - {max_date_zd}'
        )

        fig = px.bar(
            df_years,
            x='Год',
            y='Вес, т',
            color='Кто',
            barmode='stack',
            hover_data=['Кто2', 'ФО'],
            title=f'{region_name} отгрузки конкурентов'

        )

        zavod_list = df['Кто2'].unique().tolist()

        need_zavods = spravochnik_nsi[spravochnik_nsi['Кто2'].isin(zavod_list)]

        x_lists = need_zavods['x_rez'].unique().tolist()
        y_lists = need_zavods['y_rez'].unique().tolist()

        x_lists[:] = [x for x in x_lists if x != 0]
        y_lists[:] = [x for x in y_lists if x != 0]


        # Добавляем точки заводов
        new_r_map = russia_map
        new_r_map.add_trace(go.Scatter(x=x_lists,
                                        y=y_lists,
                                        # name=r.NL_NAME_1),
                                        mode="markers",  # Только маркер (без линии)
                                        marker=dict(size=12, color="red"),  # Красный маркер большего размера
                                        name="Красная точка"
                                        )
                            )


        # return f'You clicked on: {russia_map.data[clickData_input['points'][0]['curveNumber']].name}'
        return ({'display': 'flex','justifyContent': 'center','alignItems': 'center',},
                [dcc.Graph(figure=fig), dcc.Graph(figure=fig_kv)],
                new_r_map
                )

    return {'display': 'none'}, None, russia_map
