import json

json.dumps(某obj, default=lambda o: o.__dict__)