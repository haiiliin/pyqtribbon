pdm-lock:
	pdm lock --python=">=3.10,<3.14" --group :all
	pdm lock --python=">=3.8,<3.10" --group :all --append

pdm-export:
	pdm export -o requirements.txt --without-hashes --group :all
	pdm export -o docs/requirements.txt --without-hashes --group docs

pdm-install:
	pdm install --group :all
