# Eremetic synchronous client

A Python client for [Eremetic](https://www.github.com/eremetic-framework/eremetic), an [Apache Mesos](https://mesos.apache.org) framework to run one-off jobs in [Docker](https://docker.io) containters.

This client simply provides a synchronous interface over the HTTP API.

The major and minor version of this package mirrors the version of Eremetic with which it's compatible. The patch version may vary independently.

## Example

### Preparing the root logger

```python
import sys, logging
logging.root.handlers = []
logging.basicConfig(stream=sys.stdout, level=logging.INFO, format='%(levelname)s - %(message)s')
```

### Preparing (and showing) the request

```python
import eremetic_synchronous_client
request = eremetic_synchronous_client.Request(cpu=1, mem=1024, image='busybox', command='echo $(date)')
request.payload()
```

#### Return value

```python
{'network': 'HOST', 'mem': 1024, 'image': 'busybox', 'force_pull_image': False, 'command': 'echo $(date)', 'cpu': 1}
```

### Shooting the request 

```python
request.to('http://eremetic-url')
```

#### Output

```
INFO - Task "eremetic-task.232e3359-dead-babe-beef-9872ed82ba90" status progression: QUEUED -> STAGING -> RUNNING -> FINISHED
INFO - TASK_FINISHED: "eremetic-task.232e3359-dead-babe-beef-9872ed82ba90", status page: http://eremetic-url/task/eremetic-task.232e3359-dead-babe-beef-9872ed82ba90
```

#### Return value
```python
(u'eremetic-task.232e3359-dead-babe-beef-9872ed82ba90', u'TASK_FINISHED')
```
