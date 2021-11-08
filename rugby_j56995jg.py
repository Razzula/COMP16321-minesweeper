inp = input()

scores = []
for i in range(0, len(inp), 3):
    scores.append(inp[i:i+3])

T1 = 0
T2 = 0

for score in scores:
    if score[2] == 't':
        increment = 5
    elif score[2] == 'c':
        increment = 2
    elif score[2] == 'p':
        increment = 3
    elif score[2] == 'd':
        increment = 3

    if score[1] == '1':
        T1 += increment
    else:
        T2 += increment

print(str(T1) + ":" + str(T2))