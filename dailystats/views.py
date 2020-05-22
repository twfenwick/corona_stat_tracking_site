import os

from django.shortcuts import render
from django.template.loaders.app_directories import Loader

import plotly.graph_objects as go
import matplotlib.pyplot as plt
import plotly.express as px
import pandas


def index(request):
    # return HttpResponse("Hello, world. You're at the polls indexaaa.")
    # pandafunc('North Carolina', 'Orange')
    # pandafunc('District of Columbia')
    # pandafunc('Florida')
    # pandafunc('South Carolina')
    # pandafunc('Alaska')
    # pandafunc('Utah')
    # pandafunc('New York')
    pandafunc('Texas')
    return render(request, 'dailystats/index.html', {'empty': 'entry'})


def pandamix(request):
    # file_path = pandafunc('District of Columbia')
    # file_path = pandafunc('Florida')
    # file_path = pandafunc('South Carolina')
    # file_path = pandafunc('Alaska')
    # file_path = pandafunc('New York')
    # file_path = pandafunc('North Carolina')

    return render(request, 'dailystats/index.html')


import argparse


path_counties = '/Users/tim/code/github/nytimes/covid-19-data/us-counties.csv'
path_states = '/Users/tim/code/github/nytimes/covid-19-data/us-states.csv'

# yaxis_type = 'log'
yaxis_type = 'linear'

"""
When I enter county and state
Then I see a trend chart of the county infection rate

When I enter a state
Then I see a trend chart of the state infection rate 
"""


def pandafunc(state='North Carolina', county=None):
    pull_latest_corona_data()
    match = [state, county]
    path = path_counties if county else path_states
    df = pandas.read_csv(path)

    df = df[df['state'].isin(match)]
    if county:
        df = df[df['county'].isin(match)]
        title = f'{county} County, {state}'
        local_plot = f'plots/{state}/{county}'
    else:
        title = state
        local_plot = f'plots/{state}'

    new_cases = df['cases'].diff()
    new_deaths = df['deaths'].diff()

    fig = create_plot_overlays(df, title, new_cases, new_deaths, yaxis_type)

    import plotly.io as pio
    # local_plot = local_plot.replace(' ', '')
    local_plot = f'{os.getcwd()}/dailystats/templates/dailystats/index.html'

    # # ldr = Loader(engine='')
    # # print(Loader.get_dirs(ldr))
    # # template_path = Loader.get_dirs(ldr)[0]
    # # deep_path = f'{template_path}/{local_plot}'
    # print(local_plot)
    #
    # # if not os.path.exists(local_plot):
    # #     os.makedirs(local_plot)
    #
    # # Repo not updated:
    # #  pull_latest_corona_data()
    # #  write the file
    # # Repo is current but file doesn't exist:
    # #  write the file
    #
    file_path = f'{local_plot}'
    pio.write_html(fig, file=file_path, auto_open=False)
    # # plot = pio.to_html(fig)
    #
    # return file_path

    # import chart_studio.tools as tls
    # tls.get_embed('file:///Users/tim/code/bitbucket/twfenwick/corona_tracker/index.html')

    # basic_browser_plot(count, df, logy, title)

    # basic_local_plot(count, df, logy, title)


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


def basic_local_plot(count, df, logy, title):
    # Local plots:
    df.plot(logy=logy, kind='bar', x='date', y=count, grid=True, title=title)
    plt.show()
    plt.close()


def basic_browser_plot(count, df, logy, title):
    # Browser plots:
    fig = px.bar(df, x='date', y=count, title=title, log_y=logy, barmode='overlaid')
    fig.show()


def main():
    args = parse_args()
    pull_latest_corona_data()
    pandafunc(args['state'], args['county'])


parser = argparse.ArgumentParser(description='Show trend of infection rate per state or county.')


def parse_args():
    parser.add_argument('-s', '--state', help='Required for any query.', required=True)
    parser.add_argument('-c', '--county', help='Optional for specific county per state.')
    parser.add_argument('-q', '--quiet', help='Quiet mode: generate plots in html, don\'t show', action='store_true')
    args = vars(parser.parse_args())
    return args


def pull_latest_corona_data():
    # TODO: Clone repo if doesn't exist
    # TODO: Update repo if not fetched latest
    os.system('cd /Users/tim/code/github/nytimes/covid-19-data; pwd; git pull origin master')


if __name__ == '__main__':
    main()
