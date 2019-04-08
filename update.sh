#!/bin/bash

NAME="mail-attachments-archiver"

git fetch --all
git reset --hard $NAME/master
git pull $NAME master
