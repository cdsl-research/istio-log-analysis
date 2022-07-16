task_extend() {
    filelist=$(ls v2-logs/*.csv)
    for f in $filelist
    do
        echo "Extend: $f"
        FILE=$f python extend.py
    done
}