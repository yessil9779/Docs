# [Книга] Kubernetes в действии
## Основы
### Основные понятия Docker
**Layer**. Каждый Docker-образ состоит из слоёв, каждый из которых описывает какую-то инструкцию. Далее — Docker объединяет информацию из каждого слоя, и создает шаблон-образ, из которого запускается контейнер, в котором выполняются инструкции из каждого слоя, который был включен в данный образ.

**Registry**. Хранилище Docker – это репозиторий, в котором хранятся образы Docker и который упрощает обмен этими образами между различными людьми и компьютерами. Когда вы создаете образ, вы можете либо запустить его на компьютере, на котором вы его создали, либо отправить (закачать) образ в хранилище, а затем извлечь (скачать) его на другом компьютере и запустить его там.

**Image**. Образ контейнера на основе Docker – это то, во что вы упаковываете свое приложение и его среду. Он содержит файловую систему, которая будет доступна приложению, и другие метаданные, такие как путь к исполняемому файлу, который должен быть исполнен при запуске образа.

**Container**. Контейнер на основе Docker – это обычный контейнер Linux, созданный из образа контейнера на основе Docker. Выполняемый контейнер – это процесс, запущенный на хосте, на котором работает Docker, но он полностью изолирован как от хоста, так и от всех других процессов, запущенных на нем. Процесс также ограничен ресурсами, имея в виду, что он может получать доступ и использовать только тот объем ресурсов (ЦП, ОЗУ и т. д.), который ему выделен.

Книга не про Docker, так что приведу лишь команды как собрать и запушить контейнер:
```
docker build . -t {name}<:optional_tagname>
docker tag {name} {docker-hub.username}/{name}<:optional_tagname>
docker push {docker-hub.username}/{name}<:optional_tagname>
docker run --name {run_name} -p 8080:8080 -d {image_name}
```

Инструкции Dockerfile:
- `FROM` — задает базовый (родительский) образ. Сообщает Docker о том, чтобы при сборке образа использовался бы базовый образ, который соответствует предоставленному имени и тегу. Базовый образ, кроме того, еще называют родительским образом.
- `LABEL` — описывает метаданные. Например — сведения о том, кто создал и поддерживает образ. Объявление меток не замедляет процесс сборки образа и не увеличивает его размер. Они лишь содержат в себе полезную информацию об образе Docker, поэтому их рекомендуется включать в файл.
- `ENV` — устанавливает постоянные переменные среды, которые будут доступны в контейнере во время его выполнения. Инструкция хорошо подходит для задания констант. -e some_variable_name=a_value
- `RUN` — выполняет команду и создает слой образа. После ее выполнения в образ добавляется новый слой, его состояние фиксируется. Инструкция часто используется для установки в образы дополнительных пакетов.
- `COPY` — копирует в контейнер файлы и папки. Сообщает Docker о том, что нужно взять файлы и папки из локального контекста сборки и добавить их в текущую рабочую директорию образа. Если целевая директория не существует, эта инструкция ее создаст.
- `ADD` — позволяет решать те же задачи, что и COPY. Также, с помощью этой инструкции можно добавлять в контейнер файлы, загруженные из удаленных источников, и распаковывать локальные .tar-файлы.
- `CMD` — описывает команду с аргументами, которую нужно выполнить когда контейнер будет запущен. Аргументы могут быть переопределены при запуске контейнера. В файле может присутствовать лишь одна инструкция CMD.
- `WORKDIR` — задает рабочую директорию для следующей инструкции. С этой директорией работают инструкции COPY, ADD, RUN, CMD и ENTRYPOINT.
- `ARG` — задает переменные для передачи Docker во время сборки образа. В отличие от ENV-переменных, ARG-переменные недоступны во время выполнения контейнера. (--build-arg some_variable_name=a_value)
- `ENTRYPOINT` — предоставляет команду с аргументами для вызова во время выполнения контейнера. Похожа на команду CMD, но параметры, задаваемые в ENTRYPOINT, не перезаписываются в том случае, если контейнер запускают с параметрами командной строки.
- `EXPOSE` — указывает на то, какие порты планируется открыть для того, чтобы через них можно было бы связаться с работающим контейнером. Эта инструкция не открывает порты.
- `VOLUME` — создает точку монтирования — место, которое контейнер будет использовать для постоянного хранения файлов и для работы с такими файлами.

### Minikube
Чтобы развернуть kubernetes локально можно использовать minikube.
```bash
$ brew install minikube
$ minikube start
```

### Архитектура Kubernetes
```txt
+--------------------+     +---------------+
| Kubernetes API     | <-- | kubelet       |
| Scheduler          |     | kube-proxy    |
| Controller Manager |     | Docker (|rkt) |
| etcd               |     |               |
+--------------------+     +---------------+
     Master Node               Cluster Node
```
Master:
- сервер Kubernetes API, с которым взаимодействуете вы и другие компоненты плоскости управления;
- планировщик (**scheduler**), который распределяет приложения (назначает рабочий узел каждому развертываемому компоненту приложения);
- менеджер контроллеров, выполняющий функции кластерного уровня, такие как репликация компонентов, отслеживание рабочих узлов, обработка аварийных сбоев узлов и т. д.;
- **etcd**, надежное распределенное хранилище данных, которое непрерывно сохраняет конфигурацию кластера.

Cluster Node:
- Docker, rkt или другая среда выполнения контейнеров, в которой выполняются контейнеры;
- **kubelet**, агент, который обменивается с сервером API и управляет контейнерами на своем узле;
- служебный прокси Kubernetes (**kube-proxy**), который балансирует нагрузку сетевого трафика между компонентами приложения

## Pods
### Основы
**Pod** (модуль) – это размещенная рядом группа контейнеров, которая представляет собой основной строительный блок в Kubernetes. Все контейнеры пода работают на одном узле. Контейнеры модуля используют одно и то же пространство IP-адресов и портов.
`kubectl get po {podname} -o yaml` - получить конфигурацию пода.
- метаданные (metadata) – включают имя, пространство имен, метки и другую информацию о модуле;
- спецификация (spec) – содержит фактическое описание содержимого модуля, например контейнеры модуля, тома и другие данные;
- статус (status) – содержит текущую информацию о работающем модуле, такую как условие, в котором находится модуль, описание и статус каждого контейнера, внутренний IP модуля, и другую базовую информацию.
```yaml
apiVersion: v1                        <- описание соответствует версии v1 API Kubernetes
kind: Pod                             <- описывается модуль
metadata:
    name: vacancy-api-doc             <- имя модуля
spec:
    containers:
        - image: zinvapel/tsw         <- образ контейнера
          name: vacancy-api-doc       <- имя контейнера
          ports:                      |
              - containerPort: 8080   |<- порты (носит лишь информационный характер)
                protocol: TCP         |
```

`kubectl explain po` - документация по yaml.

`kubectl create -f file.yml` - создает поды согласно описанию.

`kubectl logs {pod-name} -c {container-name}` - прочитать логи.

`kubectl port-forward {pod-name} 8888:8080` - проброс порта с локальной машины.

### Labels
**Label** (метка) – это произвольная пара «ключ-значение», присоединяемая к ресурсу, которая затем используется при отборе ресурсов с помощью селекторов меток.
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: vacancy-api-doc
  labels:                      <- список меток
    type: doc
    env: test
spec:
  containers:
    - image: zinvapel/tsw
      name: vacancy-api-doc
      ports:
        - containerPort: 8080
          protocol: TCP
```

`kubectl get po --show-labels`, `kubectl get po -L creation_method,env` - вывести информацию с метками.

`kubectl label po vacancy-api-doc env=debug --overwrite` - переопределить метки.

Селекторы:
- `kubectl get po -l env=debug`
- `kubectl get po -l env` - все поды у которых есть метка env
- `kubectl get po -l '!env'`
- `kubectl get po -l env!=debug`
- `kubectl get po -l 'env in (debug, test)'`
- `kubectl get po -l 'env notin (debug, test)'`

Можно вешать метки на ноды (узлы).
```bash
$  kubectl get nodes
NAME       STATUS   ROLES    AGE     VERSION
minikube   Ready    master   5h46m   v1.17.2
$  kubectl label node minikube gpu=true
node/minikube labeled
$  kubectl get nodes -l gpu
NAME       STATUS   ROLES    AGE     VERSION
minikube   Ready    master   5h47m   v1.17.2
$  kubectl get nodes -l '!gpu'
No resources found in default namespace.
```

Селектор нод
```yml
apiVersion: v1
kind: Pod
metadata:
  name: vacancy-api-doc
  labels:
    type: doc
    env: test
spec:
  nodeSelector:                |
    gpu: "true"                |<- Расположит только на ноде, у который label gpu=true
  containers:
    - image: zinvapel/tsw
      name: vacancy-api-doc
      ports:
        - containerPort: 8080
          protocol: TCP
```

**Аннотации** в отличие от меток носят только информационный характер.

`kubectl annotate pod vacancy-api-doc somekey='{"type": "ann", "val": "json"}'` - добавление аннотации

`kubectl describe po vacancy-api-doc` - информация о поде.

```yaml
...
metadata:
  annotations:
    json_version: |
      {"key": "value", "key2": "value2"}
