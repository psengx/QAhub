# Рабочий протокол «Медиаполка»

Автор, группа: Коровина Дарья, ИТ-9.24.3-ДН. Дата: 31.10.2026. Требования: 1.0. Использованный Python: 3.14.8.

## 1. Короткий план до исправлений

Цель: [какие нарушения хотим обнаружить и какой результат получить].

Проверяем: [правила и действия]. За рамками: добавление прочего функционала (например, фамилии получателей, сроки, штрафы, бронь на дату, сохранение после выхода, параллельные пользователи, мобильная версия).

Начнём, когда: [условия запуска и исходные данные]. Сначала проверим: [что и почему]. Остановимся для разбора, если: [условие]. Починку считаем завершённой, когда: [измеримые условия]. Если время закончится раньше: [что зафиксируем].

| № | Правило | Исходные данные и действие | Ожидание до запуска | Приоритет / причина | Имя теста или ручная проверка |
| --- | --- | --- | --- | --- | --- |
| 1 | R2 | Микрофон: 10</br>Штатив: 5 </br>LED-свет: 0</br>**Действие**: выдача 3 микрофонов| Число доступных микрофонов составляет 7 шт, добавлена выдача с новым ID на число 3 микрофонов | По правилу выдача должна осуществляться **до 3 включительно** | […] |
| 2 | R3 |  Микрофон: 3 </br>Штатив: 1 </br>LED-свет: 0 </br>**Действие**: выдача 2 штативов при доступном количестве - 1 | Вывод сообщения "Недостаточно оборудования", выдача не выполняется | Важно не допустить выдачу бОльшего количества, чем есть в наличии | […] |
| 3 | R5 |  Микрофон: 3 </br>Штатив: 0 </br>LED-свет: 0 </br>Выдачи:</br>ID 1: Микрофон, 3 шт., Возвращено</br>ID 2: Штатив, 1 шт., Выдано**Действие**: возврат по записи c id > 1 | Успешный возврат, вывод сообщения "Возвращено", изменение количества с исходного на исходное + 1 | Приоритет высокий, так как нам важен корректный возврат | […] |
| 4 | R6 | Микрофон: 3</br>Штатив: 1</br>LED-свет: 0</br>Выдачи:</br>ID 1: Штатив, 1 шт., Возвращено</br>**Действие**: попытка повторного возврата по той же записи выдачи | Попытка возврата отклоняется, выводится сообщение "Уже возвращено", состояние остается прежним | Приоритет высокий, так как важно не допустить некорректных остатков в системе | […] |
| 5 | R2 | Микрофон: 3</br>Штатив: 1</br>LED-свет: 0</br>**Действие**: попытка выдачи оборудования при вводе некорректного значения в поле "Количество" | Вывод сообщения: "Введите целое количество от 1 до 3", сохранение прежнего состояния | Приоритет высокий, так как важно не допустить некорректных остатков в системе и возникновения ошибок из-за некорректных данных | […] |
| 6 | R4 | Микрофон: 3</br>Штатив: 1</br>LED-свет: 0</br>**Действие**: выдача допустимого количества оборудования из доступного | Выврл сообщение "Выдано", создание записи выдачи с выданным количеством оборудования, коррекция остатков доступного оборудования | Приоритет высокий, так как в этом весь смысл программы | […] |

Дополняйте строки по ходу исследования. Планируемые проверки не помечайте как выполненные до реального запуска.

## 2. Причины и исправления

Для каждой самостоятельно найденной причины заполните короткую запись. Копируйте блок по необходимости: количество блоков не является подсказкой о числе неисправностей.

### №1 Выдача 3 микрофонов

#### Правило, данные и шаги:

| Правило | Исходные данные                           | Шаги (ввод в консоль)                           |
| ------- | ----------------------------------------- | ----------------------------------------------- |
| R2      | Микрофон: 10<br>Штатив: 5 <br>LED-свет: 0 | Выдача - 1, <br>Позиция - 1, <br>Количество - 3 |

#### Ожидалось / получилось до исправления: 
>**Ожидалось:** выдача 3 микрофонов
>
>**Получено:** ошибка выдачи, вывод сообщения `Введите целое число от 1 до 3`

#### Обнаруживающий тест и файл вывода до исправления: 

```python
def test_issue_max_microphone_count(self):
	state = new_state()
	result = issue(state, "mic", "3")
	self.assertEqual(state["stock"]["mic"], 0)
	self.assertEqual(len(state["loans"]), 1)
	self.assertEqual(state["loans"][0]["status"], "issued")
```

