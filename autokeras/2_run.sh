#!/bin/bash
set -e
tasklist='task.list'

if [ ! -f ${tasklist} ] || [ ! -f main.py ]; then
	echo "not found main.py or "${tasklist}
fi

rm *.log -f

cnt=0
while read line
do
  line2=$(echo ${line} | sed 's/ //g')
  # 跳过空白行， 跳过'#'好开头的行
  if [ ${#line2} -lt 1 ] || [ ${line2:0:1}'x' == '#x' ]; then
      continue
  fi
  cnt=$(( $cnt + 1 ))

  array=(${line2//,/ })
  if [ ! ${#array[@]} -eq 4 ]; then
      echo "invalied task!!!  "${line2}
  fi

  task_type=$(echo ${array[0]} | sed 's/"//g')
  task_dir=$(echo ${array[1]} | sed 's/"//g')
  task_mod=$(echo ${array[2]} | sed 's/"//g')
  task_desc=$(echo ${array[3]} | sed 's/"//g')

  pushd ${task_dir}
    rm -rf resize_* predict_error_data/* *.csv
  popd
  
  if [ ! -d ${task_dir} ]; then
    echo "not found "${task_dir}
    exit 1
  fi

  if [ ${task_type}'x' == 'predictx' ] && [ ! -f ${task_mod} ];then
    echo "not found "${task_mod}
    exit 1
  fi
  #删除不是图片的文件 
  find ${task_dir} -name ".ipynb_checkpoints" | xargs rm -rf

  echo $cnt'  '${task_desc}
  echo 'python main.py --task '${task_type}' --taskdir '${task_dir}' --modfile '${task_mod}
  python main.py --task ${task_type} --taskdir ${task_dir} --modfile ${task_mod} | tee $cnt'.log'
  echo ""
done < ${tasklist}
