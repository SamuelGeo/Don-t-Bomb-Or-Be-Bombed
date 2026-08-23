
def splitMessage(message: str, limit: int) -> list[str]:

    for letter in message :
        if not(letter == letter.lower() or letter == " ") :
            return "Message does not consist of only lowercase english letters"
        
    if len(message) >= 1 and len(message) <= 104 and limit >= 1 and limit <= 104:

        NumberOfParts = 999
        CurrentPartNumber = 1
        CurrentSuffix = "<" + str(CurrentPartNumber) +  "/" + str(NumberOfParts) + ">"
        PartsArray = [CurrentSuffix]

        for letter in message :

            if len(PartsArray[CurrentPartNumber - 1]) == limit :
                

                CurrentPartNumber = CurrentPartNumber + 1
                CurrentSuffix = "<" + str(CurrentPartNumber) + "/" + str(NumberOfParts) + ">"
                PartsArray.append(CurrentSuffix)

            #PartsArray[CurrentPartNumber - 1] = PartsArray[CurrentPartNumber - 1] + letter

            PartsArray[CurrentPartNumber - 1] = PartsArray[CurrentPartNumber - 1].replace("<", letter + "<")
                #print( PartsArray[CurrentPartNumber - 1])

        for iterate in range(100) :

            NumberOfParts = CurrentPartNumber
            CurrentPartNumber = 1
            CurrentSuffix = "<" + str(CurrentPartNumber) +  "/" + str(NumberOfParts) + ">"
            PartsArray = [CurrentSuffix]

            for letter in message :

                if len(PartsArray[CurrentPartNumber - 1]) == limit :
                    

                    CurrentPartNumber = CurrentPartNumber + 1
                    CurrentSuffix = "<" + str(CurrentPartNumber) + "/" + str(NumberOfParts) + ">"
                    PartsArray.append(CurrentSuffix)

                #PartsArray[CurrentPartNumber - 1] = PartsArray[CurrentPartNumber - 1] + letter

                PartsArray[CurrentPartNumber - 1] = PartsArray[CurrentPartNumber - 1].replace("<", letter + "<")
                    #print( PartsArray[CurrentPartNumber - 1])
        if len(PartsArray[len(PartsArray)-1]) > limit :
            return ()


        return PartsArray
    
    else :
        return []


print(splitMessage("this is really a very awesome message", limit = 9))
print(splitMessage("short message", limit = 15))
print(splitMessage("short message", limit = 6))
print(splitMessage("tHis is really a ,, very awesome message", limit = 9))