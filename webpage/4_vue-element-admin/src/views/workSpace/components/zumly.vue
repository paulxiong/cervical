'''
Hellow World simple
'''
<template>
  <div class="example zumly-canvas"></div>
</template>
<script>
import Zumly from "zumly/dist/zumly.mjs"
export default {
    name: 'B_export',
    // components: {
    //     Zumly
    // },
    props: {
        msg_inB: {
            type: String,
            default: '000'
        }
    },    
    data() {
        return {
            app: ''
        }
    },
    mounted() {
    },
    methods: {
        method1(idx) {
            if (idx != '') {
              this.msg_inB = idx
            }
            // alert('In Zumly is ready, Go! \ n' + this.msg_inB)
            const hello = `
            <div class="z-view hello">
            H E L L O <br>
            W <span class="zoom-me o" data-to="world0">O</span> R L D!
            <img src = “` + this.msg_inB + `“/>
            </div>
            `;
            // alert("boostx:" + hello)
            const hello1 = `
            <div class="z-view hello">
            H E L L O 1 <br>
            W <span class="zoom-me o" data-to="world">O</span> R L D!
            </div>
            `;
            let image_src1 = this.msg_inB;
            const world0 = `
                   <div class="z-view world">
                    <img src= ${image_src1} />
                  </div>                      
            `;
            //! Error with following func, due to using async render()
            const world ={
              async render() {
                  // let image_src = "https://raw.githubusercontent.com/zumly/website/gh-pages/images/world.png"
                  let image_src = this.msg_inB;
                  alert("boostx in zumly.vue:" + image_src);
                  return `
                  <div class="z-view world">
                    <img src= ${image_src} />
                  </div>                      
                  `
                }
            };
            // alert("boostx: world = "+ img_src);
            this.app = new Zumly({
                mount: '.example',
                initialView: 'hello',
                views: {
                hello,
                hello1,
                world0,
                world
                }
            })
            this.app.init()





        }
    }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
.world{
  width: 250px;
  height: 250px;
  top: -5px
}
.o {
  border: 3px solid #ffcc00
}
.hello {
  font-size: 4em;
  text-align: center;
  font-family: arial;
  font-weight: bold;
   width: 400px;
  height: 200px;
}

</style>