```sh
FAIL: test_issue_max_microphone_count (test_student.StudentTests.test_issue_max_microphone_count)
---------------------------------------------------------------------
Traceback (most recent call last):
  File ".../test_student.py", in test_issue_max_microphone_count
    self.assertEqual(state["stock"]["mic"], 0)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 3 != 0
```

#### Причина в коде и изменение: 

```python
def issue(state, item, quantity_text):
	...
	if quantity < 1 or quantity >= 3:
	~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^
		return {"ok": False, "message": "Введите целое количество от 1 до 3"}
```

`>=` изменено на `>`

```python
def issue(state, item, quantity_text):
	...
	if quantity < 1 or quantity > 3:
	~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^
		return {"ok": False, "message": "Введите целое количество от 1 до 3"}
```

#### Повторная и соседняя проверки: 

```python
test_issue_max_light_count (test_student.StudentTests.test_issue_max_light_count) ... ok
test_issue_max_microphone_count (test_student.StudentTests.test_issue_max_microphone_count) ... ok
test_issue_max_tripod_count (test_student.StudentTests.test_issue_max_tripod_count) ... ok
```

### №2 Выдача 2 штативов при доступном количестве - 1

#### Правило, данные и шаги:

| Правило | Исходные данные                          | Шаги (ввод в консоль)                           |
| ------- | ---------------------------------------- | ----------------------------------------------- |
| R3      | Микрофон: 3<br>Штатив: 1 <br>LED-свет: 0 | Выдача - 1, <br>Позиция - 2, <br>Количество - 2 |

#### Ожидалось / получилось до исправления: 
>**Ожидалось:** вывод сообщения "Недостаточно оборудования", выдача не выполняется
>
>**Получено:** выдача двух штативов, изменение количества микрофонов с `1` на `-1`, создание записи выдачи

#### Обнаруживающий тест и файл вывода до исправления: 

```python
def test_issue_more_than_available_tripod(self):
	state = new_state()
	stock = state["stock"]["tripod"]
	result = issue(state, "tripod", (str)(state["stock"]["tripod"] + 1))
	self.assertEqual(state["stock"]["tripod"], stock)
	self.assertEqual(len(state["loans"]), 0)
	self.assertFalse(result["ok"])
```

```sh
FAIL: test_issue_more_than_available_tripod (test_student.StudentTests.test_issue_more_than_available_tripod)
------------------------------------------------------------------
Traceback (most recent call last):
  File ".../tests/test_student.py", in test_issue_more_than_available_tripod
    self.assertEqual(state["stock"]["tripod"], stock)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: -1 != 1
```

#### Причина в коде и изменение: 

```python
def issue(state, item, quantity_text):
	available = state["stock"][item]
	if available < 1:
	~~~~~~~~~~~~~^^^^
		return {"ok": False, "message": "Недостаточно оборудования"}
```

`>=` изменено на `>`

```python
def issue(state, item, quantity_text):
	available = state["stock"][item]
	if available < quantity:
	~~~~~~~~~~~~~^^^^^^^^^^^
		return {"ok": False, "message": "Недостаточно оборудования"}
```

#### Повторная и соседняя проверки: 

```python
test_issue_more_than_available_light (test_student.StudentTests.test_issue_more_than_available_light) ... ok
test_issue_more_than_available_microphone (test_student.StudentTests.test_issue_more_than_available_microphone) ... ok
test_issue_more_than_available_tripod (test_student.StudentTests.test_issue_more_than_available_tripod) ... ok
```

### №3 Возврат по записи с id > 1

#### Правило, данные и шаги:

| Правило | Исходные данные                                                                                                                  | Шаги (ввод в консоль)           |
| ------- | -------------------------------------------------------------------------------------------------------------------------------- | ------------------------------- |
| R5      | Микрофон: 3  <br>Штатив: 0  <br>LED-свет: 0<br>Выдачи:  <br>- ID 1: Микрофон, 1 шт., Возвращено<br>- ID 2: Штатив, 1 шт., Выдано | Возврат - 2,  <br>ID записи - 2 |

#### Ожидалось / получилось до исправления: 
>**Ожидалось:** Успешный возврат, вывод сообщения "Возвращено", изменение количества с исходного на исходное + 1
>
>**Получено:** вывод сообщения "Возвращено", количество не изменилось (предмет не вернулся)

#### Обнаруживающий тест и файл вывода до исправления: 

```python
def test_return_loan_id_two(self):
    state = new_state()
    issue(state, "mic", "1")
    before_count = state["stock"]["mic"]
    issue(state, "mic", "1")
    result = return_loan(state, 2)
    self.assertEqual(before_count, state["stock"]["mic"])
```

```sh
FAIL: test_return_loan_id_two (test_student.StudentTests.test_return_loan_id_two)
--------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/psengx/Документы/proghub/QAhub/project/tests/test_student.py", line 118, in test_return_loan_id_two
    self.assertEqual(before_count, state["stock"]["mic"])
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 2 != 1
```

