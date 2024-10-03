# print openMV stream

## install dependencies

### install cups

```bash
sudo apt update
sudo apt install gcc python3-dev libcups2-dev
pip install pycups
pip install pygame
pip install reportlab
```

## Start app, after the UI loads
```bash
# append to the last line of .bashrc
if pgrep -f "python.*pygame_printer/main.py" > /dev/null
then
    echo "...pygame_printer is already running."
else
    echo "...pygame_printer is not running. Starting it now..."
    # Run main.py (adjust python to python3 if necessary)
    export DISPLAY=:0
    python /home/senseable/pygame_printer/main.py &
fi
```