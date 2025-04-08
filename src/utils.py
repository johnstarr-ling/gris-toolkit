import numpy as np 
import pandas as pd 
import re 
import math
import ast 


#########################
# === GENERAL === 
#########################

def pairwise_distance(coordinate1, coordinate2, categorical=False):
    """
    Calculate the pairwise distance between two coordinates. 

    Parameters:
    - coordinate1 (tuple of ints): A coordinate with dimensions (x, y) or (x_cat, y_cat, x, y).
    - coordinate2 (tuple of ints): A coordinate with dimensions (x, y) or (x_cat, y_cat, x, y).

    Returns:
    - float: the Euclidean distance between coordinate1 and coordinate2.
    """

    # Counting only the first two numbers (aka differences in categories)
    if categorical == False:
        return math.dist([coordinate1[-2], coordinate1[-1]], 
                        [coordinate2[-2], coordinate2[-1]]) 
    
    # Counting only the last two numbers (aka positional differences only)
    return math.dist([coordinate1[0], coordinate1[1],
                     [coordinate2[0], coordinate2[1]]])


def compute_action_times(df, participant_col="MD5.hash.of.participant.s.IP.address",
                         item_col="Order.number.of.item"):
    """
    For each trial, compute:
    - the order of events within a trial                (EventIndex)
    - how long it took to complete the current event    (TimeSinceLastEvent)
    - how long the full trial took for this participant (TotalItemTime)

    Note that this function has been optimized with pandas,
    at the cost of some readability. I have added comments where appropriate.

    Parameters:
    - df (pd.DataFrame): Input dataframe.
    - participant_col (str): Name for column that defines participant. 
    - item_col (str): Name for column that defines item.

    Returns:
    - df (pd.DataFrame): Output dataframe with the three statistics mentioned above:
                         (EventIndex, TimeSinceLastEvent, TotalItemTime)
    """
        
    # Required columns.
    required_cols = [
        "MD5.hash.of.participant.s.IP.address", 
        "Order.number.of.item", 
        "EventTime"
    ]

    # Check for required columns.
    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"Missing required column: {col}")

    # Sort data.
    df = df.sort_values(by=[participant_col, item_col, "EventTime"]).reset_index(drop=True)

    # Compute time since last event.
    df['TimeSinceLastEvent'] = df.groupby([participant_col, item_col])['EventTime'].diff().fillna(0)

    # Compute total item time for each group.
    first_event = df.groupby([participant_col, item_col])['EventTime'].transform('first')
    last_event = df.groupby([participant_col, item_col])['EventTime'].transform('last')
    df['TotalItemTime'] = last_event - first_event

    # Create EventIndex within each group.
    df['EventIndex'] = df.groupby([participant_col, item_col]).cumcount()

    # Rename columns to match output format.
    df = df.rename(columns={
        participant_col: "Participant",
        item_col: "Item"
    })

    # Reorder columns: move the new ones to the front.
    reordered_cols = (
        ["Participant", "Item", "EventIndex", "EventTime", "TimeSinceLastEvent", "TotalItemTime"]
        + [col for col in df.columns if col not in {"Participant", "Item", "EventIndex", "EventTime", "TimeSinceLastEvent", "TotalItemTime"}]
    )

    return df[reordered_cols]

def z_score(df, groupby_col = ['Participant'], measure_col='distance'):
    """
    Z-score your measurements by group(s).

    Parameters:
    - df (pd.DataFrame): Input dataframe.
    - groupby_col (list of str): Name(s) of column(s) that delineate groups. 
    - measure_col (str): Name of column with measure that is to be z-scored.

    Returns:
    - df (pd.DataFrame): Output dataframe with the three statistics mentioned above:
                         (EventIndex, TimeSinceLastEvent, TotalItemTime)
    """
    return df.groupby(groupby_col)[measure_col].transform(lambda x: (x - x.mean()) / x.std())



#########################
# === LINE FUNCTIONS === 
#########################

