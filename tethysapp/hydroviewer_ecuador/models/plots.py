####################################################################################################
##                                   LIBRARIES AND DEPENDENCIES                                   ##
####################################################################################################

# Geoglows
import geoglows
import numpy as np
import math
import hydrostats as hs
import hydrostats.data as hd
import HydroErr as he
import plotly.graph_objs as go
import datetime as dt
import pandas as pd
from plotly.offline import plot as offline_plot


####################################################################################################
##                                      PLOTTING FUNCTIONS                                        ##
####################################################################################################

# Plotting daily averages values
def get_daily_average_plot(sim, comid):
    # Generate the average values
    daily_avg_sim = hd.daily_average(sim)
    # Generate the plots on Ploty
    daily_avg_sim_Q = go.Scatter(x = daily_avg_sim.index, y = daily_avg_sim.iloc[:, 0].values, name = 'Simulated', )
    # PLot Layout
    layout = go.Layout(
        title='Daily average streamflow <br>Reach COMID: {0}'.format(comid),
        xaxis=dict(title='Days', ), 
        yaxis=dict(title='Discharge (m<sup>3</sup>/s)', autorange=True),
        showlegend=False)
    # Generate the output
    chart_obj = go.Figure(data=[daily_avg_sim_Q], layout=layout)
    return(chart_obj)

# Plotting monthly averages values
def get_monthly_average_plot(sim, comid):
    # Generate the average values
    daily_avg_sim = hd.monthly_average(sim)
    # Generate the plots on Ploty
    daily_avg_sim_Q = go.Scatter(x = daily_avg_sim.index, y = daily_avg_sim.iloc[:, 0].values, name = 'Simulated', )
    # PLot Layout
    layout = go.Layout(
        title='Monthly Average Streamflow <br>Reach COMID: {0}'.format(comid),
        xaxis=dict(title='Months', ), 
        yaxis=dict(title='Discharge (m<sup>3</sup>/s)', autorange=True),
        showlegend=False)
    # Generate the output
    chart_obj = go.Figure(data=[daily_avg_sim_Q], layout=layout)
    return(chart_obj)


# Acumulate volume
def get_acumulated_volume_plot(sim, comid):
    # Parse dataframe to array
    sim_array = sim.iloc[:, 0].values * 0.0864
    # Convert from m3/s to Hm3
    sim_volume = sim_array.cumsum()
    # Generate plots
    simulated_volume = go.Scatter(x = sim.index, y = sim_volume, name='Simulated', )
    # Plot layouts
    layout = go.Layout(
                title='Simulated Cumulative Volume <br>{0}'.format(comid),
                xaxis=dict(title='Dates', ), 
                yaxis=dict(title='Volume (Mm<sup>3</sup>)', autorange=True),
                showlegend=False)
    # Integrating the plots
    chart_obj = go.Figure(data=[simulated_volume], layout=layout)
    return(chart_obj)



# Forecast plot
def get_forecast_plot(comid, stats, rperiods, records):
    corrected_stats_df = stats
    corrected_rperiods_df = rperiods
    fixed_records = records
    ##
    hydroviewer_figure = geoglows.plots.forecast_stats(stats=corrected_stats_df, titles={'Reach ID': comid})
    x_vals = (corrected_stats_df.index[0], corrected_stats_df.index[len(corrected_stats_df.index) - 1], corrected_stats_df.index[len(corrected_stats_df.index) - 1], corrected_stats_df.index[0])
    max_visible = max(corrected_stats_df.max())
    ##
    corrected_records_plot = fixed_records.loc[fixed_records.index >= pd.to_datetime(corrected_stats_df.index[0] - dt.timedelta(days=8))]
    corrected_records_plot = corrected_records_plot.loc[corrected_records_plot.index <= pd.to_datetime(corrected_stats_df.index[0] + dt.timedelta(days=2))]
    ##
    if len(corrected_records_plot.index) > 0:
      hydroviewer_figure.add_trace(go.Scatter(
          name='1st days forecasts',
          x=corrected_records_plot.index,
          y=corrected_records_plot.iloc[:, 0].values,
          line=dict(color='#FFA15A',)
      ))
      x_vals = (corrected_records_plot.index[0], corrected_stats_df.index[len(corrected_stats_df.index) - 1], corrected_stats_df.index[len(corrected_stats_df.index) - 1], corrected_records_plot.index[0])
      max_visible = max(max(corrected_records_plot.max()), max_visible)
    ## Getting Return Periods
    r2 = round(corrected_rperiods_df.iloc[0]['return_period_2'], 1)
    ## Colors
    colors = {
        '2 Year': 'rgba(254, 240, 1, .4)',
        '5 Year': 'rgba(253, 154, 1, .4)',
        '10 Year': 'rgba(255, 56, 5, .4)',
        '20 Year': 'rgba(128, 0, 246, .4)',
        '25 Year': 'rgba(255, 0, 0, .4)',
        '50 Year': 'rgba(128, 0, 106, .4)',
        '100 Year': 'rgba(128, 0, 246, .4)',
    }
    ##
    if max_visible > r2:
      visible = True
      hydroviewer_figure.for_each_trace(lambda trace: trace.update(visible=True) if trace.name == "Maximum & Minimum Flow" else (), )
    else:
      visible = 'legendonly'
      hydroviewer_figure.for_each_trace(lambda trace: trace.update(visible=True) if trace.name == "Maximum & Minimum Flow" else (), )
    ##
    def template(name, y, color, fill='toself'):
      return go.Scatter(
          name=name,
          x=x_vals,
          y=y,
          legendgroup='returnperiods',
          fill=fill,
          visible=visible,
          line=dict(color=color, width=0))
    ##
    r5 = round(corrected_rperiods_df.iloc[0]['return_period_5'], 1)
    r10 = round(corrected_rperiods_df.iloc[0]['return_period_10'], 1)
    r25 = round(corrected_rperiods_df.iloc[0]['return_period_25'], 1)
    r50 = round(corrected_rperiods_df.iloc[0]['return_period_50'], 1)
    r100 = round(corrected_rperiods_df.iloc[0]['return_period_100'], 1)
    ##
    hydroviewer_figure.add_trace(template('Return Periods', (r100 * 0.05, r100 * 0.05, r100 * 0.05, r100 * 0.05), 'rgba(0,0,0,0)', fill='none'))
    hydroviewer_figure.add_trace(template(f'2 Year: {r2}', (r2, r2, r5, r5), colors['2 Year']))
    hydroviewer_figure.add_trace(template(f'5 Year: {r5}', (r5, r5, r10, r10), colors['5 Year']))
    hydroviewer_figure.add_trace(template(f'10 Year: {r10}', (r10, r10, r25, r25), colors['10 Year']))
    hydroviewer_figure.add_trace(template(f'25 Year: {r25}', (r25, r25, r50, r50), colors['25 Year']))
    hydroviewer_figure.add_trace(template(f'50 Year: {r50}', (r50, r50, r100, r100), colors['50 Year']))
    hydroviewer_figure.add_trace(template(f'100 Year: {r100}', (r100, r100, max(r100 + r100 * 0.05, max_visible), max(r100 + r100 * 0.05, max_visible)), colors['100 Year']))
    ##
    hydroviewer_figure['layout']['xaxis'].update(autorange=True)
    return(hydroviewer_figure)

