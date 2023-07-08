import Vue from 'vue'
import App from './App.vue'


import { BootstrapVue, IconsPlugin } from 'bootstrap-vue'

// Import Bootstrap and BootstrapVue CSS files (order is important)
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import RegionTableVue from './components/RegionTable.vue'
import ItemLevelsVue from './components/ItemLevels.vue'

// Make BootstrapVue available throughout your project
Vue.use(BootstrapVue)
// Optionally install the BootstrapVue icon components plugin
Vue.use(IconsPlugin)

Vue.component("RegionTable", RegionTableVue)
Vue.component("ItemLevels", ItemLevelsVue)

Vue.config.productionTip = false

new Vue({
  render: h => h(App),
}).$mount('#app')
