import os.path

import matplotlib.pyplot as plt
import pandas as pd
from timple.timedelta import strftimedelta
import fastf1
import fastf1.plotting
from fastf1.core import Laps
import data

team_colours = data.team_colours

def fastest_race_laps(year, round):
    dirname = os.path.dirname(__file__)
    fastf1.Cache.enable_cache(f'{dirname}/cache')

    # Delta set up
    fastf1.plotting.setup_mpl(mpl_timedelta_support=True, color_scheme=None, misc_mpl_mods=False)

    # Sessions set up
    session = fastf1.get_session(year, round, 'R')
    session.load()

    # Get array of all drivers
    drivers = pd.unique(session.laps['Driver'])
    print(drivers)

    # Get teams data
    list_fastest_laps = list()
    for drv in drivers:
        if (session.laps.pick_driver(drv).pick_fastest()['LapTime'] == "NaT"):
            break
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

    plt.suptitle(f"{session.event['EventName']} {session.event.year} Race\n"
                 f"Fastest Lap: {lap_time_string} ({pole_lap['Driver']})")

    plt.show()

def average_race_pace(year, round):
    dirname = os.path.dirname(__file__)
    fastf1.Cache.enable_cache(f'{dirname}/cache')

    # Delta set up
    fastf1.plotting.setup_mpl(mpl_timedelta_support=True, color_scheme=None, misc_mpl_mods=False)

    # Sessions set up
    session = fastf1.get_session(year, round, 'R')
    session.load()

    # Get array of all drivers
    drivers = pd.unique(session.laps['Driver'])
    print(drivers)

    # Get teams data
    list_laps = list()
    average_laps = list()
    for drv in drivers:
        average_pace = 0
        drvs_laps = session.laps.pick_driver(drv).pick_accurate()
        list_laps.append(drvs_laps)
        for i in range (len(drvs_laps['LapNumber'])):
            average_pace = average_pace + drvs_laps
        average_pace / len(drvs_laps['LapNumber'])
        average_laps.append(average_pace)
    #print(list_laps)
    print(average_laps)


def driver_pace(year, round, driver, team):
    dirname = os.path.dirname(__file__)
    fastf1.Cache.enable_cache(f'{dirname}/cache')

    # Delta set up
    fastf1.plotting.setup_mpl()

    # Sessions set up
    session = fastf1.get_session(year, round, 'R')
    session.load()

    laps = session.laps.pick_driver(driver).pick_accurate()

    fig, ax = plt.subplots()
    ax.plot(laps['LapNumber'], laps['LapTime'], color=team_colours[team], label=driver)
    ax.set_xlabel('Lap Number')
    ax.set_ylabel('Lap Time')

    ax.legend()
    plt.suptitle(f"Lap Times\n "
                 f"{session.event['EventName']} {session.event.year} Race Pace")

    plt.show()

def pace_head_to_head(year, round, driver_one, driver_two, team_one, team_two):
    dirname = os.path.dirname(__file__)
    fastf1.Cache.enable_cache(f'{dirname}/cache')

    # Delta set up
    fastf1.plotting.setup_mpl()

    # Sessions set up
    session = fastf1.get_session(year, round, 'R')
    session.load()

    driver_one_laps = session.laps.pick_driver(driver_one).pick_accurate()
    driver_two_laps = session.laps.pick_driver(driver_two).pick_accurate()

    fig, ax = plt.subplots()
    ax.plot(driver_one_laps['LapNumber'], driver_one_laps['LapTime'], color=team_colours[team_one], label=driver_one)
    ax.plot(driver_two_laps['LapNumber'], driver_two_laps['LapTime'], color=team_colours[team_two], label=driver_two)
    ax.set_xlabel('Lap Number')
    ax.set_ylabel('Lap Time')

    ax.legend()
    plt.suptitle(f"Lap Times\n "
                 f"{session.event['EventName']} {session.event.year} Race Pace")

    plt.show()