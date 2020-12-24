<template>
<div class="q-pa-md" style="width: 100%; margin-top: -20px">
        <div class="row">
            <div class="col">
                <stock-status :stockdata="a_box_data" class = 'bg-secondary'>
                </stock-status>
                <stock-status :stockdata="a_up_data" class = 'bg-purple'>
                </stock-status>
                <stock-status :stockdata="a_middle_data" class = 'bg-red'>
                </stock-status>
                <stock-status :stockdata="a_bottom_data" class = 'bg-green'>
                </stock-status>
                <stock-status :stockdata="battery_data" class = 'bg-yellow'>
                </stock-status>
            </div>
            <div class="col">
                <stock-status :stockdata="b_box_data" class = 'bg-secondary'>
                </stock-status>
                <stock-status :stockdata="b_up_data" class = 'bg-purple'>
                </stock-status>
                <stock-status :stockdata="b_middle_data" class = 'bg-red'>
                </stock-status>
                <stock-status :stockdata="b_bottom_data" class = 'bg-green'>
                </stock-status>
                <stock-status :stockdata="battery_lid_data" class = 'bg-blue'>
                </stock-status>
            </div>
        </div>
</div>
</template>
    <router-view />

<script>
// import { openURL } from 'quasar'
import { getauth } from 'boot/axios_request'
import StockStatus  from './stockStatus.vue'


const fake_data = function (data, index, quantity, color){
    for (let i = 0; i < index; i++) {
    data.push({ name: i, quantity: 20 + Math.ceil(50 * Math.random()), color: color })
  }
}

const a_box_data = []
const a_up_data = []
const a_middle_data = []
const a_bottom_data = []

const b_box_data = []
const b_up_data = []
const b_middle_data = []
const b_bottom_data = []

const battery_data = []
const battery_lid_data = []

fake_data(a_box_data, 6,1,'red')
fake_data(a_up_data, 6,1,'blue')
fake_data(a_middle_data, 6,1,'green')
fake_data(a_bottom_data, 6,1,'yellow')
fake_data(battery_data, 2,1,'red')

fake_data(b_box_data, 6,1,'red')
fake_data(b_up_data, 6,1,'blue')
fake_data(b_middle_data, 6,1,'green')
fake_data(b_bottom_data, 6,1,'yellow')
fake_data(battery_lid_data, 2,1,'red')

export default {
  name: 'Pagestocktopo',
  components: {
    StockStatus
  },
  data () {
    return {
      openid: '',
      login_name: '',
      authin: '0',
      pathname: 'stock/stocktopo/',
      pathname_previous: '',
      pathname_next: '',
      separator: 'cell',
      loading: false,
      height: '',


      a_box_data,
      a_up_data,
      a_middle_data,
      a_bottom_data,
      battery_data,
      b_box_data,
      b_up_data,
      b_middle_data,
      b_bottom_data,
      battery_lid_data
    }
  },
  computed: {
  },
  methods: {
  },
  created () {
    var _this = this
    if (_this.$q.localStorage.has('openid')) {
      _this.openid = _this.$q.localStorage.getItem('openid')
    } else {
      _this.openid = ''
      _this.$q.localStorage.set('openid', '')
    }
    if (_this.$q.localStorage.has('login_name')) {
      _this.login_name = _this.$q.localStorage.getItem('login_name')
    } else {
      _this.login_name = ''
      _this.$q.localStorage.set('login_name', '')
    }
    if (_this.$q.localStorage.has('auth')) {
      _this.authin = '1'
      _this.getList()
    } else {
      _this.authin = '0'
    }
  },
  mounted () {
    if (this.$q.platform.is.electron) {
      this.height = String(this.$q.screen.height - 90) + 'px'
    } else {
      this.height = this.$q.screen.height - 90 + '' + 'px'
    }
  },
  updated () {
  },
  destroyed () {
  }
}
</script>


