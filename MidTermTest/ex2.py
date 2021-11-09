with open('test_file1.txt', 'r') as file:
    line = file.read()

line = list(line)
c = ''

for i in range(20):
    if line[i] == ':':
        c = line[i - 1]
        del line[:i + 1]
        break

if c == 'x':
    letters = []
    line.append(' ')
    for i in range(len(line)):
        if line[i] == ' ':
            letter = ''.join(line[i-2:i])
            letter = bytes.fromhex(letter)
            letter = letter.decode("ASCII")
            letters.append(letter)

    print(''.join(letters))



elif c == ')':
    alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o',
                'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    decoder = ['x', 'y', 'z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o',
               'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

    message = []
    words = ''.join(line)
    words = words.split(' ')
    words[-1] += ' '

    for word in words:
        startIndex = 0
        letters = []
        for i in range(len(word)):
            if word[i] == ' ':
                continue
            else:
                letters.append(decoder[alphabet.index(word[i])])
        message.append(''.join(letters))

    print(' '.join(message))


elif c == 'e':
    decoder = {'.-': 'a', '-...': 'b', '-.-.': 'c',
               '-..': 'd', '.': 'e', '..-.': 'f', '--.': 'g',
               '....': 'h', '..': 'i', '.---': 'j', '-.-': 'k',
               '.-..': 'l', '--': 'm', '-.': 'n', '---': 'o', '.--.': 'p', '--.-': 'q',
               '.-.': 'r', '...': 's', '-': 't', '..-': 'u', '...-': 'v',
               '.--': 'w', '-..-': 'x', '-.--': 'y', '--..': 'z'
               }

    message = []
    words = ''.join(line)
    words = words.split('/ ')
    words[-1] += ' '

    for word in words:
        startIndex = 0
        letters = []
        for i in range(len(word)):
            if word[i] == ' ':
                letters.append(decoder[word[startIndex:i]])
                startIndex = i + 1
        message.append(''.join(letters))

    print(' '.join(message))
