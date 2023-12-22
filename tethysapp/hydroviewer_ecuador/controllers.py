####################################################################################################
##                                   LIBRARIES AND DEPENDENCIES                                   ##
####################################################################################################

# Tethys platform
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from tethys_sdk.routing import controller
from tethys_sdk.gizmos import PlotlyView

# Postgresql
import io
import psycopg2
import pandas as pd
import geopandas as gpd
from sqlalchemy import create_engine
from pandas_geojson import to_geojson

# App settings
from .app import HydroviewerEcuador as app

# App models
from .models.data import *
from .models.plots import *

import requests

####################################################################################################
##                                       STATUS VARIABLES                                         ##
####################################################################################################

# Import enviromental variables 
DB_USER = app.get_custom_setting('DB_USER')
DB_PASS = app.get_custom_setting('DB_PASS')
DB_NAME = app.get_custom_setting('DB_NAME')
APP_NAME = "hydroviewer_ecuador"
APP_URL = APP_NAME.replace("_", "-")

# Generate the conection token
tokencon = "postgresql+psycopg2://{0}:{1}@localhost:5432/{2}".format(DB_USER, DB_PASS, DB_NAME)




####################################################################################################
##                                   CONTROLLERS AND REST APIs                                    ##
####################################################################################################
@controller #(name='home', url=APP_URL)
def home(request):
    context = {
        "server": app.get_custom_setting('SERVER'),
        "app_name": APP_NAME
    }
    return render(request, '{0}/home.html'.format(APP_NAME), context)


@controller(name='get_alerts',url='{0}/get-alerts'.format(APP_URL))
def get_alerts(request):
    # Establish connection to database
    db = create_engine(tokencon)
    conn = db.connect()
    # Query to database
    stations = pd.read_sql("select * from drainage_network where alert != 'R0'", conn);
    conn.close()
    stations = to_geojson(
        df = stations,
        lat = "latitude",
        lon = "longitude",
        properties = ["comid", "latitude", "longitude", "river", "loc0", "loc1", "loc2", "alert"]
    )
    return JsonResponse(stations)


@controller(name='get_alerts_drought',url='{0}/get-alerts-drought'.format(APP_URL))
def get_alerts_drought(request):
    # Establish connection to database
    db = create_engine(tokencon)
    conn = db.connect()
    # Query to database
    stations = pd.read_sql("select * from drainage_network where drought != 'S0'", conn);
    conn.close()
    stations = to_geojson(
        df = stations,
        lat = "latitude",
        lon = "longitude",
        properties = ["comid", "latitude", "longitude", "river", "loc0", "loc1", "loc2", "drought"]
    )
    return JsonResponse(stations)


@controller(name='get_rivers',url='{0}/get-rivers'.format(APP_URL))
def get_rivers(request):
    # Establish connection to database
    db = create_engine(tokencon)
    conn = db.connect()
    # Query to database
    stations = pd.read_sql("select * from drainage_network", conn);
    conn.close()
    stations = to_geojson(
        df = stations,
        lat = "latitude",
        lon = "longitude",
        properties = ["comid", "latitude", "longitude", "river", "loc0", "loc1", "loc2", "alert"]
    )
    return JsonResponse(stations)


@controller(name='get_data',url='{0}/get-data'.format(APP_URL))
def get_data(request):
    # Retrieving GET arguments
    station_comid = request.GET['comid']
    plot_width = float(request.GET['width']) - 12
    plot_width_2 = 0.5 * plot_width
    # Establish connection to database
    db= create_engine(tokencon)
    conn = db.connect()
    # Data series
    simulated_data = get_format_data("select * from r_{0} where datetime < '2022-06-01' and datetime > '1979-01-02';".format(station_comid), conn)
    ensemble_forecast = get_format_data("select * from f_{0};".format(station_comid), conn)
    forecast_records = get_format_data("select * from fr_{0};".format(station_comid), conn)
    ensemble_stats = get_ensemble_stats(ensemble_forecast)
    return_periods = get_return_periods(station_comid, simulated_data)
    # Close conection
    conn.close()
    # Plots and tables
    data_plot = get_historic_simulation(
                                    hist = simulated_data,
                                    rperiods = return_periods,
                                    comid = station_comid)
    daily_average_plot = get_daily_average_plot(
                                    sim = simulated_data,
                                    comid = station_comid)
    monthly_average_plot = get_monthly_average_plot(
                                    sim = simulated_data,
                                    comid = station_comid)
    flow_duration_curve = get_flow_duration_curve(
                                    sim = simulated_data,
                                    comid = station_comid)
    acumulated_volume_plot = get_acumulated_volume_plot(
                                    sim = simulated_data,
                                    comid = station_comid)
    forecast_plot = get_forecast_stats(
                            stats = ensemble_stats,
                            rperiods = return_periods,
                            comid = station_comid,
                            records=forecast_records,
                            sim = simulated_data,)
    forecast_table = get_probabilities_table(
                                    stats = ensemble_stats,
                                    ensem = ensemble_forecast, 
                                    rperiods = return_periods)

    #returning
    context = {
        "data_plot": PlotlyView(data_plot.update_layout(width = plot_width)),
        "daily_average_plot": PlotlyView(daily_average_plot.update_layout(width = plot_width)),
        "monthly_average_plot": PlotlyView(monthly_average_plot.update_layout(width = plot_width)),
        "flow_duration_curve": PlotlyView(flow_duration_curve.update_layout(width = plot_width_2)),
        "acumulated_volume_plot": PlotlyView(acumulated_volume_plot.update_layout(width = plot_width_2)),
        "forecast_plot": PlotlyView(forecast_plot.update_layout(width = plot_width)),
        "forecast_table": forecast_table,
    }
    return render(request, '{0}/panel.html'.format(app.package), context) 


