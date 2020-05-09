<template>
  <div class="tools flex">
    <el-pagination
      :background="background"
      :current-page.sync="currentPage"
      :page-size="pageSize"
      :page-sizes="pageSizes"
      :layout="layout"
      :total="total"
      @size-change="handleSizeChange"
      @current-change="handleCurrentChange"
    />
  </div>
</template>

<script>
import { scrollTo } from '@/utils/scroll-to'
import { mapState } from 'vuex'

export default {
  name: 'Pagination2',
  props: {
    subpath: { // 区分一个路由下面的多个分页
      required: true,
      type: String,
      default: ''
    },
    total: {
      required: true,
      type: Number
    },
    pageSizes: {
      type: Array,
      default() {
        return [10, 20, 30, 50]
      }
    },
    layout: {
      type: String,
      default: 'total, sizes, prev, pager, next, jumper'
    },
    background: {
      type: Boolean,
      default: true
    },
    autoScroll: {
      type: Boolean,
      default: true
    },
    hidden: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      routerpath: '',
      show: false,
      currentPage: 1,
      pageSize: 10
    }
  },
  computed: {
    ...mapState({
      pagestate: state => state.pagestate.pagestate
    })
  },
  created() {
    if (!this.routerpath) {
      this.routerpath = this.$route.path
    }
    if (this.pagestate && this.pagestate[this.routerpath] && this.pagestate[this.routerpath][this.subpath]) {
      this.currentPage = this.pagestate[this.routerpath][this.subpath].currentpage
      this.pageSize = this.pagestate[this.routerpath][this.subpath].pagesize
    }
    this.$emit('pagination', { page: this.currentPage, limit: this.pageSize }) // 触发拉数据
  },
  methods: {
    pagechanged(currentpage, pagesize) {
      this.$store.dispatch('pagestate/setPageState', {
        'routerpath': this.routerpath,
        'subpath': this.subpath,
        'currentpage': currentpage,
        'pagesize': pagesize
      })
    },
    handleSizeChange(val) {
      this.pageSize = val
      this.$emit('pagination', { page: this.currentPage, limit: this.pageSize })
      this.pagechanged(this.currentPage, val)
      if (this.autoScroll) {
        scrollTo(0, 800)
      }
    },
    handleCurrentChange(val) {
      this.currentPage = val
      this.$emit('pagination', { page: this.currentPage, limit: this.pageSize })
      this.pagechanged(val, this.pageSize)
      if (this.autoScroll) {
        scrollTo(0, 800)
      }
    }
  }
}
</script>

<style scoped>
.tools {
  background: #fff;
  justify-content: space-around;
  bottom: 0px;
  position: fixed;
  left: 0;
  right: 0;
  margin-left: auto;
  margin-right: auto;
}
</style>
