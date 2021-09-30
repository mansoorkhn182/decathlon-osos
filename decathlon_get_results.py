import decathlon
### scores function will get the data file and create scores for all the athlets and save it in scores columns
def scores(datafile):
    prepared_data = {}
    score_list_tmp = []
    #print(datafile)
    for i,row in datafile.iterrows():
        updated_data = {} ## create new disctionary which can be converted to JSON
        
        updated_data['Athlets'] = row['Athlets']
        updated_data['100m'] = row['100m']
        updated_data['Long.jump'] = row['Long.jump']
        updated_data['Shot.put'] = row['Shot.put']
        updated_data['High.jump'] = row['High.jump']
        updated_data['400m'] = row['400m']
        updated_data['110m.hurdle'] = row['110m.hurdle']
        updated_data['Discus'] = row['Discus']
        updated_data['Pole.vault'] = row['Pole.vault']
        updated_data['Javeline'] = row['Javeline']
        updated_data['1500m'] = row['1500m']

        ## find score per event and add them to find the final result
        r100m = decathlon.find_100m(row['100m'])
        rlongjump = decathlon.find_longjump(row['Long.jump'])
        rshotput = decathlon.find_shotput(row['Shot.put'])
        highjump = decathlon.find_highjump(row['High.jump'])
        r400m = decathlon.find_400m(row['400m'])
        r100hurdle = decathlon.find_110mhurdles(row['110m.hurdle'])
        rdiscus = decathlon.find_discusthrow(row['Discus'])
        rpolevault = decathlon.find_polevault(row['Pole.vault'])
        rjaveline = decathlon.find_javelinthrow(row['Javeline'])
        r1500 = decathlon.find_1500m(row['1500m'])

        ## add all the scores from each event and append it to the dictinary and score list
        total_score = r100m + rlongjump + rshotput + highjump + r400m + r100hurdle + rdiscus + rpolevault + rjaveline + r1500
        score_list_tmp.append(total_score)
        updated_data['scores'] = total_score
        prepared_data[i] = updated_data

    #sort the data on the basis of scores column
    prepared_data = sorted(prepared_data.items(), key = lambda x: x[1]['scores'], reverse=True)
    
    ## add place of the athelts and check if there are same score which will have same place
    final_data = add_athelets_place(prepared_data,score_list_tmp)
    

    return final_data

### calculate place and check same scores athelets to assign them same place
def add_athelets_place(prepared_data,score_list_tmp):
    testdata = {}
    r = 1
    tmp = 0
    for x in prepared_data:
        i, j = x
        if j['scores'] in score_list_tmp:
            find_place = score_list_tmp.count(j['scores'])
            #print(find_place)
        if find_place > 1 and testdata:
            #print(testdata)
            for m in testdata.items():
                l, k = m
                tmp = k['place']
                break
        if tmp > 0:
            j['place'] = tmp
        else:
            j['place'] = r
            r += 1
        testdata[i] = j
    prepared_data = sorted(testdata.items(), key = lambda x: x[1]['scores'], reverse=True)
    return prepared_data