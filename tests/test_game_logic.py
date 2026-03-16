from logic_utils import check_guess, parse_guess, update_score, get_range_for_difficulty

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    result = check_guess(50, 50)
    assert result == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    result = check_guess(60, 50)
    assert result == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    result = check_guess(40, 50)
    assert result == "Too Low"

def test_parse_guess_valid_int():
    ok, value, err = parse_guess("5")
    assert ok == True
    assert value == 5
    assert err is None

def test_parse_guess_valid_float_int():
    ok, value, err = parse_guess("5.0")
    assert ok == True
    assert value == 5
    assert err is None

def test_parse_guess_invalid_float():
    ok, value, err = parse_guess("5.5")
    assert ok == False
    assert value is None
    assert err == "Please enter a whole number."

def test_parse_guess_invalid_string():
    ok, value, err = parse_guess("abc")
    assert ok == False
    assert value is None
    assert err == "That is not a number."

def test_parse_guess_none():
    ok, value, err = parse_guess(None)
    assert ok == False
    assert value is None
    assert err == "Enter a guess."

def test_parse_guess_empty():
    ok, value, err = parse_guess("")
    assert ok == False
    assert value is None
    assert err == "Enter a guess."

def test_update_score_win():
    result = update_score(0, "Win", 1)
    assert result == 80  # 100 - 10*(1+1) = 80

def test_update_score_too_high():
    result = update_score(10, "Too High", 1)
    assert result == 5  # 10 - 5

def test_update_score_too_low():
    result = update_score(10, "Too Low", 1)
    assert result == 5  # 10 - 5

def test_update_score_invalid():
    result = update_score(10, "Invalid", 1)
    assert result == 10  # unchanged

def test_get_range_easy():
    low, high = get_range_for_difficulty("Easy")
    assert low == 1
    assert high == 20

def test_get_range_normal():
    low, high = get_range_for_difficulty("Normal")
    assert low == 1
    assert high == 100

def test_get_range_hard():
    low, high = get_range_for_difficulty("Hard")
    assert low == 1
    assert high == 50

def test_get_range_invalid():
    try:
        get_range_for_difficulty("Invalid")
        assert False, "Should raise ValueError"
    except ValueError as e:
        assert "Invalid difficulty" in str(e)
