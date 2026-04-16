#!/usr/bin/env bash

conda env create --prefix ./.env -f environment.yml
source activate base && conda activate ./.env
npm install
npm run serve
