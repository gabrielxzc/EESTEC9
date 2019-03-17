from pynput import keyboard
import socketio

SIO = socketio.Client()
SIO.connect('http://10.81.176.102')


def emit(command, value):
    cmd = {
        'key': 'fjm30c2qa05t3e43',
        'commands': {
            command: value
        }
    }

    SIO.emit('command', cmd)


def on_key_press(key):
    try:
        if key.name == 'down':
            print('down')
            emit('down', True)
        elif key.name == 'left':
            print('left')
            emit('left', True)
        elif key.name == 'right':
            print('right')
            emit('right', True)
        elif key.name == 'up':
            print('up')
            emit('up', True)
    except Exception:
        pass


def on_key_release(key):
    try:
        if key.name == 'down':
            print('down')
            emit('down', False)
        elif key.name == 'left':
            print('left')
            emit('left', False)
        elif key.name == 'right':
            print('right')
            emit('right', False)
        elif key.name == 'up':
            print('up')
            emit('up', False)
    except Exception:
        pass


with keyboard.Listener(on_press=on_key_press, on_release=on_key_release) as listener:
    listener.join()
