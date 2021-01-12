
import csv
from collections import Counter


def avg(lst):
	x = sum(lst)
	c = len(lst)
	return x/c


def do(lst):
    print(len(lst))
    reachyn = Counter([x['reachable'] for x in lst])
    print(reachyn, reachyn['True']/len(lst))
    rp = Counter([(x['reachable'],x['errors']) for x in lst])
    print(Counter([(x['reachable'],x['errors']) for x in lst]))
    print(Counter([(x['errorlist']) for x in lst]))
    print('time1',max([x['time1'] for x in lst]), avg([float(x['time1']) for x in lst]), )
    print('time2',max([x['time2'] for x in lst]), avg([float(x['time2']) for x in lst]), )
    print('time3',max([x['time3'] for x in lst if x['reachable'] == 'True']), avg([float(x['time3']) for x in lst if x['reachable'] == 'True' and x['errors']== 'False']) )
    # Instance size","Decision Time & Unreachable (Percentage) & Invariant Proof Time & Reachable (Percentage) & Reachable+Proof & Reachability Proof Time
    return {
        "Instance size": lst[0]['size'],
        "Decision time avg": avg([float(x['time1']) for x in lst]), 
        "Decision time max": max([float(x['time1']) for x in lst]),
        "Unreachable": (reachyn['False'], reachyn['False']/len(lst)*100),
        "Invariant Proof Time avg": avg([float(x['time2']) for x in lst]),
        "Invariant Proof Time max": max([float(x['time2']) for x in lst]),
        "Reachable": (reachyn['True'], reachyn['True']/len(lst)*100),
        "Reachable+Proof": (rp[('True', 'False')], rp[('True', 'False')]/reachyn['True']*100),
        "Reachability Proof Time avg": avg([float(x['time3']) for x in lst if x['reachable'] == 'True' and x['errors']== 'False']), 
        "Reachability Proof Time max": max([float(x['time3']) for x in lst if x['reachable'] == 'True'])
    }    

    # stcodes= set([x['stcode'] for x in lst])
    # for code in stcodes:
    #     print(code, len([x for x in lst if x['stcode'] ==code and  x['reachable'] =='True']), len([x for x in lst if x['stcode'] ==code and  x['reachable'] =='False']), len([x for x in lst if x['stcode'] ==code and  x['reachable'] =='True' and x['errors'] == 'False']), len([x for x in lst if x['stcode'] ==code and  x['reachable'] =='True' and x['errors'] == 'True']))
 


with open('document.csv', mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file,delimiter=',')
    # print(list(csv_reader)[0])
    lst = list(csv_reader)
    sizes = list(set([int(x['size']) for x in lst]))
    sizes.sort()
    print("all")
    a = do(lst)
    a['Instance size'] = 'all'
    mylist = [a]
    for sz in sizes:
        print("Size",sz)
        a = do([x for x in lst if x['size'] == str(sz)])
        mylist.append(a)

    ordering = ["Instance size","Decision time avg","Decision time max","Unreachable",
    "Invariant Proof Time avg","Invariant Proof Time max","Reachable","Reachable+Proof","Reachability Proof Time avg","Reachability Proof Time max"]
    for x in mylist:
        strings = []
        for y in ordering:
            ob = x[y]
            if type(x[y]) is tuple:
                this = ""
                for i in range(2):
                    this+=" " 
                    if i == 1:
                        this+= "("
                    if int(float(x[y][i])) == x[y][i]:
                        this+=  str(x[y][i])
                    else: 
                        this+= f'{x[y][i]:.3}'

                    if i == 1:
                        this+= "\%)"
                strings.append(this)
            else:
                if type(x[y]) is str and  not x[y].isnumeric():
                    strings.append(str(x[y]))
                elif int(float(x[y])) == float(x[y]):
                    strings.append(str(x[y]))
                else: 
                    strings.append( f'{float(x[y]):.3f}')

        ot = " & ".join(strings) + " \\\\ "
        print(ot)

