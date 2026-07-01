from pynput import keyboard

def on_press(key):
    print("Pressed: ", key)

listener = keyboard.Listener(on_press=on_press)
listener.start()

print("Listening...")

listener.join()