def clean_string(line):
    """
    Fix various formatting complications with the `Final` graphs.

    Parameters:
    - line (str): Value from the `Final` row for a trial.

    Returns:
    - obj_list (list of tuples): Indexable tuples of objects and their locations.
    """

    # Fix comma replacement
    line = line.replace('%2C', ',')

    # Separate objects from one another
    obj_and_location = line.split(';')
    
    # Prepare object-location container
    obj_list = []

    # Go through each object-location pair:
    for obj_location in obj_and_location:
        obj, location = obj_location.split(':')

        # Get the location and evaluate it as a tuple (not a string)
        location = ast.literal_eval(location)

        # Add cleaned item to the object-location container
        obj_list.append(tuple((obj, location)))

    return obj_list


def expand_graphs(df):
    """
    Explode the dataframe (in a good way) by giving
    each object-location pair its own row (to facilitate
    downstream calculations).

    Parameters:
    - df (pd.DataFrame): Input dataframe.

    Returns:
    - output (pd.DataFrame): Output dataframe rows that have been
                             exploded by obj-location values.
    """

    # Graphs are lists of objects and their locations. 
    # Explode this list (but keep the columns). 
    output = df.explode('final_graphs')
    
    # Extract the object into its own column.
    output['object'] = output['final_graphs'].apply(lambda x: x[0])

    # Extract the location into its own column.
    output['location'] = output['final_graphs'].apply(lambda x: x[1])

    return output


def compute_pairwise_distances(df, group_cols, location_col='location', object_col='object',
                               categorical=False):
    """
    Compute pairwise distances between rows within each group using only the last two
    dimensions of the coordinate vectors (as per the custom distance function).

    Given that we are looking at all pairwise distances between all objects,
    this function has been optimized (using numpy) at the cost of some
    readability. I have added comments where appropriate.

    Parameters:
    - df (pd.DataFrame): Input dataframe.
    - group_cols (list of str): Columns to group by.
    - location_col (str): Name of the coordinate column (expects vectors).
    - object_col (str): Name of the object identifier column.
    - categorical (bool): Determining categorical differences (True) or not (False).

    Returns:
    - pd.DataFrame: Compact pairwise comparison results.
    """
    
    # Make copy of df.
    df = df.copy()

    # Prepare results container (a list of dfs).
    all_results = []

    # Begin groupby.
    for _, group in df.groupby(group_cols):
        group = group.reset_index(drop=True)
        
        # Find length of each trial for each participant.
        num_rows = len(group)

        # Edge case (should not be a problem with normal experiments).
        if num_rows < 2:
            continue

        # Extract relevant data
        locations = np.stack(group[location_col].values)

        if categorical == False:
            two_coords = locations[:, -2:]  # Use only last two coordinates for gradient 
        else:
            two_coords = locations[:, :2]   # Use only first two coordinates for categorical

        object_ids = group[object_col].values
        metadata = group.drop(columns=[location_col, object_col])

        # Create pairwise index arrays, without duplicate pairs.
        # (aka: including sent1~sent2, sent2~sent3, sent1~sent3, AND
        #       excluding sent2~sent1, sent3~sent2, etc.)
        idx1 = np.repeat(np.arange(num_rows), num_rows)
        idx2 = np.tile(np.arange(num_rows), num_rows)
        mask = idx1 < idx2

        idx1 = idx1[mask]
        idx2 = idx2[mask]

        # Some GRIS experimenters may only use two-part coordinates, 
        # so this ensures that the proper distances are being calculated.
        coords1 = two_coords[idx1]
        coords2 = two_coords[idx2]

        # Compute Euclidean distance between each coordinate pair.
        deltas = coords1 - coords2
        distances = np.sqrt((deltas ** 2).sum(axis=1))

        # Collect results.
        metadata1 = metadata.iloc[idx1].reset_index(drop=True)
        obj1 = object_ids[idx1]
        obj2 = object_ids[idx2]
        loc2 = group[location_col].iloc[idx2].values

        # Build output dataframe.
        result_df = metadata1.copy()
        result_df[object_col] = obj1
        result_df[f'{object_col}_2'] = obj2
        result_df[f'{location_col}_2'] = loc2
        result_df['distance'] = distances

        # Add results to container.
        all_results.append(result_df)

    return pd.concat(all_results, ignore_index=True)




#########################
# === DRAW FUNCTIONS === 
#########################

# Not yet implemented.