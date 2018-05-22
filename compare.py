count = 0
with open("queries2.txt", "r") as file:
    for line in file:
        line = line.strip()
        count = count + 1


print(count)