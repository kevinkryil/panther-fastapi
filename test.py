from datetime import datetime
import string
import shortuuid

def shortuuid_random():
    alphabet = string.ascii_lowercase + string.digits
    su = shortuuid.ShortUUID(alphabet=alphabet)
    return su.random(length=8)

def guid_gen(word="TMP"):
    try:
        datetime_now = datetime.now()
        year = datetime_now.year
        month = datetime_now.month
        day = datetime_now.day
        wordshort_form = word[0:3].lower()
        uuid = wordshort_form+ str(year)+ str(month) + str(day)+shortuuid_random()
        return uuid
    
    except:
        return {'detail':'Error Found!'}


print(guid_gen('kevin'))