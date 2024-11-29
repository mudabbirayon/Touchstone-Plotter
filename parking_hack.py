import numpy as np
import random

#
#map format: [{"coord_x": 1,"coord_y": 1,"is_parking_slot":true, "is_free": true, "is_obstacle": false},..........]

def generate_2d_map(dimensions, custom_data):
    """
    Generates a 2D map as a list of dictionaries.

    Args:
        dimensions (tuple): Dimensions of the map as (rows, columns).
        custom_data (list of lists): List of lists, where each sublist contains:
            [x_coordinate, y_coordinate, is_parking_slot, is_free, is_obstacle].

    Returns:
        list of dict: A list of dictionaries representing the 2D map.
    """
    rows, columns = dimensions
    
    # Initialize the map with all boolean values set to False
    map_data = [
        {
            "x_coordinate": x,
            "y_coordinate": y,
            "is_parking_slot": False,
            "is_free": True,
            "is_obstacle": False
        }
        for x in range(0, rows)
        for y in range(0, columns)
    ]

    # Update the map with the custom data provided
    for entry in custom_data:
        x, y, is_parking_slot, is_free, is_obstacle = entry

        # Find the corresponding dictionary in the map_data
        for slot in map_data:
            if slot["x_coordinate"] == x and slot["y_coordinate"] == y:
                slot["is_parking_slot"] = is_parking_slot
                slot["is_free"] = is_free
                slot["is_obstacle"] = is_obstacle

    print(map_data)
    return map_data

def find_spot(starting_coord,map):
    
    distance = np.inf
    map_size = len(map)
    distances_from_start = np.ones((map_size,map_size)) * np.inf
    
    obstacle_map = np.zeros((map_size,map_size))
    restricted_points = [point for point in map if (not point["is_free"] or point['is_obstacle']) ]
    accessible_coords = [[point['x_coordinate'],point['y_coordinate']] for point in map if (point['is_parking_slot'] and point['is_free']) ]
    found = False
    for point in restricted_points:
        obstacle_map[point['x_coordinate']][point['y_coordinate']] = 1
    

    distances_from_start[starting_coord[0]][starting_coord[1]] = 0
    obstacle_map[starting_coord[0]][starting_coord[1]] = 5
    
    while True:
            obstacle_map[starting_coord[0]][starting_coord[1]] = 5
            min_dist = np.min(distances_from_start)
            current = np.unravel_index(np.argmin(distances_from_start, axis=None), distances_from_start.shape)

            if (list(current) in accessible_coords):
                distance = abs(current[0]-starting_coord[0]) + abs(current[1]-starting_coord[1])
                found = True
                break
            elif min_dist > (map_size**4):
                break
            obstacle_map[current] = 2
            
            distances_from_start[current] = np.inf
            A=[-1,1,0,0]
            B=[0,0,-1,1]
            

            for i in range(4):
                if (current[0]+A[i]>=0) and (current[0]+A[i]<map_size) and (current[1]+B[i]>=0) and (current[1]+B[i]<map_size):
                    if (obstacle_map[current[0]+A[i]][current[1]+B[i]] == 0):
                        distances_from_start[current[0]+A[i]][current[1]+B[i]] = min_dist+1
                        obstacle_map[current[0]+A[i]][current[1]+B[i]] = 3
            
    if found:
         print("Nearest Accessible Slot at: ", current,"\n",distance, "units away from you")
         print(list(current),starting_coord)
         return {'destination':list(current), 'current_loc':starting_coord}
    else:
         print("Very Sad.... No available slots :(")
         return {'destination':starting_coord, 'current_loc':starting_coord}

import matplotlib.pyplot as plt
import numpy as np

