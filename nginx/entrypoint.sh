#!/bin/sh
certbot certonly --standalone -d pcost.tech,api.pcost.tech --email yaroslav@pcost.tech -n --agree-tos --expand
/usr/sbin/nginx -g "daemon off;"