<template>
  <div>
    <b-table hover class="text-left mb-0" small :items="items" :fields="fields">
      <template v-slot:thead>
        <thead class="ItemLevel__thead"></thead>
      </template>
      <template #table-busy>
        <div class="text-center text-danger my-2">
          <b-spinner class="align-middle"></b-spinner>
          <strong>Загрузка...</strong>
        </div>
      </template>
      <template #cell(child_elems)="row">
        <i 
          class="bi bi-chevron-right"
          :class="row.detailsShowing && 'collapsed'"
          @click="row.toggleDetails"></i>
      </template>

      <template #row-details="row">
        <ItemLevels class="pl-5" :parentId=parentId :levelId=row.item._id :hierarchy=row.item.hierarchy />
      </template>

      <template #cell(levelName)="data">
        {{ `${data.item.levelName}` }}
      </template>
      <!-- <template #row-details="row">
        <b-card>
          <b-row class="mb-2">
            <b-col sm="3" class="text-sm-right"><b>Age:</b></b-col>
            <b-col>{{ row.item.age }}</b-col>
          </b-row>

          <b-row class="mb-2">
            <b-col sm="3" class="text-sm-right"><b>Is Active:</b></b-col>
            <b-col>{{ row.item.isActive }}</b-col>
          </b-row>

          <b-button size="sm" @click="row.toggleDetails">Hide Details</b-button>
        </b-card>
      </template> -->
    </b-table>
  </div>
</template>

<script>
export default {
  name: 'ItemHierarchy',
  props: {
    parentId: Number
  },
  data() {
    return {
      fields: [
        {
          key: "child_elems",
          label: " ",
          thClass: "ItemLevel__thead",
          tdClass: "level"
        },
        {
          key: "typeName",
          thClass: "ItemLevel__thead"
        }
      ],
      items: [
        {
          typeName: "Административное деление",
          hierarchy: "adm"
        },
        {
          typeName: "Муниципальное деление",
          hierarchy: "mun"
        },
      ],
    }
  },
  // beforeCreate: function () {
  //   this.$nextTick(async function () {
  //     this.loading = true
  //     try {
  //       const response = await fetch(`/polls/levels/${this.parentId}/`)
  //       if (!response.ok) throw new Error

  //       const data = await response.json()
  //       // console.log(data)
  //       data.length && (this.items = data)
  //     }
  //     catch (e) {
  //       console.log("Ошибка: " + e)
  //     }
  //     this.loading = false
  //   })
  // }
}
</script>

<style>
.ItemLevel__thead {
  display: none;
}

i::before {
  transition: .25s transform ease-in-out;
}

i.collapsed::before {
  transform: rotate(90deg);
}

.level {
  padding-left: 2rem!important;
  width: 1.5rem;
}
</style>
