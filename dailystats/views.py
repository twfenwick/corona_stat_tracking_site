import os
import logging
import argparse

from django.shortcuts import render
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.io as pio
import pandas

from corona_stat_tracking_site.states import STATES

logger = logging.getLogger('covidtrack')
logging.getLogger()
# yaxis_type = 'log'
yaxis_type = 'linear'
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
    pandafunc()
    logger.info(f'Render: US stats')
    return render(request, 'dailystats/US.html', {'empty': 'entry'})


def states(request, state_abrv: str):
    return counties(request, state_abrv=state_abrv.upper(), county='')
    # logger.info(f'Render: {STATES.get(state_abrv)}')
    # return render(request, f'dailystats/{state_abrv.upper()}.html', {'empty': 'entry'})


def counties(request, state_abrv: str, county: str):
    state_abrv = state_abrv.upper()
    county = county.capitalize()
    # global yaxis_type
    # if 'LOG' in state_abrv.upper():
    #     yaxis_type = 'log'
    #     state_abrv = state_abrv.replace('log', '').replace('LOG', '')
    # else:
    #     yaxis_type = 'linear'
    pandafunc(state_abrv=state_abrv, county=county)
    countytxt = f'{county}, ' if county else ''
    logger.info(f'Render: {countytxt}{STATES.get(state_abrv)}')
    return render(request, f'dailystats/{state_abrv}{county}.html', {'empty': 'entry'})


def pandafunc(state=None, county='', state_abrv=None):
    state = STATES.get(state_abrv.upper()) if state_abrv else state
    county = county.capitalize() if county else county
    pull_latest_corona_data()
    match = [state, county]
    path = path_counties if county else path_states
    df = pandas.read_csv(path)

    df = df[df['state'].isin(match)] if state else pandas.read_csv(path_us)
    if county:
        df = df[df['county'].isin(match)]
        title = f'{county} County, {state}'
        local_plot = f'plots/{state}/{county}'
    elif state:
        title = state
        local_plot = f'plots/{state}'
    else:
        title = 'United States'

    new_cases = df['cases'].diff()
    new_deaths = df['deaths'].diff()

    fig = create_plot_overlays(df, title, new_cases, new_deaths, yaxis_type)

    # local_plot = local_plot.replace(' ', '')
    filename = f'{state_abrv.upper()}{county}' if state else 'US'
    local_plot = f'{os.getcwd()}/dailystats/templates/dailystats/{filename}.html'
    os.remove(local_plot) if os.path.exists(local_plot) else None
    file_path = f'{local_plot}'
    pio.write_html(fig, file=file_path, auto_open=False)
    # # plot = pio.to_html(fig)
    #
    # return file_path

    # import chart_studio.tools as tls
    # tls.get_embed('file:///Users/tim/code/bitbucket/twfenwick/corona_tracker/index.html')


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


# ****************** Command line and local runs ****************** #


parser = argparse.ArgumentParser(description='Show trend of infection rate per state or county.')


def basic_local_plot(count, df, logy, title):
    # Local plots:
    df.plot(logy=logy, kind='bar', x='date', y=count, grid=True, title=title)
    plt.show()
    plt.close()


def basic_browser_plot(count, df, logy, title):
    # Browser plots:
    fig = px.bar(df, x='date', y=count, title=title, log_y=logy, barmode='overlaid')
    fig.show()


def parse_args():
    parser.add_argument('-s', '--state', help='Required for any query.', required=True)
    parser.add_argument('-c', '--county', help='Optional for specific county per state.')
    parser.add_argument('-q', '--quiet', help='Quiet mode: generate plots in html, don\'t show', action='store_true')
    args = vars(parser.parse_args())
    return args


def main():
    args = parse_args()
    pull_latest_corona_data()
    pandafunc(args['state'], args['county'])


if __name__ == '__main__':
    main()
