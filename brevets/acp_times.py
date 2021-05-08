"""
Open and close time calculations
for ACP-sanctioned brevets
following rules described at https://rusa.org/octime_alg.html
and https://rusa.org/pages/rulesForRiders
"""
import arrow, datetime


#  You MUST provide the following two functions
#  with these signatures. You must keep
#  these signatures even if you don't use all the
#  same arguments.
#

control_min_speed = {"0-600": 15, "600-1000": 11.428, "1000-1300": 13.333}
control_max_speed = {"0-200": 34, "200-400": 32, "400-600": 30, "600-1000": 28, "1000-1300": 26}
set_time_limit = {200: 13.5, 300: 20, 400: 27, 600: 40}

def open_time(control_dist_km, brevet_dist_km, brevet_start_time):
    """
    Args:
       control_dist_km:  number, control distance in kilometers
       brevet_dist_km: number, nominal distance of the brevet
           in kilometers, which must be one of 200, 300, 400, 600,
           or 1000 (the only official ACP brevet distances)
       brevet_start_time:  A date object (arrow)
    Returns:
       A date object indicating the control open time.
       This will be in the same time zone as the brevet start time.
    """
    time = 0

    if control_dist_km > brevet_dist_km:
        control_dist_km = brevet_dist_km

    for control_dist_range in control_max_speed:
        max_speed = control_max_speed[control_dist_range]
        low_dist, high_dist = list(map(int, control_dist_range.split("-")))
        if low_dist <= control_dist_km <= high_dist:
            time += (control_dist_km - low_dist) / max_speed
            break
        if control_dist_km > high_dist:
            time += high_dist / max_speed

    hour, minute = divmod(time, 1)
    minute = round(minute * 60)
    return brevet_start_time.shift(hours=hour, minutes=minute)


def close_time(control_dist_km, brevet_dist_km, brevet_start_time):
    """
    Args:
       control_dist_km:  number, control distance in kilometers
       brevet_dist_km: number, nominal distance of the brevet
          in kilometers, which must be one of 200, 300, 400, 600, or 1000
          (the only official ACP brevet distances)
       brevet_start_time:  A date object (arrow)
    Returns:
       A date object indicating the control close time.
       This will be in the same time zone as the brevet start time.
    """
    assert control_dist_km >= 0

    time = 0

    # Case: When the control distance is greater than equal to the brevet distance
    if control_dist_km >= brevet_dist_km:
        time = set_time_limit[brevet_dist_km]
    # Oddities
    elif control_dist_km <= 60:
        time += (control_dist_km / 20) + 1
    else:
        for control_dist_range in control_min_speed:
            min_speed = control_min_speed[control_dist_range]
            low_dist, high_dist = list(map(int, control_dist_range.split("-")))
            if low_dist <= control_dist_km <= high_dist:
                time += (control_dist_km - low_dist) / min_speed
                break
            if control_dist_km > high_dist:
                time += high_dist / min_speed

    hour, minute = divmod(time, 1)
    minute = round(minute * 60)
    return brevet_start_time.shift(hours=hour, minutes=minute)