#### Причина в коде и изменение: 

```python
def return_loan(state, loan_id):
	for loan in state["loans"]:
		if loan["id"] == loan_id:
			state["stock"][loan["item"]] += loan["quantity"]
			loan["status"] = "returned"
		return {"ok": True, "message": "Возвращено"}
		^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
		""" принудительное завершение цикла на первой итерации, 
		если id != loan_id"""
		
	return {"ok": False, "message": "Выдача не найдена"}
```

Изменена структура кода возврата, успешный return вынесен за пределы цикла for

```python
def return_loan(state, loan_id):
    found_loan = None
    for loan in state["loans"]:
        if loan["id"] == loan_id:
            found_loan = loan
            break
    if found_loan == None:
        return {"ok": False, "message": "Выдача не найдена"}
    
    if loan["status"] == "returned":
        return {"ok": False, "message": "Уже возвращено"}
    
    state["stock"][loan["item"]] += loan["quantity"]
    loan["status"] = "returned"
    return {"ok": True, "message": "Возвращено"}
```

#### Повторная и соседняя проверки: 

```python
test_return_loan_id_three (test_student.StudentTests.test_return_loan_id_three) ... ok
test_return_loan_id_two (test_student.StudentTests.test_return_loan_id_two) ... ok
```

### №4 Повторный возврат штатива по записи выдачи

#### Правило, данные и шаги:

| Правило | Исходные данные                                                                               | Шаги (ввод в консоль)           |
| ------- | --------------------------------------------------------------------------------------------- | ------------------------------- |
| R5      | Микрофон: 3  <br>Штатив: 1  <br>LED-свет: 0<br>Выдачи:  <br>- ID 1: Штатив, 1 шт., Возвращено | Возврат - 2,  <br>ID записи - 1 |

#### Ожидалось / получилось до исправления: 
>**Ожидалось:** вывод сообщения об ошибке "Уже возвращено", состояние остается прежним
>
>**Получено:** повторный возврат штатива по существующей записи выдачи

#### Обнаруживающий тест и файл вывода до исправления: 

```python
def test_return_returned_loan_tripod(self):
	state = new_state()
	loan = {
		"id": state["next_id"],
		"item": "tripod",
		"quantity": 1,
		"status": "returned",
		}
	state["loans"].append(loan)
	
	before_count = state["stock"]["tripod"]
	result = return_loan(state, loan["id"])
	self.assertEqual(before_count, state["stock"]["tripod"])
```

```sh
FAIL: test_return_loan_tripod (test_student.StudentTests.test_return_loan_tripod)
-------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/psengx/Документы/proghub/QAhub/project/tests/test_student.py", line 82, in test_return_returned_loan_tripod
    self.assertEqual(before_count, state["stock"]["tripod"])
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 1 != 2
```

#### Причина в коде и изменение: 

```python
def return_loan(state, loan_id):
    for loan in state["loans"]:
        if loan["id"] == loan_id:
            found_loan = loan
            break
    if found_loan == None:
        return {"ok": False, "message": "Выдача не найдена"}
        
    """ отсутствие проверки на статус записи """
    
    state["stock"][loan["item"]] += loan["quantity"]
    loan["status"] = "returned"
    return {"ok": True, "message": "Возвращено"}
```

добавлена проверка на статус записи - `Возвращено` и вывод ошибки возврата

```python
def return_loan(state, loan_id):
    for loan in state["loans"]:
        if loan["id"] == loan_id:
            found_loan = loan
            break
    if found_loan == None:
        return {"ok": False, "message": "Выдача не найдена"}
    
    if loan["status"] == "returned":
        return {"ok": False, "message": "Уже возвращено"}
    
    state["stock"][loan["item"]] += loan["quantity"]
    loan["status"] = "returned"
    return {"ok": True, "message": "Возвращено"}
```

#### Повторная и соседняя проверки: 

```python
test_return_returned_loan_light (test_student.StudentTests.test_return_returned_loan_light) ... ok
test_return_returned_loan_microphone (test_student.StudentTests.test_return_returned_loan_microphone) ... ok
test_return_returned_loan_tripod (test_student.StudentTests.test_return_returned_loan_tripod) ... ok
```

## 3. Итог

Команда финального запуска: […]. Обнаружено тестов: […]. Прошло / упало / ошибки: […]. Вывод сохранён в: […].

Какие проверки появились после уточнения плана: […].

Что осталось неисправленным или непроверенным: […].

Техническая помощь с запуском/синтаксисом: […].

Ответы на три вопроса задания: […].