...
```

### Namespaces
По-умолчанию все поды привязываются к неймспейсу default. Чтобы случайно не изменить лишние поды, их можно сгруппировать в неймспейсы. Создание неймспейса:
```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: debug-namespace
```
или `kubectl create namespace debug-namespace`.

При создании подов используется опция `--namespace {ns}` если нужно его определить в кастомный неймспейс. Поменять контекст можно командой:
```bash
$ kubectl config set-context $(kubectl config current-context) --namespace debug-namespace
Context "minikube" modified.
$ kubectl get pods
No resources found in debug-namespace namespace.
```

### Удаление
Удаление объектов в kubernetes выполняется командой `kubectl delete {type} [-l ...labels]`. `kubectl delete all --all` удаляет все объекты.

## Репликация
### livenessProbe
Для каждого контейнера в спецификации модуля можно указать проверку живучести. Kubernetes будет периодически выполнять проверку и перезапускать контейнер в случае несработки проверки.
Типы:
- `httpGet` - проверка HTTP GET выполняет запрос HTTP GET на IP-адрес, порт и путь контейнера, которые вы укажете. Если проверка получает отклик и код ответа не представляет ошибку (другими словами, если код отклика HTTP будет 2xx или 3xx), проверка считается сработавшей. Если сервер возвращает отклик с кодом ошибки или вообще не отвечает, то проверка считается несработавшей, и в результате контейнер будет перезапущен;
- `tcpSocket` - проверка сокета TCP пытается открыть TCP-подключение к указанному порту контейнера. Если подключение установлено успешно, то проверка сработала. В противном случае контейнер перезапускается;
- `exec` - проверка Exec выполняет произвольную команду внутри контейнера и проверяет код состояния на выходе из команды. Если код состояния равен 0, то проверка выполнена успешно. Все остальные коды считаются несработавшими.

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: vacancy-api-doc
  labels:
    type: doc
    env: test
spec:
  containers:
    - image: zinvapel/tsw
      name: vacancy-api-doc
      ports:
        - containerPort: 8080
          protocol: TCP
      livenessProbe:            
        httpGet:                <- будет послан GET запрос
          path: /health         <- на этот путь
          port: 8080            <- на этот порт
        initialDelaySeconds: 20 <- первый раз через 20 секунд после запуска контейнера
        periodSeconds: 10       <- и будет опрашивать каждые 10 секунд
        failureThreshold: 10    <- контейнер будет перезапущен если проверка не будет пройдена 10 раз подряд
        timeoutSeconds: 1       <- если контейнер отвечает больше 1 секунды, то проверка помечается как непройденная
```
`kubectl logs mypod --previous` дает логи с предыдущего контейнера, там можно найти код выхода, который формируется как `128 + x`, где `x` - код сигнала.  Код выхода 137 сигнализирует о том, что процесс был убит внешним сигналом (код выхода 128 + 9 (SIGKILL). Аналогичным образом код выхода 143 соответствует 128 + 15 (SIGTERM).

### ReplicationController (deprecated)
**Контроллер репликации** (ReplicationController) – это ресурс Kubernetes, который обеспечивает поддержание постоянной работы его модулей. Если модуль исчезает по любой причине, например в случае исчезновения узла из кластера или потому, что модуль был вытеснен из узла, контроллер репликации замечает отсутствующий модуль и создает сменный модуль.
Контроллер репликации состоит из трех основных частей:
- селектор меток, определяющий, какие модули находятся в области действия контроллера репликации;
- количество реплик, указывающее на требуемое количество модулей, которые должны быть запущены;
- шаблон модуля, используемый при создании новых реплик модуля.
```yaml
apiVersion: v1
kind: ReplicationController
metadata:
    name: rc-vacancy-api-doc
spec:
    replicas: 4
    selector:
        type: doc
        app: vacancy-api
    template:
        metadata:
            name: vacancy-api-doc
            labels:
                type: doc
                app: vacancy-api
                env: prod
        spec:
            containers:
                -
                    image: zinvapel/tsw
                    name: vacancy-api-doc
                    ports:
                        -
                            containerPort: 8080
                            protocol: TCP
```
При смене labels контейнеры не уничтожаются, а просто переходят из-под контроля.
```bash
$ kubectl get pods -L type
NAME                       READY   STATUS    RESTARTS   AGE    TYPE
rc-vacancy-api-doc-5phsj   1/1     Running   0          136m   doc
rc-vacancy-api-doc-7wwnj   1/1     Running   0          136m   doc
rc-vacancy-api-doc-bmpzk   1/1     Running   0          136m   doc
rc-vacancy-api-doc-q2fwx   1/1     Running   0          136m   doc
$ kubectl label po type=test -l type=doc --overwrite
pod/rc-vacancy-api-doc-5phsj labeled
pod/rc-vacancy-api-doc-7wwnj labeled
pod/rc-vacancy-api-doc-bmpzk labeled
pod/rc-vacancy-api-doc-q2fwx labeled
$ kubectl get pods -L type
NAME                       READY   STATUS              RESTARTS   AGE    TYPE
rc-vacancy-api-doc-5phsj   1/1     Running             0          137m   test
rc-vacancy-api-doc-7wwnj   1/1     Running             0          137m   test
rc-vacancy-api-doc-9qdtn   0/1     ContainerCreating   0          3s     doc
rc-vacancy-api-doc-bmpzk   1/1     Running             0          137m   test
rc-vacancy-api-doc-cxvjf   0/1     ContainerCreating   0          3s     doc
rc-vacancy-api-doc-gnnwh   0/1     ContainerCreating   0          3s     doc
rc-vacancy-api-doc-q2fwx   1/1     Running             0          137m   test
rc-vacancy-api-doc-w4n92   0/1     ContainerCreating   0          3s     doc
```

### ReplicaSet
Аналогичны контроллерам, но имеют более выразительные селекторы модуля.
```yaml
apiVersion: apps/v1
kind: ReplicaSet
metadata:
    name: rs-vacancy-api-doc
spec:
    replicas: 2
    selector:
        matchExpressions:
          - key: type
            operator: In
            values:
              - doc
              - test
        matchLabels:
            type: doc
            app: vacancy-api
    template:
        metadata:
            name: vacancy-api-doc
            labels:
                type: doc
                app: vacancy-api
                env: prod
        spec:
            containers:
                -
                    image: zinvapel/tsw
                    name: vacancy-api-doc
                    ports:
                        -
                            containerPort: 8080
                            protocol: TCP
```
`matchExpressions` может быть:
- In – значение метки должно совпадать с одним из указанных значений
values;
- NotIn – значение метки не должно совпадать с любым из указанных значений values;
- Exists – модуль должен содержать метку с указанным ключом (значение не важно). При использовании этого оператора не следует указывать поле values;
- DoesNotExist – модуль не должен содержать метку с указанным ключом. Свойство values не должно быть указано.
`kubectl scale rs rs-vacancy-api-doc --replicas 3` - увеличить количество реплик

### DaemonSet
**DaemonSet** запускает ровно по одному контейнеру на каждой ноде
```yaml
apiVersion: apps/v1
kind: DaemonSet
metadata:
    name: ds-vacancy-api-doc
spec:
    selector:
        matchLabels:
            type: doc
            app: vacancy-api
    template:
        metadata:
            name: vacancy-api-doc
            labels:
                type: doc
                app: vacancy-api
                env: prod
        spec:
            containers:
                -
                    image: zinvapel/tsw
                    name: vacancy-api-doc
                    ports:
                        -
                            containerPort: 8080
                            protocol: TCP
```

### Job
Job - модуль, контейнер которого не перезапускается, когда процесс, запущенный внутри, заканчивается успешно. 
```yaml
aapiVersion: batch/v1
kind: Job
metadata:
    name: echo-job
spec:
    completions: 4                   <- количество заданий, которые надо выполнить
    parallelism: 2                   <- количество параллельных заданий
    activeDeadlineSeconds: 10        <- количество секунд, выделенное на выполнение
    backoffLimit: 2                  <- количество попыток
    template:
        metadata:
            labels:
                env: prod
        spec:
            restartPolicy: OnFailure <- что делать при ошибке
            containers:
                - name: echo
                  image: busybox
                  command:
                      - echo
                      - "Hello world"
```
`restartPolicy`:
- `OnFailure` - перезапускать при ошибке
- `Never` - не перезапускать
` kubectl scale job rs-vacancy-api-doc --replicas 30` - увеличить количество заданий.

### CronJob
Выполнение периодических заданий
```yaml
apiVersion: batch/v1beta1
kind: CronJob
metadata:
    name: echo-cron-job
spec:
    schedule: "* * * * *"
    jobTemplate:
        spec:
            completions: 4
            parallelism: 2
            activeDeadlineSeconds: 10
            backoffLimit: 2
            template:
                metadata:
                    labels:
                        env: prod
                spec:
                    restartPolicy: OnFailure
                    containers:
                        - name: echo
                          image: busybox
                          command:
                              - echo
                              - "Hello world"
```

## Services
### Зачем
Сервисы предоставляют доступ к подам
- поды эфемерны – они могут появляться и исчезать в любое время;
- Kubernetes назначает IP-адрес модулю, после того как модуль был назначен узлу, и до момента его запуска – следовательно, клиенты не могут знать заранее IP-адрес серверного модуля;
- горизонтальное масштабирование означает, что несколько модулей могут обеспечивать одну и ту же службу – каждый из этих модулей имеет свой собственный IP-адрес. Клиенты не должны заботиться о том, сколько модулей поддерживают службу и каковы их IP-адреса.

### Внутренние службы
Определение службы
```yaml
apiVersion: v1
kind: Service
metadata:
    name: doc
spec:
    ports:
      - port: 80
        targetPort: 8080
    selector:
        type: doc
        app: vacancy-api
 ```
Таким образом мы определяем сервис, у которого открыт 80 порт и который перенаправляет все запросы случайному под из набора селекторов. Если указать в spec сервиса `sessionAffinity: ClientIP` (по-умолчанию None), то клиенты с одного IP адреса будут попадать на один и тот же бэкенд. 

Можно использовать несколько портов и даже давать им имена.
```yaml
apiVersion: apps/v1
kind: ReplicaSet
metadata:
    name: rs-vacancy-api-doc-v2
spec:
    selector:
        matchLabels:
            type: doc-v2
            app: vacancy-api-v2
    replicas: 2
    template:
        metadata:
            name: vacancy-api-doc-v2
            labels:
                type: doc-v2
                app: vacancy-api-v2
        spec:
            containers:
                -
                    image: zinvapel/tsw
                    name: vacancy-api-doc
                    ports:
                        -
                            name: http           <-+
                            containerPort: 8080    |
                            protocol: TCP          |
                        -                          |
                            name: https            |
                            containerPort: 8433    |
                            protocol: TCP          |
                                                   |
---                                                |-- Именованный порт
apiVersion: v1                                     |
kind: Service                                      |
metadata:                                          |
    name: doc-v2                                   |
spec:                                              |
    ports:                                         |
        -                                          |
            name: http                             |
            port: 80                               |
            targetPort: http                     <-+
        -
            name: https
            port: 443
            targetPort: https
    selector:
        type: doc-v2
        app: vacancy-api-v2
```
`kubectl exec pod/rs-vacancy-api-doc-v2-vlqwd -- env` - выполнить команду.
```bash
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
HOSTNAME=rs-vacancy-api-doc-v2-vlqwd
KUBERNETES_SERVICE_PORT_HTTPS=443
KUBERNETES_PORT=tcp://10.96.0.1:443
DOC_V2_PORT_443_TCP=tcp://10.108.164.135:443
DOC_V2_SERVICE_HOST=10.108.164.135
DOC_PORT_80_TCP_PROTO=tcp
DOC_V2_PORT_443_TCP_PORT=443
KUBERNETES_SERVICE_HOST=10.96.0.1
KUBERNETES_PORT_443_TCP=tcp://10.96.0.1:443
DOC_SERVICE_HOST=10.96.135.142
DOC_V2_SERVICE_PORT=80
DOC_V2_PORT_443_TCP_PROTO=tcp
DOC_PORT_80_TCP_ADDR=10.96.135.142
DOC_SERVICE_PORT=80
DOC_PORT_80_TCP=tcp://10.96.135.142:80
DOC_PORT_80_TCP_PORT=80
DOC_V2_SERVICE_PORT_HTTPS=443
DOC_V2_PORT=tcp://10.108.164.135:80
KUBERNETES_SERVICE_PORT=443
DOC_V2_PORT_80_TCP_ADDR=10.108.164.135
DOC_V2_PORT_443_TCP_ADDR=10.108.164.135
KUBERNETES_PORT_443_TCP_PROTO=tcp
KUBERNETES_PORT_443_TCP_PORT=443
DOC_V2_PORT_80_TCP=tcp://10.108.164.135:80
DOC_V2_PORT_80_TCP_PROTO=tcp
DOC_V2_PORT_80_TCP_PORT=80
KUBERNETES_PORT_443_TCP_ADDR=10.96.0.1
DOC_V2_SERVICE_PORT_HTTP=80
DOC_PORT=tcp://10.96.135.142:80
NGINX_VERSION=1.17.7
NJS_VERSION=0.3.7
PKG_RELEASE=1
API_KEY=**None**
SWAGGER_JSON=/usr/share/nginx/html/api-doc/swagger.yml
PORT=8080
BASE_URL=
HOME=/root
```

### DNS
Под запускает DNS-сервер, для использования которого автоматически настраиваются все остальные модули, работающие в кластере (Kubernetes делает это, изменяя файл /etc/resolv.conf каждого контейнера). Любой DNS-запрос, выполняемый процессом, запущенным в модуле, будет обрабатываться собственным DNS-сервером Kubernetes, который знает все службы, работающие в вашей системе. 

С помощью свойства [dnsPolicy](https://kubernetes.io/docs/concepts/services-networking/dns-pod-service/#pod-s-dns-policy) в поле spec ресурса каждого модуля можно настроить, будет модуль использовать внутренний DNS-сервер или нет.

Каждая служба получает DNS-запись во внутреннем DNS-сервере, и клиентские модули, которые знают имя службы, могут обращаться к ней через полностью квалифицированное доменное имя (FQDN) вместо использования переменных среды.
`{service-name}.default.svc.cluster.local` - так выглядит доменное имя, причем суффикс можно опустить.

### Endpoints
При создании сервиса неявно создается свойство Endpoints с адресами управляемых подов.
```bash
$ kubectl describe service/doc-v2
Name:              doc-v2
Namespace:         default
Labels:            <none>
Annotations:       <none>
Selector:          app=vacancy-api-v2,type=doc-v2
Type:              ClusterIP
IP:                10.108.164.135
Port:              http  80/TCP
TargetPort:        http/TCP
Endpoints:         172.17.0.6:8080,172.17.0.7:8080 <- Вот здесь
Port:              https  443/TCP
TargetPort:        https/TCP
Endpoints:         172.17.0.6:8433,172.17.0.7:8433
Session Affinity:  None
Events:            <none>
```
Список Endpoints можно создать самостоятельно и сделать службу для внешнего ресурса, например.
```yaml
apiVersion: v1
kind: Service
metadata:
    name: external-service  <-+
spec:                         |
    ports:                    |
        - port: 80            |
                              |-- Одинаковые имена
---                           |
apiVersion: v1                |
kind: Endpoints               |
metadata:                     |
    name: external-service  <-+
subsets:
    - addresses:
        - ip: 11.11.11.11
        - ip: 22.22.22.22
    - ports:
        - port: 80
 ```
 
### Alias
Можно создать псевдоним для внешней службы (технически создается CNAME во внутреннем DNS-сервере)
```yaml
apiVersion: v1
kind: Service
metadata:
    name: external-service
spec:
    type: ExternalName
    externalName: someapi.somecompany.com <- Служба доступна по имени сервиса (external-service внутри кластера)
    ports:
        - port: 80 
 ```
 
### NodePort
Можно пробрасывать порт с каждого узла до сервиса.
```yaml
apiVersion: v1
kind: Service
metadata:
    name: doc
spec:
    type: NodePort
    ports:
        -
            name: http
            port: 80
            targetPort: http
            nodePort: 31000
    selector:
        type: doc
        app: vacancy-api
```
 
### LoadBalancer
Кластеры Kubernetes, работающие на облачных провайдерах, обычно поддерживают автоматическое резервирование балансировщика нагрузки из облачной инфраструктуры. 
```yaml
apiVersion: v1
kind: Service
metadata:
    name: doc
spec:
    type: LoadBalancer
    ports:
        -
            name: http
            port: 80
            targetPort: http
    selector:
        type: doc
        app: vacancy-api
```
Балансировщику будет выдан externalIp. `externalTrafficPolicy: Local` делает так, чтобы трафик шел к поду, который работает на том же узле, что и получил подключение. 

IP адрес клиента недоступен внутри кластера.

### Ingress
Одна из важных причин заключается в том, что для каждой службы LoadBalancer требуется собственный балансировщик нагрузки с собственным общедоступным IP-адресом, в то время как для Ingress’а требуется только один, даже когда предоставляется доступ к десяткам служб. Когда клиент отправляет HTTP-запрос ко входу, хост и путь в запросе определяют, к какой службе этот запрос перенаправляется.
```yaml
apiVersion: networking.k8s.io/v1beta1
kind: Ingress
metadata:
    name: vacancy-api-doc-ingress
    annotations:
        nginx.ingress.kubernetes.io/rewrite-target: /$1
spec:
    rules:
        -
            host: vacancy.api-doc.local
            http:
                paths:
                    -
                        path: /other
                        backend:
                            serviceName: other-service
                            servicePort: 80
                    -
                        backend:
                            serviceName: vacancy-api-doc-http
                            servicePort: 80
```
Чтобы добавить HTTPS, нужно сгенерировать ключи, создать секрет и прописать их в секции spec.tls.
```bash
$ openssl genrsa -out tls.key 2048
$ openssl req -new -x509 -key tls.key -out tls.cert -days 360 -subj /CN=vacancy.api-doc.local
$  kubectl create secret tls tls-secret --cert=tls.cert --key=tls.key
secret "tls-secret" created
```
```yaml
...
spec:
    tls:
        -
            hosts:
                - vacancy.api-doc.local
            secretName: tls-secret
...
```

### Readiness Probe
По аналогии с livenessProbe, существует readinessProbe. На контейнер не будут подаваться запросы с сервиса, если проверка не прошла.
```yaml
apiVersion: apps/v1
kind: ReplicaSet
metadata:
    name: vacancy-api-doc-rs
spec:
    selector:
        matchLabels:
            type: doc
            app: vacancy-api
    replicas: 2
    template:
        metadata:
            name: vacancy-api-doc
            labels:
                type: doc
                app: vacancy-api
        spec:
            containers:
                -
                    image: zinvapel/tsw
                    name: vacancy-api-doc
                    ports:
                        -
                            name: http
                            containerPort: 8080
                            protocol: TCP
                    readinessProbe:
                        exec:
                            command:
                                - ls
                                - /var/ready
```

### Headless
Kubernetes позволяет клиентам обнаруживать IP-адреса модулей посредством поиска в DNS. Обычно, когда вы выполняете DNS-запрос, DNS-сервер возвращает единственный кластерный IP-адрес службы. Но если вы сообщите системе Kubernetes, что для вашей службы вам не нужен кластерный IP-адрес (это можно сделать, присвоив полю clusterIP значение None в спецификации службы), то вместо единственного IP-адреса службы DNS-сервер будет возвращать IP-адреса модулей. 

Вместо того чтобы возвращать одну A-запись DNS, DNS-сервер будет возвращать для службы несколько A-записей, каждая с указанием на IP-адрес отдельного модуля, поддерживающего службу в данный момент. 
```yaml
apiVersion: v1
kind: Service
metadata:
    name: vacancy-api-doc-http
    annotations:
        service.alpha.kubernetes.io/tolerate-unready-endpoints: "true" <- указание этой аннотации говорит показыывать IP адреса даже неготовых сервисов
spec:
    clusterIP: None
    type: NodePort
    ports:
        -
            name: http
            port: 80
            targetPort: http
    selector:
        type: doc
        app: vacancy-api
```

## Персистентность
### Volume
**Volume** существует в рамках пода и может использоваться совместно для всех контейнеров пода. Список типов:
- emptyDir – простой пустой каталог, используемый для хранения временных данных;
- hostPath – используется для монтирования каталогов из файловой системы рабочего узла в модуль;
- gitRepo – том, инициализируемый в ходе проверки содержимого репозитория Git;
- nfs – общий ресурс NFS, монтируемый в модуле;
- gcePersistentDisk (Google Compute Engine Persistent Disk), awsElasticBlockStore (Amazon Web Services Elastic Block Store Volume), azureDisk (Microsoft Azure Disk Volume) – используются для монтирования систем хранения данных, специфичных для поставщика облачных служб;
- cinder, cephfs, iscsi, flocker, glusterfs, quobyte, rbd, flexVolume, vsphereVolume, photonPersistentDisk, scaleIO – используются для монтирования других типов сетевых хранилищ;
- configMap, secret, downwardAPI – специальные типы томов, используемые для предоставления модулю определенных ресурсов Kubernetes и кластерной информации;
- persistentVolumeClaim – способ использовать заранее или динамически резервируемое постоянное хранилище.

### emptyDir
**emptyDir** создает пустой Volume, при этом он перетирает всё что туда пытаются положить контейнеры.
```yaml
apiVersion: apps/v1
kind: ReplicaSet
metadata:
    name: php-info-rs
spec:
    selector:
        matchLabels:
            app: php-info
    replicas: 2
    template:
        metadata:
            name: php-info
            labels:
                app: php-info
        spec:
            containers:
                - image: zinvapel/php-info:0.0.4
                  name: php-info-php
                  volumeMounts:
                    - mountPath: /var/run
                      name: php-socket
                    - mountPath: /var/www
                      name: php-code
                - image: zinvapel/php-info-nginx:0.0.4
                  name: php-info-nginx
                  ports:
                    - containerPort: 8080
                      name: http
                  volumeMounts:
                    - mountPath: /var/run
                      name: php-socket
                    - mountPath: /var/www
                      name: php-code
            volumes:
              - name: php-socket
                emptyDir: {}
              - name: php-code
                emptyDir: {}

---
apiVersion: v1
kind: Service
metadata:
    name: php-info-http
spec:
    type: NodePort
    ports:
        -
            name: http
            port: 80
            targetPort: http
    selector:
        app: php-info
```

### gitRepo
Аналог emptyDir, но в созданную директорию выкачивается репозиторий.
```yaml
gitRepo:
 repository: https://github.com/owner/app.git
 revision: master
 directory: .
```

В текущий момент считается deprecated и рекомендуется использовать initController.

### hostPath
Том hostPath указывает на определенный файл или каталог в файловой системе узла. Модули, работающие на одном узле и использующие один и тот же путь в томе hostPath, видят одни и те же файлы.
```yaml
hostPath:
    path: /var/www/vacancy
```

### Persistent Volume
Чтобы скрыть фактическую инфраструктуру хранилища как от приложения, так и от его разработчика используется PersistentVolume и PersistentVolumeClaim.
```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
    name: test-pv
spec:
    capacity:
        storage: 1G
    accessModes:
        - ReadWriteOnce                    
        - ReadOnlyMany
    persistentVolumeReclaimPolicy: Retain
    hostPath:
      path: /var/storage/test
```

`persistentVolumeReclaimPolicy` — что будет происходить с pv после удаления pvc. 
- `Retain` — pv удален не будет.
- `Recycle` — pv будет очищен.
- `Delete` — pv будет удален.

`accessModes` - режимы доступа.
- RWO – ReadWriteOnce – только один узел может монтировать том для чтения и записи;
- ROX – ReadOnlyMany – несколько узлов могут монтировать том для чтения;
- RWX – ReadWriteMany – несколько узлов могут монтировать том как для чтения, так и для записи.

Когда пользователю кластера необходимо использовать постоянное хранилище в одном из своих модулей, он сначала создает манифест с заявкой PersistentVolumeClaim, указывая минимальный размер и требуемый режим доступа. 

Затем пользователь отправляет манифест с заявкой PersistentVolumeClaim в API-сервер Kubernetes, и Kubernetes находит соответствующий ресурс PersistentVolume и связывает его с заявкой.

Заявка PersistentVolumeClaim затем может использоваться как один из томов в модуле. Другие пользователи не могут использовать тот же том PersistentVolume до тех пор, пока он не будет высвобожден путем удаления связанной заявки PersistentVolumeClaim.
```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: test-pvc
spec:
  resources:
    requests:
      storage: 1G
  accessModes:
    - ReadWriteOnce
  storageClassName: ""

---
apiVersion: v1
kind: Pod
metadata:
  name: test-p
spec:
  containers:
    - name: bb
      image: busybox
      command: ["sleep", "900000"]
      volumeMounts:
        - mountPath: /var/volumes/test
          name: data
  volumes:
    - name: data
      persistentVolumeClaim:
        claimName: test-pvc
```

При установлении значения persistentVolumeReclaimPolicy в Retain, без администратора нельзя будет переназначить PersistentVolume, так как там могут остаться данные от предыдущего контейнера.

### StorageClass
Администратор кластера, вместо того чтобы создавать ресурсы PersistentVolume, может развернуть поставщика (provisioner) ресурса PersistentVolume и определить один или более объектов StorageClass, чтобы позволить пользователям выбрать, какой тип ресурса PersistentVolume они хотят. Пользователи могут ссылаться на класс хранилища StorageClass в своих заявках PersistentVolumeClaim, и поставщик будет принимать это во внимание при резервировании постоянного хранилища.
```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
    name: fast
provisioner: k8s.io/minikube-hostpath <- плагин, используемый для резервирования
reclaimPolicy: Retain
parameters:
    type: pd-ssd                      <- параметры, передаваемые плагину
```

Вот так выглядит заявка
```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
    name: test-pvc-2
spec:
  resources:
    requests:
      storage: 1G
  accessModes:
    - ReadWriteOnce
  storageClassName: fast
```

По-умолчанию уже существует один StorageClass, к которому привязываются заявки, у которых не указан storageClassName
```bash
$ kubectl get sc
NAME                 PROVISIONER                RECLAIMPOLICY   VOLUMEBINDINGMODE   ALLOWVOLUMEEXPANSION   AGE
fast                 k8s.io/minikube-hostpath   Delete          Immediate           false                  10m
standard (default)   k8s.io/minikube-hostpath   Delete          Immediate           false                  169m
```

Именно поэтому для привязки к конкретному PersistentVolume мы указываем `storageClassName: ""`.

## Конфигурация и секреты
### Аргументы командной строки
В файле Dockerfile две инструкции определяют две части:
- ENTRYPOINT определяет исполняемый файл, вызываемый при запуске контейнера;
- CMD задает аргументы, которые передаются в точку входа.
```
...
ENTRYPOINT ["/bin/script.sh"]
CMD ["10"]
```
```bash
$ docker run image 
10 was passed
$ docker run image 15
15 was passed
```

В Kubernetes при указании контейнера можно переопределять и инструкцию ENTRYPOINT, и инструкцию CMD. 
```yaml
...
kind: Pod
spec:
    containers:
        – image: some/image
          command: ["/bin/command"]
          args: ["arg1", "arg2", "arg3"]
...
```

### Переменные окружения
Kubernetes позволяет передавать переменные окружения в контейнер.
```yaml
...
kind: Pod
spec:
    containers:
        – image: some/image
          env:
              - name: FIRST_VAR
                value: "foo"
              - name: SECOND_VAR
                value: "$(FIRST_VAR)bar"
...
```

### ConfigMap
Kubernetes позволяет выделить параметры конфигурации в отдельный объект, называемый ConfigMap, который представляет собой ассоциативный массив, содержащий пары ключ-значение, где значения варьируются от коротких литералов до полных файлов конфигурации.
```bash
$ kubectl create configmap my-config \
    --from-file=foo.json \         # - файл
    --from-file=bar=foobar.conf \  # файл с собственным ключом
    --from-file=config-opts/ \     # весь каталог
    --from-literal=some=thing      # строка
```

Использование литералов
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
    name: test-cm
data:
    key.public: |
        qewhoiqhweoifhoiewhf
        qwehjofhqewohfoie2h3fiohqew
        qwehfoiqwehofiq2h034hf9283g4f78108
        1fy23f7t231f132ty912yf912
    sleep: "10"

---
apiVersion: v1
kind: Pod
metadata:
    name: cm-testing-pod
spec:
    containers:
        - name: busybox
          image: busybox
          command: [sleep, "99999999"]
          env:
              - name: SLEEP_TIME         | 
                valueFrom:               | 
                    configMapKeyRef:     |
                        optional: true   | <- Использование в качестве env
                        name: test-cm    |
                        key: sleep       |

---
apiVersion: v1
kind: Pod
metadata:
    name: cm-testing-pod-v2
spec:
    containers:
        - name: busybox
          image: busybox
          command: [sleep, "99999999"]
          envFrom:
              - prefix: CONFIG_          |
                configMapRef:            | <- Копируем весь Volume и задаем префикс
                    name: test-cm        |
```

```bash
$ kubectl exec cm-testing-pod -- env
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
HOSTNAME=cm-testing-pod
SLEEP_TIME=10
HOME=/root
$ kubectl exec cm-testing-pod-v2 -- env
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
HOSTNAME=cm-testing-pod-v2
CONFIG_key.public=qewhoiqhweoifhoiewhf
qwehjofhqewohfoie2h3fiohqew
qwehfoiqwehofiq2h034hf9283g4f78108
1fy23f7t231f132ty912yf912

CONFIG_my.key=vwebiohoivrhiovrhiowerhioiohirwovrwhiovrhiovrhiovrhio

CONFIG_sleep=10
HOME=/root
```

Использование файлов:
```yaml
apiVersion: apps/v1
kind: ReplicaSet
metadata:
    name: php-info-rs
spec:
    selector:
        matchLabels:
            app: php-info
    replicas: 2
    template:
        metadata:
            name: php-info
            labels:
                app: php-info
        spec:
            containers:
                - image: zinvapel/php-info:0.0.4
                  name: php-info-php
                  volumeMounts:
                    - mountPath: /var/run
                      name: php-socket
                    - mountPath: /var/www/index.php
                      name: php-code
                      subPath: index.php                 | <- Монтируем только 1 файл
                - image: nginx
                  name: php-info-nginx
                  ports:
                    - containerPort: 8080
                      name: http
                  volumeMounts:
                    - mountPath: /var/run
                      name: php-socket
                    - mountPath: /var/www/index.php
                      name: php-code
                      subPath: index.php
                    - mountPath: /etc/nginx/conf.d        | <- Монтируем в директорию
                      name: nginx-config
            volumes:
              - name: php-socket
                emptyDir: {}
              - name: php-code
                configMap:                                | Volume типа configMap
                    name: php-info-nginx-config           | имя ConfigMap
                    items:                                | В volume помеваем только значения по ключам
                      - key: index.php                    | Значение по ключу `index.php`
                        path: index.php                   | Кладем в файл `index.php`
                    defaultMode: 0777                     | Права
              - name: nginx-config
                configMap:
                    name: php-info-nginx-config           | А здесь копируем все вместе

---
apiVersion: v1
kind: Service
metadata:
    name: php-info-http
spec:
    type: NodePort
    ports:
        -
            name: http
            port: 80
            targetPort: http
    selector:
        app: php-info

---
apiVersion: v1
kind: ConfigMap
metadata:
    name: php-info-nginx-config
data:
    php-info.conf: |
        server {
            listen          8080 default_server;
            server_name     php-info.local;
            charset         utf-8;

            root /var/www;

            location / {
                try_files $uri /index.php$is_args$args;
            }

            location ~ ^/index\.php(/|$) {
                fastcgi_pass unix:/var/run/php-fpm.sock;
                fastcgi_split_path_info ^(.+\.php)(/.*)$;
                include fastcgi_params;

                fastcgi_param SCRIPT_FILENAME $realpath_root$fastcgi_script_name;
                fastcgi_param DOCUMENT_ROOT $realpath_root;

                internal;
            }

            location ~ \.php$ {
                return 404;
            }

            error_log /var/log/nginx/error.log;
            access_log /var/log/nginx/access.log;
        }
    index.php: |
        <?php

        phpinfo();
```

Когда копируется вся директория, то при обновлении ConfigMap, директория обновляется автоматически. Если копируется отдельный файл (subPath), то обновления не происходит. Это достигается за счет того, что на самом деле в ConfigMap хранятся симлинки на настоящие значения.

### Secrets
Secrets похожи на ConfigMap, но в yaml описании содержатся base64-encoded данные.
```yaml
$  kubectl create secret generic php-info --from-literal=POSTGRES_PASS=postgres
secret/php-info created
$ kubectl get secret/php-info -o yaml
apiVersion: v1
data:
  POSTGRES_PASS: cG9zdGdyZXM=
kind: Secret
metadata:
  creationTimestamp: "2020-02-13T17:54:12Z"
  name: php-info
  namespace: default
  resourceVersion: "43455"
  selfLink: /api/v1/namespaces/default/secrets/php-info
  uid: ff97336b-e25b-4b11-99a4-9d4fbcad4289
type: Opaque
```

Чтобы использовать строковые данные, то используется stringData атрибут.
```yaml
apiVersion: v1
kind: Secret
metadata:
    name: php-info-secrets
stringData:
    postgresUser: postgres
    postgresPassword: postgres
data:
    cert.key: c2VjcmV0Cg==
    
---
...
env:
    - name: POSTGRES_PASS
      valueFrom:
        secretKeyRef:
          key: postgresPassword
          name: nginx-secret-config
...
volumes:
  - name: nginx-secret-config
    secret:
        secretName: php-info-secrets
```
secretKeyRef не требует монтирования секрета, нужно обращаться сразу по имени

### Docker registry secret
Docker Hub, помимо общедоступных репозиториев образов, также позволяет создавать приватные репозитории. Вы можете отметить репозиторий как приватный, войдя в http://hub.docker.com с помощью вашего веб-браузера, найдя репозиторий и проставив галочку.
Для запуска модуля, использующего образ из приватного репозитория, необходимо выполнить два действия:
- создать секрет, содержащий учетные данные для реестра Docker;
- указать этот секрет в поле imagePullSecrets манифеста модуля.
```bash
$ kubectl create secret docker-registry mydockerhubsecret \
     --docker-username=myusername --docker-password=mypassword \
     --docker-email=my.email@provider.com
```
```yaml
apiVersion: v1
kind: Pod
metadata:
    name: private-pod
spec:
    imagePullSecrets:
      – name: mydockerhubsecret
    containers:
      – image: username/private:tag
        name: main
```
 
## Метаданные
Downward API позволяет предоставлять собственные метаданные пода процессам, запущенным внутри этого пода.
```yaml
apiVersion: v1
kind: Pod
metadata:
    name: downward
spec:
    containers:
      - name: main
        image: busybox
        command: ["sleep", "9999999"]
        resources:
            requests:
                cpu: 15m
                memory: 100Ki
            limits:
                cpu: 100m
                memory: 4Mi
        env:
          - name: POD_NAME
            valueFrom:
                fieldRef:
                    fieldPath: metadata.name
          - name: POD_NAMESPACE
            valueFrom:
                fieldRef:
                    fieldPath: metadata.namespace
          - name: POD_IP
            valueFrom:
                fieldRef:
                    fieldPath: status.podIP
          - name: NODE_NAME
            valueFrom:
                fieldRef:
                     fieldPath: spec.nodeName
          - name: SERVICE_ACCOUNT
            valueFrom:
                fieldRef:
                    fieldPath: spec.serviceAccountName
          - name: CONTAINER_CPU_REQUEST_MILLICORES
            valueFrom:
                resourceFieldRef:
                    resource: requests.cpu
                    divisor: 1m
          - name: CONTAINER_MEMORY_LIMIT_KIBIBYTES
            valueFrom:
                resourceFieldRef:
                    resource: limits.memory
                    divisor: 1Ki
```

Можно также смонтировать как Volume.
```yaml
apiVersion: v1
kind: Pod
metadata:
    name: downward
spec:
    containers:
      - name: main
        image: busybox
        command: ["sleep", "9999999"]
        volumeMounts:
          - mountPath: /etc/downward
            name: downward
    volumes:
      - name: downward
        downwardAPI:
            items:
                - path: "podName"
                  fieldRef:
                      fieldPath: metadata.name
                - path: "containerCpuRequestMilliCores"
                  resourceFieldRef:
                      containerName: main
                      resource: requests.cpu
                      divisor: 1m
```

### Kubernetes API
Можно общаться с Kubernetes посредством kubectl proxy, либо из контейнера, с помощью переменных окружения `KUBERNETES_SERVICE_*`. Всё, для коннекта лежит в директории ` /var/run/secrets/kubernetes.io/serviceaccount`.
```bash
$ curl --cacert /var/run/secrets/kubernetes.io/serviceaccount/ca.crt https://kubernetes
Unauthorized
$ export CURL_CA_BUNDLE=/var/run/secrets/kubernetes.io/serviceaccount/ca.crt
Unauthorized
$ TOKEN=$(cat /var/run/secrets/kubernetes.io/serviceaccount/token)
$ curl -H "Authorization: Bearer $TOKEN" https://kubernetes
{
     "paths": [
         "/api",
         "/api/v1",
         "/apis",
         "/apis/apps",
         "/apis/apps/v1beta1",
         "/apis/authorization.k8s.io",
         ...
         "/ui/",
         "/version"
     ]
}
```

## Deployments
### Методы деплоя в Kubernetes
Сине-зеленый деплой:
- Выкатавыем новую ReplicaSet
- Меняем В Service селектор (kubectl set selector)
- Удаляем старую версию

Скользящее обновление (rolling update) (+канареечный):
- Уменьшаем количество реплик на старой
- Добавляем на новой понемногу

### Rolling update
kubectl поддерживает команду для автоматического выполнения rolling update, для этого нужно выполнить команду `kubectl rolling-update {replication-controller-name-1} {replication-controller-name-2} --image={new/image:tag}`. Этот метод плох тем, что он выполняется не на сервере и при возникновении система окажется в недодеплоенном состоянии.

Вам следует осознавать, что принятая по умолчанию политика выгрузки образа imagePullPolicy зависит от тега образа. Если контейнер ссылается на тег latest (явно или не указывая тег вообще), по умолчанию imagePullPolicy равняется Always, но если же контейнер ссылаетс

### Deployment
Объект типа Deployment под собой создает ReplicaSet. Его особенностью является то, что он автоматически выполняет развертвование на основании описанной стратегии.
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
    name: echo
spec:
    replicas: 2
    minReadySeconds: 10                | Как долго вновь созданный модуль должен быть в готовности
    revisionHistoryLimit: 3            | Длина истории старых версий
    progressDeadlineSeconds: 60        | Максимальное время на весь деплой
    strategy:
        type: RollingUpdate            | Скользящее окно (Recreate заменяет все контейнеры разом)
        rollingUpdate:                 | Настройки окна
            maxSurge: 1                | Максимальное количество избыточных сервисов в процессе деплоя
            maxUnavailable: 1          | Максимальное количество недостающих сервисов в процессе деплоя
    selector:
        matchLabels:
            app: echo
    template:
        metadata:
            labels:
                app: echo
            name: echo
        spec:
              containers:
                - name: echo
                  image: busybox
                  imagePullPolicy: Always
                  command: ["watch"]
                  args: ["echo", "Hello world", "&&", "sleep", "10"]
```

Выполнять обновления можно с помощью `kubectl apply` или `kubectl set image` (а также `edit`, `patch`, `replace`).
```bash
$ kubectl set image deployment echo nodejs=echo/echo:v2
```

Управление процессом развертывания:
- `kubectl rollout status deployment {name}` - статус
- `kubectl rollout undo deployment {name} <--to-revision=1>` - откатить (опционально до версии)
- `kubectl rollout history deployment {name}` - список версий
- `kubectl rollout pause deployment {name}` - приостановить
- `kubectl rollout resume deployment {name}` - продолжить

## StatefulSet
Наборы ReplicaSet создают множество реплик модуля из одного шаблона модуля. Эти реплики не отличаются друг от друга, кроме как по имени и IP-адресу. Если шаблон модуля содержит том, который относится к конкретной заявке на получение тома постоянного хранения (PersistentVolumeClaim), то все реплики набора реплик ReplicaSet будут использовать ту же заявку и, следовательно, тот же том постоянного хранения PersistentVolume. 

Варианты использования персональных хранилищ:
- Ручное содание подов
- Несколько ReplicaSet по одному поду в каждом
- Поддиректории в Volume
- StatefulSet

Каждому модулю, создаваемому набором StatefulSet, присваивается порядковый индекс (с отсчетом от нуля), который затем используется, чтобы произвести имя и хостнейм модуля, и закрепить за этим модулем надежное хранилище. 
```bash
$ kubectl describe statefulset vacancy-api-db
Name:               vacancy-api-db
Namespace:          default
CreationTimestamp:  Tue, 18 Feb 2020 09:48:35 +0300
Selector:           kind=db
Labels:             <none>
Annotations:        kubectl.kubernetes.io/last-applied-configuration:
                      {"apiVersion":"apps/v1","kind":"StatefulSet","metadata":{"annotations":{},"name":"vacancy-api-db","namespace":"default"},"spec":{"replicas...
Replicas:           2 desired | 2 total
Update Strategy:    RollingUpdate
  Partition:        824633993512
Pods Status:        2 Running / 0 Waiting / 0 Succeeded / 0 Failed
Pod Template:
  Labels:  kind=db
  Containers:
   db:
    Image:      postgres:10
    Port:       5432/TCP
    Host Port:  0/TCP
    Environment:
      POSTGRES_USER:      <set to the key 'postgresUser' in secret 'vacancy-api-secrets'>      Optional: false
      POSTGRES_PASSWORD:  <set to the key 'postgresPassword' in secret 'vacancy-api-secrets'>  Optional: false
    Mounts:
      /var/lib/postgresql/data from pgdata (rw)
  Volumes:  <none>
Volume Claims:
  Name:          pgdata
  StorageClass:  vacancy-api-storage
  Labels:        <none>
  Annotations:   <none>
  Capacity:      1G
  Access Modes:  [ReadWriteOnce]
Events:
  Type    Reason            Age   From                    Message
  ----    ------            ----  ----                    -------
  Normal  SuccessfulCreate  28s   statefulset-controller  create Claim pgdata-vacancy-api-db-1 Pod vacancy-api-db-1 in StatefulSet vacancy-api-db success
  Normal  SuccessfulCreate  28s   statefulset-controller  create Pod vacancy-api-db-1 in StatefulSet vacancy-api-db successful
  
$ kubectl get po
NAME                       READY   STATUS                  RESTARTS   AGE
vacancy-api-db-0           1/1     Running                 1          2d
vacancy-api-db-1           1/1     Running                 0          59s
```

Заявка PersistentVolumeClaim остается после уменьшения масштаба, означает, что последующее увеличение масштаба может повторно закрепить ту же самую заявку вместе со связанным с ней постоянным томом PersistentVolume и его содержимым за новым экземпляром модуля.

Для доступа к подам используются headless-службы, таким образом каждый из подов будет доступен по адресу `{podname}-{podnumber}.{service-name}.{namespace}.svc.cluster.local`
```yaml
apiVersion: v1
kind: Service
metadata:
    name: app-db-srv
spec:
    clusterIP: None                 <- headless служба
    selector:
        kind: db
    ports:
        - port: 5432

---
apiVersion: apps/v1
kind: StatefulSet
metadata:
    name: app-db
spec:
    serviceName: app-db-srv         <- Имя службы
    replicas: 1
    selector:
        matchLabels:
            kind: db
    template:
        metadata:
            labels:
                kind: db
        spec:
            containers:
                - name: db
                  image: postgres:10
                  ports:
                    - containerPort: 5432
                      name: pgport
                  volumeMounts:
                      - mountPath: /var/lib/postgresql/data
                        name: pgdata
                  env:
                      - name: POSTGRES_USER
                        valueFrom:
                            secretKeyRef:
                                name: app-secrets
                                key: postgresUser
                      - name: POSTGRES_PASSWORD
                        valueFrom:
                            secretKeyRef:
                                name: app-secrets
                                key: postgresPassword
    volumeClaimTemplates:
        - metadata:
              name: pgdata
          spec:
              resources:
                  requests:
                      storage: 1G
              accessModes:
                  - "ReadWriteOnce"
              storageClassName: "app-storage"

---
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
    name: app-storage
provisioner: k8s.io/minikube-hostpath
reclaimPolicy: Retain
parameters:
    type: pd-ssd
```

Обнаружить все инстансы можно с помощью DNS:
```bash
$ kubectl run -it srvlookup --image=tutum/dnsutils --rm --restart=Never -- dig SRV app-db-srv.default.svc.cluster.local

; <<>> DiG 9.9.5-3ubuntu0.2-Ubuntu <<>> SRV app-db-srv.default.svc.cluster.local
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 28878
;; flags: qr aa rd; QUERY: 1, ANSWER: 2, AUTHORITY: 0, ADDITIONAL: 3
;; WARNING: recursion requested but not available

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 4096
;; QUESTION SECTION:
;app-db-srv.default.svc.cluster.local. IN SRV

;; ANSWER SECTION:
app-db-srv.default.svc.cluster.local. 30 IN SRV	0 50 5432 app-db-1.vacancy-api-db-srv.default.svc.cluster.local.
app-db-srv.default.svc.cluster.local. 30 IN SRV	0 50 5432 app-db-0.vacancy-api-db-srv.default.svc.cluster.local.

;; ADDITIONAL SECTION:
app-db-1.vacancy-api-db-srv.default.svc.cluster.local. 30 IN A 172.17.0.12
app-db-0.vacancy-api-db-srv.default.svc.cluster.local. 30 IN A 172.17.0.2

;; Query time: 34 msec
;; SERVER: 10.96.0.10#53(10.96.0.10)
;; WHEN: Thu Feb 20 07:29:40 UTC 2020
;; MSG SIZE  rcvd: 477

pod "srvlookup" deleted
```

## Архитектура Kubernetes
### Схема
```txt
             Master Node                           Cluster Node
+--------------------------------------+     +------------------------+
| +------+      +---------------+      |     |     +------------+     |
| | etcd |<---- |   Kubernetes  |<-----+-----+-----| kube-proxy |     |
| +------+      |      API      |<-----+-----+-+   +------------+     |
|               +---------------+      |     | |                      |
|                ^  ^                  |     | |                      |
| +-----------+  |  | +--------------+ |     | |   +------------+     |
| | Scheduler |--+  +-|  Controller  | |     | +---|   Kubelet  |     |
| +-----------+       |    Manager   | |     |     +------------+     |
|                     +--------------+ |     |            |           |
+--------------------------------------+     |            v           |
                                             |   +----------------+   |
                                             |   | Virtualization |   |
                                             |   |     System     |   |
                                             |   |    (Docker)    |   |
                                             |   +----------------+   |
                                             +------------------------+
```
Компоненты плоскости управления, а также kube-proxy могут быть развернуты в системе напрямую или работать как модули.
```bash
$ kubectl get po -o custom-columns=POD:metadata.name,NODE:spec.nodeName --sort-by spec.nodeName -n kube-system
POD                                NODE
coredns-6955765f44-8dx8w           minikube
coredns-6955765f44-xq9pl           minikube
etcd-minikube                      minikube
kube-apiserver-minikube            minikube
kube-controller-manager-minikube   minikube
kube-proxy-kbbsp                   minikube
kube-scheduler-minikube            minikube
storage-provisioner                minikube
```

### etcd
etcd - быстрое, распределенное и согласованное хранилище в формате ключ-значение. Поскольку хранилище etcd является распределенным, для обеспечения высокой доступности и повышения производительности вы можете запускать несколько его экземпляров. 

*Единственным компонентом, который напрямую взаимодействует с хранилищем etcd, является сервер API Kubernetes*. Хранилище etcd является единственным местом, где Kubernetes хранит состояние кластера и метаданные. Kubernetes хранит все свои данные в etcd в /registry. 

Для достижения этого в хранилище etcd используется консенсусный алгоритм RAFT, который гарантирует, что в любой момент состояние каждого узла является либо тем, что большинство узлов соглашается считать текущим состоянием, либо одним из ранее согласованных состояний. Для перехода кластера в следующее состояние консенсусному алгоритму требуется большинство (или кворум). В результате этого, если кластер разделится на две несвязанные группы узлов, состояние в этих двух группах никогда не может расходиться, так как для перехода из предыдущего состояния в новое требуется более половины узлов, принимающих участие в изменении состояния. 

***
Оптимистическое управление параллелизмом (иногда называемое оптимистической блокировкой) – это метод, в котором вместо блокировки порции данных и предотвращения ее чтения или обновления порция данных во время блокировки содержит номер версии. При каждом обновлении данных номер версии увеличивается. При обновлении данных проверяется, увеличился ли номер версии между временем чтения данных клиентом и временем отправки им обновления. Если это происходит, то обновление отклоняется, и клиент должен повторно прочитать новые данные и попытаться обновить их снова.

В результате этого, когда два клиента пытаются обновить одну и ту же запись данных, успешно выполняется только первая.
Все ресурсы Kubernetes содержат поле metadata.resourceVersion, которое клиенты должны передавать обратно на сервер API при обновлении объекта. Если эта версия не совпадает с версией, хранящейся в etcd, то сервер API обновление отклоняет.
***

### Kubernetes API
Kubernetes API предоставляет интерфейс CRUD для запросов и изменения состояния кластера через API RESTful. Он хранит это состояние в хранилище etcd. Одним из клиентов сервера API является инструмент командной строки kubectl.

Прежде чем выполнить запрос клиента, клиент аутентифицируется и авторизовывается. Примеры плагинов контроля допуска:
- AlwaysPullImages – переопределяет политику imagePullPolicy модуля, присваивая ей значение Always и заставляя извлекать образ всякий раз, когда модуль развертывается;
- ServiceAccount – применяет принятую по умолчанию учетную запись службы к модулям, которые не задают ее явно;
- NamespaceLifecycle – предотвращает создание модулей в пространствах имен, которые находятся в процессе удаления, а также в несуществующих пространствах имен;
- ResourceQuota – гарантирует, что модули в определенном пространстве имен используют только такой объем ЦП и памяти, который был выделен пространству имен. 

Сервер API ничего не делает, кроме того что мы обсуждали. Например, он не создает модули при создании ресурса ReplicaSet и не управляет конечными точками службы. Этим занимаются контроллеры в менеджере контроллеров. 

Но сервер API даже не говорит этим контроллерам, что делать. Он лишь позволяет этим контроллерам и другим компонентам наблюдать за изменениями в развернутых ресурсах. Компонент плоскости управления может запросить уведомление при создании, изменении или удалении ресурса. Это позволяет компоненту выполнять любую задачу, необходимую в ответ на изменение метаданных кластера. 

Клиенты следят за изменениями, открывая соединение HTTP с сервером API. Через это соединение клиент будет получать поток изменений в наблюдаемых объектах. 

### Scheduler
Работа планировщика заключается в том, чтобы на основе реализованного в сервере API механизма наблюдения ждать
вновь созданных модулей и назначать узел для каждого нового модуля, для которого узел еще не был задан.

_Планировщик не предписывает выбранному узлу запускать модуль_. Планировщик лишь обновляет определение модуля через сервер API. Затем сервер API уведомляет Kubelet о том, что модуль назначен. Как только агент Kubelet на целевом узле увидит, что модуль назначен на его узел, он создает и запускает контейнеры модуля. Вместо выполнения одного планировщика в кластере можно выполнять несколько планировщиков. Затем для каждого модуля указывать планировщика, который должен назначать конкретный модуль, задав в спецификации модуля свойство schedulerName.

### Controller Manager
Единый процесс менеджера контроллеров в настоящее время объединяет множество контроллеров, выполняющих различные задачи согласования:
- контроллер репликации (контроллер для ресурсов ReplicationController);
- контроллер набора реплик ReplicaSet, набора демонов DaemonSet и задания Job;
- контроллер ресурса развертывания Deployment;
- контроллер набора модулей с внутренним состоянием StatefulSet;
- контроллер узла;
- контроллер службы Service;
- контроллер конечных точек Endpoints;
- контроллер пространства имен Namespace;
- контроллер постоянного тома PersistentVolume;
- другие.

Контроллеры делают много разных вещей, но все они наблюдают за изменениями ресурсов на сервере API и выполняют операции для каждого изменения, будь то создание нового объекта или обновление или удаление существующего объекта. Они никогда не обмениваются друг с другом напрямую. 

### Kubelet
Агент Kubelet – это компонент, отвечающий за все, что выполняется на рабочем узле. Его первоначальная задача – зарегистрировать узел, на котором он работает, путем создания ресурса узла на сервере API.

Затем он должен непрерывно отслеживать сервер API для модулей, которые были назначены на этот узел, и запускать контейнеры модуля. Он это делает, поручая сконфигурированной среде выполнения контейнеров (то есть платформе Docker, CoreOS платформы rkt или чему-то еще) запустить контейнер из конкретного образа контейнера. 

Kubelet постоянно отслеживает запущенные контейнеры и сообщает об их статусе, событиях и потреблении ресурсов серверу API.

Агент Kubelet также является тем компонентом, который выполняет проверки живучести контейнеров, перезапуская контейнеры, когда проверки не срабатывают. 

Наконец, он завершает работу контейнеров, когда их модуль удаляется из сервера API, и уведомляет сервер о том, что модуль прекратил работу.

### Kube-proxy
Цель kube-proxy – убедиться, что клиенты могут подключаться к службам, которые вы определяете посредством API Kubernetes. Сетевой прокси kube-proxy гарантирует, что подключения к IP-адресу и порту службы в итоге окажутся в одном из модулей, привязанных к службе (или других, немодульных, конечных точках службы). Когда служба поддерживается несколькими модулями, прокси выполняет балансировку нагрузки между этими модулями.

Kube-proxy получил свое имя, потому что он представлял собой фактический прокси. Однако текущая, гораздо более эффективная реализация для перенаправления пакетов на случайно выбранный внутренний модуль без передачи их через фактический прокси-сервер использует только правила iptables.

### Надстройки
Надстройки необязательны и включают такие функциональные средства, как DNS-поиск служб Kubernetes, предоставление нескольких служб HTTP через один внешний IP-адрес, веб-панель мониторинга Kubernetes и т. д. Некоторые из этих компонентов развертываются через ресурс развертывания Deployment или ресурс контроллера репликации ReplicationController, а некоторые – через набор демонов DaemonSet.

Модуль DNS-сервера предоставляется через службу kube-dns, что позволяет перемещать модуль по кластеру, как и любой другой модуль. IP-адрес службы указан в качестве nameserver в файле /etc/resolv.conf внутри каждого контейнера, развернутого в кластере. Модуль kube-dns использует механизм отслеживания сервера API для наблюдения за изменениями служб и конечных точек и обновляет свои ресурсные записи DNS с каждым изменением, позволяя своим клиентам всегда получать (относительно) актуальную информацию DNS. Здесь слово «относительно» использовано потому, что во время между обновлением ресурса службы или конечных точек и временем, когда модуль DNS получает уведомление от наблюдения, записи DNS могут быть неактуальными.

Контроллер входа Ingress запускает обратный прокси-сервер (например, Nginx) и держит его сконфигурированным в соответствии с ресурсами входа Ingress, службы Service и конечных точек Endpoints, определенными в кластере. Этот контроллер, следовательно, должен наблюдать за данными ресурсами (опять же, через механизм наблюдения) и изменять конфигурацию прокси-сервера каждый раз, когда один из них изменяется.

Пример цепочки контроллеров на примере Deployment:
- Контроллер развертывания (DeploymentController) создает набор реплик (ReplicaSet) путем обращения к REST Kubernetes.
- Контроллер набора реплик (ReplicaContoller) создает ресурсы подов (PodController) путем обращения к REST Kubernetes.
- Планировщик (scheduler) назначает узел вновь созданным подам.
- Kubelet запускает контейнеры подов.

### Высокодоступность
Для того чтобы сделать Kubernetes высокодоступным, необходимо запустить несколько ведущих узлов, на которых выполняется несколько экземпляров следующих компонентов:
- etcd – распределенное хранилище данных, в котором хранятся все объекты API;
- сервер API (+ балансировщик);
- менеджер контроллеров – это процесс, в котором работают все контроллеры (first leader);
- планировщик (first leader);

## Защита сервера
### Аутентификация
Существует несколько плагинов аутентификации
- из сертификата клиента;
- из токена аутентификации, переданного в заголовке http;
- в результате обычной HTTP-аутентификации;
- другими.

Плагин аутентификации возвращает имя пользователя и группы аутентифицируемого пользователя. Kubernetes различает два вида клиентов, подключающихся к серверу API:
- реальные люди (пользователи);
- поды.

Подразумевается, что пользователи должны управляться внешней системой, такой как система единого входа (Single Sign On, SSO, см. http://kubernetes.io/docs/admin), но модули используют механизм, называемый учетными записями служб, которые создаются и хранятся в кластере как ресурсы ServiceAccount.

Возвращаемые плагином группы являются не чем иным, как строковыми значениями, представляющими произвольные имена групп, однако встроенные группы имеют особое значение:
- группа system:unauthenticated используется для запросов, где ни один из плагинов аутентификации не мог аутентифицировать клиента;
- группа system:authenticated автоматически назначается пользователю, успешно прошедшему аутентификацию;
- группа system:serviceaccounts охватывает все учетные записи ServiceAccount в системе;
- группа system:serviceaccounts:<пространство имен> включает в себя все учетные записи ServiceAccount в определенном пространстве имен.

### ServiceAccount
Имена пользователей учетной записи ServiceAccount форматируются следующим образом `system:serviceaccount:<пространство имен>:<имя учетной записи службы>`.

Учетные записи ServiceAccount – это ресурсы, такие же, как модули, секреты, словари конфигурации и т. д., которые ограничиваются отдельными пространствами имен. Устанавливаемая по умолчанию учетная запись ServiceAccount создается автоматически для каждого пространства имен (именно их и использовали ваши модули все время).

Секрет индивидуально настроенного токена был создан и связан с учетной записью службы. Если посмотреть на данные секрета с помощью команды kubectl describe secret {saname}-token-qzq7j, то можно увидеть, что он содержит те же элементы (сертификат CA, пространство имен и токен), что и у токена учетной записи службы по умолчанию (сам токен, очевидно, будет другим). 

Учетная запись ServiceAccount также может содержать список секретов для выгрузки образов. Добавление секретов выгрузки образов в учетную запись ServiceAccount избавляет от необходимости добавлять их в каждый модуль по отдельности.
```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
    name: my-service-account
imagePullSecrets:
  - name: my-dockerhub-secret
```

После создания дополнительных учетных записей ServiceAccount вам нужно назначить их модулям. Это делается путем выставления в определении модуля имени учетной записи службы в поле `spec.serviceAccountName`.

### RBAC
Управление ролевым доступом RBAC предотвращает несанкционированный просмотр и изменение состояния кластеров. Учетная запись службы по умолчанию не может просматривать состояние кластера, не говоря уже об изменении его каким-либо образом, если только вы не предоставляете ей дополнительные привилегии.

Для Minikube может потребоваться активировать плагин RBAC, запустив Minikube с параметром --extra-config=apiserver.Authorization.Mode=RBAC.

Правила авторизации RBAC настраиваются с помощью четырех ресурсов, которые можно сгруппировать в две группы:
- роли Role и кластерные роли ClusterRole, которые задают, какие глаголы могут выполняться на ресурсах;
- привязки ролей RoleBinding и привязки кластерных ролей ClusterRoleBinding, которые привязывают вышеуказанные роли к определенным пользователям, группам или учетным записям ServiceAccount.

Роли определяют, что вообще можно делать, в то время как привязки определяют, кто может это делать. Различие между ролью и кластерной ролью или между привязкой роли и привязкой кластерной роли состоит в том, что роль и привязка роли являются ресурсами, организованными в пространство имен, тогда как кластерная роль и привязка кластерной роли являются ресурсами уровня кластера.
```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
    namespace: foo                          <- namespace
    name: service-reader
rules:
  - apiGroups: [""]                         <- См. https://kubernetes.io/docs/concepts/overview/kubernetes-api/#api-groups
    verbs: ["get", "list"]                  <- операции
    resources: ["services"]                 <- над какими ресурсами
    resourceNames: ["api-http", "admin-http"] <- только к ресурсам api-http и admin-http (опционально)   
```

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
    namespace: foo
    name: test
roleRef:
    apiGroup: rbac.authorization.k8s.io   |
    kind: Role                            |<- привязывает эту роль
    name: service-reader                  |
subjects:
  - kind: ServiceAccount                  |
    name: default                         |<- к этому ServiceAccount 
    namespace: foo                        |
  - kind: ServiceAccount
    name: default
    namespace: bar                        |<- даем роль к аккаунту из другого namespace
  - kind: User                            |<- даем права пользователю
    name: alice
```

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole                         |<- кластерная роль
metadata:
    name: pv-reader
rules:
  - apiGroups: [""]
    resources: ["persistentvolumes"]
    nonResourceURLs:                      |<- Доступ к URL Kubernetes API
      - "/api"
    verbs: ["get", "list"]
```
Для кластерной роли всегда нужен ClusterRoleBinding. Кластерная роль может ссылаться не на ресурсы, а на URL-пути (вместо поля resources используется поле nonResourceURLs).

Полный контроль над кластером Kubernetes может быть предоставлен путем присвоения субъекту кластерной роли cluster-admin. 

## Защита узлов кластера
### Дополнительные возможности
К поду можно привязать порт узла с помощью `hostPort: 9000`.
Определенные поды (обычно системные) должны работать в стандартных пространствах имен хоста, что позволяет им видеть и управлять ресурсами и устройствами уровня узла. Например, модулю может потребоваться использовать сетевые адаптеры узла вместо собственных виртуальных сетевых адаптеров. Это может быть достигнуто путем присвоения значения true свойству `hostNetwork` в секции spec модуля. Свойства `hostPID` и `hostIPC` секции spec модуля аналогичны параметру hostNetwork. Если задать для них значение true, то контейнеры модуля будут использовать пространства имен PID и IPC узла, позволяя процессам, запущенным в контейнерах, соответственно видеть все другие процессы на узле или взаимодействовать с ними через IPC. 

### Security context
Свойства securityContext могут быть указаны непосредственно в секции spec модуля и внутри секции spec отдельных контейнеров.
- `runAsUser: 405` - запустить от пользователя.
- `runAsNonRoot: true`- запретить root.
- `privileged: true` - привелигерованный режим.
- `readOnlyRootFilesystem: true` - запрет на запись в файловую систему контейнера.
- Возможности ядра:
```yaml
capabilities:
     add:
       – SYS_TIME
     drop:
       – CHOWN
 ```
- fsGroup используется, когда процесс создает файлы в томе, тогда как свойство supplementalGroups определяет список дополнительных идентификаторов групп, с которыми связан пользователь
```yaml
securityContext:
     fsGroup: 555
     supplementalGroups: [666, 777]
```

### PodSecurityPolicy
PodSecurityPolicy – это ресурс кластерного уровня (без пространства имен), который определяет, какие функциональные средства безопасности пользователи могут или не могут использовать в своих модулях. 
```yaml
apiVersion: policy/v1beta1
kind: PodSecurityPolicy
metadata:
    name: default
spec:
    allowedCapabilities:           <- какие возможности МОЖНО добавлять в контейнеры
      - SYS_TIME
    defaultAddCapabilities:        <- какие возможности БУДУТ добавлены в контейнеры
      - CHOWN
    requiredDropCapabilities:      <- какие возможности БУДУТ удалены из контейнеров
      - SYS_ADMIN
    hostIPC: false
    hostPID: false
    hostNetwork: false
    hostPorts:
      - max: 50000
        min: 40000
      - max: 30000
        min: 20000
    privileged: false
    readOnlyRootFilesystem: true
    runAsUser:
        rule: MustRunAsNonRoot
    fsGroup:
        rule: RunAsAny
    supplementalGroups:
        rule: MustRunAs
        ranges:
          - max: 10
            min: 1
    seLinux:
        rule: RunAsAny
    volumes:                      <- можно использовать синтаксис - '*'
      - emptyDir
      – configMap
      – secret
      – downwardAPI
      – persistentVolumeClaim
```

Политики можно привязывать к ролям.
```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
    name: pv-reader
rules:
  - apiGroups: [""]
    resources: ["persistentvolumes"]
    resourceNames: ["default"]
    verbs: ["get", "list"]
```

Можно создавать пользователей.
```bash
$ kubectl config set-credentials alice --username=alice --password=password
User "alice" set.
```

### Изоляция сети модуля
NetworkPolicy применяется к модулям, которые совпадают с ее селектором меток, и указывает либо на то, какие источники могут получать доступ к совпавшим модулям, либо на то, к каким целевым назначениям можно получить доступ из совпавших модулей. Это настраивается посредством правил соответственно входа (ingress) и выхода (egress).
```yaml
---
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
    name: default-deny
spec:
    podSelector:
        matchLabels:
            app: backend            <- к этим модулям
    ingress:                        <- могут подключаться
      - from:                       
          - podSelector:            <- только поды с меткой
            - matchLabels:
                app: frontend
        ports:
          - port: 80                <- только по этому порту

---
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
    name: default-deny
spec:
    podSelector:
        matchLabels:
            app: backend            <- к этим модулям
    ingress:                        <- могут подключаться
      - from:
          - namespaceSelector:      <- только поды из неймспейса
              matchLabels:
                  env: test
        ports:
          - port: 80

---
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
    name: default-deny
spec:
    podSelector:
        matchLabels:
            app: backend            <- эти модули
    egress:                         <- могут подключаться
      - to:
          - ipBlock:                <- только к адресам
              cidr: 192.168.1.0/24  <- с указанным CIDR
        ports:
          - port: 80
```

## Вычислительные ресурсы
### Запрос на ресурсы
При создании модуля можно указать объем ЦП и памяти, необходимый контейнеру.
```yaml
apiVersion: v1
kind: Pod
metadata:
    name: requests-pod
spec:
    containers:
      - image: busybox
        command: ["dd", "if=/dev/zero", "of=/dev/null"]
        name: main
        resources:
            requests:
                cpu: 200m     <- нужно 200 миллиядер (1/5 ядра)
                memory: 10M   <- 10 мегабайт
```

Если на узле не будет достаточно свободной (то есть никем не зарезервированной запросами), то модуль не будет назначен на узел. Под CPU имеется в виду процессорное время.

Kubernetes также позволяет добавлять в узел собственные настраиваемые ресурсы и запрашивать их в ресурсных запросах модуля. Прежде всего вам, очевидно, нужно поставить Kubernetes в известность о вашем, созданном пользователем ресурсе, добавив его в поле capacity объекта Node. Это можно сделать, выполнив HTTP-запрос PATCH. Имя ресурса может быть любым, например example.org/my-resource, – любым до той поры, пока он не начинается с домена kubernetes.io. Заданное количество должно быть целым числом. Это значение будет автоматически скопировано из поля capacity в поле allocatable.

### Лимиты
Не лимитируя память, контейнер (или модуль), работающий на рабочем узле, может съесть всю доступную память и повлиять на все другие модули на узле и любые новые модули, назначаемые узлу.
```yaml
apiVersion: v1
kind: Pod
metadata:
    name: requests-pod
spec:
    containers:
      - image: busybox
        command: ["dd", "if=/dev/zero", "of=/dev/null"]
        name: main
        resources:
            requests:
                cpu: 200m
                memory: 10M
            limits:
                cpu: 400m
                memory: 50M
```

В отличие от ресурсных запросов, ресурсные лимиты не ограничены выделяемыми объемами ресурсов узла. Сумме всех лимитов всех модулей на узле разрешено превышать 100% емкости узла.

Контейнеры всегда видят память узла, а не контейнера. Контейнеры также видят все ядра ЦП узла.

### Классы QoS
Какой контейнер должен быть уничтожен в случае переполнения ресурсов? Kubernetes классифицирует поды на три класса качества обслуживания (QoS):
- BestEffort (самый низкий приоритет);
- Burstable;
- Guaranteed (самый высокий).

| Запросы и лимиты на ЦП | Запросы и лимиты на память | Класс QoS контейнера |
|---|---|---|
| Оба не установлены | Оба не установлены | BestEffort |
| Оба не установлены | Запросы < Лимиты | Burstable |
| Оба не установлены | Запросы = Лимиты | Burstable |
| Запросы < Лимиты | Оба не установлены | Burstable |
| Запросы < Лимиты | Запросы < Лимиты | Burstable |
| Запросы < Лимиты | Запросы = Лимиты | Burstable |
| Запросы = Лимиты | Запросы = Лимиты | Guaranteed |

Из двух контейнеров с одинаковым классом QoS будет уничтожен тот, который в процентном соотношении использует больше своей запрошенной памяти, чем другой.

### LimitRange
LimitRange позволяет указывать (для каждого пространства имен) не только минимальный и максимальный лимит, который можно установить для контейнера по каждому ресурсу, но и стандартные ресурсные запросы для контейнеров, которые не устанавливают запросы явным образом.
```yaml
apiVersion: v1
kind: LimitRange
metadata:
    name: example
spec:
    limits:
      - type: Pod
        min:
            cpu: 50m
            memory: 5Mi
        max:
            cpu: 1
            memory: 1Gi
      - type: Container
        defaultRequest:
            cpu: 100m
            memory: 10Mi
        default:
            cpu: 200m
            memory: 100Mi
        min:
            cpu: 50m
            memory: 5Mi
        max:
            cpu: 1
            memory: 1Gi
        maxLimitRequestRatio: <- Максимальное соотношение между лимитом и запросом на каждый ресурс
            cpu: 4
            memory: 10
      - type: PersistentVolumeClaim
        min:
            storage: 1Gi
        max:
            storage: 10Gi
```

### ResourceQuota
ResourceQuota лимитирует общий объем ресурсов, доступных в пространстве имен. Объект ResourceQuota применяется к пространству имен, в котором он создан, как и объект LimitRange, но он применяется ко всем ресурсным запросам и лимитам модулей в целом, а не к каждому отдельному модулю или контейнеру по отдельности.
```yaml
apiVersion: v1
kind: ResourceQuota
metadata:
    name: cpu-and-mem
spec:
    hard:
        requests.cpu: 400m
        requests.memory: 200Mi

        limits.cpu: 600m
        limits.memory: 500Mi

        requests.storage: 500Gi
        ssd.storageclass.storage.k8s.io/requests.storage: 300Gi
        standard.storageclass.storage.k8s.io/requests.storage: 1Ti

        pods: 10
        replicationcontrollers: 5
        secrets: 10
        configmaps: 10
        persistentvolumeclaims: 4
        services: 5
        services.loadbalancers: 1
        services.nodeports: 2
        ssd.storageclass.storage.k8s.io/persistentvolumeclaims: 2
```

ReqourceQuota также могут быть лимитированы набором областей действия квот. 
```yaml
apiVersion: v1
kind: ResourceQuota
metadata:
    name: cpu-and-mem
spec:
    scopes:
      - BestEffort      <- Класс QoS (NotBestEffort)
      - NotTerminating  <- с неустановленным activeDeadlineSeconds
    hard:
        requests.cpu: 400m
```

### Мониторинг
Kubelet содержит агент cAdvisor, который собирает базовый набор данных о потреблении ресурсов как для отдельных контейнеров, работающих на узле, так и для узла в целом. Для централизованного сбора этих статистических данных по всему кластеру необходимо запустить дополнительный компонент под названием Heapster.

Можно подключить InfluxDB и Grafana.

## Автомасштабирование
### HorizontalPodAutoscaler
Горизонтальное автомасштабирование модуля – это автоматическое масштабирование количества реплик модуля, управляемых контроллером. Оно выполняется горизонтальным контроллером, который активируется и конфигурируется путем создания ресурса HorizontalPodAutoscaler.
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
    name: kubia
spec:
    replicas: 3
    strategy:
        type: RollingUpdate
        rollingUpdate:
            maxSurge: 1
            maxUnavailable: 1
    selector:
        matchLabels:
            app: kubia
    template:
        metadata:
            name: kubia
            labels:
                app: kubia
        spec:
            containers:
              - image: luksa/kubia:v1
                name: nodejs
                resources:
                    requests:
                        cpu: 100m

---
apiVersion: autoscaling/v2beta2
kind: HorizontalPodAutoscaler
metadata:
    name: kubia
spec:
    scaleTargetRef:
        apiVersion: apps/v1
        kind: Deployment
        name: kubia
    minReplicas: 1
    maxReplicas: 10
    metrics:
        - type: Resource
          resource:
              name: cpu
              target:
                  type: Utilization
                  averageUtilization: 50 <- средняя нагрузка на процессор
        - type: Pod
          pods:
            metric:
              name: packets-per-second
            target:
              type: AverageValue
              averageValue: 50          <- средняя количество пакетов
        - type: Object
          object:
              metric:
                  name: requests-per-second
              describedObject:
                  apiVersion: networking.k8s.io/v1beta1
                  kind: Ingress
                  name: main-route
              target:
                  type: Value
                  value: 2k             <- средняя количество запросов
```

Самым простым способом является kubectl `kubectl autoscale deployment kubia --cpu-percent=30 --min=1 --max=5`.

### Горизонтальное масштабирование нод
Новый узел будет зарезервирован, если после создания нового модуля планировщик не сможет назначить его ни на один из существующих узлов. Кластерный автопреобразователь масштаба высматривает такие модули и запрашивает у поставщика облачных служб запустить дополнительный узел. 

Если запросы на ЦП и память всех модулей, работающих на данном узле, ниже 50%, то узел считается ненужным. Если на узле работает системный модуль, то этот узел не будет отменен. Когда узел, который должен быть закрыт, выбран, этот узел сначала помечается как неназначаемый, и тогда все работающие на узле модули вытесняются. 

Узел также может быть помечен как неназначаемый и опустошен вручную. Не вдаваясь в подробности, это делается с помощью следующих ниже команд kubectl:
- kubectl cordon <узел> помечает узел как неназначаемый (но не делает ничего с модулями, работающими на этом узле);
- kubectl drain <узел> помечает узел как неназначаемый, а затем вытесняет все модули узла.
В обоих случаях никакие новые модули узлу не назначаются до тех пор, пока вы снова не разблокируете его командой kubectl uncordon <узел>.

Некоторые службы требуют, чтобы всегда работало минимальное количество модулей; это особенно верно для кластерных приложений на основе кворума. По этой причине Kubernetes предоставляет способ определения минимального количества модулей, которые должны продолжать работать при выполнении этих типов операций. Это делается путем создания ресурса PodDisruptionBudget.

```yaml
apiVersion: policy/v1beta1
kind: PodDisruptionBudget
metadata:
    name: kubia-pdb
spec:
    minAvailable: 3
    maxUnavailable: 1
    selector:
        matchLabels:
            app: kubia
```

## Ограничения и допуски
### Описание
Kubernetes позволяет влиять на то, куда модули назначаются. Первоначально это делалось только путем задания селектора узлов в спецификации модуля, но позже были добавлены дополнительные механизмы, которые расширили эту функциональность. 

На узлы можно наложить ограничения. Ограничения имеют ключ, значение и проявление и представляются в формате <ключ>=<значение>:<проявление>.
```bash
$ kubectl taint node node1.k8s node-type=production:NoSchedule
node "node1.k8s" tainted
```

Существует три возможных проявления:
- Noschedule, которое значит, что модули не будут назначены узлу, если они не допускают ограничения;
- PreferNoSchedule – это мягкая версия NoSchedule, которая означает, что планировщик попытается избежать назначения модуля узлу, но назначит его узлу, если он не может назначить его где-то еще;
- NoExecute, в отличие от проявлений NoSchedule и PreferNoSchedule, которые влияют только на назначение модуля узлу, также влияет на модули, уже работающие на узле. Если в узел добавить ограничение NoExecute, то модули, которые уже работают на этом узле и не допускают ограничения NoExecute, будут вытеснены из узла.

Допуски до работы на узлах определяются в spec.tolerations.
```yaml
apiVersion: v1
kind: Pod
metadata:
    name: requests-pod
spec:
    tolerations:
      - key: node-type
        operator: Equal
        value: production
        effect: NoSchedule
    containers:
      - image: busybox
        command: ["dd", "if=/dev/zero", "of=/dev/null"]
        name: main
        resources:
            requests:
                cpu: 200m
                memory: 10M
            limits:
                cpu: 400m
                memory: 50M
```

### Использование
Допуски также можно использовать, чтобы указать, как долго Kubernetes должен ждать, прежде чем переназначить модуль на другой узел, если узел, на котором работает модуль, становится неготовым или недостижимым. 
```yaml
...
    tolerations:
      – effect: NoExecute
        key: node.alpha.kubernetes.io/notReady
        operator: Exists
        tolerationSeconds: 300
      – effect: NoExecute
        key: node.alpha.kubernetes.io/unreachable
        operator: Exists
        tolerationSeconds: 300
```

### Сходство узлов
По аналогии с nodeSelector есть более гибкий механизм назначения узлов.
```yaml
apiVersion: v1
kind: Pod
metadata:
    name: requests-pod
spec:
    affinity:
      nodeAffinity:
        requiredDuringSchedulingIgnoredDuringExecution:
          nodeSelectorTerms:
            - matchExpressions:
                - key: gpu
                  operator: In
                  values:
                    - "true"
                    - "yes"
```

- requiredDuringScheduling... означает, что правила, определенные в этом поле, задают метки, которые узел должен иметь, чтобы модуль был назначен этому узлу;
- ...IgnoredDuringExecution означает, что правила, определенные под этим полем, не влияют на модули, уже работающие на данном узле (все правила всегда заканчиваются на IgnoredDuringExecution);

Самое большое преимущество функционала сходства узлов – это возможность указывать на то, какие узлы планировщик должен предпочитать при назначении конкретного модуля. Это делается посредством поля preferredDuringSchedulingIgnoredDuringExecution.
```yaml
apiVersion: v1
kind: Pod
metadata:
    name: pod
spec:
    containers:
      - name: pod
        image: busybox
    affinity:
        nodeAffinity:
            preferredDuringSchedulingIgnoredDuringExecution:
              - preference:
                  matchExpressions:
                    - key: availability-zone
                      operator: In
                      values:
                        - zone1
                        - zone2
                weight: 20
              - preference:
                  matchExpressions:
                    - key: some-key
                      operator: In
                      values:
                        - some2
                        - some4
                weight: 20
```

По аналогии с нодами можно указать сходство по подам. По подам также можно задать podAntiAffinity.
```yaml
apiVersion: v1
kind: Pod
metadata:
    name: pod
spec:
    containers:
      - name: pod
        image: busybox
    affinity:
        podAffinity:
            requiredDuringSchedulingIgnoredDuringExecution: <- жесткое требование
              - topologyKey: kubernetes.io/hostname         <- модули этого развертывания должны быть развернуты на том же узле, что и модули
                labelSelector:                              <- которые совпадают с селектором
                    matchLabels:
                        app: backend
```

## Жизненный цикл модуля
### Правила
- Приложения должны ожидать, что они могут быть удалены и перемещены.
- Приложения должны ожидать, что IP-адрес и хостнейм могут быть изменены.
- Приложения должны ожидать, что данные, записанные на диск, исчезнут.
- Использование volume для сохранения данных при перезапусках контейнера.

Если контейнер модуля продолжает сбоить, то агент Kubelet будет бесконечно его перезапускать. Время между перезапусками будет увеличиваться экспоненциально, пока не достигнет пяти минут. Во время этих пятиминутных интервалов модуль, по существу, будет мертвым, потому что процесс его контейнера не работает. 
```bash
$ kubectl get po
NAME READY STATUS RESTARTS AGE
crashing-pods-f1tcd 0/1 CrashLoopBackOff 5 6m
```

### InitContainer
Когда Kubernetes используется для запуска приложений с несколькими модулями, нет готового способа сообщить системе Kubernetes сначала запускать определенные модули, а остальные только тогда, когда первые модули уже подняты и готовы обслуживать.

В дополнение к регулярным контейнерам поды могут также включить контейнеры инициализации (init). Как следует из названия, их можно использовать для инициализации модуля – это часто означает запись данных в тома пода, которые затем монтируются в главный контейнер пода. Под может иметь любое количество контейнеров инициализации `spec.initContainers`. 
```yaml
...
initContainers:
  - name: git-clone
    image: alpine/git
    args:
      - 'clone'
      - 'https://github.com/phpsite/site.git'
      - '/var/www'
    volumeMounts:
      - name: php-code
        mountPath: /var/www
      - name: ssh
        mountPath: /root/.ssh/
        readOnly: true
  - name: composer-install
    image: composer
    args:
      - "composer"
      - "install"
      - "--ignore-platform-reqs"
    env:
      - name: COMPOSER_HOME
        value: /tmp/.composer
...
```

Поды также позволяют определять два обработчика жизненного цикла:
- постстартовый обработчик (обработчик выполняется параллельно с главным процессом);
- предостановочный обработчик.

Обработчики жизненного цикла подобны проверкам живучести и готовности в том, что они могут:
- исполнять команду внутри контейнера;
- выполнять запрос HTTP GET по URL-адресу. 

```yaml
containers:
    - name: php
      image: zinvapel/php:7.4-fpm
      imagePullPolicy: Always
      ports:
          - containerPort: 9000
            name: fpm
      volumeMounts:
          - name: php-code
            mountPath: /var/www
      lifecycle:
          postStart:
              exec:
                  command:
                      - sh
                      - -c
                      - "echo 'Hello'"
          preStop:
              httpGet:
                   port: 8080
                   path: /shutdown
```

### Выключение модуля
Завершение работы модуля инициируется удалением объекта Pod через сервер API. При получении запроса HTTP DELETE сервер API пока объект не удаляет, а только устанавливает в нем поле deletionTimestamp. Модули, в которых установлено поле deletionTimestamp, находятся в процессе терминирования.

Как только агент Kubelet замечает, что модуль должен быть терминирован, он начинает завершать работу каждого контейнера модуля. Он дает каждому контейнеру время, чтобы тот выключился корректно, но это время ограничено. Это время называется льготным периодом терминации и настраивается для каждого модуля. Таймер запускается, как только начинается процесс терминирования. Затем выполняется следующая последовательность событий.
1. Запустить предостановочный обработчик, если он сконфигурирован, и дождаться его завершения.
2. Отправить сигнал SIGTERM в главный процесс контейнера.
3. Подождать до тех пор, пока контейнер не выключится полностью или пока не закончится льготный период терминации (`spec.terminationGracePeriodSeconds`).
4. Принудительно завершить процесс с помощью SIGKILL, если он еще не завершил работу корректно.

### Логирование
Файлом, в который процесс терминации должен по умолчанию записать сообщение, является /dev/termination-log, но его можно поменять, задав значение в поле `terminationMessagePath` в определении контейнера в секции spec модуля.

Можно перенести логи на локальную машину с помощью следующей ниже команды:
```bash
$ kubectl cp foo-pod:/var/log/foo.log foo.log
```
Для того чтобы скопировать файл с локальной машины в модуль, указывается имя модуля во втором аргументе:
```bash
$ kubectl cp localfile foo-pod:/etc/remotefile 
```

## Расширение Kubernetes
### Определение
Чтобы определить новый тип ресурса, достаточно отправить объект CustomResourceDefinition (CRD) на сервер API Kubernetes. Объект CustomResourceDefinition – это описание своего собственного типа ресурса. После отправки CRD пользователи могут создавать экземпляры своего собственного ресурса путем отправки манифестов JSON или YAML на сервере API, как и в случае с любым другим ресурсом Kubernetes.

Пример:
```yaml
kind: Website
metadata:
    name: kubia
spec:
    gitRepo: https://github.com/luksa/kubia-website-example.git

---
apiVersion: apiextensions.k8s.io/v1
kind: CustomResourceDefinition
metadata:
    # name must match the spec fields below, and be in the form: <plural>.<group>
    name: websites.extensions.example.com 
spec:
    scope: Namespaced
    group: extensions.example.com           <- Группа API
    versions:
      - name: v1                            <- версия
        # Each version can be enabled/disabled by Served flag.
        served: true
        # One and only one version must be marked as the storage version.
        storage: true
        schema:
            openAPIV3Schema:
                type: object
                properties:
                    spec:
                        type: object
                        properties:
                            gitRepo:
                                type: string
                        required:
                          - gitRepo
    names:
        kind: Website
        singular: website
        # plural name to be used in the URL: /apis/<group>/<version>/<plural>
        plural: websites
        shortNames:
          - ws
```
Для того чтобы заставить объекты Website запускать веб-серверный модуль, доступ к которому предоставляется через службу, необходимо создать и развернуть контроллер Website, который будет наблюдать за тем, как сервер API создает объекты Website, а затем для каждого из них будет создавать службу и веб-серверный модуль. (см форк https://github.com/zinvapel/k8s-website-controller)

Можно расширить API Kubernetes создав ресурс типа APIService (https://kubernetes.io/docs/tasks/access-kubernetes-api/). Одним из таких расширений является каталог сервисов (https://kubernetes.io/docs/concepts/extend-kubernetes/service-catalog/).