@controller(name='get_raw_forecast_date',url='{0}/get-raw-forecast-date'.format(APP_URL))
def get_raw_forecast_date(request):
    # Retrieving GET arguments
    station_comid = request.GET['comid']
    plot_width = float(request.GET['width']) - 12
    forecast_date = request.GET['fecha']
    # Establish connection to database
    db= create_engine(tokencon)
    conn = db.connect()
    # Data series
    simulated_data = get_format_data("select * from r_{0} where datetime < '2022-06-01 00:00:00';".format(station_comid), conn)
    ensemble_forecast = get_forecast_date(station_comid, forecast_date)
    forecast_records = get_format_data("select * from fr_{0};".format(station_comid), conn)
    #forecast_records = get_forecast_record_date(station_comid, forecast_date)
    ensemble_stats = get_ensemble_stats(ensemble_forecast)
    return_periods = get_return_periods(station_comid, simulated_data)
    # Close conection
    conn.close()
    # Plots and tables
    forecast_plot = get_forecast_stats(
                            stats = ensemble_stats,
                            rperiods = return_periods,
                            comid = station_comid,
                            records = forecast_records,
                            sim = simulated_data)
    forecast_table = get_probabilities_table(
                                    stats = ensemble_stats,
                                    ensem = ensemble_forecast, 
                                    rperiods = return_periods)

    #returning
    context = {
        "forecast_plot": PlotlyView(forecast_plot.update_layout(width = plot_width)),
        "forecast_table": forecast_table,
    }
    return render(request, '{0}/forecast_panel.html'.format(app.package), context)


@controller(name='get_simulated_data_xlsx',url='{0}/get-simulated-data-xlsx'.format(APP_URL))
def get_simulated_data_xlsx(request):
    # Retrieving GET arguments
    station_comid = request.GET['comid'] #9027406
    # Establish connection to database
    db= create_engine(tokencon)
    conn = db.connect()
    # Data series
    simulated_data = get_format_data("select * from r_{0} where datetime < '2022-06-01 00:00:00';;".format(station_comid), conn)
    simulated_data = simulated_data.rename(columns={
                                "streamflow_m^3/s": "Historical simulation (m3/s)"})
    # Crear el archivo Excel
    output = io.BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    simulated_data.to_excel(writer, sheet_name='serie_historica_simulada', index=True)  # Aquí se incluye el índice
    writer.save()
    output.seek(0)
    # Configurar la respuesta HTTP para descargar el archivo
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=serie_historica_simulada.xlsx'
    response.write(output.getvalue())
    return response


@controller(name='get_forecast_xlsx',url='{0}/get-forecast-xlsx'.format(APP_URL))
def get_forecast_xlsx(request):
    # Retrieving GET arguments
    station_comid = request.GET['comid']
    forecast_date = request.GET['fecha']
    # Raw forecast
    ensemble_forecast = get_forecast_date(station_comid, forecast_date)
    ensemble_stats = get_ensemble_stats(ensemble_forecast)
    # Crear el archivo Excel
    output = io.BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    ensemble_stats.to_excel(writer, sheet_name='ensemble_forecast', index=True)  # Aquí se incluye el índice
    writer.save()
    output.seek(0)
    # Configurar la respuesta HTTP para descargar el archivo
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=ensemble_forecast.xlsx'
    response.write(output.getvalue())
    return response




@controller(name='report', url='{0}/report'.format(APP_URL))
def report(request):
    db = create_engine(tokencon)
    conn = db.connect()
    df = pd.read_sql("select * from ffgs_stats;", conn)
    context = {
        "server": app.get_custom_setting('SERVER'),
        "app_name": app.package,
        "pacum_c": df["pacum"][0],
        "pacum_s": df["pacum"][1],
        "pacum_o": df["pacum"][2],
        "asm_c": df["asm"][0],
        "asm_s": df["asm"][1],
        "asm_o": df["asm"][2],
        "ffg_c": df["ffg"][0],
        "ffg_s": df["ffg"][1],
        "ffg_o": df["ffg"][2],
        "fmap24_c": df["fmap24"][0],
        "fmap24_s": df["fmap24"][1],
        "fmap24_o": df["fmap24"][2],
        "ffr24_c": df["ffr24"][0],
        "ffr24_s": df["ffr24"][1],
        "ffr24_o": df["ffr24"][2],
        "prov_c": df["prov"][0],
        "prov_s": df["prov"][1],
        "prov_o": df["prov"][2],
    }
    return render(request, '{0}/report.html'.format(app.package), context)





@controller(name='get_drainage_json', url='{0}/get-drainage-json'.format(APP_URL))
def get_drainage_json(request):
    # Reemplaza 'URL_DEL_GEOJSON' con la URL real de tu archivo GeoJSON
    url_geojson = 'https://geoserver.hydroshare.org/geoserver/HS-77951ba9bcf04ac5bc68ae3be2acfd90/wfs?service=WFS&version=1.0.0&request=GetFeature&typeName=ecuador-geoglows-drainage&outputFormat=application/json'
    try:
        # Descargar el GeoJSON desde la URL
        response = requests.get(url_geojson)
        response.raise_for_status()  # Verificar si la solicitud fue exitosa
        geojson_data = response.json()  # Convertir la respuesta a JSON
        # Devolver el GeoJSON como respuesta JSON
        return JsonResponse(geojson_data, safe=False)
    except requests.exceptions.RequestException as e:
        return JsonResponse({'error': f'Error al obtener el GeoJSON: {str(e)}'}, status=500)
