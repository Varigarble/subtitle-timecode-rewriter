import re

'''
Read a utf-8 text file, e.g., .srt,
search for timecodes,
add or subtract a specified amount of time to each timecode,
write original file contents to new file with new timecodes.
timecode format: 23:59:59,999
'''

filein = open("", 'r', \
            encoding='utf-8')
    
fileout = open("", 'w', \
            encoding='utf-8')

orig_sub = filein.read()

pattern = re.compile(r'\d{2}:\d{2}:\d{2},\d{3}')

calc = input("Add or subtract time (+/-)? ")

while calc != '+' and calc != '-':
    calc = input("Enter the input indicated (+/-): ")

def set_amount():
    prompt = 'Enter the amount of time to change (00:00:00,000): '
    amountck = False

    while amountck == False:

        try:
            amount = input(prompt)

            if pattern.match(amount) == None:
                prompt = 'Use the correct format (00:00:00,000): '
                raise ValueError("format")
            
            if not (0 <= int(amount[0:2]) < 24):
                prompt = 'Hours must be from "00" to "23" (23:59:59,999): '
                raise ValueError("hrs")
            
            if not (0 <= int(amount[3:5]) < 60):
                prompt = 'Minutes must be from "00" to "59" (23:59:59,999): '
                raise ValueError("mins")

            if not (0 <= int(amount[6:8]) < 60):
                prompt = 'Seconds must be from "00" to "59" (23:59:59,999): '
                raise ValueError("secs")

        except ValueError:
            amountck = False

        else:
            amountck = True
            amount_hrs = int(amount[0:2])
            amount_mins = int(amount[3:5])
            amount_secs = int(amount[6:8])
            amount_mils = int(amount[9:12])

    assert 0 <= amount_hrs < 24, 'invalid hours'
    assert 0 <= amount_mins < 60, 'invalid mins'
    assert 0 <= amount_secs < 60, 'invalid secs'
    assert 0 <= amount_mils < 1000, 'invalid milliseconds'

    return amount_hrs, amount_mins, amount_secs, amount_mils

amount_hrs, amount_mins, amount_secs, amount_mils = set_amount()

def plus(hrs_in, mins_in, secs_in, mils_in):
    
    mils_out = mils_in + amount_mils
    if mils_out > 999:
        secs_in += 1
        mils_out -= 1000
    
    secs_out = secs_in + amount_secs
    if secs_out > 59:
        mins_in += 1
        secs_out -= 60

    mins_out = mins_in + amount_mins
    if mins_out > 59:
        hrs_in += 1
        mins_out -= 60

    hrs_out = hrs_in + amount_hrs
    if hrs_out > 23:
        hrs_out -= 24

    return hrs_out, mins_out, secs_out, mils_out
    
def minus(hrs_in, mins_in, secs_in, mils_in):
    
    mils_out = mils_in - amount_mils
    if mils_out < 0:
        secs_in -= 1
        mils_out += 1000
    
    secs_out = secs_in - amount_secs
    if secs_out < 0:
        mins_in -= 1
        secs_out += 60

    mins_out = mins_in - amount_mins
    if mins_out < 0:
        hrs_in -= 1
        mins_out += 60

    hrs_out = hrs_in - amount_hrs
    if hrs_out < 0:
        hrs_out += 24

    return hrs_out, mins_out, secs_out, mils_out

if calc == '+':
    op = plus

if calc == "-": 
    op = minus

def calculator(matchobj):
    hrs_in = int(matchobj.group(0)[0:2])
    mins_in = int(matchobj.group(0)[3:5])
    secs_in = int(matchobj.group(0)[6:8])
    mils_in = int(matchobj.group(0)[9:12])

    hrs_out, mins_out, secs_out, mils_out = op(hrs_in, mins_in, secs_in, mils_in)

    matchint = ("%02d" % hrs_out, ":", \
                "%02d" % mins_out, ":", \
                "%02d" % secs_out, ",", \
                "%03d" % mils_out)
    newstr = ''.join(map(str, matchint))
    return newstr

new_sub = re.sub(r'\d{2}:\d{2}:\d{2},\d{3}', calculator, orig_sub)

fileout.write(new_sub)

