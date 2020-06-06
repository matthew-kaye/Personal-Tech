source app.env
git pull origin master
make build-production
make down-production
make up-production
make migrate-production
