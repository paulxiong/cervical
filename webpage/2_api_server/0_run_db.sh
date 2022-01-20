#!/bin/bash
pushd ../1_db
    echo 'doker up -d'
    docker-compose up -d
popd 