#!/usr/bin/bash

# activate virtual enviroment
source .env/bin/activate

pyinstaller --onefile --name maths_problems --add-data "lib/mathjax3:lib/mathjax3" main.py