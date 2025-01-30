pdm-lock:
	pdm lock --python=">=3.10,<3.14" --group :all
	pdm lock --python=">=3.8,<3.10" --group :all --append

pdm-install:
	pdm install --group :all
