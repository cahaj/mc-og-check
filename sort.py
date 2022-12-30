import json
with open("oglist/oglist.json", "r", encoding="utf-8") as f:
    oglist = json.load(f)
    oglist = [x.lower() for x in oglist]
    print(oglist)

def split_list(lst, char):
    return filter(lambda x: x[0] == char, lst)

def sort():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    for i in letters:
        words = list(split_list(oglist, i))
        with open(f"oglist/oglist_{i}.json", "w", encoding="utf-8") as f:
            json.dump(words, f)

if __name__ == '__main__':
    sort()