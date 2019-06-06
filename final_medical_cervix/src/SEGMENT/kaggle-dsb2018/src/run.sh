#!/bin/bash
#python3 schwaebische_nuclei.py predict_test --loadmodel output_from_all_models/ --predicttestonly --colouronly --cuda_device $1
#python3 schwaebische_nuclei.py predict_test --loadmodel ${2}_output/ --predicttestonly --colouronly --cuda_device $1
echo $2
echo $1
echo $3
python3 schwaebische_nuclei.py predict_test --loadmodel ${2}_output/ --predicttestonly --cuda_device $1 --$3

