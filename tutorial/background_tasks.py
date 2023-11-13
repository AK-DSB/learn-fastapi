from typing import Annotated

import uvicorn
from fastapi import BackgroundTasks, FastAPI, Depends

app = FastAPI()


def write_notification(email: str, message=''):
    with open('log.txt', mode='w') as email_file:
        content = f'notification for {email}: {message}'
        print(content)
        email_file.write(content)


@app.post('/send-notification/{email}')
async def send_notification(email: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(write_notification, email, message='some notification')
    return {"message": "Notification sent in the background"}


def write_log(message: str):
    with open('log.txt', mode='a') as log:
        log.write(message)


def get_query(background_tasks: BackgroundTasks, q: str | None = None):
    if q:
        message = f'found query: {q}\n'
        print(message)
        background_tasks.add_task(write_log, message)
    return q


@app.post('/send-q/{email}')
async def send_q(
        email: str,
        background_tasks: BackgroundTasks,
        q: Annotated[str, Depends(get_query)]
):
    message = f'message to {email}\n'
    print(q)
    background_tasks.add_task(write_log, message)
    return {"message": "Message sent"}


if __name__ == '__main__':
    uvicorn.run(app=app, host='0.0.0.0', port=5555)
