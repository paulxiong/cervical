<template>
  <div>
    <div class="wrapper">
      <div v-for="(img) in imgs" :key="img.id" class="box">
        <div v-if="img.img" style="height: 100%">
          <el-image style="height: 100%" fit="scale-down" :src="img.img" />
          <div style="position:absolute; z-index:2; left:10px; top:10px">{{ img.id }}</div>
        </div>
        <div v-else class="notload">
          {{ img.id }}
        </div>
      </div>
    </div>
  </div>
</template>

<script>

export default {
  data() {
    return {
      imgs: {
        0: { 'id': 0, w: 10, h: 10, 'img': 'http://192.168.1.160:9002/imgs/scratch/img/b20200615/m1139220706/Images/IMG018x017.jpg?quality=80' },
        1: { 'id': 1, w: 10, h: 10, 'img': 'http://192.168.1.160:9002/imgs/scratch/img/b20200615/m1139220706/Images/IMG018x018.jpg?quality=80' },
        2: { 'id': 2, w: 10, h: 10, 'img': 'http://192.168.1.160:9002/imgs/scratch/img/b20200615/m1139220706/Images/IMG019x017.jpg?quality=80' },
        3: { 'id': 3, w: 10, h: 10, 'img': 'http://192.168.1.160:9002/imgs/scratch/img/b20200615/m1139220706/Images/IMG019x018.jpg?quality=80' }
      }
    }
  },
  mounted() {
  },
  methods: {
  }
}
</script>

<style lang="scss" scoped>
.wrapper {
  background: #fff1ce;
  width: 600px;
  display: grid;
  grid-gap: 0px 0px;
  grid-template-columns: repeat(2, 1fr);
  grid-template-rows: repeat(2, 1fr);
  grid-auto-flow: row;
}
.box {
  position: relative;
  width: 300px;
  background-color: #ccc;
  color: #000;
  border-radius: 0px;
}
.el-image {
  display: inline;
}
</style>
