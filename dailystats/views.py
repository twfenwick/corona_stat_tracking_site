import os
import logging
import string
import datetime

from django.shortcuts import render
import plotly.graph_objects as go
import plotly.io as pio
import pandas

from corona_stat_tracking_site.states import STATE_NAMES, STATE_ABRV

logger = logging.getLogger('covidtrack')
logging.getLogger()
# yaxis_type = 'log'
# yaxis_type = 'linear'
auto_open = False
path_counties = ''
path_states = ''
path_us = ''


"""
When I enter county and state
Then I see a trend chart of the county infection rate

When I enter a state
Then I see a trend chart of the state infection rate 
"""


def index(request):
    """Render states list. Each has county expand menu"""
    return counties(request)


def states(request, state_abrv: str):
    return counties(request, state_abrv=state_abrv.upper(), county='')
    # logger.info(f'Render: {STATES.get(state_abrv)}')
    # return render(request, f'dailystats/{state_abrv.upper()}.html', {'empty': 'entry'})


def counties(request, state_abrv: str = '', county: str = ''):
    if 'LOG' in state_abrv.upper():
        yaxis_type = 'log'
        state_abrv = state_abrv.replace('log', '').replace('LOG', '')
    else:
        yaxis_type = 'linear'
    title, filename, html = pandafunc(state_abrv=state_abrv, county=county, yaxis_type=yaxis_type)
    logger.info(f'Render: "{title}" from file "{filename}".')
    return render(request, f'dailystats/{filename}', {'html': html})


def pandafunc(state='', county='', state_abrv='', yaxis_type='linear'):
    pull_latest_corona_data()
    # Get state name by abbreviation, get state abbreviation by name
    state = STATE_NAMES.get(state_abrv.upper(), '') if state_abrv and not state else state
    state_abrv = STATE_ABRV.get(state, '') if state and not state_abrv else state_abrv
    county = string.capwords(county) if county else county
    match = [state, county]

    if county:
        path = path_counties
    elif state:
        path = path_states
    else:
        path = path_us
    live_path = path.replace('covid-19-data', 'covid-19-data/live')

    # Add live update to historice
    df = pandas.read_csv(path)
    df_live = pandas.read_csv(live_path, header=0)
    df = pandas.concat([df, df_live])

    # If state is given, filter data from either county or state data, else it's assumed US data since state not given.
    df = df[df['state'].isin(match)] if state else df
    if county and state:
        df = df[df['county'].isin(match)]
        title = f'{county} County, {state}'
    elif state:
        title = state
    else:
        title = 'United States'

    # Get daily diffs for new case calcs
    new_cases = df['cases'].diff()
    new_deaths = df['deaths'].diff()

    # Generate the plot
    fig = create_plot_overlays(df, title, new_cases, new_deaths, yaxis_type)

    filename = f'{state_abrv.upper()}{county}.html' if state and df['date'].size else 'US.html'
    plot_path = f'{os.getcwd()}/dailystats/templates/dailystats/{filename}'

    pio.write_html(fig, file=plot_path, auto_open=auto_open)
    if not auto_open:
        with open(plot_path, 'w') as f:
            f.write('{% extends \'dailystats/base.html\' %}'
                    '{% block main_content %}'
                    '{{ html|safe }}'
                    '{% endblock %}')

    html = pio.to_html(fig)
    return title, filename, html


def pull_latest_corona_data():
    # Clone repo if doesn't exist
    logger.debug(f'current dir: {os.getcwd()}')

    if not os.path.exists(f'{os.getcwd()}/covid-19-data'):
        os.system('git clone https://github.com/nytimes/covid-19-data.git')

    os.chdir('covid-19-data')

    global path_counties
    global path_states
    global path_us

    path_counties = f'{os.getcwd()}/us-counties.csv'
    path_states = f'{os.getcwd()}/us-states.csv'
    path_us = f'{os.getcwd()}/us.csv'

    logger.debug(f'counties path: {path_counties}')
    logger.debug(f'states path: {path_states}')
    logger.debug(f'us path: {path_us}')

    # TODO: Fix update repo if not fetched latest
    status = os.system('git status')
    if 'Your branch is up to date' not in str(status):
        # print(str(status)) ...actually returns 0
        os.system('git pull origin master')
    else:
        logger.info('Skipping pull, already up to date.')
    os.chdir('..')
    logger.debug(f'current dir: {os.getcwd()}')
    date = os.environ.get('DATESTORE', 'Not set')
    today = datetime.datetime.now().date()
    if date is not today:
        os.environ['DATESTORE'] = str(today)


def create_plot_overlays(df, title, new_cases, new_deaths, yaxis_type):
    # Browser group plots:
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df['date'],
        y=df['cases'],
        name='Total Cases',
        marker_color='sandybrown'
    ))
    fig.add_trace(go.Bar(
        x=df['date'],
        y=new_cases,
        name='New Cases',
        marker_color='indianred'
    ))
    fig.add_trace(go.Bar(
        x=df['date'],
        y=df['deaths'],
        name='Deaths',
        marker_color='black'
    ))
    fig.add_trace(go.Bar(
        x=df['date'],
        y=new_deaths,
        name='New Deaths',
        marker_color='gray'
    ))
    # Here we modify the tickangle of the xaxis, resulting in rotated labels.
    fig.update_layout(title=title, barmode='overlay', xaxis_tickangle=-45, yaxis_type=yaxis_type)
    return fig
