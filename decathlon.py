from decathlon_get_results import scores
import math

def formalae_track(a,b,c,p):
    result = a * math.pow((b - p), c)
    return result

def formalae_field(a,b,c,p):
    result = a * math.pow((p - b), c)
    return result


def find_100m(score):
    a = 25.4347
    b = 18
    c = 1.81
    result = formalae_track(a, b, c, score)
    return int(result)


def find_longjump(score):
    score = convert_meter_cm(score)
    a = 0.14354
    b = 220
    c = 1.4
    result = formalae_field(a, b, c, score)
    return int(result)

def find_shotput(score):
    a = 51.39
    b = 1.5
    c = 1.05
    result = formalae_field(a, b, c, score)
    return int(result)

def find_highjump(score):
    score = convert_meter_cm(score)
    a = 0.8465
    b = 75
    c = 1.42
    result = formalae_field(a, b, c, score)
    return int(result)

def find_400m(score):
    a = 1.53775
    b = 82
    c = 1.81
    result = formalae_track(a, b, c, score)
    return int(result)

def find_110mhurdles(score):
    a = 5.74352
    b = 28.5
    c = 1.92
    result = formalae_track(a, b, c, score)
    return int(result)

def find_discusthrow(score):
    a = 12.91
    b = 4
    c = 1.1
    result = formalae_field(a, b, c, score)
    return int(result)

def find_polevault(score):
    score = convert_meter_cm(score)
    a = 0.2797
    b = 100
    c = 1.35
    result = formalae_field(a, b, c, score)
    return int(result)
    
def find_javelinthrow(score):
    a = 10.14
    b = 7
    c = 1.08
    result = formalae_field(a, b, c, score)
    return int(result)

def find_1500m(score):
    score = find_get_sec(score)
    #print(score, type(score))
    a = 0.03768
    b = 480
    c = 1.85
    result = formalae_track(a, b, c, score)
    return int(result)

def find_get_sec(time_str):
    """Get Seconds from time."""
    m, s, ms = time_str.split('.')
    seconds = int(m) * 60 + int(s)
    in_sec = str(seconds)+'.'+ms
    return float(in_sec)

# convert to centimer
def convert_meter_cm(meters):
    cm = meters * 100
    return cm