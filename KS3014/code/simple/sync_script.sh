
scp *.py pi:/tmp
inotifywait -r -m -e close_write --format '%w%f' . | while read MODFILE
do
    echo need to rsync $MODFILE ...
    scp $MODFILE pi:/tmp
done
