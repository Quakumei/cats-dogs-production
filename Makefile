.DEFAULT_GOAL := help

# Set python
export PYTHONPATH=.
python = python

.PHONY: help
help:
	@echo "USAGE"
	@echo "  make <commands>"
	@echo ""
	@echo "AVAILABLE COMMANDS"
	@echo "  - PRODUCTION - "
	@echo "  install 		Install the dependencies for deployment"
	@echo "  run_bot		Start the TG bot"
	@echo " "
	@echo "  - DEVELOPMENT -"
	@echo "  lint			Reformat code"
	@echo "  test		Run tests"
	@echo "  install_dev	Install the dependencies for development"


# ================================================================================================
# Dependencies
# ================================================================================================

# People say it takes 5 mins to 2 hours to build from sources
# https://forum.opencv.org/t/can-i-use-opencv-python-with-gpu/8947/2
build_opencv/opencv-python/dist:
	mkdir build_opencv
	cd build_opencv && git clone https://github.com/opencv/opencv && git clone https://github.com/opencv/opencv_contrib
	cd build_opencv %% cmake -DOPENCV_EXTRA_MODULES_PATH=opencv_contrib/modules  \
       -DBUILD_SHARED_LIBS=OFF \
       -DBUILD_TESTS=OFF \
       -DBUILD_PERF_TESTS=OFF \
       -DBUILD_EXAMPLES=OFF \
       -DWITH_OPENEXR=OFF \
       -DWITH_CUDA=ON \
       -DWITH_CUBLAS=ON \
       -DWITH_CUDNN=ON \
       -DOPENCV_DNN_CUDA=ON \
       /opencv
	make -j8 install
	cd opencv-python && pip wheel . --verbose

# https://stackoverflow.com/questions/27885397/how-do-i-install-a-python-package-with-a-whl-file
.PHONY: install_opencv_cuda
install_opencv_cuda: build_opencv/opencv-python/dist
	@echo Installing built pip wheel...
	$(python) -m pip install build_opencv/opencv-python/dist/*.whl

.PHONY: clean_opencv
clean_opencv:
	rm build_opencv/*
	rmdir build_opencv

.PHONY: install
install:
	$(python) -m pip install -r requirements/prod.txt

.PHONY: install_dev
install_dev:
	$(python) -m pip install -r requirements/dev.txt


# ================================================================================================
# Lint
# ================================================================================================

.PHONY:	black
black:
	$(python) -m black --line-length 80 .

.PHONY: isort
isort:
	$(python) -m isort .

.PHONY: flake
flake:
	$(python) -m flake8 .

.PHONY: lint
lint: black isort flake

# ================================================================================================
# Tests
# ================================================================================================

.PHONY: test
test:
	$(python) -m pytest

# ================================================================================================
# Start
# ================================================================================================

.env:
	# Check if .env file exists
	@echo "ERROR: You need to specify TOKENS in .env file. Read README.md for more info."
	exit 1

.PHONY: run_bot
run_bot: .env
	@echo "Running bot..."
	$(python) src/bot.py