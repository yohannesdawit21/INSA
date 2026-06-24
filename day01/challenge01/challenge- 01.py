def under_100(n):
    ones = ["", "፩", "፪", "፫", "፬", "፭", "፮", "፯", "፰", "፱"]
    tens = ["", "፲", "፳", "፴", "፵", "፶", "፷", "፸", "፹", "፺"]

    return tens[n // 10] + ones[n % 10]


def arabic_to_geez(n):
    result = ""

    if n >= 10000:
        part = n // 10000
        if part > 1:
            result += arabic_to_geez(part)
        result += "፼"
        n %= 10000

    if n >= 100:
        part = n // 100
        if part > 1:
            result += under_100(part)
        result += "፻"
        n %= 100

    if n > 0:
        result += under_100(n)

    return result


num = int(input("Enter a number: "))
print("Ge'ez:", arabic_to_geez(num))