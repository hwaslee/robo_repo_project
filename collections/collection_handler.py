import json
# import nltk
import collections


def frequency(picked_data, duration):
    if type(duration) == int:
        duration_str = str(duration)
    else:
        duration_str = duration
    result = duration_str + " times, "

    num_counts = collections.Counter(picked_data)
    # print(num_counts)
    most_common = num_counts.most_common(6)
    # print(most_common)
    for idx in range(6):
        num_array = most_common.__getitem__(idx)
        # print(num_array, num_array[0])
        result += (num_array[0] + " ")

    return result


def find_by_order(drawdata, duration="all"):
    # str = 'apple mango apple orange orange apple guava mango mango'

    # print('data to process: {}, {}'.format(type(drawdata), drawdata))
    # all_number_string = ''
    all_number_list = []
    for each_draw in drawdata:
        keys = [k for k, v in each_draw.items()]
        # print('{}, {}'.format(keys, keys[0]))
        # print('{}, {}, {}'.format(type(each_draw.keys), each_draw.keys, each_draw))
        each_number = each_draw[keys[0]]

        for ch in each_number:
            # all_number_string += (ch + ' ')
            all_number_list.append(ch)

    # print('Total picked: {}'.format(all_number_string))
    return frequency(all_number_list, duration)


def load_data():
    # --- 동작 OK, 그러나 robot이 lIST 대신, Map 파일을 생성하므로 아래를 구현
    # with open('C:\\Python\\lotto\\output\\numbersList.json') as f:                  # OK
    #     drawdata = json.load(f)

    with open('C:\\Python\\lotto\\output\\numbersMap.json') as f:  # OK
        drawdata_dict = json.load(f)

    drawdata = drawdata_dict['Picks']
    print(drawdata)

    # --- 아래도 잘 동작함
    # with open('data.json') as f:
    #     data = json.load(f)
    #     print('2', data)

    return drawdata


def pick_new_num():
    result = ""
    all_draw_data = load_data()
    for i in [10, 20, 30, 40, 100, 200, 300, 400, 500]:
        part_data = find_by_order(all_draw_data[0:i], i)
        # result.append(part_data)
        result += (part_data + "\n")
        # print('{} times {}'.format(i, part_data))

    part_data = find_by_order(all_draw_data[0:])
    # print('{} times {}'.format("all", part_data))
    # result.append(part_data)
    result += (part_data + "\n")
    return result


def add_to_dict(self, key, value, dict):
    dict[key] = value   
    return dict


# --- dictionary를 sort 후 list를 return
def sort_dict_by_key(dict, order):
    if(order=='ASC'):
        sorted_dict = sorted(dict.items(), key=lambda item: item[0], reverse=False)
    else: 
        sorted_dict = sorted(dict.items(), key=lambda item: item[0], reverse=True)
    return sorted_dict