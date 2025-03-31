#!/bin/sh
set -e



echo "Запуск MinIO..."
minio server /data --console-address ":9001" &
MINIO_PID=$!


echo "Ожидание готовности MinIO..."
until curl -s http://localhost:9000/minio/health/ready >/dev/null 2>&1; do
  sleep 1
done


echo "Настройка mc alias..."
mc alias set myminio http://localhost:9000 "${MINIO_ROOT_USER}" "${MINIO_ROOT_PASSWORD}"


if ! mc ls myminio/card-files >/dev/null 2>&1; then
  echo "Создание бакета card-files..."
  mc mb myminio/card-files
fi


echo "Добавление пользователя producer..."
mc admin user add myminio producer "${PRODUCER_MINIO_SECRET_KEY}" || echo "Пользователь producer уже существует"

echo "Добавление пользователя consumer..."
mc admin user add myminio consumer "${CONSUMER_MINIO_SECRET_KEY}" || echo "Пользователь consumer уже существует"


mc admin policy attach myminio readwrite --user producer
mc admin policy attach myminio readwrite --user consumer


wait ${MINIO_PID}
