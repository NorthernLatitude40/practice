import pytest
from tool import is_palindrome

def test_simple_palindrome():
    assert is_palindrome("madam") == True

def test_simple_non_palindrome():
    assert is_palindrome("hello") == False

def test_palindrome_with_mixed_case():
    assert is_palindrome("Racecar") == True

def test_palindrome_with_spaces_and_punctuation():
    assert is_palindrome("A man, a plan, a canal: Panama") == True

def test_empty_string():
    assert is_palindrome("") == True

def test_single_character_string():
    assert is_palindrome("a") == True
    assert is_palindrome("Z") == True

def test_non_alphanumeric_only_string():
    # After filtering, it becomes "" which is a palindrome
    assert is_palindrome("!@#$%^&*") == True

def test_complex_non_palindrome():
    assert is_palindrome("not a palindrome") == False

def test_palindrome_with_numbers():
    assert is_palindrome("12321") == True
    assert is_palindrome("A1B22B1A") == True

def test_long_palindrome():
    long_palindrome = "Was it a car or a cat I saw?"
    assert is_palindrome(long_palindrome) == True

def test_long_non_palindrome():
    long_non_palindrome = "This is a long sentence that is definitely not a palindrome."
    assert is_palindrome(long_non_palindrome) == False
