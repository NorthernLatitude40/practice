from tool import is_palindrome

def test_is_palindrome_basic():
    assert is_palindrome("racecar") is True
    assert is_palindrome("hello") is False

def test_is_palindrome_with_spaces_and_punctuation():
    assert is_palindrome("A man, a plan, a canal: Panama") is True
    assert is_palindrome("Race Car") is True

def test_is_palindrome_with_numbers():
    assert is_palindrome("12321") is True
    assert is_palindrome("No 'x' in 'Nixon'") is True
    assert is_palindrome("1a2") is False
    assert is_palindrome("12a21") is True

def test_is_palindrome_edge_cases():
    assert is_palindrome("") is True
    assert is_palindrome("a") is True
