<template>
      <q-card class="my-card" >
          <q-table
              grid
              :data="stockdata"
              :columns="columns"
              row-key="name"
              :filter="filter"
              hide-header
              hide-pagination
              :pagination.sync="pagination"
              >

              <template v-slot:item="props">
                  <div class="q-pa-xs col-xs-12 col-sm-6 col-md-6">
                      <q-btn size="sm" :color="props.row.color" :label="props.row.quantity" />
                      <!-- <strong>{{ props.row.name }}</strong>
                      <q-separator vertical /> -->

                      <!-- <q-chip dense size="xs" square>
                          <q-avatar icon="bookmark" :color="props.row.color" text-color="white" />
                          {{props.row.quantity}}
                      </q-chip> -->
                      
                      <!-- <q-badge color="red">
                      12 <q-icon name="warning" color="white" class="q-ml-xs" />
                      </q-badge> -->
                      <!-- <q-card>
                          <q-card-section class="text-center" horizontal>
                              <q-card-section>
                                  
                              </q-card-section>
                              
                              <q-card-section class="flex flex-center" >
                                  <q-btn size="sm" :color="props.row.color" :label="props.row.quantity" />
                              </q-card-section>
                          </q-card-section>
                      </q-card> -->
                  </div>
              </template>
          </q-table>
      </q-card>
</template>

<script>


export default {
  name: 'StockStatus',
  props: ['stockdata'],
  data () {
    return {
      filter: '',
      pagination: {
        page: 1,
        rowsPerPage: 30
      },
      columns: [
        { name: 'name', label: 'Name', field: 'name' },
        { name: 'quantity', label: 'Quantity', field: 'quantity' },
        { name: 'color', label: 'Color', field: 'color' }
      ],
    }
  },
  methods: {
  },
  computed: {
    classObject: function () {
      return {
        active: this.isActive && !this.error,
        'text-danger': this.error && this.error.type === 'fatal'
      }
    }
  }
}
</script>

<style lang="sass" scoped>
.my-card
  width: 100%
  max-width: 550px
</style>