import sys



def err_input( prompt):
    sys.stderr.write(prompt)
    inp = input('')
    return inp
