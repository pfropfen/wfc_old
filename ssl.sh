#!/bin/bash

sudo docker run -d --rm -p 9000:443 -v /root/auth/:/opt/auth \
                -v /root/certs/:/opt/certs -e REGISTRY_HTTP_ADDR=0.0.0.0:443 \
                -e REGISTRY_HTTP_TLS_CERTIFICATE=/opt/certs/server.crt \
                -e REGISTRY_HTTP_TLS_KEY=/opt/certs/server.key -e REFISTRY_AUTH=htpasswd \
                -e REGISTRY_AUTH_HTPASSWD_REALM=Registry-Realm \
                -e REGISTRY_AUTH_HTPASSWD_PATH=/opt/auth/htpasswd \
                --name registry2 registry:2


