Тестовое задание Mailganer:
Написать на Python 2.7* / GO (другие версии или программы не принимаем) небольшой сервис отправки имейл рассылок.
*только версия 2.7 - в работе используем ее. Остальные версии не подойдут.

Возможности сервиса:

1.  Отправка рассылок с использованием html макета и списка подписчиков.
2.  Для создания рассылки использовать ajax запрос. Форма для создания рассылки заполняется в модальном окне. Использовать библиотеки: jquery, bootstrap.
3.  Отправка отложенных рассылок.
4.  Использование переменных в макете рассылки. (Пример: имя, фамилия, день рождения из списка подписчиков)
5.  Отслеживание открытий писем.
6.  Отложенные отправки реализовать при помощи Celery.

P.S.: Способ хранения макетов писем и списков подписчиков на усмотрение исполнителя.

To install, run:

1.  git clone
2.  pip install -r requirements.txt
3.  python manage.py makemigrations
4.  python manage.py migrate
5.  python manage.py collectstatic (if you deploy the project on the server)

create a file .env in the project directory with the following content:

SECRET_KEY=your django secret
DEFAULT_DOMAIN=http://127.0.0.1:8000/ if locally or your server domain
DEFAULT_DOMAIN_IP=127.0.0.1 or your server
IP DEBUG=1 if you want debug-mode otherwise nothing
EMAIL_HOST=smtp.mail.ru or any other service
EMAIL_HOST_USER=your email service login
EMAIL_HOST_PASSWORD=your mail service password or application password
EMAIL_PORT=2525 the port of the mail service (see the documentation of the mail service)
