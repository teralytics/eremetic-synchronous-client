import logging
import json
from time import sleep
import time

import requests


class Request:

    def __init__(self, cpu=1, mem=128, image='busybox', force_pull_image=False, command=None, args=None, volumes=None,
                 network="HOST", dns=None, ports=None, env=None, masked_env=None, fetch=None, agent_constraints=None,
                 callback_uri=None):
        self.__payload = {}
        self \
            .with_cpu(cpu) \
            .with_mem(mem) \
            .with_image(image) \
            .with_force_pull_image(force_pull_image) \
            .with_command(command) \
            .with_args(args) \
            .with_volumes(volumes) \
            .with_network(network) \
            .with_dns(dns) \
            .with_ports(ports) \
            .with_env(env) \
            .with_masked_env(masked_env) \
            .with_fetch(fetch) \
            .with_agent_constraints(agent_constraints) \
            .with_callback_uri(callback_uri)

    def from_payload(self, payload):
        self.__payload = json.loads(payload)

    def with_cpu(self, cpu):
        self.__payload['cpu'] = cpu
        return self

    def with_mem(self, mem):
        self.__payload['mem'] = mem
        return self

    def with_image(self, image):
        self.__payload['image'] = image
        return self

    def with_force_pull_image(self, force_pull_image):
        self.__payload['force_pull_image'] = force_pull_image
        return self

    def with_command(self, command):
        self.__payload['command'] = command
        return self

    def with_args(self, args):
        self.__payload['args'] = args
        return self

    def with_volumes(self, volumes):
        self.__payload['volumes'] = volumes
        return self

    def with_network(self, network):
        self.__payload['network'] = network
        return self

    def with_dns(self, dns):
        self.__payload['dns'] = dns
        return self

    def with_ports(self, ports):
        self.__payload['ports'] = ports
        return self

    def with_env(self, env):
        self.__payload['env'] = env
        return self

    def with_masked_env(self, masked_env):
        self.__payload['masked_env'] = masked_env
        return self

    def with_fetch(self, fetch):
        self.__payload['fetch'] = fetch
        return self

    def with_agent_constraints(self, agent_constraints):
        self.__payload['agent_constraints'] = agent_constraints
        return self

    def with_callback_uri(self, callback_uri):
        self.__payload['callback_uri'] = callback_uri
        return self

    def payload(self):
        return {k: v for k, v in self.__payload.items() if v is not None}

    def to(self, url, polling_wait_time=1, failure_wait_time=5):
        """
        Delivers the request to Eremetic via the HTTP API. If the task is correctly created,
        a never-ending polling loop begins until the task is finished. If a failure condition is detected
        there will be one final attempt to ensure the task has not been re-scheduled by Eremetic itself.
        :param url: The base url to contact
        :param polling_wait_time: The wait time after each polling attempt
        :param failure_wait_time: The wait time to apply when a (possibly transient) failure is detected
        :return: a tuple with Eremetic task id and the last status of the task
        """
        task_id = self.submit(url)
        return task_id, self.track(url, task_id, polling_wait_time, failure_wait_time)

    def submit(self, url):
        """
        Submits a task defined in the Request to Eremetic
        :param url: HTTP endpoint of Eremetic without trailing slash
        :return: Eremetic task id
        """
        response = requests.post('{0}/api/v1/task'.format(url), data=json.dumps(self.payload()))
        task_id = response.json()
        if task_id is None:
            raise Exception(response.reason)
        logging.info("Successfully submitted the task to Eremetic, task id: '{}'".format(task_id))
        return task_id

    @staticmethod
    def task_failed(task_state):
        """
        Checks for `task_state` to be terminal, but not successful (otherwise than `TASK_FINISHED`)
        See: https://github.com/eremetic-framework/eremetic/blob/a893b393b4fefe96602d629e2e127767a1b20363/task.go#L33
        :param task_state: Mesos task state
        :return:
        """
        return task_state in {"TASK_LOST", "TASK_KILLED", "TASK_FAILED", "TASK_TERMINATING"}

    @staticmethod
    def terminate_task(url, task_id):
        """
        Sends the terminate task command to Eremetic
        :param url:
        :param task_id:
        :return:
        """
        requests.post('{0}/api/v1/task/{1}/kill'.format(url, task_id))

    @staticmethod
    def track(url, task_id, polling_wait_time=1, failure_wait_time=5, queue_max_wait_time=None):
        """
        Tracks a task within Eremetic. Blocks and begins a never-ending polling loop until the task is finished.
        If a failure condition is detected there will be one final attempt to ensure the task has not been re-scheduled
        by Eremetic itself.
        :param url: HTTP endpoint of Eremetic without trailing slash
        :param task_id: Eremetic task id to track
        :param polling_wait_time: The wait time after each polling attempt
        :param failure_wait_time: The wait time to apply when a (possibly transient) failure is detected
        :param queue_max_wait_time: Maximum time the task is allowed to be in TASK_QUEUED state.
                                   If exceeded, the task will be cancelled and exception will be thrown.
        :return: the last status of the task
        """
        last_status_is_failure = False
        while True:
            if last_status_is_failure:
                wait_time = failure_wait_time
            else:
                wait_time = polling_wait_time
            sleep(wait_time)
            task_status = requests.get('{0}/api/v1/task/{1}'.format(url, task_id))
            sorted_stages = sorted(task_status.json()['status'], key=lambda stage: stage['time'])
            statuses = list(map(lambda stage: stage['status'], sorted_stages))
            if len(statuses) > 0:
                logging.debug('Task "{0}" status progression: {1}'.format(task_id, ' -> '.join(map(lambda s: s[5:], statuses))))
                last_status = statuses[-1:][0]
                if last_status == 'TASK_FINISHED':
                    logging.info('{1}: "{0}", status page: {2}/task/{0}'.format(task_id, last_status, url))
                    return last_status
                if Request.task_failed(last_status):
                    if last_status_is_failure:
                        logging.info('{1}: "{0}", status page: {2}/task/{0}'.format(task_id, last_status, url))
                        return last_status
                    else:
                        logging.debug('{1}: "{0}", one last attempt before giving up'.format(task_id, last_status))
                        last_status_is_failure = True
                else:
                    if last_status_is_failure:
                        logging.debug('{1}: "{0}", recovery attempt detected'.format(task_id, last_status))
                        last_status_is_failure = False

                if queue_max_wait_time is not None and sorted_stages[-1:][0]['status'] == "TASK_QUEUED":
                    queued_since = sorted_stages[-1:][0]['time']
                    logging.debug("Task has been queued for  {}".format(time.time() - queued_since))
                    if time.time() - queued_since > queue_max_wait_time:
                        logging.error("Task {0} exceeded queue_max_wait_time(={1}), terminating...".format(task_id, queue_max_wait_time))
                        Request.terminate_task(url, task_id)
                        logging.error("Task {} was cancelled".format(task_id))
                        return "TASK_TERMINATING"
            else:
                logging.debug('Still not status update from task "{}"'.format(task_id))
