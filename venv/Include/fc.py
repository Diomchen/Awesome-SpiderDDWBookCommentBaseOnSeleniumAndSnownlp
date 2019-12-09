import pandas as pd
from snownlp import SnowNLP
from snownlp import seg

def segWord_positiveRateCalc(str):
    s = SnowNLP(str)
    return s.words,s.sentiments

if __name__ == '__main__':
    df = pd.read_excel('book_score_comment.xlsx')
    df = df.dropna(axis=0).drop('Unnamed: 0',axis=1)

    seg_word = []
    seg_positive_score = []
    for i in range(len(df)):
        se,ss = segWord_positiveRateCalc(df.iloc[i,0])
        seg_word.append(se)
        seg_positive_score.append(ss)

    pd.DataFrame(seg_positive_score).to_excel('seg_positive_score.xlsx')
    rightCount = 0
    good_comments_pred , good_comments_actully = 0,0
    normal_comments_pred,normal_comments_actully = 0,0
    terrible_comments_pred,terrible_comments_actully = 0,0
    for i in range(len(seg_positive_score)):
        predict = seg_positive_score[i]
        actully = int(df.iloc[i,1].split('分')[0])
        if predict<=0.01 :
            terrible_comments_pred += 1
        elif predict>0.01 and predict<=0.08:
            normal_comments_pred+=1
        elif predict>0.08:
            good_comments_pred += 1


        if actully<3 :
            terrible_comments_actully += 1
        elif actully>=3 and actully<=6:
            normal_comments_actully+=1
        elif actully>6:
            good_comments_actully += 1


        if (predict<=0.01 and actully<3)or((predict>0.01 and predict<=0.08)and (actully>=3 and actully<=6))or(predict>0.08 and actully>6):
            rightCount+=1

    print('好评预测数：{}，好评实际数：{}'.format(good_comments_pred,good_comments_actully))
    print('中评预测数：{}，中评实际数：{}'.format(normal_comments_pred, normal_comments_actully))
    print('差评预测数：{}，差评实际数：{}'.format(terrible_comments_pred, terrible_comments_actully))
    print('precise:{:.3f}'.format(rightCount/len(seg_positive_score)))
