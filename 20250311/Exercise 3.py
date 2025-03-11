# Python 提供了一個內建函數 reversed，它接受一個序列（例如列表或字串）作為參數，並返回一個包含反轉後元素的對象。

arg = reversed('parrot')

print(arg)
# reversed 對象是一個迭代器，這意味著它可以在 for 迴圈中使用。
# 如果您想要將反轉後的元素放入列表中，可以使用 list 函數。

arg = list(reversed('parrot'))

print(arg)
# ['t', 'o', 'r', 'r', 'a', 'p']
# 或者如果您想要將它們放入字串中，可以使用 join 方法。

arg = ''.join(reversed('parrot'))
'torrap'
# 因此我們可以寫一個函數來反轉一個單詞，如下所示。

def reverse_word(word):
    return ''.join(reversed(word))

# 檢查一個單詞是否為回文
def is_palindrome(word):
    return word == reverse_word(word)

# 回文是一個正反讀都一樣的單詞，例如 “noon” 和 “rotator”。寫一個名為 is_palindrome 的函數，它接受一個字串參數，如果它是回文則返回 True，否則返回 False。
# 您可以使用以下迴圈來找到單詞列表中所有至少有 7 個字母的回文。
word_list = ['noon', 'redivider', 'deified', 'civic', 'radar', 'level', 'rotor', 'kayak', 'reviver', 'racecar', 'madam', 'refer']

for word in word_list:
    if len(word) >= 7 and is_palindrome(word):
        print(word)