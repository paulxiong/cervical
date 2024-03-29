import request from '@/utils/request'

export function getPercent(query) {
  return request({
    url: '/api1/jobpercent',
    method: 'get',
    params: query
  })
}

export function getDatasetLists(query) {
  return request({
    url: '/api1/dtinfo',
    method: 'get',
    params: query
  })
}

export function getListprojects(query) {
  return request({
    url: '/api1/listprojects',
    method: 'get',
    params: query
  })
}

export function downloadImgs(query) {
  return request({
    url: '/api1/zipdownload',
    method: 'get',
    responseType: 'blob',
    params: query
  })
}

export function uploadImgs(query) {
  return request({
    url: '/api1/upload',
    method: 'get',
    params: query
  })
}

export function getImgbymid(query) {
  return request({
    url: '/api1/getimgbymid',
    method: 'get',
    params: query
  })
}

export function getBatchInfo(query) {
  return request({
    url: '/api1/batchinfo',
    method: 'get',
    params: query
  })
}

export function getMedicalIdInfo(query) {
  return request({
    url: '/api1/medicalidinfo',
    method: 'get',
    params: query
  })
}

export function getImgListOfWanted(data) {
  return request({
    url: '/api1/imglistsofwanted',
    method: 'post',
    data
  })
}

export function getImgListOneByOne(query) {
  return request({
    url: '/api1/imglistsonebyone',
    method: 'get',
    params: query
  })
}

export function getLabelByImageId(query) {
  return request({
    url: '/api1/getLabelbyimageid',
    method: 'get',
    params: query
  })
}

export function getLabelReviews(query) {
  return request({
    url: '/api1/reviews',
    method: 'get',
    params: query
  })
}

export function updateLabelReview(data) {
  return request({
    url: '/api1/review',
    method: 'post',
    data
  })
}

export function getDatasetImgs(query) {
  return request({
    url: '/api1/datasetimgs',
    method: 'get',
    params: query
  })
}

export function getimgnptypebymids(data) {
  return request({
    url: '/api1/getimgnptypebymids',
    method: 'post',
    data
  })
}

export function updatePredict(data) {
  return request({
    url: '/api1/updatepredict',
    method: 'post',
    data
  })
}

export function reviewpredict(data) {
  return request({
    url: '/api1/reviewpredict',
    method: 'post',
    data
  })
}

export function createdataset(data) {
  return request({
    url: '/api1/createdataset',
    method: 'post',
    data
  })
}

export function listdatasets(query) {
  return request({
    url: '/api1/listdatasets',
    method: 'get',
    params: query
  })
}

export function getCategoryInfo(query) {
  return request({
    url: '/api1/categoryinfo',
    method: 'get',
    params: query
  })
}

export function jobresult(data) {
  return request({
    url: '/api1/jobresult',
    method: 'post',
    data
  })
}

export function updateLabel(data) {
  return request({
    url: '/api1/updatelabelsofimage',
    method: 'post',
    data
  })
}

export function getjobresult(query) {
  return request({
    url: '/api1/jobresult',
    method: 'get',
    params: query
  })
}

export function getjoblog(query) {
  return request({
    url: '/api1/joblog',
    method: 'get',
    params: query
  })
}

export function createTrain(data) {
  return request({
    url: '/api1/train',
    method: 'post',
    data
  })
}

export function getjobmodel(query) {
  return request({
    url: '/api1/jobmodel',
    method: 'get',
    params: query
  })
}

export function savemodel(data) {
  return request({
    url: '/api1/savemodel',
    method: 'post',
    data
  })
}

export function getTrainresult(query) {
  return request({
    url: '/api1/trainresult',
    method: 'get',
    params: query
  })
}

export function getListmodel(query) {
  return request({
    url: '/api1/listmodel',
    method: 'get',
    params: query
  })
}

export function createPredict(data) {
  return request({
    url: '/api1/predict',
    method: 'post',
    data
  })
}

export function createProject(data) {
  return request({
    url: '/api1/createproject',
    method: 'post',
    data
  })
}

export function getPredictResult(query) {
  return request({
    url: '/api1/predictresult',
    method: 'get',
    params: query
  })
}

export function getPredictResult2(query) {
  return request({
    url: '/api1/predictresult2',
    method: 'get',
    params: query
  })
}

export function getOverview(query) {
  return request({
    url: '/api1/overview',
    method: 'get',
    params: query
  })
}

export function getVerificationcnt(query) {
  return request({
    url: '/api1/verificationcnt',
    method: 'get',
    params: query
  })
}

export function getAllPredictResult(query) {
  return request({
    url: '/api1/allpredictresult',
    method: 'get',
    params: query
  })
}

export function getPredictsByPID(query) {
  return request({
    url: '/api1/predictsbypid',
    method: 'get',
    params: query
  })
}

export function getPredictsByPID2(query) {
  return request({
    url: '/api1/predictsbypid2',
    method: 'get',
    params: query
  })
}

export function setPredictsReview(data) {
  return request({
    url: '/api1/setpredictsreview',
    method: 'post',
    data
  })
}

export function downloadReviews(data) {
  return request({
    url: '/api1/downloadreviews',
    method: 'post',
    responseType: 'blob',
    data
  })
}

export function removeProject(query) {
  return request({
    url: '/api1/removeproject',
    method: 'get',
    params: query
  })
}

export function createProjectResult(data) {
  return request({
    url: '/api1/result',
    method: 'post',
    data
  })
}

export function listProjectResult(query) {
  return request({
    url: '/api1/result',
    method: 'get',
    params: query
  })
}

export function downloadResults(data) {
  return request({
    url: '/api1/downloadresult',
    method: 'post',
    responseType: 'blob',
    data
  })
}

export function removeDataSet(query) {
  return request({
    url: '/api1/removedataset',
    method: 'get',
    params: query
  })
}

// 跳转页面下载
export const downloadCellsURL = '/api1/downloadcells'

export function getScantxtByDID(query) {
  return request({
    url: '/api1/scantxtbydid',
    method: 'get',
    params: query
  })
}

export function getReviewsByPid(query) {
  return request({
    url: '/api1/reviewsbypid',
    method: 'get',
    params: query
  })
}

export function getProjectsToReview(query) {
  return request({
    url: '/api1/projectsbyvid',
    method: 'get',
    params: query
  })
}

export function getBidMid(query) {
  return request({
    url: '/api1/bidmid',
    method: 'get',
    params: query
  })
}

export function updateLabel2(data) {
  return request({
    url: '/api1/updatelabel2s',
    method: 'post',
    data
  })
}

export function getlabel2sbypid(query) {
  return request({
    url: '/api1/label2sbypid',
    method: 'get',
    params: query
  })
}

export function uploadCustomMedical(data) {
  return request({
    url: '/api1/uploadm',
    method: 'post',
    headers: { 'Content-Type': 'multipart/form-data' },
    data
  })
}

export function makeCustomMedicalScanTxt(data) {
  return request({
    url: '/api1/uploadms',
    method: 'post',
    data
  })
}
