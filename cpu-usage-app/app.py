from __future__ import annotations

import multiprocessing
from threading import Lock

from flask import Flask, Response

app = Flask(__name__)


class StressController:
    def __init__(self) -> None:
        self._lock = Lock()
        self._workers: list[multiprocessing.Process] = []

    @staticmethod
    def _burn_cpu() -> None:
        value = 0
        while True:
            value += 1
            if value > 1_000_000:
                value = 0

    def start(self) -> None:
        with self._lock:
            if self.is_running():
                return

            worker_count = max(1, multiprocessing.cpu_count())
            self._workers = []

            for _ in range(worker_count):
                process = multiprocessing.Process(target=self._burn_cpu)
                process.start()
                self._workers.append(process)

    def stop(self) -> None:
        with self._lock:
            for process in self._workers:
                if process.is_alive():
                    process.terminate()

            for process in self._workers:
                process.join(timeout=1)

            self._workers = []

    def is_running(self) -> bool:
        return any(process.is_alive() for process in self._workers)


controller = StressController()


@app.get("/start-stress")
def start_stress() -> Response:
    controller.start()
    return Response("Mode=stress\n", mimetype="text/plain")


@app.get("/stop-stress")
def stop_stress() -> Response:
    controller.stop()
    return Response("Mode=normal\n", mimetype="text/plain")


@app.get("/health")
def health() -> Response:
    status = "stress" if controller.is_running() else "normal"
    return Response(f"Mode={status}\n", mimetype="text/plain")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
