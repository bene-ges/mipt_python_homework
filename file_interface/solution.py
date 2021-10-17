import doctest
import os
import tempfile
import uuid

class File:
    def __init__(self, filename):
        assert(len(filename) > 0)
        self.filename = filename
        if not os.path.exists(self.filename):
            f = open(self.filename, 'w')
            f.close()

    def read(self):
        f = open(self.filename)
        s = "".join(f.readlines())
        f.close()
        return s

    def write(self, text):
        f = open(self.filename, "w")
        n = f.write(text)
        f.close()
        return n

    def __add__(self, other):
        assert(os.path.exists(other.filename))
        new_name = os.path.join(tempfile.gettempdir(), str(uuid.uuid4()))
        new_file = File(new_name)
        s1 = self.read()
        s2 = other.read()
        new_file.write(s1 + s2)
        return new_file
        
    def __str__(self):
        return self.filename

    def __iter__(self):
        yield from open(self.filename)


def run_tests():
    """
    # doctest: +ELLIPSIS
    >>> path_to_file = 'some_filename'
    >>> os.path.exists(path_to_file)
    False
    >>> file_obj = File(path_to_file)
    >>> os.path.exists(path_to_file)
    True
    >>> print(file_obj)
    some_filename
    >>> file_obj.read()
    ''
    >>> file_obj.write('some text')
    9
    >>> file_obj.read()
    'some text'
    >>> file_obj.write('other text')
    10
    >>> file_obj.read()
    'other text'
    >>> file_obj_1 = File(path_to_file + '_1')
    >>> file_obj_2 = File(path_to_file + '_2')
    >>> file_obj_1.write('line 1\\n')
    7
    >>> file_obj_2.write('line 2\\n')
    7
    >>> new_file_obj = file_obj_1 + file_obj_2
    >>> isinstance(new_file_obj, File)
    True
    >>> str(new_file_obj).startswith(tempfile.gettempdir())
    True
    >>> for line in new_file_obj:
    ...    print(ascii(line))  
    'line 1\\n'
    'line 2\\n'
    >>> new_path_to_file = str(new_file_obj)
    >>> os.path.exists(new_path_to_file)
    True
    >>> file_obj_3 = File(new_path_to_file)
    >>> str(file_obj_3).startswith(tempfile.gettempdir())
    True
    >>>
    """
    return

if __name__ == "__main__":
    doctest.testmod()


    