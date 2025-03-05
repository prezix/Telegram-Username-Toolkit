import itertools

# Словарь замен символов. Ключи — буквы, значения — списки возможных замен.
SUBSTITUTIONS = {
    'a': ['4', '@'],
    'b': ['8', 'ß'],
    'c': ['<', '{', '[', '¢'],
    'd': ['|)', 'đ'],
    'e': ['3', '€'],
    'f': ['ƒ'],
    'g': ['6', '9'],
    'h': ['#'],
    'i': ['1', '!', '|'],
    'j': ['_|'],
    'k': ['|<'],
    'l': ['1', '|', '£'],
    'm': ['/\\/\\', '|\\/|'],
    'n': ['|\\|'],
    'o': ['0', '()', 'Ø'],
    'p': ['|*', '¶'],
    'q': ['0_', 'kw'],
    'r': ['|2', '®'],
    's': ['5', '$', '§'],
    't': ['7', '+'],
    'u': ['(_)', 'µ'],
    'v': ['\\/', '|/'],
    'w': ['\\/\\/', 'VV'],
    'x': ['><', '}{'],
    'y': ['`/', '¥'],
    'z': ['2', '7_'],
    # Дополнительные замены для заглавных букв
    'A': ['4', '@'],
    'B': ['8', 'ß'],
    'C': ['<', '{', '[', '¢'],
    'D': ['|)', 'Đ'],
    'E': ['3', '€'],
    'F': ['ƒ'],
    'G': ['6', '9'],
    'H': ['#'],
    'I': ['1', '!', '|'],
    'J': ['_|'],
    'K': ['|<'],
    'L': ['1', '|', '£'],
    'M': ['/\\/\\', '|\\/|'],
    'N': ['|\\|'],
    'O': ['0', '()', 'Ø'],
    'P': ['|*', '¶'],
    'Q': ['0_', 'KW'],
    'R': ['|2', '®'],
    'S': ['5', '$', '§'],
    'T': ['7', '+'],
    'U': ['(_)', 'µ'],
    'V': ['\\/', '|/'],
    'W': ['\\/\\/', 'VV'],
    'X': ['><', '}{'],
    'Y': ['`/', '¥'],
    'Z': ['2', '7_']
}

def generate_substituted_variants(base_username):
    """
    Генерирует все возможные варианты ника, заменяя символы на похожие символы.
    
    :param base_username: Оригинальный никнейм.
    :return: Список всех возможных вариантов.
    """
    # Для каждого символа в нике получаем список возможных замен, включая оригинал.
    substitution_lists = []
    for char in base_username:
        if char in SUBSTITUTIONS:
            substitution_options = SUBSTITUTIONS[char]
            substitution_lists.append(substitution_options + [char])
        else:
            substitution_lists.append([char])
    
    # Генерируем декартово произведение всех замен.
    all_combinations = itertools.product(*substitution_lists)
    
    # Объединяем символы в строки и убираем дубликаты.
    variants = set(''.join(combo) for combo in all_combinations)
    
    return sorted(variants)

def save_variants(variants, filename='username_substituted_variants.txt'):
    """
    Сохраняет сгенерированные варианты в текстовый файл.
    
    :param variants: Список вариантов ника.
    :param filename: Имя файла для сохранения.
    """
    with open(filename, 'w', encoding='utf-8') as f:
        for variant in variants:
            f.write(f"{variant}\n")
    print(f"Сгенерировано {len(variants)} вариантов. Сохранено в файл '{filename}'.")

def main():
    base_username = input("Введите ваш оригинальный ник: ").strip()
    if not base_username:
        print("Никнейм не может быть пустым.")
        return
    
    print("Генерация вариантов, пожалуйста подождите...")
    variants = generate_substituted_variants(base_username)
    save_variants(variants)

if __name__ == "__main__":
    main()
