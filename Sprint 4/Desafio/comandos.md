2. **Comandos utilizados neste desafio**:   
    ```bash
    docker build -t name-image .  

    docker images

    docker run --name name-container name-image

    docker ps -a

    docker start <id>

    docker exec -it <id> bash 

    docker run -it --name name-container name-dados

    docker-compose up -d

    docker-compose ps -a

    docker logs <id>

    docker-compose down