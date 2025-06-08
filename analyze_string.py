def analyze_string(letters):
    vowels = 'aeiouAEIOU'
    vowel_list = []
    consonant_list = []

    for ch in letters:
        if ch.isalpha():
            if ch in vowels:
                vowel_list.append(ch)
            else:
                consonant_list.append(ch)

    vowel_str = ''.join(vowel_list)
    consonant_str = ''.join(consonant_list)
    consonant_number = len(consonant_list)

    return (vowel_str, consonant_number, consonant_str)


input_str = input("Введіть рядок: ")
result = analyze_string(input_str)
print(result)
