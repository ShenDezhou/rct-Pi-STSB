import random
import re
import pandas
pat = re.compile(".*ui: \['(.*)'\], click:  '(.*)'")
df = pandas.DataFrame()

THRESHOLD=128
GROUP=4
LEAF_PER_GROUP=32

def get_split(sid):
    if sid % 10 == 9:
        return 'test'
    if sid % 10 == 8:
        return 'dev'
    return 'train'

sid = 1
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
                loser = random.choice(candidates)
                candidates = [candidate.replace('_', ' ', 10 ** 9) for candidate in candidates]
                winner = winner.replace('_', ' ', 10 ** 9)
                item = {'split':get_split(sid),'dataset':"xiaoao",'sid':sid, 'score': 1, 'sentence1': " ".join(candidates), 'sentence2': winner}
                df = df.append(item, ignore_index=True)
                sid += 1

                loser = loser.replace('_', ' ', 10 ** 9)
                item = {'split':get_split(sid),'dataset':"xiaoao",'sid':sid, 'score': 0, 'sentence1': " ".join(candidates), 'sentence2': loser}
                df = df.append(item, ignore_index=True)
                sid += 1
            else:
                for _ in range(times):
                    s_can = random.choices(candidates, k=LEAF_PER_GROUP -1)
                    s_can.append(winner)
                    s_can = [candidate.replace('_', ' ', 10 ** 9) for candidate in s_can]
                    winner = winner.replace('_', ' ', 10 ** 9)
                    item = {'split':get_split(sid),'dataset':"xiaoao",'sid':sid, 'score':1, 'sentence1': " ".join(s_can), 'sentence2': winner}
                    df = df.append(item, ignore_index=True)
                    sid += 1
                for _ in range(random.randint(1, times)):
                    s_can = random.choices(candidates, k=LEAF_PER_GROUP -1)
                    loser = random.choice(s_can)
                    s_can = [candidate.replace('_', ' ', 10 ** 9) for candidate in s_can]
                    loser = loser.replace('_', ' ', 10 ** 9)
                    item = {'split':get_split(sid),'dataset':"xiaoao",'sid':sid, 'score':0, 'sentence1': " ".join(s_can), 'sentence2': loser}
                    df = df.append(item, ignore_index=True)
                    sid += 1

    df['sid'] = df['sid'].astype(int)
    df['score'] = df['score'].astype(int)
    df.to_csv("xiaoao_train_alpha.csv", columns=['split', 'dataset', 'sid', 'score','sentence1','sentence2'], index=False)
print('done')

