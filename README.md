# Road Vision Lab

Tesla-sector-inspired synthetic lane geometry: robust line fits, residual errors and canvas overlay.

An AI-assisted educational portfolio project prepared for Erik Vera's internship learning. This is a working prototype, not production software. Authorship and skills should be represented based on what you can explain and change independently.

## Public demo

[Open browser demo](https://erickvera610.github.io/road-vision-lab/). Visitors can run examples on their device without write access to this repository.

## Run in two minutes

Requires Python 3.11 or newer; no pip dependencies.

```bash
git clone https://github.com/erickvera610/road-vision-lab.git
cd road-vision-lab
python app.py
```

Open http://127.0.0.1:8000. On Windows, use `py app.py` if `python` is unavailable. Stop with Ctrl+C. Run `python -m unittest discover -v` to execute tests.

## Architecture

- `index.html`: responsive accessible interface; renders output with textContent.
- `app.py`: local HTTP service, `/health`, and validated JSON POST `/api/run`.
- `core.py`: domain logic separated from transport and presentation.
- `test_core.py`: deterministic behavior and failure cases.
- `.github/workflows/tests.yml`: Python 3.11 and 3.12 CI.
- `TUTORIAL_ES.md`: beginner Spanish guide and interview practice.

## API

POST a JSON object to `/api/run`; inputs are the same fields used by the interface. Responses are JSON. Invalid inputs return 400; unknown paths return 404. GET `/health` returns `{"status":"ok"}`.

## Design and limits

Se generan coordenadas de carriles con ruido. Ajusto x=a*y+b con mínimos cuadrados y descarto puntos con residuo grande antes de volver a ajustar. ROI es la región de interés; aquí las coordenadas están entre y=80 e y=240. RMSE mide error en píxeles. Este ejercicio no detecta carriles de una foto real: prepara la geometría para un futuro pipeline de visión.

The built-in HTTP server is for a local demonstration. There is no authentication, rate limiting, or public production deployment. Never enter personal application records on a publicly exposed demo. Bind to localhost by default. For Codespaces only, run `HOST=0.0.0.0 python app.py` and keep the forwarded port private; usage may consume your GitHub quota.

## Review and contribution workflow

Create a feature branch, make one small change, run the tests, commit it, push the branch, and open a pull request. Explain the change and validation. Do not fabricate collaboration or commit history. Suggested first improvement: add a new input option with one behavior test and update this README.

## References

- https://docs.python.org/3/library/http.server.html
- https://docs.github.com/en/actions/tutorials/build-and-test-code/python

License: MIT.
