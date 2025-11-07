1. ```brew install vals```
2. ```brew install helm```
3. ```brew install helm-secrets```
4. Запуск minikube
5. Запуск vault

    ```helm install vault hashicorp/vault -n vault -f vault-values.yaml``` # с прокси
    
    Через дашборд смотрим - работает ли vault.

6. ```./deploy.sh``` - запуск приложения с прочитанными из vault секретами.


### Как использовать vault?
1. Прокинуть порты через kubectl
    ```kubectl port-forward pod/vault-0 -n vault 8200:8200```
2. Проходим на localhost:8200/ui
3. Указываем кол-во unseal keys и threshhold - сохраняем токены.
4. Логинимся.
5. Дальше по гайду https://disk.360.yandex.ru/d/TLRdA7tVhKGPJg 40ая минута.

