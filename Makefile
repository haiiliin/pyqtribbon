install:
	pip install cppbinder==1.4.2.4

bindings:
	binder \
		--root-module qtribbon \
		--bind qtribbon \
		--prefix bindings \
		--include-pybind11-stl \
		--annotate-includes \
		--skip-line-number \
		--suppress-errors \
		--single-file \
		  binder_includes.hpp \
		-- \
		-std=c++11 \
		-I.

format:
	pre-commit run --all-files
