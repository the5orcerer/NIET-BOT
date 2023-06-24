import requests

today = requests.get('__SERVER__').text.lower()
def get_time(dayName):
    dayName = dayName.lower()
    try: 
        routine = list()
        list_tup = [('__ROUTINE__')]

        keys = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'] 
        values = ['__ORDERS__']
        vardict = {k: v for k, v in zip(keys, values)}

        def tORp():
                index = keys.index(today)
                next_index = (index + 1) % len(keys)
                yester_index = (index - 1) % len(keys)
                return keys[next_index], keys[yester_index]
        tommorrow = tORp()
        def day_call(dayName): 
            match dayName:
                case 't' | 'p':
                    tommorrow_dayName = tommorrow[0] if dayName == 't' else tommorrow[1]
                    if tommorrow_dayName in ['friday', 'saturday']:
                        routine.append(f'Routine - {tommorrow_dayName.title()}\n')
                        return ['H']
                    else:
                        routine.append(f'Routine - {tommorrow_dayName.title()}\n')
                        return [list_tup[index] for index in vardict[tommorrow_dayName]]
                case ['friday', 'saturday']:
                    return ['H']
                case _:
                    if dayName in ['friday', 'saturday']:
                        return ['H']
                    else:
                        routine.append(f'Routine - {dayName.title()}\n')
                        return [list_tup[index] for index in vardict[dayName]]
        for elem in day_call(dayName):
            if elem[0] == 'H':
                routine.append(f'Have a rest, there are no classes for the asked day!')
            else:
                routine.append(f"{elem[0]: <5} - {elem[1]: <5} - {elem[2]}\n")
        return ''.join(routine)
    except KeyError as e:
        print(e)
        return 'Wrong Keyword used!'