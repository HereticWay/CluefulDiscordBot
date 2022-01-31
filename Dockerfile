FROM python:3.10-slim

WORKDIR /App
COPY ./cluefulbot ./cluefulbot
COPY ./requirements.txt .
COPY ./main.py .

RUN apt-get update && \
    apt-get install -y build-essential curl git && \
    apt-get clean \

RUN pip3 install --no-cache-dir -r requirements.txt

# We must build lavasnek_rs because it cannot be installed right now on python 3.10 through pip
# Install Rust
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y

# Clone lavasnek_rs and build it
RUN git clone https://github.com/vicky5124/lavasnek_rs.git && \
    cd lavasnek_rs && \
    . $HOME/.cargo/env && \
    maturin build \

# Install the build
RUN pip3 install lavasnek_rs/target/wheels/lavasnek_rs-*.whl

ENTRYPOINT ["python", "main.py"]