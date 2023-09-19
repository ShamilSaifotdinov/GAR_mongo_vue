<template>
  <div>
    <b-table hover selectable :busy="loading" striped small 
      :select-mode="selectMode"
      class="text-left mb-0" 
      :items="items" :fields="fields">
      <template #table-busy>
        <div class="text-center text-danger my-2">
          <b-spinner class="align-middle"></b-spinner>
          <strong>Загрузка...</strong>
        </div>
      </template>
      <template #cell(child_elems)="row">
        <i class="bi bi-chevron-right"
          :class="row.detailsShowing && 'collapsed'"
          @click="row.toggleDetails"></i>
      </template>
      
      <template v-if="levelId === 1" #row-details="row">
        <ItemHierarchy :parentId=row.item.objectId />
      </template>
      <template v-else #row-details="row">
        <ItemLevels :parentId=row.item.objectId :hierarchy="hierarchy" />
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
    <p v-if="!loading && !items" role="alert">Данные отсутствуют</p>
  </div>
</template>

<script>
import ItemHierarchy from './ItemHierarchy.vue';

export default {
    name: "RegionTable",
    props: {
        parentId: Number,
        levelId: Number,
        hierarchy: String
    },
    data() {
        return {
            fields: [
                {
                    key: "child_elems",
                    label: " ",
                    tdClass: "item"
                },
                // {
                //     key: "objectId",
                //     label: "ID"
                // },
                {
                    key: "name",
                    label: "Наименование"
                },
                {
                    key: "typename",
                    label: "Тип",
                    tdClass: "typename"
                },
                {
                    key: "CODE",
                    label: "КЛАДР",
                    tdClass: "CODE"
                },
                {
                    key: "OKATO",
                    label: "ОКАТО",
                    tdClass: "OKATO"
                },
                {
                    key: "OKTMO",
                    label: "ОКТМО",
                    tdClass: "OKTMO"
                },
                {
                    key: "postIndex",
                    label: "Почтовый индекс",
                    tdClass: "postIndex"
                },
                {
                    key: "CODE_city",
                    label: "Классификатор НП",
                    tdClass: "CODE_city"
                },
                {
                    key: "edited",
                    label: "Пользовательский",
                    tdClass: "edited"
                }
            ],
            items: null,
            loading: null,
            selectMode: 'range',
            selected: []
        };
    },
    beforeCreate: function () {
        this.$nextTick(async function () {
            this.loading = true;
            try {
                const response = await fetch(`/address/${this.parentId}/${this.hierarchy}/${this.levelId}/`);
                if (!response.ok)
                    throw new Error;
                const data = await response.json();
                if (this.hierarchy === 'adm') data.sort((a, b) => a.CODE - b.CODE || a.OKTMO - b.OKTMO)
                else data.sort((a, b) => a.OKTMO - b.OKTMO || a.CODE - b.CODE )
                // console.log(data)
                data.length && (this.items = data);
            }
            catch (e) {
                console.log("Ошибка: " + e);
            }
            this.loading = false;
        });
    },
    methods: {
      onRowSelected(items) {
        this.selected = items
      },
    },
    components: { ItemHierarchy }
}
</script>

<style>
.item {
  width: 1.5rem;
}

i::before {
  transition: .25s transform ease-in-out;
}

i.collapsed::before {
  transform: rotate(90deg);
}
.b-table-details {
  background-color: transparent!important;
}
.b-table-details > td {
  padding: 0!important;
}
.b-table-row-selected {
  background-color: #468FFF40!important;
}

.typename {
  width: 7rem;
}
.CODE {
  width: 10rem;
}
.OKATO{
  width: 7rem;
}
.OKTMO {
  width: 7rem;
}
.postIndex {
  width: 5rem;
}
.CODE_city {
  width: 8rem;
}
.edited {
  width: 10rem;
}
</style>
