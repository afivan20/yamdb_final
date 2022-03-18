![example workflow](https://github.com/afivan20/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)
# Документация к API проекта YAMDB (v1)

## Описание
Проект YaMDb собирает отзывы пользователей на различные произведения. 
Он полность готов для автоматического развертывания его на удалленном сервере.

## Как запустить проект на удаленном сервере:
- Сделать форк данного репозитория и клонировать его себе на локальную машину:
```
git clone https://github.com/afivan20/yamdb_final.git
``` 
- Зайти в папку infra и перенести файлы `docker-compose.yaml` и `/nginx/default.conf` на удаленный сервер:
```
scp ./docker-compose.yaml <имя-пользователя>@<ip-address>:~/
```
```
scp ./nginx/default.conf <имя-пользователя>@<ip-address>:~/
```
- Прописать секреты в `https://github.com/<ваш-username>/yamdb_final/settings/secrets/actions`:
<dl>
<dt>для удаленного сервера:</dt>
HOST
USER
<dd>SSH_PASSWORD</dd>

<dt>для базы данных:</dt>
<dd>DB_ENGINE</dd>
<dd>DB_NAME</dd>
<dd>POSTGRES_USER</dd>
<dd>POSTGRES_PASSWORD</dd>
<dd>DB_HOST</dd>
<dd>DB_PORT</dd>

<dt>для логина в DockerHub:</dt>
<dd>DOCKER_USERNAME</dd>
<dd>DOCKER_PASSWORD</dd>

<dt>для уведомлений от Телеграм-бота</dt>
<dd>TELEGRAM_TOKEN</dd>
<dd>TELEGRAM_TO</dd>
</dl>
- Запушить проект на гит-хаб. С помощью CI/CD проект запустит тесты, сделает пуш образа на DockerHub и развернет проект на удаленном сервере, после успешного выполнения всех этапов получите уведомление в Telegram.
- Выполнить миграции на удаленном сервере:
```
sudo docker-compose exec web python manage.py migrate
```
- Подключить статику:
```
docker-compose exec web python manage.py collectstatic --no-input
```
Ресурс доступен на [удаленном сервере](http://178.154.229.26/)

Ознакомиться с документацией - 
[тут](http://178.154.229.26/redoc/)


### Алгоритм получения токена:
#### 1. Получить код подтвержения.
в теле передать JSON
{
  "username": "имя_пользователя",
  "email": "адрес эл. почты"
}
POST-запрос на эндпоинт:
```
/api/v1/auth/signup/
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
/api/v1/auth/token/
```
Использовать полученный токен для авторизации.

### Дополнительные команды:
- Создать Супер Пользовтеля:
```
docker-compose exec web python manage.py createsuperuser
```
- Загрузить тестовую Базу Данных:
```
docker-compose exec web python manage.py importcsv
```
- Посмотреть структуру проекта на сервере:
```
sudo docker-compose run web bash
```
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