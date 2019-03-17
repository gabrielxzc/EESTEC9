from pynput import keyboard
import socketio

SIO = socketio.Client()
SIO.connect('http://10.81.176.102')


def emit(command):
    cmd = {
        'key': 'c37krkse1hkepmns',
        'type': 'menu_command',
        'menu_key': command,
        'is_player_2': False
    }

    SIO.emit('admin', cmd)


def on_key_press(key):
    try:
        if key.name == 'down':
            print('down')
            emit('down')
        elif key.name == 'left':
            print('left')
            emit('left')
        elif key.name == 'right':
            print('right')
            emit('right')
        elif key.name == 'up':
            print('up')
            emit('up')
        elif key.name == 'enter':
            print('enter')
            emit('enter')
        elif key.name == 'esc':
            print('esc')
            emit('escape')
    except Exception:
        pass


with keyboard.Listener(on_press=on_key_press) as listener:
    listener.join()
