

def admin_validator(qDict):
    vDict = {"district":"district","province":"province"}
    try:
        adminLevel = vDict[qDict["admin-level"]]
    except:
        raise ValueError(f"Distribution does not understand input '{qDict['admin-level'}'.")


def distro_validator(qDict):
    vDict = {
             "sex":     {"total":"total","male":"male","female":"female"},
             "year":    {"2002":"2002","2012":2012,"2022":"2022"},
             "grain":   {"district":"district","ward":"ward","province":"province"},
            }
    for key in qDict:
        try:
            qDict["sex"] = vDict["sex"][qDict["sex"]]
        except:
            raise ValueError(f"Distribution does not understand input '{qDict['sex']}'.")
    
    
             

