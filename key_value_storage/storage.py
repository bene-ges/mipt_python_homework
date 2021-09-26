import argparse
import os
import tempfile
import json

def put(key, value, data):
    if key not in data:
        data[key] = []
    data[key].append(value)


def get(key, data):
    if key in data:
        print(", ".join(data[key]))
    else:
        print() #выводим пустую строку, как требуется

def main():
    storage_path = os.path.join(tempfile.gettempdir(), 'storage.data')

    parser = argparse.ArgumentParser(description='Key-value storage.')
    parser.add_argument('--key')
    parser.add_argument('--val')
    parser.add_argument('--clear', action='store_true')
    args = parser.parse_args()
    if args.clear:
        os.remove(storage_path)
        return

    json_data = {}
    try:
        with open(storage_path, 'r') as f:
            json_data = json.load(f)
    except:
        pass

    assert(args.key), "Expect --key argument"
    if args.val is not None:
        put(args.key, args.val, json_data)
        with open(storage_path, 'w') as f:
            json.dump(json_data, f)
    else:
        get(args.key, json_data)


if __name__ == '__main__':
    main()



