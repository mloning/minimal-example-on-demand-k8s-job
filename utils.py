from pathlib import Path
import yaml
import kubernetes as k8s
from uuid import uuid4

_LABEL = "on-demand-job"


def load_yml(file: Path):
    assert isinstance(file, Path)
    with open(file, "r") as f:
        content = yaml.safe_load(f)
        return content


def make_uid():
    return str(uuid4())[:6]


def get_api():
    k8s.config.load_kube_config()
    # configuration = k8s.client.Configuration()
    # client = k8s.client.ApiClient(configuration)
    return k8s.client.BatchV1Api()


def _specify_job(
    name: str,
    image: str,
    namespace: str = "default",
) -> k8s.client.V1Job:
    # Load job specification from yml file.
    # content = load_yml(Path("job.yml"))
    # body = k8s.client.V1Job(content)

    # Pod specification
    command = [
        "sh",
        "-c",
        "echo $(date): On-demand job is running ...; sleep 5; echo Done.",
    ]
    container = k8s.client.V1Container(
        name="job-container", image=image, command=command
    )
    spec = k8s.client.V1PodSpec(containers=[container], restart_policy="Never")
    template = k8s.client.V1PodTemplateSpec(spec=spec)

    # Job specification
    spec = k8s.client.V1JobSpec(template=template)
    metadata = k8s.client.V1ObjectMeta(
        namespace=namespace,
        name=name,
        labels={_LABEL: name},
    )
    status = k8s.client.V1JobStatus()
    job = k8s.client.V1Job(
        api_version="batch/v1",
        kind="Job",
        status=status,
        metadata=metadata,
        spec=spec,
    )
    return job


def _run_job(api, namespace: str, job: k8s.client.V1Job) -> None:
    r = api.create_namespaced_job(namespace, body=job, pretty=True)
    return r


def wait_for_job_completion(
    api: k8s.client.BatchV1Api,
    name: str,
    namespace: str = "default",
):
    # We here make a synchronous HTTP request using `list_namespaced_job`.
    # It should be possible to write this as an asynchronous request.
    watcher = k8s.watch.Watch()
    stream = watcher.stream(
        api.list_namespaced_job,
        namespace,
        label_selector=_LABEL,
    )
    for event in stream:
        obj = event["object"]

        if obj.metadata.name == name:
            if obj.status.succeeded:
                break
            else:
                AssertionError()
        else:
            continue
    return event


def create_job(
    api: k8s.client.BatchV1Api,
    name: str,
    image: str,
    namespace: str = "default",
) -> None:
    job = _specify_job(name=name, image=image)
    return _run_job(api, namespace, job)
