with open('test_file3.txt', 'r') as file:
    line = file.read()

T1 = 0
T2 = 0
for i in range(len(line)):
    if line[i] == 'T':
        continue
    elif line[i] == '1':
        i += 1
        if line[i] == 't':
            T1 += 5
        elif line[i] == 'p' or line[i] == 'd':
            T1 += 3
        elif line[i] == 'c':
            T1 += 2
    elif line[i] == '2':
        i += 1
        if line[i] == 't':
            T2 += 5
        elif line[i] == 'p' or line[i] == 'd':
            T2 += 3
        elif line[i] == 'c':
            T2 += 2

with open('output.txt', 'w') as file:
    file.write(f'{T1}:{T2}')




