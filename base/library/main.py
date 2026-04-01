class A:
    x = 1

def file_counter():
    counter = 0
    while True:
        yield counter
        counter += 1

counter = file_counter()
