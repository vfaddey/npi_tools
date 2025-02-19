#!/bin/bash
set -e


echo "Запуск RabbitMQ..."
rabbitmq-server -detached

echo "Ожидание запуска RabbitMQ..."
until rabbitmqctl status > /dev/null 2>&1; do
  sleep 1
done

RABBITMQ_DEFAULT_USER=${RABBITMQ_DEFAULT_USER:-admin}
RABBITMQ_DEFAULT_PASS=${RABBITMQ_DEFAULT_PASS:-password}
VHOST="my_vhost"


if ! rabbitmqctl list_users | grep -q "^${RABBITMQ_DEFAULT_USER}"; then
  echo "Создание пользователя ${RABBITMQ_DEFAULT_USER}..."
  rabbitmqctl add_user "${RABBITMQ_DEFAULT_USER}" "${RABBITMQ_DEFAULT_PASS}"
  rabbitmqctl set_user_tags "${RABBITMQ_DEFAULT_USER}" administrator
fi


if ! rabbitmqctl list_vhosts | grep -q "^${VHOST}"; then
  echo "Создание виртуального хоста ${VHOST}..."
  rabbitmqctl add_vhost "${VHOST}"
fi


echo "Установка разрешений для пользователя ${RABBITMQ_DEFAULT_USER}..."
rabbitmqctl set_permissions -p "${VHOST}" "${RABBITMQ_DEFAULT_USER}" ".*" ".*" ".*"
rabbitmqctl set_permissions -p "/" "${RABBITMQ_DEFAULT_USER}" ".*" ".*" ".*"

echo "Перезапуск приложения RabbitMQ..."
rabbitmqctl stop_app
rabbitmqctl start_app

echo "Запуск RabbitMQ в переднем плане..."
rabbitmq-server
