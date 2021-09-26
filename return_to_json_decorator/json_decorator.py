import json
import functools

def to_json(func):
    @functools.wraps(func) #чтоб не терять атрибуты функции
    def wrapped(*args, **kwargs):
        return json.dumps(func(*args, **kwargs))
    return wrapped

@to_json
def get_data():
  return {
    'data': 42
  }
  
print(get_data())
print(type(get_data())) #str
print(get_data.__name__) #get_data
print(get_data.__dict__) 
