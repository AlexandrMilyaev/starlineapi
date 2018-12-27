Набор скриптов для быстрого входа в разработку с использованием StarLine Open API.
Данные скрипты можно использовать как дополнительные материалы к документации на https://developer.starline.ru/.

Примеры использования скриптов:

python3 get_app_code.py -i your_application_id -s your_application_secret

python3 get_app_token.py -i your_application_id -s your_application_secret -c your_application_code

python3 get_slid_user_token.py -a your_application_token -l your_login -p your_password

python3 get_slnet_token.py -s your_slid_token

python3 auth.py -i your_application_id -s your_application_secret -l your_login -p your_password

Установка:

pip install -r requirements.txt