import re
import pandas
pat = re.compile(".*ui: \['(.*)'\], click:  '(.*)'")
df = pandas.DataFrame()

with open('ui_candidate_click_train.log','r') as f:
    for line in f:
        if 'click center' in line:
            continue
        result = re.match(pat, line)
        if result:
            candidates = result.group(1).split("', '")
            candidates = [candidate.replace('_',' ', 10**9) for candidate in candidates]
            winner = result.group(2).replace('_',' ', 10**9)
            item = {'score':1, 's1': " ".join(candidates), 's2': winner}
            df = df.append(item, ignore_index=True)

    df.to_csv("xiaoao_train.csv", index=False)
print('done')

