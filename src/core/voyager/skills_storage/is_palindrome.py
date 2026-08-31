import re

def is_palindrome(text: str) -> bool:
    """
    檢查一個字串是否為回文 (Palindrome)。
    會忽略大小寫和非字母數字字元。

    Args:
        text (str): 待檢查的字串。

    Returns:
        bool: 如果是回文則返回 True，否則返回 False。

    Examples:
        >>> is_palindrome("Madam")
        True
        >>> is_palindrome("A man, a plan, a canal: Panama")
        True
        >>> is_palindrome("hello")
        False
        >>> is_palindrome("Racecar")
        True
    """
    # 將字串轉換為小寫並移除所有非字母數字字元
    processed_text = re.sub(r'[^a-zA-Z0-9]', '', text).lower()

    # 檢查處理後的字串是否等於其反轉
    return processed_text == processed_text[::-1]
