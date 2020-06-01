import argparse

from matplotlib import pyplot as plt
from plotly import express as px

from dailystats import views
from dailystats.views import pandafunc


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
    state = args.get('state', '')
    county = args.get('county', '')
    views.auto_open = True
    pandafunc(state=state, county=county) if len(state) > 2 else pandafunc(state_abrv=state, county=county)


if __name__ == '__main__':
    main()
