import os.path
import matplotlib.pyplot as plt
import pandas as pd
from timple.timedelta import strftimedelta
import fastf1
import fastf1.plotting
from fastf1.core import Laps
import data

team_colours = data.team_colours

def fastest_lap_practice(year, round, practice_session):
    dirname = os.path.dirname(__file__)
    fastf1.Cache.enable_cache(f'{dirname}/cache')

    # Delta set up
    fastf1.plotting.setup_mpl(mpl_timedelta_support=True, color_scheme=None, misc_mpl_mods=False)

    # Sessions set up
    session = fastf1.get_session(year, round, practice_session)
    session.load()

    # Get array of all drivers
    drivers = pd.unique(session.laps['Driver'])
    print(drivers)

    # Get teams data
    list_fastest_laps = list()
    for drv in drivers:
        drvs_fastest_lap = session.laps.pick_driver(drv).pick_fastest()
        list_fastest_laps.append(drvs_fastest_lap)
    fastest_laps = Laps(list_fastest_laps).sort_values(by='LapTime').reset_index(drop=True)

    # Begin plot
    pole_lap = fastest_laps.pick_fastest()
    fastest_laps['LapTimeDelta'] = fastest_laps['LapTime'] - pole_lap['LapTime']

    print(fastest_laps[['Driver', 'LapTime', 'LapTimeDelta']])

    # Team colours
    team_colors = list()
    for index, lap in fastest_laps.iterlaps():
        color = fastf1.plotting.team_color(lap['Team'])
        team_colors.append(color)

    # Data plotting
    fig, ax = plt.subplots()
    ax.barh(fastest_laps.index, fastest_laps['LapTimeDelta'], color=team_colors, edgecolor='grey')
    ax.set_yticks(fastest_laps.index)
    ax.set_yticklabels(fastest_laps['Driver'])

    # Fastest on top, to slowest
    ax.invert_yaxis()

    ax.set_axisbelow(True)
    ax.xaxis.grid(True, which='major', linestyle='--', color='black', zorder=-1000)

    lap_time_string = strftimedelta(pole_lap['LapTime'], '%m:%s.%ms')

    plt.suptitle(f"{session.event['EventName']} {session.event.year} {practice_session}\n"
                 f"Fastest Lap: {lap_time_string} ({pole_lap['Driver']})")

    plt.show()

def driver_pace(year, round, practice_session, driver, team):
    dirname = os.path.dirname(__file__)
    fastf1.Cache.enable_cache(f'{dirname}/cache')

    # Delta set up
    fastf1.plotting.setup_mpl()

    # Sessions set up
    session = fastf1.get_session(year, round, practice_session)
    session.load()

    laps = session.laps.pick_driver(driver)
    print(laps['LapNumber'])

    fig, ax = plt.subplots()
    ax.plot(laps['LapNumber'], laps['LapTime'], color=team_colours[team], label=driver)
    ax.set_xlabel('Lap Number')
    ax.set_ylabel('Lap Time')

    ax.legend()
    plt.suptitle(f"Lap Times\n "
                 f"{session.event['EventName']} {session.event.year} Race Pace")

    plt.show()