with open('test_file1.txt', 'r') as file:
    line = file.read()

line = list(line)
c = ''
for i in range(20):
    if line[i] == ':':
        c = line[i-1]
        del line[:i+1]
        break

if c == 'x':
    print('hexadecimal')

elif c == ')':
    print('caesar')

elif c == 'e':
    print('morse')

#    for i in range( len(line)):



