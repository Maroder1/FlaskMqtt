import json
from datetime import datetime, timezone


def check_json(input):
    try:
        temp = json.dumps(input)
        value = json.loads(temp)
        return value
    except:
        return input

a = {"name": "John",
     "age": 31,
     "Salary": 25000,
     "time": 0}
print (a)
#a = 3
print (check_json(a))
print (check_json(a)["Salary"])


now = datetime.utcnow().replace(tzinfo=timezone.utc).isoformat()
print (now)
