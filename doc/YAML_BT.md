## Документация к YAML-файлу "background_training.yml" GitHub Actions

Файл описывает workflow для автоматического запуска итеративного обучения модели. Workflow запускается при пушах в ветку `main`, при создании pull request в ветку `main`.

---

### Разбор параметров

#### 1. **`name`**
```yaml
name: Background Training
```
- Имя workflow. Оно отображается в разделе **Actions** вашего репозитория на GitHub.
- В данном случае workflow называется `Background Training`.

---

#### 2. **`on`**
```yaml
on:
  push:
    branches:
      - main
  pull_request:
    branches:
      - main
```
- Определяет события, которые запускают workflow.
- **`push`**: Workflow запускается при каждом пуше в ветку `main`.
- **`pull_request`**: Workflow запускается при создании pull request в ветку `main`.

---

#### 3. **`jobs`**
```yaml
jobs:
  background-training:
    runs-on: ubuntu-latest
```
- **`jobs`**: Содержит описание задач, которые выполняются в рамках workflow.
- **`background-training`**: Имя задачи. Это имя используется для идентификации задачи внутри workflow.
- **`runs-on`**: Указывает, на какой виртуальной машине будет выполняться задача. В данном случае используется `ubuntu-latest` — последняя версия Ubuntu.

---

#### 4. **`steps`**
```yaml
steps:
    - name: Checkout code
      uses: actions/checkout@v3
```
- **`steps`**: Список шагов, которые выполняются в рамках задачи.
- Каждый шаг выполняется последовательно.

---

##### Шаг 1: **Checkout code**
```yaml
- name: Checkout code
  uses: actions/checkout@v3
```
- **`name`**: Имя шага. В данном случае — `Checkout code`.
- **`uses`**: Указывает действие, которое используется в этом шаге. Здесь используется `actions/checkout@v3`, чтобы клонировать код репозитория в виртуальную машину.

---

##### Шаг 2: **Install dependencies**
```yaml
- name: Install dependencies
  run: |
    python -m pip install --upgrade pip
    pip install -r requirements.txt
```
- **`name`**: Имя шага. В данном случае — `Install dependencies`.
- **`run`**: Указывает команды, которые выполняются в рамках этого шага.
  - `python -m pip install --upgrade pip`: Обновляет менеджер пакетов `pip`.
  - `pip install -r requirements.txt`: Устанавливает зависимости, указанные в файле requirements.txt.

---

##### Шаг 3: **Run training script with periodic artifact generation**
```yaml
- name: Run training script with periodic artifact generation
  run: |
    for i in {1..5}; do  # Запускаем 5 итераций с задержкой
      python main.py --mode single  # Запускаем одну итерацию обучения
      sleep 60  # Задержка в 60 секунд между итерациями
    done
```
- **`name`**: Имя шага. В данном случае — `Run training script with periodic artifact generation`.
- **`run`**: Указывает команды, которые выполняются в рамках этого шага.
  - Цикл `for i in {1..5}` запускает 5 итераций обучения.
  - `python main.py --mode single`: Запускает скрипт main.py с параметром `--mode single`, который выполняет одну итерацию обучения.
  - `sleep 60`: Добавляет задержку в 60 секунд между итерациями.

---

##### Шаг 4: **Upload logs**
```yaml
- name: Upload logs
  uses: actions/upload-artifact@v4
  with:
    name: background-training-logs
    path: training.log
```
- **`name`**: Имя шага. В данном случае — `Upload logs`.
- **`uses`**: Указывает действие, которое используется в этом шаге. Здесь используется `actions/upload-artifact@v4` для загрузки артефактов.
- **`with`**: Передает параметры для действия:
  - **`name`**: Имя артефакта. В данном случае — `background-training-logs`.
  - **`path`**: Путь к файлу или директории, которые нужно загрузить как артефакт. Здесь указывается файл `training.log`.

---

### Итоговая структура workflow
1. Клонируется код репозитория.
2. Устанавливаются зависимости из requirements.txt.
3. Запускается скрипт main.py в цикле с задержкой между итерациями.
4. Логи работы загружаются как артефакт.

---

### Достоинства
- Workflow автоматически запускается при пуше в ветку `main`.
- Логи работы сохраняются и доступны для загрузки в разделе **Actions** на GitHub.
- Можно контролировать количество итераций обучения через YAML.

### Недостатки
- Для получения артефакта необходимо дождать полного завершения обучения (нельзя контролировать промежуточные результаты).
- Время обучения ограничено возможностями GitHub Actions (6 часов).
- Нельзя обеспечить обучение по расписанию (каждый раз модель будет обучаться с нуля).