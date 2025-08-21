FROM mcr.microsoft.com/devcontainers/base:jammy
# FROM mcr.microsoft.com/devcontainers/base:jammy 

ARG DEBIAN_FRONTEND=noninteractive
ARG USER=vscode

RUN DEBIAN_FRONTEND=noninteractive \
    && apt-get update \ 
    && apt-get install -y build-essential --no-install-recommends \
        bat \
        bison \
        bsdmainutils \
        build-essential \
        ca-certificates \
        cmake \
        curl \
        file \
        gcc \
        git \
        iputils-ping \
        jq \
        libbz2-dev \
        libedit-dev \
        libffi-dev \
        liblzma-dev \
        libncurses-dev \
        libncurses5-dev \
        libncursesw5-dev \
        libreadline-dev \
        libsqlite3-dev \
        libssl-dev \
        libxml2-dev \
        libxmlsec1-dev \
        llvm \
        make \
        nala \
        net-tools \
        pipx \
        procps \
        software-properties-common \
        telnet \
        tk-dev \
        tzdata \
        unzip \
        vim \
        wget \
        xz-utils \
        zlib1g-dev

# Install yq
ENV YQ_VERSION="v4.47.1"
RUN wget -qO /usr/local/bin/yq https://github.com/mikefarah/yq/releases/download/${YQ_VERSION}/yq_linux_amd64 \
 && chmod +x /usr/local/bin/yq

# Run setup eza script
COPY scripts/setup-eza.sh /tmp/setup-eza.sh
RUN chmod +x /tmp/setup-eza.sh && /tmp/setup-eza.sh

# Run setup fnm script
COPY scripts/setup-fnm.sh /tmp/setup-fnm.sh
RUN chmod +x /tmp/setup-fnm.sh && /tmp/setup-fnm.sh

# Python and poetry installation
USER $USER
ARG HOME="/home/$USER"
ARG PYTHON_VERSION=3.9
# ARG PYTHON_VERSION=3.10

ENV PYENV_ROOT="${HOME}/.pyenv"
ENV PATH="${PYENV_ROOT}/shims:${PYENV_ROOT}/bin:${HOME}/.local/bin:$PATH"

COPY ./dotfiles/ /tmp/setup/

RUN <<"EOT" bash
    set -eux
    
    # Create Symbolic Links
    sudo mkdir -p /opt/certs /opt/Documents /opt/Downloads /opt/.ssh
    sudo ln -sf /opt/Documents ~/Documents
    sudo ln -sf /opt/Downloads ~/Downloads
EOT

RUN <<"EOT" bash
    set -eux

    ### Setup shell
    sudo cp -r /tmp/setup/. ~/
    sudo chown -R ${USER}:${USER} ~/.
EOT

RUN echo "done 0" \
    && curl https://pyenv.run | bash \
    && echo "done 1" \
    && pyenv install ${PYTHON_VERSION} \
    && echo "done 2" \
    && pyenv global ${PYTHON_VERSION} \
    && echo "done 3" \
    && curl -sSL https://install.python-poetry.org | python3 - \
    && poetry config virtualenvs.in-project true
