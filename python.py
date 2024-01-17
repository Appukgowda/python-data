import string
def load_values(file_path):
    values = {}
    with open(file_path, 'r') as file:
        for line in file:
            try:
                letter, value = line.strip().split()
                values[letter] = int(value)
            except ValueError:
                pass
    return values


def calculate_score(letter, position, is_first, is_last, values):
    try:
        if is_first:
            return 0
        elif is_last:
            return 20 if letter == 'E' else 5
        else:
            position_value = 1 if position == 2 else (2 if position == 3 else 3)
            return position_value + values.get(letter, 0)
    except KeyError:
        return 0
    return values



def generate_abbreviations(name, values):
    words = [word.strip(string.punctuation) for word in name.split()]
    abbreviations = set()
    for word in words:
        first_letter = word[0]
        for i in range(1, len(word) - 1):
            second_letter = word[i]
            for j in range(i + 1, len(word)):
                third_letter = word[j]
                abbreviation = f"{first_letter}{second_letter}{third_letter}"
                score = calculate_score(second_letter, i, False, j == len(word) - 1, values) + calculate_score(third_letter, j, False, True, values)
                abbreviations.add((abbreviation, score))
    return abbreviations




def main():
    input_file = input("Enter the name of the input file (with .txt extension): ")
    values_file = "values.txt" 
    values = load_values(values_file)
    with open(input_file, 'r') as file:
        names = [line.strip() for line in file]
    surname = input("Enter your surname: ")
    output_file = f"{surname.lower()}_{input_file[:-4]}_abbrevs.txt"
    with open(output_file, 'w') as file:
        for name in names:
            abbreviations = generate_abbreviations(name.upper(), values)
            best_abbreviation, best_score = min(abbreviations, key=lambda x: x[1])
            file.write(f"{name.upper()}: {best_abbreviation} ({best_score} points)\n")



if __name__ == "__main__":
    main()


