<template>
  <div class="card">
    <section class="train-info">
      <el-form label-position="left">
        <el-form-item label="id">
          <span>{{ trainInfo.id }}</span>
        </el-form-item>
        <el-form-item label="描述">
          <span>{{ trainInfo.desc }}</span>
        </el-form-item>
        <el-form-item label="本次训练出的所有模型里面最优模型是第几个">
          <span>{{ trainInfo.best_model }}</span>
        </el-form-item>
        <el-form-item label="被哪次dataset训练的">
          <span>{{ trainInfo.did }}</span>
        </el-form-item>
        <el-form-item label="评估准确度">
          <span>{{ trainInfo.evaluate_value }}</span>
        </el-form-item>
        <el-form-item label="训练输入的尺寸">
          <span>{{ trainInfo.input_shape }}</span>
        </el-form-item>
        <el-form-item label="损失">
          <span>{{ trainInfo.loss }}</span>
        </el-form-item>
        <el-form-item label="训练的准确度">
          <span>{{ trainInfo.metric_value }}</span>
        </el-form-item>
        <el-form-item label="产生的模型个数">
          <span>{{ trainInfo.model_count }}</span>
        </el-form-item>
        <el-form-item label="训练有几个分类">
          <span>{{ trainInfo.n_classes }}</span>
        </el-form-item>
        <el-form-item label="训练用了多少张图片">
          <span>{{ trainInfo.n_train }}</span>
        </el-form-item>
        <el-form-item label="模型文件路径">
          <span>{{ trainInfo.path }}</span>
        </el-form-item>
        <el-form-item label="训练评估得到的准确率">
          <span>{{ trainInfo.precision }}</span>
        </el-form-item>
        <el-form-item label="训练评估得到的召回率">
          <span>{{ trainInfo.recall }}</span>
        </el-form-item>
        <el-form-item label="模型类别">
          <span>{{ trainInfo.type }}</span>
        </el-form-item>
      </el-form>
    </section>
    <!-- <el-card class="box-card" shadow="hover">
      <div slot="header" class="clearfix">
        <span>Cell20198_231125978646576151</span>
      </div>
      <div class="flex model-info">
        <section class="info flex created">
          <h3>Created</h3>
          <b>{{trainInfo.created_at}}</b>
          <i>1 computer hour</i>
        </section>
        <section class="info flex analyzed">
          <h3>Analyzed</h3>
          <b>5238 images</b>
          <i>2 labels,520 test images</i>
        </section>
        <section class="info flex avg">
          <h3>Avg precision</h3>
          <b>0.996</b>
        </section>
        <section class="percent">
          <el-progress
            type="circle"
            class="percent"
            :percentage="trainInfo.precision===-1?0:trainInfo.precision"
          ></el-progress>
          <h4 class="percent-title">Precision</h4>
          <el-tooltip placement="bottom" class="percent-tip">
            <div slot="content">
              percent
              <br />表示精确度
            </div>
            <i class="el-icon-question"></i>
          </el-tooltip>
        </section>
        <section class="recall">
          <el-progress
            type="circle"
            class="recall"
            :percentage="trainInfo.recall===-1?0:trainInfo.recall"
          ></el-progress>
          <h4 class="recall-title">Recall</h4>
          <el-tooltip placement="bottom" class="recall-tip">
            <div slot="content">
              recall
              <br />表示有点东西
            </div>
            <i class="el-icon-question"></i>
          </el-tooltip>
        </section>
      </div>
    </el-card> -->
  </div>
</template>

<script>
import { modelType } from '@/const/const'

export default {
  name: 'Card',
  components: {},
  props: {
    trainInfo: {
      type: Object,
      default: {}
    }
  },
  filters: {
    filterModelType(value) {
      return modelType[value].name
    }
  }
}
</script>

<style lang="scss" scoped>
.card {
  i {
    color: #ccc;
    font-style: normal;
  }
  b {
    font-size: 22px;
  }
  .model-info {
    justify-content: space-around;
    .info {
      flex-direction: column;
      justify-content: flex-start;
    }
    .percent {
      position: relative;
    }
    .percent-title {
      position: absolute;
      top: 10px;
      left: 30px;
    }
    .el-icon-question {
      position: absolute;
      bottom: 30px;
      left: 55px;
    }
    .recall {
      position: relative;
    }
    .recall-title {
      position: absolute;
      top: 10px;
      left: 40px;
    }
  }
}
</style>
