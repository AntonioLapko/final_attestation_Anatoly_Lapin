# final_attestation_Anatoly_Lapin
БД PostgreSQL 12.9 и СУБД pgAdmin 4 разворачиваются через docker, приложение запускается через IDE. Использую в качестве IDE PyCharm 2022.2. 

Подготовлено два ноутбука с анализом данных выбранного датасета milk_training_data_csv, обучением моделей, определения их точности.
Первый ноутбук (final_attestation_Anatoly_Lapin.ipynb) с моделью машинного обучения CatBoost, второй (knn.ipynb) с моделью машинного обучения kNN (k Nearest Neighbor).

Точность модели CatBoost определена с помощью функций: accuracy_score, f1_score. 
Тоность модели kNN вычислена с помощью средней оценки точности с использованием перекрестной проверки для всех выбранных k.

Обучение модели осуществялось по параметрам: 
- титруемая килостность (перевод из активности кислотности pH);
- температура (temperature);
- цвет (color).

Модели сохранены как файлы проекта: Catboost - model_milk_grade.cbm, kNN - knnpickle_file.

## Установка связей между контейнерами:
docker network create -d bridge docker_network

## Разворачивание БД PostgreSQL: 
docker run --name final_attestation_postresSQL-12.9 --network docker_network -p 5432:5432 -e POSTGRES_USER=alapin -e POSTGRES_PASSWORD=1234 -e POSTGRES_DB=final_attestation -d postgres:12.9

## Разворачивание pgAdmin: 
docker run --name pgadmin-dev --network docker_network -e PGADMIN_DEFAULT_EMAIL=ya@mail.ru -e PGADMIN_DEFAULT_PASSWORD=1234 -p 82:80 -d dpage/pgadmin4

## Доступ к pgAdmin: 
  - http://localhost:82/
  - логин: ya@mail.ru
  - пароль: 1234
Доступ к БД: 
  - логин:  alapin
  - пароль: 1234
  - название БД: final_attestation

## Установка зависимостей проекта: 
pip install -r requirements.txt

## Описание сервиса:
### Модуль работы с записями о качестве партий молока:
1. Создание записи POST /milk
2. Получение всех записей GET /milk
3. Получение записи по номеру партии (параметр: lot) GET /milk/{lot}
4. Изменение записи по номеру партии (параметр: lot) PUT /milk/{lot}
5. Удаление записи по номеру партии (параметр: lot) DELETE /milk/{lot}
6. Внутренний алгоритм классификации партии молока с помощью предобученной моделью машинного обучения CatBoost
7. Внутренний алгоритм перевода активной кислотности pH в титруемую кислотность T

## Планируемое развитие:
1. Добавления модуля работы с моделью машинного обучения: переобучение.
2. Добавление модуля авторизации: ролевая модель (лаборант, администратор).
3. Развитие модуля работы с записями о качестве партий молока:
  - сохранение в БД идентификатор лаборанта, проводившего исследование;
  - выбор модели для классификации.
4. Разработка пользовательского интерфейса.
5. Размещение приложение в контейнере docker.
6. Формирование файла docker-compose.yml для упрощения разворачивания приложения. 
