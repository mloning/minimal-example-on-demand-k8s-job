from pydantic import BaseModel
from fastapi import FastAPI
from utils import create_job, get_api, make_uid, wait_for_job_completion

app = FastAPI()


class Params(BaseModel):
    name: str


@app.get("/")
def read_root():
    return {"message": "Hello world!"}


@app.post("/run_job/")
def run_job(params: Params):
    IMAGE = "busybox:1.28"
    NAMESPACE = "default"

    uid = make_uid()
    job_name = "-".join([params.name, uid])

    api = get_api()
    _ = create_job(
        api=api,
        name=job_name,
        namespace=NAMESPACE,
        image=IMAGE,
    )
    try:
        _ = wait_for_job_completion(
            api=api,
            name=job_name,
            namespace=NAMESPACE,
        )
        msg = f"{params.name} succeeded"
    except AssertionError:
        msg = f"{params.name} failed."
    return {"response": msg}
