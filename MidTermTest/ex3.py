with open('test_file4.txt', 'r') as file:
    f = list(file.read())
f.append(' ')
with open('EnglishWords.txt', 'r') as file:
    words = []
    for word in file.readlines():
        word = word.strip()
        words.append(word)


punctuation = [',', '.', ';', ':', '?', '!', '[', ']', '{', '}', '/', '\\', '@', '#', '&', '(', ')',
               '\'', '\"', '~', '+', '=', '-', '_', '>', '<', '`', '|']

n_up = 0
n_punctuation = 0
n_numeric = 0
n_correct_words = 0
n_wrong_words = 0

start_index = 0

i = 0
while i < len(f):
    if f[i].isupper():
        n_up += 1
        f[i] = f[i].lower()
    elif f[i] in punctuation:
        n_punctuation += 1
        del f[i]
        i -= 1
    elif f[i].isnumeric():
        n_numeric += 1
        del f[i]
        i -= 1
    elif f[i] == ' ':
        if ''.join(f[start_index: i]) in words:
            n_correct_words += 1
        else:
            n_wrong_words += 1
        start_index = i+1
    i += 1

out = []
out.append("Formatting ###################\n")
out.append(f"Number of upper case words transformed: {n_up}\n")
out.append(f"Number of punctuation’s removed: {n_punctuation}\n")
out.append(f"Number of numbers removed: {n_numeric}\n")
out.append("Spellchecking ###################\n")
out.append(f"Number of words in file: {n_correct_words + n_wrong_words}\n")
out.append(f"Number of correct words in file: {n_correct_words}\n")
out.append(f"Number of incorrect words in file: {n_wrong_words}")

print(''.join(out))