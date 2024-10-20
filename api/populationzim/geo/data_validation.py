'''
simple script to validate & sanitize input from FE
returns True if input validated successfully
otherwise, throws an ambiguous ValueError
'''

def admin_validator(qDictIn):
    vDict = {"ward":"ward","district":"district","province":"province"}
    try:
        adminLevel = vDict[qDictIn["admin"]]
    except:
        raise ValueError(f"Distribution does not understand input '{qDict['admin-level']}'.")
    return True

def distro_validator(qDictIn):
    vDict = {
             "category": {"distribution":"distribution"},
             "sex":      {"total":"total","male":"male","female":"female"},
             "year":     {"2002":"2002","2012":2012,"2022":"2022"},
             "grain":    {"district":"district","ward":"ward","province":"province"}
            }
    qDictOut = {}
    for key in qDictIn:
        if key != "admin":
            try:
                qDictOut.setdefault(key,vDict[key][qDictIn[key]])
            except:
                raise ValueError(f"""Distribution does not understand input '{key}'.""")
        else:
            admin_validator(qDictIn)
    return True
