FROM ubuntu:20.04 AS build

ARG FAAS_CLI_VERSION

ENV DEBIAN_FRONTEND=noninteractive
ENV DOCKERVERSION=20.10.9

WORKDIR /root

RUN apt update && apt install -y git curl \
    && curl -sSL https://github.com/openfaas/faas-cli/releases/download/${FAAS_CLI_VERSION}/faas-cli --output /usr/local/bin/faas-cli \
    && chmod u+x /usr/local/bin/faas-cli \
    && faas-cli template pull \
    && faas-cli template pull https://gitlab.hidora.com/softozor/faas-templates.git \
    && curl -fsSLO https://download.docker.com/linux/static/stable/x86_64/docker-${DOCKERVERSION}.tgz \
    && tar xzvf docker-${DOCKERVERSION}.tgz --strip 1 -C /usr/local/bin docker/docker \
    && chmod u+x /usr/local/bin/docker

FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive

ARG CNI_VERSION
ARG CONTAINERD_VER
ARG FAASD_VERSION

COPY --from=build /usr/local/bin/faas-cli /usr/local/bin/faas-cli
COPY --from=build /root/template /faas-template/template
COPY --from=build /usr/local/bin/docker /usr/local/bin/docker

# cf. https://github.com/openfaas/faasd/blob/master/hack/install.sh
# install_required_packages
RUN apt update && apt install -y openssh-server curl runc bridge-utils iptables netcat \
    && /sbin/sysctl -w net.ipv4.conf.all.forwarding=1 \
    && echo "net.ipv4.conf.all.forwarding=1" | tee -a /etc/sysctl.conf \
    # install_cni_plugins
    && mkdir -p /opt/cni/bin \
    && curl -sSL https://github.com/containernetworking/plugins/releases/download/${CNI_VERSION}/cni-plugins-linux-amd64-${CNI_VERSION}.tgz | tar -xvz -C /opt/cni/bin \
    # install_containerd
    && curl -sLSf https://github.com/containerd/containerd/releases/download/v${CONTAINERD_VER}/containerd-${CONTAINERD_VER}-linux-amd64.tar.gz | tar -xvz --strip-components=1 -C /usr/local/bin/ \
    && systemctl unmask containerd || : \
    && curl -SLfs https://raw.githubusercontent.com/containerd/containerd/v${CONTAINERD_VER}/containerd.service --output /etc/systemd/system/containerd.service \
    && systemctl enable containerd \
    # install_faasd
    && curl -fSLs https://github.com/openfaas/faasd/releases/download/${FAASD_VERSION}/faasd --output /usr/local/bin/faasd \
    && chmod a+x /usr/local/bin/faasd \
    && mkdir -p /faasd-installation/hack  \
    && curl -fSLs https://raw.githubusercontent.com/openfaas/faasd/${FAASD_VERSION}/docker-compose.yaml --output /faasd-installation/docker-compose.yaml \
    && curl -fSLs https://raw.githubusercontent.com/openfaas/faasd/${FAASD_VERSION}/prometheus.yml --output /faasd-installation/prometheus.yml \
    && curl -fSLs https://raw.githubusercontent.com/openfaas/faasd/${FAASD_VERSION}/resolv.conf --output /faasd-installation/resolv.conf \
    && curl -fSLs https://raw.githubusercontent.com/openfaas/faasd/${FAASD_VERSION}/hack/faasd-provider.service --output /faasd-installation/hack/faasd-provider.service \
    && curl -fSLs https://raw.githubusercontent.com/openfaas/faasd/${FAASD_VERSION}/hack/faasd.service --output /faasd-installation/hack/faasd.service
