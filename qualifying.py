import os.path
import matplotlib.pyplot as plt
import pandas as pd
from timple.timedelta import strftimedelta
import fastf1
import fastf1.plotting
from fastf1.core import Laps
import data

team_colours = data.team_colours

team_names = data.team_names

def head_to_head():
    dirname = os.path.dirname(__file__)
    fastf1.Cache.enable_cache(f'{dirname}/cache')

    # Set ups plotting
    fastf1.plotting.setup_mpl()

    # Loading session
    session = fastf1.get_session(2022, 'Canadian Grand Prix', 'Q')
    session.load()

    # Lap selection
    ver_lap = session.laps.pick_driver('VER').pick_fastest()
    alo_lap = session.laps.pick_driver('ALO').pick_fastest()

    # Assign telemetry data
    ver_tel = ver_lap.get_car_data().add_distance()
    alo_tel = alo_lap.get_car_data().add_distance()

    # Plot based on team colours
    rbr_color = team_colours[1]
    alp_color = team_colours[0]

    fig, ax = plt.subplots()
    ax.plot(ver_tel['Distance'], ver_tel['Speed'], color=rbr_color, label='VER')
    ax.plot(alo_tel['Distance'], alo_tel['Speed'], color=alp_color, label='ALO')

    ax.set_xlabel('Distance in m')
    ax.set_ylabel('Speed in km/h')

    ax.legend()
    plt.suptitle(f"Fastest Lap Comparison \n "
                 f"{session.event['EventName']} {session.event.year} Qualifying")

    plt.show()

def head_to_head(year, round, driver_one, driver_two, team_one, team_two):
    dirname = os.path.dirname(__file__)
    fastf1.Cache.enable_cache(f'{dirname}/cache')

    # Set ups plotting
    fastf1.plotting.setup_mpl()

    # Loading session
    session = fastf1.get_session(year, round, 'Q')
    session.load()

    # Lap selection
    driver_one_lap = session.laps.pick_driver(driver_one).pick_fastest()
    driver_two_lap = session.laps.pick_driver(driver_two).pick_fastest()

    # Assign telemetry data
    driver_one_tel = driver_one_lap.get_car_data().add_distance()
    driver_two_tel = driver_two_lap.get_car_data().add_distance()

    # Plot based on team colours
    rbr_color = team_colours[1]
    alp_color = team_colours[0]

    fig, ax = plt.subplots()
    ax.plot(driver_one_tel['Distance'], driver_one_tel['Speed'], color=team_colours[team_one], label=driver_one)
    ax.plot(driver_two_tel['Distance'], driver_two_tel['Speed'], color=team_colours[team_two], label=driver_two)

    ax.set_xlabel('Distance in m')
    ax.set_ylabel('Speed in km/h')

    ax.legend()
    plt.suptitle(f"Fastest Lap Comparison \n "
                 f"{session.event['EventName']} {session.event.year} Qualifying")

    plt.show()

def qualifying_results():
    dirname = os.path.dirname(__file__)
    fastf1.Cache.enable_cache(f'{dirname}/cache')

    # Delta set up
    fastf1.plotting.setup_mpl(mpl_timedelta_support=True, color_scheme=None, misc_mpl_mods=False)

    # Sessions set up
    session = fastf1.get_session(2021, 'Spanish Grand Prix', 'Q')
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
    ax.barh(fastest_laps.index, fastest_laps['LapTimeDelta'],
            color=team_colors, edgecolor='grey')
    ax.set_yticks(fastest_laps.index)
    ax.set_yticklabels(fastest_laps['Driver'])

    # Fastest on top, to slowest
    ax.invert_yaxis()


    ax.set_axisbelow(True)
    ax.xaxis.grid(True, which='major', linestyle='--', color='black', zorder=-1000)

    lap_time_string = strftimedelta(pole_lap['LapTime'], '%m:%s.%ms')

    plt.suptitle(f"{session.event['EventName']} {session.event.year} Qualifying\n"
                 f"Fastest Lap: {lap_time_string} ({pole_lap['Driver']})")

    plt.show()


def qualifying_results(year, round):
    dirname = os.path.dirname(__file__)
    fastf1.Cache.enable_cache(f'{dirname}/cache')

    # Delta set up
    fastf1.plotting.setup_mpl(mpl_timedelta_support=True, color_scheme=None, misc_mpl_mods=False)

    # Sessions set up
    session = fastf1.get_session(year, round, 'Q')
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
    ax.barh(fastest_laps.index, fastest_laps['LapTimeDelta'],
            color=team_colors, edgecolor='grey')
    ax.set_yticks(fastest_laps.index)
    ax.set_yticklabels(fastest_laps['Driver'])

    # Fastest on top, to slowest
    ax.invert_yaxis()

    ax.set_axisbelow(True)
    ax.xaxis.grid(True, which='major', linestyle='--', color='black', zorder=-1000)

    lap_time_string = strftimedelta(pole_lap['LapTime'], '%m:%s.%ms')

    plt.suptitle(f"{session.event['EventName']} {session.event.year} Qualifying\n"
                 f"Fastest Lap: {lap_time_string} ({pole_lap['Driver']})")

    plt.show()