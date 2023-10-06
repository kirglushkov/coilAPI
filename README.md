## Предварительные требования
Перед запуском Docker-контейнеров убедитесь, что у вас установлены следующие компоненты:
- Docker: Чтобы установить Docker, следуйте инструкциям из официальной документации Docker по адресу [https://docs.docker.com/engine/install/](https://docs.docker.com/engine/install/)
- Docker Compose: Если вы планируете использовать файлы `docker-compose.yml` для управления несколькими контейнерами, убедитесь, что у вас установлен Docker Compose. Вы можете установить его, следуя инструкциям из официальной документации Docker Compose по адресу [https://docs.docker.com/compose/install/](https://docs.docker.com/compose/install/)

## Шаги по запуску Docker-контейнеров

1. Клонируйте репозиторий проекта на ваше локальное устройство:

   ```
   git clone <URL репозитория>
   ```

2. Перейдите в каталог проекта:

   ```
   cd <каталог проекта>
   ```

3. Запустите Docker-контейнеры:

     ```
     docker-compose build
     ```

     ```
     docker-compose up
     ```
     для ребилда
     ```
      docker-compose up --build
     ```


## Шаги если докер не запускается

1. Клонируйте репозиторий проекта на ваше локальное устройство:

   ```
   git clone <URL репозитория>
   ```

2. Перейдите в каталог проекта:

   ```
   cd <каталог проекта>
   ```

3. Запустите Docker-контейнеры:

     ```
     pip install -r requirements.txt
     ```
     
     ```
     cd ./test.withoutDocker
     ```
      ```
     python main.py
     ```
