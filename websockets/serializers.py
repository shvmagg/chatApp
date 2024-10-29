import json

#fromuserId, toUserId, message(client)
#how data is present in txt ->"{\"key\":\"value\"}" -> {"key":"value"}

def deserializer(txt):#{text:hi}
    print(txt)
    print(type(txt))
    x=json.loads(txt)
    print(x)
    if type(x) == dict:
        x.update({
            'status':'success'
        })
        print("deserializer executed")
        return x
    print("deserializer executed")
    return {'status':'failed'}

    