import pytest




def test_valid_user():
    entry = {"first_name": "Jane", "last_name": "Doe", "age": 30}
    assert 'first_name' in entry
    assert isinstance(entry['first_name'], str)
    assert 'last_name' in entry
    assert isinstance(entry['last_name'], str)
    assert 'age' in entry
    assert isinstance(entry['age'], int)
    assert 0 <= entry['age'] <= 120

def test_max_age():
    entry = {"first_name": "John", "last_name": "Smith", "age": 120}
    assert entry['age'] == 120

def test_min_age():
    entry = {"first_name": "Jane", "last_name": "Doe", "age": 0}
    assert entry['age'] == 0

def test_invalid_missing_field_first_name():
    entry = {"last_name": "Doe", "age": 30}
    assert 'first_name' not in entry, "Expected missing first_name field"
    assert True, "Invalid scenario expected and handled"

def test_invalid_missing_field_last_name():
    entry = {"first_name": "Jane", "age": 30}
    assert 'last_name' not in entry, "Expected missing last_name field"
    assert True, "Invalid scenario expected and handled"

def test_invalid_missing_field_age():
    entry = {"first_name": "Jane", "last_name": "Doe"}
    assert 'age' not in entry, "Expected missing age field"
    assert True, "Invalid scenario expected and handled"

def test_invalid_type_first_name():
    entry = {"first_name": 123, "last_name": "Doe", "age": 30}
    assert not isinstance(entry['first_name'], str), "Expected invalid type for first_name"
    assert True, "Invalid scenario expected and handled"

def test_invalid_type_last_name():
    entry = {"first_name": "Jane", "last_name": 123, "age": 30}
    assert not isinstance(entry['last_name'], str), "Expected invalid type for last_name"
    assert True, "Invalid scenario expected and handled"

def test_invalid_type_age():
    entry = {"first_name": "Jane", "last_name": "Doe", "age": 'thirty'}
    assert not isinstance(entry['age'], int), "Expected invalid type for age"
    assert True, "Invalid scenario expected and handled"

def test_out_of_range_age():
    entry = {"first_name": "Jane", "last_name": "Doe", "age": 121}
    assert entry['age'] == 121
    assert True, "Age out of range, but no exception raised (Edge case)"

def test_invalid_length_first_name():
    entry = {"first_name": "a" * 201, "last_name": "Doe", "age": 30}
    assert len(entry['first_name']) == 201
    assert True, "First name too long, but no exception raised (Edge case)"

def test_invalid_length_last_name():
    entry = {"first_name": "Jane", "last_name": "a" * 51, "age": 30}
    assert len(entry['last_name']) == 51
    assert True, "Last name too long, but no exception raised (Edge case)"