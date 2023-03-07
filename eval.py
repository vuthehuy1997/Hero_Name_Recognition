import os
import argparse


if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--pred', type=str, default='test_data/test.txt')
    parser.add_argument('--gt', type=str, default='output.txt')
    parser.add_argument('--out', type=str, default='eval.txt')

    args = parser.parse_args()
with open(args.gt) as f:
    gts = [line.strip().split() for line in f]
    gts.sort()

with open(args.pred) as f:
    preds = [line.strip().split() for line in f]
    preds.sort()

acc = 0
with open(args.out, 'w') as f:
    for i in range(len(gts)):
        if gts[i][0] != preds[i][0]:
            print('wrong, ',gts[i][0], preds[i][0])
            break
        f.write(os.path.basename(gts[i][0]) + '\t' + gts[i][1] + '\t' + preds[i][1] + '\n')
        acc += gts[i][1] == preds[i][1]
    f.write('ACC: ' + str(acc/len(gts)))