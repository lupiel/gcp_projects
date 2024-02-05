# deal with complex requirements.txt dependencies using pip-compile
conda create -y --name=venv-app python=3.9
conda activate venv-app
pip install --upgrade pip
python -m pip install pip-tools
pip-compile --allow-unsafe --annotation-style=line --max-rounds=4 --no-emit-index-url --output-file=requirements_compiled_linux.txt --pip-args='--use-pep517 --retries 8 --timeout 30' --resolver=backtracking requirements-app.txt requirements.txt
pip install -r requirements_compiled_linux.txt
