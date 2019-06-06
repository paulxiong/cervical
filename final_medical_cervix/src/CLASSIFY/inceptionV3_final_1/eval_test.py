import pandas as pd
import numpy as np
from sklearn.metrics import roc_auc_score, accuracy_score, recall_score,precision_score,f1_score


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    
    parser.add_argument('--threshold',
                        default=0.9,
                        type=float)
    args = parser.parse_args()
    
    test_df = pd.read_csv('./submission.csv')
    
    test_df.head()
    
    gt = test_df['gt'].values
    gt = np.where(gt>0,1,0)
    
    pred = test_df['positive'].values
    pred_bin = np.where(pred>args.threshold,1,0)
    
    print("AUC Score:",roc_auc_score(gt,pred))
    print("Accuracy:",accuracy_score(gt,pred_bin))
    print("Recall:", recall_score(gt,pred_bin))
    print("Precision:", precision_score(gt,pred_bin))
    print("F1 Score:", f1_score(gt,pred_bin))