### Документация к cron_training.yml

Файл описывает workflow для автоматического запуска обучения модели по расписанию (каждый час), а также при пушах и создании pull request в ветку `main`. Workflow включает в себя загрузку артефактов из предыдущих запусков, выполнение обучения и сохранение новых артефактов и логов.

---

### Разбор параметров

#### 1. **`name`**
```yaml
name: CRON Background Training
```
- Имя workflow. Оно отображается в разделе **Actions** вашего репозитория на GitHub.
- В данном случае workflow называется `CRON Background Training`.

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
  schedule:
    - cron: "0 * * * *"
```
- Определяет события, которые запускают workflow.
- **`push`**: Workflow запускается при каждом пуше в ветку `main`.
- **`pull_request`**: Workflow запускается при создании pull request в ветку `main`.
- **`schedule`**: Workflow запускается по расписанию. В данном случае используется `cron: "0 * * * *"`, что означает запуск каждый час.

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

##### Шаг 3: **Attempt to download previous artifacts**
```yaml
- name: Attempt to download previous artifacts
  uses: dawidd6/action-download-artifact@v6
  with:
    workflow: cron_training.yml
    name: training-artifacts
    path: loc
    workflow_conclusion: success
    branch: main
  continue-on-error: true
```
- **`name`**: Имя шага. В данном случае — `Attempt to download previous artifacts`.
- **`uses`**: Указывает действие `dawidd6/action-download-artifact@v6`, которое используется для загрузки артефактов из предыдущих workflow.
- **`with`**: Передает параметры для действия:
  - **`workflow`**: Имя workflow, из которого загружаются артефакты. Здесь указано cron_training.yml.
  - **`name`**: Имя артефакта, который нужно загрузить. В данном случае — `training-artifacts`.
  - **`path`**: Путь, куда будут извлечены артефакты. Здесь указана папка loc.
  - **`workflow_conclusion`**: Указывает, что артефакты загружаются только из успешных запусков workflow.
  - **`branch`**: Указывает ветку, из которой загружаются артефакты. Здесь указана `main`.
- **`continue-on-error`**: Если артефакт не найден, шаг завершится успешно, и workflow продолжит выполнение.

---

##### Шаг 4: **Run training script with periodic artifact generation**
```yaml
- name: Run training script with periodic artifact generation
  run: python main.py --mode single
```
- **`name`**: Имя шага. В данном случае — `Run training script with periodic artifact generation`.
- **`run`**: Указывает команды, которые выполняются в рамках этого шага.
  - `python main.py --mode single`: Запускает скрипт main.py с параметром `--mode single`, который выполняет одну итерацию обучения.

---

##### Шаг 5: **Upload new artifacts**
```yaml
- name: Upload new artifacts
  uses: actions/upload-artifact@v4
  with:
    name: training-artifacts
    path: loc/
```
- **`name`**: Имя шага. В данном случае — `Upload new artifacts`.
- **`uses`**: Указывает действие `actions/upload-artifact@v4`, которое используется для загрузки артефактов.
- **`with`**: Передает параметры для действия:
  - **`name`**: Имя артефакта. В данном случае — `training-artifacts`.
  - **`path`**: Путь к файлам или директории, которые нужно загрузить как артефакт. Здесь указана папка loc.

---

##### Шаг 6: **Upload logs**
```yaml
- name: Upload logs
  uses: actions/upload-artifact@v4
  with:
    name: training-logs
    path: training.log
```
- **`name`**: Имя шага. В данном случае — `Upload logs`.
- **`uses`**: Указывает действие `actions/upload-artifact@v4`, которое используется для загрузки логов.
- **`with`**: Передает параметры для действия:
  - **`name`**: Имя артефакта. В данном случае — `training-logs`.
  - **`path`**: Путь к файлу, который нужно загрузить как артефакт. Здесь указан файл `training.log`.

---

### Итоговая структура workflow
1. Клонируется код репозитория.
2. Устанавливаются зависимости из requirements.txt.
3. Загружаются артефакты из предыдущих запусков workflow (если они существуют).
4. Запускается скрипт main.py, который выполняет одну итерацию обучения.
5. Сохраняются новые артефакты (`training-artifacts`) и логи (`training-logs`).

---

### Достоинства
- В качестве артефактов сохраняется логи работы и текущая версия модели, которые доступны для загрузки в разделе **Actions** на GitHub.
- Создание артефактов происходит итеративно (можно контролировать промежуточные результаты).
- Итерации запускаются по расписанию (каждая последующая итерация использует "наработки" предыдущих запусков).