def is_palindrome(s: str) -> bool:
    """
    判斷字串是否為回文 (Palindrome)。
    忽略大小寫和非字母數字字元。

    Args:
        s (str): 待檢查的字串。

    Returns:
        bool: 如果字串是回文則返回 True，否則返回 False。
    """
    # 將字串轉換為小寫，並過濾掉所有非字母數字字元
    processed_s = "".join(filter(str.isalnum, s)).lower()
    
    # 檢查處理後的字串是否與其反轉相同
    return processed_s == processed_s[::-1]
