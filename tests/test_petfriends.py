import os

from api import PetFriends
from settings import valid_email, valid_password, invalid_email, invalid_password, invalid_key, invalid_id

pf = PetFriends()

def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """ Проверяем что запрос api ключа возвращает статус 200 и в результате содержится слово key"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)
    # Сверяем полученные данные с нашими ожиданиями
    assert status == 200
    assert 'key' in result

def test_get_all_pets_with_valid_key(filter=''):
    """ Проверяем что запрос всех питомцев возвращает не пустой список.
       Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее используя этого ключ
       запрашиваем список всех питомцев и проверяем что список не пустой.
       Доступное значение параметра filter - 'my_pets' либо '' """
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0


def test_add_new_pet_with_valid_data(name='BOB', animal_type='catt',
                                     age='7', pet_photo='images/cat.jpg'):
    """Проверяем что можно добавить питомца с корректными данными"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name

def test_successful_delete_self_pet():
    """Проверяем возможность удаления питомца"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.pet_delete(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()

def test_update_pet_info(name='Poppy', animal_type='dog', age = 77):
    """Проверяем возможность обновления информации о питомце"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, filter = 'my_pets')

    # Если список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name

        # если список питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
    else:
        raise Exception ('There are no my pets')

#1
def test_add_new_pet_without_photo(name='Patrick', animal_type = 'star', age = 69):
    """Проверяем добавление нового питомца без фото"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)
    assert status == 200
    assert result['name'] == name
#2
def test_add_photo_of_pet(pet_photo='images/cat.jpg'):
    """Проверяем возможность добавления фото для существующего питомца"""
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, filter='my_pets')
    if len(my_pets['pets']) > 0:
        status, result = pf.add_photo_of_pet(auth_key, my_pets['pets'][0]['id'], pet_photo)

        assert status == 200
        assert 'pet_photo' in result.keys()

    else:
        raise Exception ('There are no my pets')

#3
def test_get_api_key_for_invalid_email_user(email=invalid_email, password=valid_password):
    """Проверяем, что запрос ключа для пользователя с неверным имейл возвращает статус-код 403 и ответ не содержит слово 'key' """
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'key' not in result

#4
def test_get_api_key_for_invalid_password_user(email=valid_email, password=invalid_password):
    """Проверяем, что запрос ключа для пользователя с неверным паролем возвращает статус-код 403 и ответ не содержит слово 'key' """
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'key' not in result

#5
def test_get_all_pets_with_no_key(filter=''):
    """ Проверяем что запрос всех питомцев не отрабатывает без api ключа """
    try:
        auth_key = None
        status, result = pf.get_list_of_pets(auth_key, filter)
    except TypeError:
        assert True
    else:
        assert status != 200

#6
def test_get_all_pets_with_invalid_key(filter=''):
    """Проверяем, что запрос на получение списка животных не выполняется с несуществующим api ключом """
    auth_key = invalid_key
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 403
    assert 'Forbidden' in result

#7
def test_update_pet_info_with_empty_name(name='', animal_type='new-type2', age = 5):
    """Проверяем возможность обновления информации о питомце с пустым именем"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, filter = 'my_pets')

    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
        assert status == 200
        assert result['animal_type'] == animal_type
#8
def test_add_incorrect_format_photo_of_pet(pet_photo='images/incorrect_format_photo.bmp'):
    """Проверяем невозможность добавить фото питомца в неподдерживаемом формате bmp"""
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, filter='my_pets')
    if len(my_pets['pets']) > 0:
        status, result = pf.add_photo_of_pet(auth_key, my_pets['pets'][0]['id'], pet_photo)

        assert status == 400

    else:
        raise Exception ('There are no my pets')

#9
def test_unsuccessful_update_pet_info_with_incorrect_id(name='Poppy', animal_type='dog', age = 77):
    """Проверяем невозможность обновления информации о питомце с несуществующим id"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, filter = 'my_pets')
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet(auth_key, invalid_id, name, animal_type, age)
        assert status == 400

    else:
        raise Exception ('There are no my pets')

#10
def test_add_photo_of_pet_with_incorrect_id(pet_photo='images/cat.jpg'):
    """Проверяем невозможность добавить фото для животного с несуществующим id"""
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, filter='my_pets')
    if len(my_pets['pets']) > 0:
        status, result = pf.add_photo_of_pet(auth_key, invalid_id, pet_photo)

        assert status == 500
        assert 'pet_photo' not in result

    else:
        raise Exception ('There are no my pets')