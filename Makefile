.PHONY: all build-python build-cpp build-rust build-go build-java test deploy

all: build-python build-cpp build-rust build-go build-java

build-python:
	pip install -r requirements.txt
	python -m pytest tests/ -q

build-cpp:
	cd services/cpp && mkdir -p build && cd build && cmake .. -DCMAKE_BUILD_TYPE=Release && make -j8

build-rust:
	cd services/rust && cargo build --release

build-go:
	cd services/go && go build ./...

build-java:
	cd services/java && mvn clean package -DskipTests

test:
	pytest tests/ -v
	cd services/rust && cargo test
	cd services/go && go test ./...
	cd services/java && mvn test

deploy:
	docker-compose up -d --build
	echo 'All services deployed'

dashboard:
	streamlit run dashboard/app.py --server.port 8501
