import os
import time
import ConfigParser
import pandas as pd
import re

def get_svm_score(config):
    #global config
    experiment_root = os.path.join(config.get('data','experiment_root'), config.get('model','path'))
    score = {}
    with open(os.path.join(experiment_root,'log')) as f:
        tmp = f.readlines()
        tmp.reverse()
        for i, string in enumerate(tmp):
            x = re.search(r'SVM - (.*):(.*)', string)
            if x is not None:
                score[x.group(1)] = x.group(2)
                for j in range(2):
                    string = tmp[i-1-j]
                    x = re.search(r'(.*):(.*)', string)
                    assert x is not None, "Error, there is some bug of {} line in log to get score,{}".format(i, string)
                    score[x.group(1)] = x.group(2)
                break
    return score   


class Archiver():
    
    def init(self):
        config = ConfigParser.ConfigParser()
        config_path = os.path.join(os.path.dirname(__file__), "configure.conf")
        
        config.read(config_path)
        self._experiment_root = os.path.abspath(config.get('data', 'experiment_root'))
        
        self._trn_n_image_path = os.path.join(self._experiment_root,config.get('data', 'train_path_n'))
        self._trn_p_image_path = os.path.join(self._experiment_root,config.get('data', 'train_path_p'))
        
        self._tst_n_image_path = os.path.join(self._experiment_root,config.get('data', 'test_path_n'))
        self._tst_p_image_path = os.path.join(self._experiment_root,config.get('data', 'test_path_p'))
        
        self._model_path = os.path.join(self._experiment_root,config.get('model', 'path'))
        self._purity = config.get('model', 'purity')
        self._entropy = config.get('model', 'entropy')
        self._itera = config.get('model', 'itera')
        
        score = get_svm_score(config)
        print(score)
        
        self._score_precision = score['precision']
        self._score_recall = score['recall']
        self._score_f1 = score['f1_score']
        
        self._username = config.get('user', 'username')
        
        store_root = os.path.abspath(config.get('path', 'store_path'))
        self._ts = int(time.time())
        self._store_path = os.path.join(store_root, self._username, str(self._ts))
        if not os.path.exists(self._store_path):
            os.makedirs(self._store_path)
            
        self._db_path = config.get('path', 'db')
        
    def archive_train(self):
        for src in [self._trn_n_image_path, self._trn_p_image_path]:
            src = os.path.dirname(src)
            dirname = os.path.dirname(src)
            print(dirname)
            name = os.path.join(self._store_path, os.path.basename(src))
            print(name)
            cmd = "cd {} && tar czvf {}.tar.gz {}".format(dirname, name, os.path.basename(src))
            code = os.system(cmd) 
            if code == 0:
                print("Archive-Train: {} archive success!".format(name))
            else:
                print("Archive-Train: {} archive failed, error code {}!".format(name, code))
        
    def archive_test(self):
        for src in [self._tst_n_image_path, self._tst_p_image_path]:
            src = os.path.dirname(src)
            dirname = os.path.dirname(src)
            name = os.path.join(self._store_path, os.path.basename(src))
            cmd = "cd {} && tar czvf {}.tar.gz {}".format(dirname, name, os.path.basename(src))
            code = os.system(cmd) 
            if code == 0:
                print("Archive-Test: {} archive success!".format(name))
            else:
                print("Archive-Test: {} archive failed, error code {}!".format(name, code))
                
    def archive_model(self):
        model_path = os.path.join(self._model_path, 'model')
        name = os.path.join(self._store_path, 'gan_model')
        
        cmd = "cd {} && tar czvf {}.tar.gz ./net*{}_{}_{}.pth".format(model_path, name, self._purity,self._entropy, self._itera)
        code = os.system(cmd)
        
        if code == 0:
            print("Archive-Model: {} archive success!".format(name))
        else:
            print("Archive-Model: {} archive failed, error code {}!".format(name, code))
    
    def update_db(self, archive_type):
        
        assert archive_type in ['Train', 'Test'], 'Error archive type: {}'.format(archive_type)
        
        date = time.localtime(self._ts)
        date = time.strftime("%Y--%m--%d", date)
        values = [self._username, self._ts, date, self._store_path, archive_type, self._score_precision, self._score_recall, self._score_f1]
        columns = ['Username', 'TimeStamp', 'Date', 'Checkpoint_path','Archive_Type', 'Precision', 'Recall', 'F1']
        entry = pd.DataFrame([values], columns=columns)
        
        try:
            db = pd.read_csv(self._db_path)
        except:
            db = pd.DataFrame([], columns=columns)
        
        db = db.append(entry, ignore_index=True)
        
        db.to_csv(self._db_path, index=False)
        

if __name__=='__main__':
    saver = Archiver()
    score = {'precision':0.5, 'recall':0.5, 'f1':0.5}
    
    saver.init()
    saver.archive_train()
    saver.archive_test()
    saver.archive_model()
    saver.update_db('Test')
        