def visualize_2d_map(map_data, dimensions, strt_end):
    """
    Visualizes a 2D map with specific colors:
    - Black for obstacles
    - Green for free parking slots
    - Red for occupied parking slots
    - Grey for empty spaces

    Args:
        map_data (list of dict): List of dictionaries representing the map.
        dimensions (tuple): Dimensions of the map as (rows, columns).
    """
    rows, cols = dimensions
    grid = np.zeros((rows, cols))

    # Map the data to grid values
    for cell in map_data:
        x = cell["x_coordinate"]
        y = cell["y_coordinate"]
        if cell["is_obstacle"]:
            grid[x, y] = 3  # Obstacles
        elif cell["is_parking_slot"] and cell["is_free"]:
            grid[x, y] = 1  # Free parking slots
        elif cell["is_parking_slot"] and not cell["is_free"]:
            grid[x, y] = 2  # Occupied parking slots

        if [x,y] == strt_end['current_loc']:
            grid[x,y] = 5

        if [x,y] == strt_end['destination']:
            grid[x,y] = 4
            print('here')
            

        
            
        
         

    # Define colors
    cmap = plt.cm.get_cmap("tab20c", 6)
    colors = ["grey", "green", "red", "black","blue","yellow"]
    custom_cmap = plt.matplotlib.colors.ListedColormap(colors)

    plt.figure(figsize=(cols, rows))
    plt.imshow(grid, cmap=custom_cmap, origin="upper")

    # Add gridlines
    ax = plt.gca()
    ax.set_xticks(np.arange(-0.5, cols, 1), minor=True)
    ax.set_yticks(np.arange(-0.5, rows, 1), minor=True)
    ax.grid(which='minor', color='white', linestyle='-', linewidth=2)
    ax.tick_params(which='minor', bottom=False, left=False)

    # Add color legend
    cbar = plt.colorbar(ticks=[0,0.9,1.8,2.7, 3.6,4.5])
    cbar.ax.set_yticklabels(['Empty', 'Free Parking', 'Occupied Parking', 'Obstacle','Destination','Starting point'])

    # Add axis labels
    plt.xticks(range(cols), range(0, cols))
    plt.yticks(range(rows), range(0, rows))
    plt.xlabel("X Coordinate")
    plt.ylabel("Y Coordinate")
    plt.title("2D Map Visualization")
    plt.show()
         
dimensions = (10, 10)
custom_data = [
    [i, j, True, True, False] for i in range(7,10) for j in range(7,10)
]

for i in range(0,4):
    for j in range(0,4):
        custom_data.append([i, j, True, True, False])

for i in range(0,4):
    for j in range(7,10):
        custom_data.append([i, j, True, True, False])

for i in range(7,10):
    for j in range(0,4):
        custom_data.append([i, j, True, True, False])

# #########################################################################################################
# for i in range(4,6):
#     for j in range(3,5):
#         custom_data.append([i, j, False, False, True])
# for i in range(3,6):
#     for j in range(4,7):
#         custom_data.append([i, j, False, False, True])

# ####################################################################################################################

# for i in range(0,4):
#     for j in range(2,4):
#         custom_data.append([i, j, True, False, False])

# for i in range(7,10):
#     for j in range(2,4):
#         custom_data.append([i, j, True, False, False])

# for i in range(2,4):
#     for j in range(7,9):
#         custom_data.append([i, j, True, False, False])

# for i in range(7,10):
#     for j in range(7,9):
#         custom_data.append([i, j, True, False, False])


#######################################################################################################################

# custom_data = []
# for i in range(3,8):
#     for j in range(3,8):
#         custom_data.append([i, j, True, False, False])

# for i in range(4,6):
#     for j in range(4,6):
#         custom_data.append([i, j, True, True, False])
#####################################################################################################################
#custom_data = [[9,9,True,True,False]]
####################################################################################################################

#custom_data = [[i, j, False, False, False] for i in range(7,10) for j in range(7,10)]


map_result = generate_2d_map(dimensions, custom_data)




x = find_spot([1,1],map_result)
visualize_2d_map(map_result, dimensions, x)

                        