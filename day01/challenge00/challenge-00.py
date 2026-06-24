def josephus(n, k):
    people = []

    # Create the list of people
    for i in range(1, n + 1):
        people.append(i)

    index = 0

    while len(people) > 1:

        # Move k-1 steps forward
        for j in range(k - 1):
            index = index + 1

            # If we reach the end, go back to the beginning
            if index >= len(people):
                index = 0

        eliminated = people.pop(index)
        print("Person", eliminated, "is eliminated")

        # If the removed person was the last element
        if index >= len(people):
            index = 0

    return people[0]


n = int(input("Enter number of people: "))
k = int(input("Enter elimination index: "))

survivor = josephus(n, k)

print("Last surviving person is:", survivor)