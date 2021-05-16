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
set_time_limit = {200: 13.5, 300: 20, 400: 27, 600: 40, 1000: 75, 1200: 90, 1400: 116.4, 2200: 220}

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
    assert (control_dist_km >= 0) and (control_dist_km <= brevet_dist_km * 1.2)

    time = 0

    # When the control distance is greater than the brevet distance,
    # need to set the control distance to brevet distance by the rule.
    if control_dist_km > brevet_dist_km:
        control_dist_km = brevet_dist_km

    # Iterate through each control location range
    for control_dist_range in control_max_speed:
        # Get the maximum speed corresponding to the control location range
        max_speed = control_max_speed[control_dist_range]
        # Get the lowest and highest bound of the control location range
        low_dist, high_dist = list(map(int, control_dist_range.split("-")))
        # Case 1: When control distance is within the control location range
        if low_dist <= control_dist_km <= high_dist:
            # Since time for the lowest bound of the control location range is already added
            # on Case 2, add time for the difference between lowest bound and control distance
            time += (control_dist_km - low_dist) / max_speed
            break
        # Case 2: When control distance is bigger than the highest bound of the control location range
        if control_dist_km > high_dist:
            # Add time based on the range of the control location
            time += (high_dist - low_dist) / max_speed

    # Convert the time in decimal into the format in minutes and hours
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
    assert (control_dist_km >= 0) and (control_dist_km <= brevet_dist_km * 1.2)

    time = 0

    # When the control distance is greater than equal to the brevet distance,
    # need to set the time to the set time limits by the rule.
    if control_dist_km >= brevet_dist_km:
        time = set_time_limit[brevet_dist_km]
    # Oddities (When the control distance is less than or equal to 60 km)
    elif control_dist_km <= 60:
        time += (control_dist_km / 20) + 1
    else:
        # Iterate through each control location range
        for control_dist_range in control_min_speed:
            # Get the minimum speed corresponding to the control location range
            min_speed = control_min_speed[control_dist_range]
            # Get the lowest and highest bound of the control location range
            low_dist, high_dist = list(map(int, control_dist_range.split("-")))
            # Case 1: When control distance is within the control location range
            if low_dist <= control_dist_km <= high_dist:
                # Since time for the lowest bound of the control location range is already added
                # on Case 2, add time for the difference between lowest bound and control distance
                time += (control_dist_km - low_dist) / min_speed
                break
            # Case 2: When control distance is bigger than the highest bound of the control location range
            if control_dist_km > high_dist:
                # Add time based on the range of the control location
                time += (high_dist - low_dist) / min_speed

    # Convert the time in decimal into the format in minutes and hours
    hour, minute = divmod(time, 1)
    minute = round(minute * 60)
    return brevet_start_time.shift(hours=hour, minutes=minute)

if __name__ == '__main__':
    a = open_time(570, 600, arrow.get("2018-11-17T06:00"))
    print(a)