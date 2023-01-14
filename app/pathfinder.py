import psycopg2

from dbaccess import DbAccess

# class PathFinder:

#     def __init__(self) -> None:
#         pass


def find_path(cursor, starting_point, places, starting_time,  transport):
    pass
    print("find_path")

    print(starting_point)
    print(places)
    print(starting_time)
    print(transport)

    # cursor.execute("SELECT * FROM closest_points({long}, {lat})".format(long=starting_point["lng"], lat=starting_point["lat"]))
    # point_id, = cursor.fetchone()
    
    # point_id, = DbAccess.get_closest_point(starting_point["lng"], starting_point["lat"])
    closest_points_ids = _get_closest_point_ids(starting_point, places)
    
    # print(closest_points_ids)

    paths = _get_paths(closest_points_ids)

    # print(f"paths: {paths}")

    costs = _extract_costs(paths)

    print(costs)

def _get_closest_point_ids(starting_point, places):
    points = [starting_point] + [{'lat': place["lat"], 'lng': place["lng"]} for place in places]

    closest_pids = []

    for point in points:
        pid, = DbAccess.get_closest_point(point["lng"], point["lat"])
        closest_pids.append(pid)

    return closest_pids

def _get_paths(pids):
    paths = []

    for source in pids:
        for target in [pid for pid in pids if pid != source]:
            result = DbAccess.get_shortest_path(source, target)
            paths.append(result)
    
    return paths

def _extract_costs(paths):
    # returns list of dictionaries 
    # source target 
    costs = [{"source": path[0][2], "target": path[-1][2], "cost": path[-1][5]} for path in paths]

    return costs