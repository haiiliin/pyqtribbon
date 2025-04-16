pdm-lock:
	python -m pdm lock --python=">=3.10,<3.14" --group :all
	python -m pdm lock --python=">=3.8,<3.10" --group :all --append

pdm-export:
	python -m pdm export -o requirements.txt --without-hashes --group :all
	python -m pdm export -o docs/requirements.txt --without-hashes --group docs

pdm-install:
	python -m pdm install --group :all
