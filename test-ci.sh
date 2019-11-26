#!/bin/bash

# TODO: consider pulling docker images from ECR to speed up this build, 
# instead of building the images from scratch each time

env=$1
fails=""

inspect() {
    if [ $1 -ne 0 ]; then
        fails="${fails} $2"
    fi
}

# run client and server-side tests
dev() {
    docker-compose up -d --build
    docker-compose exec users python manage.py test
    inspect $? users
    docker-compose exec users black -l 79 project
    inspect $? users-black
    docker-compose exec users flake8 project
    inspect $? users-lint
    docker-compose exec exercises python manage.py test
    inspect $? exercises
    docker-compose exec exercises flake8 project
    inspect $? exercises-lint
    docker-compose exec client npm test -- --coverage
    inspect $? client
    docker-compose down
}

# run e2e tests
e2e() {
    docker-compose -f docker-compose-$1.yml up -d --build
    docker-compose -f docker-compose-$1.yml exec users python manage.py recreate_db
    ./node_modules/.bin/cypress run --config baseUrl=http://localhost --env REACT_APP_API_GATEWAY_URL=$REACT_APP_API_GATEWAY_URL,LOAD_BALANCER_STAGE_DNS_NAME=$LOAD_BALANCER_STAGE_DNS_NAME
    inspect $? e2e
    docker-compose -f docker-compose-$1.yml down
}

# run appropriate tests
if [[ "${env}" == "development" ]]; then
    echo "Running client and server-side tests!"
    dev
elif [[ "${env}" == "staging" ]]; then
    echo "Running e2e tests!"
    e2e stage
elif [[ "${env}" == "production" ]]; then
    echo "Running e2e tests!"
    e2e prod
else
    echo "Running client and server-side tests!"
    dev
fi

# return proper code
if [ -n "${fails}" ]; then
    echo "Tests failed: ${fails}"
    exit 1
else
    echo "Tests passed!"
    exit 0
fi