

task_extend() {
    filelist=$(ls v2-logs/*.csv | grep -v ext)
    for f in $filelist
    do
        echo "Extend: $f"
        FILE=$f python extend.py
    done
}

task_summary() {
    filelist=$(ls v2-logs/*-ext.csv)
    for f in $filelist
    do
        echo "Summary: $f"
        FILE=$f python csv_analysis_v2.py
    done
}