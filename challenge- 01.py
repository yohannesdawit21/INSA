def geez_to_arabic(geez):
    digits = {
        '፩': 1, '፪': 2, '፫': 3, '፬': 4, '፭': 5,
        '፮': 6, '፯': 7, '፰': 8, '፱': 9,
        '፲': 10, '፳': 20, '፴': 30, '፵': 40,
        '፶': 50, '፷': 60, '፸': 70, '፹': 80,
        '፺': 90
    }

    total = 0
    current = 0

    for ch in geez:
        if ch == '፻':
            if current == 0:
                current = 1
            total += current * 100
            current = 0

        elif ch == '፼':
            if current == 0:
                current = 1
            total += current * 10000
            current = 0

        else:
            current += digits[ch]

    return total + current


print(geez_to_arabic("፩፻፳፭"))  # 125
print(geez_to_arabic("፲፻"))    # 1000
print(geez_to_arabic("፻፼"))    # 1000000