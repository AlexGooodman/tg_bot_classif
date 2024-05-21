import re
from typing import Union

def get_file(file: str):
    """Принимает путь к сохраненному файлу. Читает txt, возвращает текст из документа"""
    with open(file, 'r', encoding='utf-8') as file_obj:
        content = file_obj.readlines()
        return content

def find_elements_after_colon(sentence: str) -> str:
    """Сепаратор. Делит строчку по двоеточию. Возвращает 2 строчки"""
    key_group = re.match(r'[^:]*', sentence.strip('\n|\t')).group(0)
    value_group = re.findall(r'(?<=:).*$', sentence)
    value_group = ((',').join(value_group)).split(',')
    return key_group, value_group

def print_nested_values(dictionary: dict, path: list) -> list:
    """Рекурсия. Принимает словарь. Отдает 2 списка (ключи, значения)""" 
    values = []
    all_keys = []
    for key, value in dictionary.items():
        current_path = path + [key]

        if isinstance(value, dict):
            nested_values, nested_keys = print_nested_values(value, current_path)
            values.extend(nested_values)
            all_keys.extend(nested_keys)
        else:
            values.append(value)
            all_keys.append(current_path)

    return values, all_keys

def main(file_name: str) -> Union[list, bool, None]:
    """
    Парсит передаваемый текст. Возвращает 2 списка(ключ, значение),
    При ошибках возвращает: False - некорректно отформатирован документ,
    None - вводимый документ не txt формата.
    """
    try:
        content = get_file(file_name)
        key1 = {}
        a = None
        b = None
        c = None
        d = None
        e = None

        for group in content:
            if re.match(r'^[^\t].*:', group):
                a = None
                if re.findall(r':\s*$', group):
                    a = group.strip(': \n\t')
                    a += ';\n'
                    key1[a] = {}
                else:
                    a1= None
                    a, _ = find_elements_after_colon(group)
                    _, a1 = find_elements_after_colon(group)
                    key1[a] = {'.': a1}
                b = None
            elif re.match(r'^\t[^\t].*', group):
                if re.findall(r':\s*$', group):
                    b = group.strip(': \n|\t')
                    b += ';\n'
                    key1[a][b] = {}
                else:
                    b1= None
                    b, _ = find_elements_after_colon(group)
                    _, b1 = find_elements_after_colon(group)
                    key1[a][b] = {'.': b1}
                c = None
            elif re.match(r'^\t\t[^\t].*', group):
                if re.findall(r':\s*$', group):
                    c = group.strip(': \n|\t')
                    c += ';\n'
                    key1[a][b][c] = {}
                else:
                    c1= None
                    c, _ = find_elements_after_colon(group)
                    _, c1 = find_elements_after_colon(group)
                    key1[a][b][c] = {'.': c1}
                d = None
            elif re.match(r'^\t\t\t[^\t].*', group):
                if re.findall(r':\s*$', group):
                    d = group.strip(': \n|\t')
                    d += ';\n'
                    key1[a][b][c][d] = {}
                else:
                    d1= None
                    d, _ = find_elements_after_colon(group)
                    _, d1 = find_elements_after_colon(group)
                    key1[a][b][c][d] = d1
                e = None
            elif re.match(r'^\t\t\t\t[^\t].*', group):
                if re.findall(r':\s*$', group):
                    e = group.strip(': \n|\t')
                    e += ';\n'
                    key1[a][b][c][d] = {}
                else:
                    e1 = None
                    e, _ = find_elements_after_colon(group)
                    _, e1 = find_elements_after_colon(group)
                    key1[a][b][c][d][e] = e1
        return print_nested_values(key1, path=[])
    except KeyError:
        return False
    except UnicodeDecodeError:
        return None
