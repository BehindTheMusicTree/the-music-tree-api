upstream bodzify_api {
    server web:443;
}

server {
    listen 80;
    bodzify bodzify.com www.bodzify.com;

    # Redirect HTTP to HTTPS
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl;
    bodzify bodzify.com www.bodzify.com;

    ssl_certificate /etc/ssl/bodzify/www_bodzify_com.crt;
    ssl_certificate_key /etc/ssl/bodzify/www.bodzify.com.key;

    access_log /var/log/nginx/access.log;
    error_log /var/log/nginx/error.log;

    location /static/ {
        alias /var/www/static/;
    }

    location / {
        proxy_pass http://bodzify_api;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $host;
        proxy_redirect off;
    }
}