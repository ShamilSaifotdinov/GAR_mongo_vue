<template>
  <div>
    <b-table hover :busy="loading" class="text-left mb-0" small :items="items" :fields="fields">
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
        <RegionTable class="pl-5" :parentId=parentId :levelId=row.item._id :hierarchy=hierarchy />
      </template>

      <template #cell(levelName)="data">
        {{ `${data.item.levelName}` }}
        <!-- {{ ` (${data.item.count})` }} -->
        <b-badge variant="dark" pill>{{ `${data.item.count}` }}</b-badge>
      </template>
    </b-table>
    <p v-if="!loading && !items" role="alert">Данные отсутствуют</p>
  </div>
</template>

<script>
export default {
  name: 'ItemLevels',
  props: {
    parentId: Number,
    hierarchy: String
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
          key: "levelName",
          thClass: "ItemLevel__thead"
        }
      ],
      items: null,
      loading: null
    }
  },
  beforeCreate: function () {
    this.$nextTick(async function () {
      this.loading = true
      try {
        const response = await fetch(`/address/levels/${this.parentId}/${this.hierarchy}/`)
        if (!response.ok) throw new Error

        const data = await response.json()
        // console.log(data)
        data.length && (this.items = data)
      }
      catch (e) {
        console.log("Ошибка: " + e)
      }
      this.loading = false
    })
  }
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