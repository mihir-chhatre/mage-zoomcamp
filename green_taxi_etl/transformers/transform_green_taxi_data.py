import re
import pandas as pd

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


def camel_to_snake(name):
    """
    Convert a string from CamelCase to snake_case.
    """
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

@transformer
def transform(data, *args, **kwargs):
    # Rename columns from Camel Case to Snake Case
    data.columns = [camel_to_snake(column) for column in data.columns]

    # Convert lpep_pickup_datetime to datetime and create a new column for the date
    data['lpep_pickup_datetime'] = pd.to_datetime(data['lpep_pickup_datetime'])
    data['lpep_pickup_date'] = data['lpep_pickup_datetime'].dt.date

    # Filter out rows where passenger_count is 0 or trip_distance is 0
    filtered_data = data[(data['passenger_count'] > 0) & (data['trip_distance'] > 0)]

    return filtered_data

@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    # Assertions for vendor_id, passenger_count, and trip_distance
    assert output['vendor_id'].isin([1, 2]).all(), 'vendor_id contains invalid values'
    assert (output['passenger_count'] > 0).all(), 'There are rides with 0 or fewer passengers'
    assert (output['trip_distance'] > 0).all(), 'There are rides with 0 or negative trip distance'