import random
import json
import sys

def write(start, key, data):
    if (start < 10000000 or start > 99999999):
        print("The start value must be 8 digits long")
        return False

    if (len(str(key)) % 3 != 0):
        print("The length of the key must be a multiple of 3")
        return False

    f = open("data.txt", "w")
    f.truncate(0)

    toWrite = [str(start)]
    for i in range(len(data)):
        ki = (i%(len(str(key))/3))*3
        if (ord(data[i])+int(str(key)[ki:ki+3])>999):
            print("Invalid key")
            f.close()
            return False

        toWrite.append(str(ord(data[i])+int(str(key)[ki:ki+3])))

    end1 = str(key*start-key)
    end2 = end1[0:8]
    toWrite.append(end2)
    f.write("".join(toWrite))
    f.close()
    # print("Written")
    return True

try:
    # write(12345678, 123456, '[{"date":"1/1/1", "entry":"Test"}]')
    print("Press Control+C at any time to cancel")
    dataFile = open("data.txt", "r+")
    key = int(raw_input("Key: "))
    dataRead = dataFile.read()
    a = int(dataRead.rstrip()[:8], 10)
    b = dataRead.rstrip()[-8:]
    c = str(a*key-key)[:8]

    if b == c:
        encodedData = dataRead[8: len(dataRead)-8]
        encodedNumbers = []
        splitKey = []
        decoded = []

        for i in range(len(encodedData)/3):
            encodedNumbers.append(int(encodedData[i*3:i*3+3]))

        for i in range(len(encodedNumbers)):
            ki = (i%(len(str(key))/3))*3
            decoded.append(chr(encodedNumbers[i]-int(str(key)[ki:ki+3])))

        decoded = "".join(decoded)
        decoded = json.loads(decoded)

        if "enter" in sys.argv or 'write' in sys.argv:
            date = raw_input("Todays Date: ")
            entry = raw_input("Entry: ")
            decoded.append({"date": date, "entry": entry})

        elif "read" in sys.argv or "find" in sys.argv:
            date = raw_input("Entry Date: ")
            for i in decoded:
                if i["date"] == date:
                    print(i["date"]+" | "+i["entry"])

        elif "reset" in sys.argv or "delete" in sys.argv:
            y = raw_input("Are you sure? You wont be able to get it back y/n: ")
            if y == "y":
                decoded = []

        elif "dump" in sys.argv or "export" in sys.argv:
            txt = open("export.txt", "w")
            txt.truncate(0)
            for i in decoded:
                txt.write(i["date"]+" | "+i["entry"]+"\n")

            print("Exported to export.txt")

        else:
            print("Can't parse arguments, visit the Github page for a list of valid arguments")

        nk = int(str(random.randint(100, 700))+str(random.randint(100, 700))+str(random.randint(100, 700))+str(random.randint(100, 700)))
        write(random.randint(10000000, 99999999), nk, json.dumps(decoded))
        print("Your new key is "+str(nk)+". Keep it somewhere safe so you can recover your stuff")
    else:
        print("Incorrect key")
finally:
    dataFile.close()
