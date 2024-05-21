import random
from core.parser_logic.txt_pars import main

def recursiv_add_groups(group, enum, length, words1, dict_group_value):
    """Рекурсия. Добавляет строки в словарь, если длина списка > 1"""
    if length < len(words1[enum]):
        if  len(words1[enum][length]) < 1:
            return False
        else:
            dict_group_value[("".join(words1[enum][length])).rstrip('. \t;')] = (''.join(group).strip('., '))
            return recursiv_add_groups(group, enum, length+1, words1, dict_group_value)
    return True

def add_one_group(group, enum, words1, dict_group_value):
    """Добавляет строку в словарь, если длина списка = 1"""
    if len(words1[enum]) < 1:
        return False
    else:
        dict_group_value[("".join(words1[enum])).rstrip('. \t;')] = (''.join(group).strip('., '))


def randomize_keys(dictionary: dict) -> dict:
    """Пересобирает словарь в рандомном порядке"""
    keys = list(dictionary.keys())
    random.shuffle(keys)
    values = [dictionary[key] for key in keys]
    new_dict = dict(zip(keys, values))
    return new_dict

def create_dict(file_name: str) -> dict:
    """
    Принимает путь к файлу. Получает 2 списка с ключами и значениями.
    Обрабатывает их и объединяет в словарь.
    """
    if main(file_name) is False:
        return False
    elif main(file_name) is None:
        return None
    else:
        dict_group_value = {}
        words1, _ = main(file_name)
        _, words2 = main(file_name)
        enum = 0
        for groups in words2:
            if len(words1[enum]) == 1:
                add_one_group(groups, enum, words1, dict_group_value)
                enum += 1 
            else:
                recursiv_add_groups(groups, enum, 0, words1, dict_group_value)
                enum +=1
        randomized_dict = randomize_keys(dict_group_value)
        finally_dict = {}
        
        for key, key_group in randomized_dict.items():
            if len(key) < 1:
                continue
            else:
                finally_dict[key] = key_group
        return finally_dict
