# final_attestation_Anatoly_Lapin
## Установка связей между контейнерами:
docker network create -d bridge docker_network

##Разворачивание БД PostgreSQL: 
docker run --name final_attestation_postresSQL-12.9 --network docker_network -p 5432:5432 -e POSTGRES_USER=alapin -e POSTGRES_PASSWORD=1234 -e POSTGRES_DB=final_attestation -d postgres:12.9

##Разворачивание pgAdmin: 
docker run --name pgadmin-dev --network docker_network -e PGADMIN_DEFAULT_EMAIL=ya@mail.ru -e PGADMIN_DEFAULT_PASSWORD=1234 -p 82:80 -d dpage/pgadmin4

##Доступ к pgAdmin: http://localhost:82/

##Установка зависимостей проекта: pip install -r requirements.txt
