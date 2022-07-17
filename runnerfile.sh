#!/bin/bash

task_extend() {
    filelist=$(ls v2-logs/*.csv | grep -v ext)
    for f in $filelist
    do
        echo
        echo "Extend: $f"
        echo
        FILE=$f python extend.py
    done
}

task_summary() {
    filelist=$(ls v2-logs/*-ext.csv)
    for f in $filelist
    do
        attrs="DateTime DateTime,EndpointMethod,EndpointPath DateTime,EndpointMethod,EndpointPath,ServiceTracing DateTime,ServiceTracing"
        for attr in $attrs
        do
            echo
            echo "***** ***** Summary: $f ***** *****"
            echo "attr=$attr"
            echo
            FILE=$f ATTRS=$attr python csv_analysis_v2.py
        done
    done
}
