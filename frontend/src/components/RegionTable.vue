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

      <template #cell()="row">
        <template v-if="row.value.versions">
          <div class="d-flex" style="gap: 8px;">
            <div>{{ row.value.value }}</div>
            <b-button v-if="row.value.versions.length > 0" v-b-toggle="'collapse-' + row.item.objectId + '-' + row.field.key" size="sm"><b-icon-chevron-compact-down /></b-button>
          </div>

          <b-collapse :id="'collapse-' + row.item.objectId + '-' + row.field.key" style="font-size: small;">
            <b-table v-if="row.field.key == 'name'" :items="row.value.versions"
              :fields="[ { key: 'name' }, { key: 'typename'}, { key: 'level'}, { key: 'ISACTUAL'}, { key: 'ISACTIVE'} ]"
            ></b-table>
            <template v-else>
              <div>Прошлые версии:</div>
              <div v-for="version, index in row.value.versions" :key="index">{{ version.value }}</div>
            </template>
          </b-collapse>

        </template>

        <template v-else>{{ row.value }}</template>
      </template>
      
      <template v-if="levelId === 1" #row-details="row">
        <ItemHierarchy :parentId=row.item.objectId />
      </template>
      <template v-else #row-details="row">
        <ItemLevels :parentId=row.item.objectId :hierarchy="hierarchy" />
      </template>
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
                {
                    key: "objectId",
                    label: "ID"
                },
                {
                    key: "name",
                    label: "Наименование",
                },
                {
                    key: "objectType",
                    label: "Тип",
                    tdClass: "typename"
                },
                {
                    key: "CODE",
                    label: "КЛАДР",
                    tdClass: "CODE",
                },
                {
                    key: "OKATO",
                    label: "ОКАТО",
                    tdClass: "OKATO",
                },
                {
                    key: "OKTMO",
                    label: "ОКТМО",
                    tdClass: "OKTMO",
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

                data.forEach((elem) => {
                  const actual_version = elem.versions.find((version) => version.ISACTUAL == "1" && version.ISACTIVE == "1")
                  if (!actual_version) console.log(elem)

                  elem.name = { value: actual_version?.name, versions: elem.versions.filter((version) => version.ISACTUAL == "0" || version.ISACTIVE == "0") || [] }
                  elem.objectType = actual_version?.typename
                  elem.levelId = actual_version?.level

                  for (const key of ['CODE', 'OKTMO', 'OKATO']) {
                    elem[key] = { value : elem[key].find((param) => param.CHANGEIDEND == "0")?.value, versions: elem[key].filter((param) => param.CHANGEIDEND != "0") }
                  }
                })

                if (this.hierarchy === 'adm') data.sort((a, b) => a.CODE - b.CODE || a.OKTMO - b.OKTMO)
                else data.sort((a, b) => a.OKTMO - b.OKTMO || a.CODE - b.CODE )

                console.log("table:", data)

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
