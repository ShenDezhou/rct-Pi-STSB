import random
import re
import pandas
pat = re.compile(".*ui: \['(.*)'\], click:  '(.*)'")
df = pandas.DataFrame()

THRESHOLD=128
GROUP=4
LEAF_PER_GROUP=32

with open('ui_candidate_click_train.log','r') as f:
    for line in f:
        if 'click center' in line:
            continue
        result = re.match(pat, line)
        if result:
            candidates = result.group(1).split("', '")
            winner = result.group(2)  # .replace('_',' ', 10**9)
            # candidates = [candidate.replace('_',' ', 10**9) for candidate in candidates]
            times = len(candidates) // LEAF_PER_GROUP + 1
            if times == 1:
                candidates = [candidate.replace('_', ' ', 10 ** 9) for candidate in candidates]
                winner = winner.replace('_', ' ', 10 ** 9)
                item = {'score': 1, 's1': " ".join(candidates), 's2': winner}
                df = df.append(item, ignore_index=True)
            else:
                for _ in range(times):
                    s_can = random.choices(candidates, k=LEAF_PER_GROUP -1)
                    s_can.append(winner)
                    s_can = [candidate.replace('_', ' ', 10 ** 9) for candidate in s_can]
                    winner = winner.replace('_', ' ', 10 ** 9)
                    item = {'score':1, 's1': " ".join(s_can), 's2': winner}
                    df = df.append(item, ignore_index=True)

    df.to_csv("xiaoao_train_alpha.csv", index=False)
print('done')

