![example workflow](https://github.com/github/docs/actions/workflows/yamdb_workflow.yml/badge.svg)
# Документация к API проекта YAMDB (v1)

## Описание
Проект YaMDb собирает отзывы пользователей на различные произведения;

## Как запустить проект:
- Клонировать репозиторий и перейти в него в командной строке:
```
git clone https://github.com/afivan20/api_yamdb.git
cd infra_sp2; cd infra
``` 
- Запустить контейнеры Docker в папке с файлом docker-compose.yaml:
```
docker-compose up -d --build
```
- Выполнить миграции внутри проекта:
```
docker-compose exec web python manage.py migrate
```
- Создать Супер Пользовтеля:
```
docker-compose exec web python manage.py createsuperuser
```
- Подключить статику:
```
docker-compose exec web python manage.py collectstatic --no-input
```
- Загрузить тестовую Базу Данных:
```
docker-compose exec web python manage.py importcsv
```
Ресурс доступен в [localhost](http://localhost/)

Ознакомиться с документацией - 
[тут](http://localhost/redoc/)

### Алгоритм получения токена:
#### 1. Получить код подтвержения.
в теле передать JSON
{
  "username": "имя_пользователя",
  "email": "адрес эл. почты"
}
POST-запрос на эндпоинт:
```
localhost/api/v1/auth/signup/
```


в папке sent_emails найти письмо и скопировать полученный код подвтерждения.

#### 2. Получить токен.
в теле передать JSON
{
  "username": "имя_пользователя",
  "confirmation_code": "код_подвтержения"
}
POST-запрос на эндпоинт:
```
localhost/api/v1/auth/token/
```
Использовать полученный токен для авторизации.

### Дополнительные команды:
- Создать дамп (резервную копию) базы:
```
docker-compose exec web python manage.py dumpdata > fixtures.json
#(unicode != UTF-8)
```
- Удалить запущенные контейнеры:
```
docker-compose down -v
```
- Скачать образ с DockerHub:
```
docker pull afivan20/api_yamdb:latest
```

### Автор
_Иван Афанасьев, python-devloper_