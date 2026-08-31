import pytest
from tool import is_palindrome

def test_simple_palindromes():
    assert is_palindrome("madam") is True
    assert is_palindrome("racecar") is True
    assert is_palindrome("level") is True

def test_palindromes_with_spaces_and_punctuation():
    assert is_palindrome("A man, a plan, a canal: Panama") is True
    assert is_palindrome("No 'x' in Nixon") is True
    assert is_palindrome("Eva, can I see bees in a cave?") is True

def test_palindromes_with_mixed_case():
    assert is_palindrome("Madam") is True
    assert is_palindrome("Racecar") is True
    assert is_palindrome("LeveL") is True

def test_non_palindromes():
    assert is_palindrome("hello") is False
    assert is_palindrome("world") is False
    assert is_palindrome("Python") is False

def test_empty_string():
    assert is_palindrome("") is True

def test_single_character_string():
    assert is_palindrome("a") is True
    assert is_palindrome("Z") is True
    assert is_palindrome("7") is True

def test_string_with_only_non_alphanumeric_chars():
    assert is_palindrome("!!!") is True
    assert is_palindrome(" , ") is True
    assert is_palindrome(" . , ; : ") is True

def test_numbers_as_palindromes():
    assert is_palindrome("121") is True
    assert is_palindrome("12321") is True
    assert is_palindrome("1001") is True
    assert is_palindrome("123") is False
