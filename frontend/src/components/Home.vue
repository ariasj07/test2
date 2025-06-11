<script setup>
import { computed, ref } from 'vue';
import { onMounted } from 'vue';
import Sidebar from './Sidebar.vue';
import { useAlert } from '../composables/useAlert';
const { alert, alertIsTrue, message, verify } = useAlert()
const filters = ['Todos', 'Ocultos', 'Menor stock', 'Mayor stock']
const active = ref('Todos')
const total = ref(0)
const selected = ref([])
const areItemsSelected = ref(false)
const title = ref('Todos')

onMounted(async function () {
    const data = await fetch("http://127.0.0.1:8000/get/inventory", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            id: "josueadmin"
        })
    })
    const res = await data.json()
    console.log(res)
    products.value = res.data
    total.value = products.value.reduce(function (acc, curr) {
        return acc + (parseFloat(curr.product_price) * parseFloat(curr.product_stock));
    }, 0);
    console.log(total.value)


})
const print = function () {
    if (selected.value.length >= 1 && active.value == "Todos") {
        areItemsSelected.value = "todos"
    } else if (selected.value.length >= 1 && active.value == "Ocultos") {
        areItemsSelected.value = true
        areItemsSelected.value = "ocultos"
        console.log("Vista de: ", active.value)
    } else if (selected.value.length >= 1 && active.value == "Menor stock") {
        areItemsSelected.value = true
        console.log("Vista de: ", active.value)
    }
    else {
        areItemsSelected.value = false
    }
}

const products = ref([])
const productsComputed = computed(function (item) {
    console.log("Computed:")
    console.log(active.value)
    if (active.value == "Todos") {
        if (searching.value) {
            return products.value.filter(producto => producto.product_is_hidden == 0 && producto.product_name.toLowerCase().includes(searching.value))
        }
        return products.value.filter(producto => producto.product_is_hidden == 0)
    } else if (active.value == "Ocultos") {
        if (searching.value) {
            return products.value.filter(producto => producto.product_is_hidden == 1 && producto.product_name.toLowerCase().includes(searching.value))
        }
        return products.value.filter(producto => producto.product_is_hidden == 1)
    } else if (active.value == "Menor stock") {
        return products.value.sort((a, b) => b.product_stock - a.product_stock);
    }
})

const hiddenItems = async function () {
    const toHide = []
    for (const item of selected.value) {
        toHide.push(item)
    }
    const data = await fetch("http://127.0.0.1:8000/hide/inventory", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            id: "josueadmin",
            toHide: toHide
        })
    })
    console.log("From hidden function:")
    console.log(selected.value)
    selected.value = []
    areItemsSelected.value = false
    const res = await data.json()
    verify(res)
    console.log(res)
    products.value = res.data

}
const showItems = async function () {
    const toHide = []
    for (const item of selected.value) {
        toHide.push(item)
    }
    const data = await fetch("http://127.0.0.1:8000/show/inventory", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            id: "josueadmin",
            toShow: toHide
        })
    })
    console.log("From hidden function:")
    console.log(selected.value)
    selected.value = []
    areItemsSelected.value = false
    const res = await data.json()
    verify(res)
    console.log(res)
    products.value = res.data

}

const changeView = function (item) {
    console.log("Change:")
    console.log(item)
    title.value = item
    active.value = item
}

const searching = ref('')



</script>

<template>
    <div class="grid grid-cols-[0.2fr_0.8fr] h-screen relative">
        <div class="absolute w-full flex justify-center py-5 top-0 duration-200 transition-all pointer-events-none"
            :class="{ 'opacity-100': alert == true, 'opacity-0': alert == false }">
            <div class="flex items-center gap-2 border bg-white shadow-sm border-black/15 p-2 rounded-lg ">
                <svg v-if="alertIsTrue" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"
                    stroke-width="1.5" stroke="currentColor" class="w-6 h-6 text-green-500">
                    <path stroke-linecap="round" stroke-linejoin="round"
                        d="M9 12.75 11.25 15 15 9.75M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />
                </svg>
                <svg v-else xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                    stroke="currentColor" class="w-6 h-6 text-red-500">
                    <path stroke-linecap="round" stroke-linejoin="round"
                        d="m9.75 9.75 4.5 4.5m0-4.5-4.5 4.5M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />
                </svg>
                <p class="text-sm">{{ message }}</p>
            </div>
        </div>
        <Sidebar active="productos_vista_general"></Sidebar>
        <div class="p-6 h-screen overflow-auto bg-gray-50">
            <div class="flex justify-between items-center">
                <h1 class="font-bold text-3xl">Inventario - {{ title }}</h1>
                <div v-if="!areItemsSelected" class="flex gap-2 items-center">
                    <button class="px-4 py-2 text-sm rounded-md bg-white border border-black/15 cursor-pointer hover:bg-gray-100">Descargar en Excel</button>
                    <router-link to="/inventory/create" class="px-4 py-2 text-sm rounded-md bg-blue-500 text-white cursor-pointer hover:bg-blue-600">Añadir nuevo</router-link>
                </div>
                <div v-if="areItemsSelected == 'todos'" class="flex gap-2 items-center">
                    <button
                        class="px-4 py-2 text-sm rounded-md bg-white border border-black/15 cursor-pointer hover:bg-gray-100">Descargar
                        selección en Excel</button>
                    <button @click="hiddenItems"
                        class="px-4 py-2 text-sm rounded-md bg-blue-500 text-white cursor-pointer hover:bg-blue-600">Ocultar
                        seleccionados</button>
                </div>
                <div v-else-if="areItemsSelected == 'ocultos'" class="flex gap-2 items-center">
                    <button
                        class="px-4 py-2 text-sm rounded-md bg-white border border-black/15 cursor-pointer hover:bg-gray-100">Descargar
                        selección en Excel</button>
                    <button @click="showItems"
                        class="px-4 py-2 text-sm rounded-md bg-blue-500 text-white cursor-pointer hover:bg-blue-600">Mostrar
                        seleccionados</button>
                </div>
            </div>
            <p class="text-base text-gray-600">Última actualizacion: 1 hora</p>

            <div class="overflow-scroll relative  w-full p-5 mt-5 bg-white rounded-md  border border-black/15">
                <div class="flex justify-between items-center">
                    <div class="relative  flex items-center">
                        <svg class="w-5 h-5 absolute ms-3 text-black" xmlns="http://www.w3.org/2000/svg" fill="none"
                            viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round"
                                d="m21 21-5.197-5.197m0 0A7.5 7.5 0 1 0 5.196 5.196a7.5 7.5 0 0 0 10.607 10.607Z" />
                        </svg>
                        <input type="text" v-model="searching" @input="searchingValue" placeholder="Buscar productos..."
                            class="pl-10 pr-3 py-2 text-sm border border-black/15 bg-white rounded-md outline-none focus:border-2 focus:border-black focus:outline focus:outline-black w-full" />
                    </div>
                    <div class="flex gap-2 items-center">
                        <select name="" id="" class="text-sm p-2 border border-black/15 rounded-md bg-white">
                            <option v-for="(item, key) in filters" @click="changeView(item)" :value="item">{{ item }}
                            </option>
                        </select>
                    </div>
                </div>
                <div class="my-5">
                    <div class="h-[400px] overflow-scroll">
                        <table class="w-full border-collapse relative">
                            <thead class="sticky top-0 bg-white z-10">
                                <tr class="border-b border-black/15">
                                    <th class="px-2 py-2 text-start border-black/15 text-gray-500 text-sm font-medium">
                                    </th>
                                    <th class="px-2 py-2 text-start border-black/15 text-gray-500 text-sm font-medium">
                                        Nombre</th>
                                    <th class="px-2 py-2 text-start border-black/15 text-gray-500 text-sm font-medium">
                                        Descripción</th>
                                    <th class="px-2 py-2 text-start border-black/15 text-gray-500 text-sm font-medium">
                                        Precio</th>
                                    <th class="px-2 py-2 text-start border-black/15 text-gray-500 text-sm font-medium">
                                        Cantidad</th>
                                    <th class="px-2 py-2 text-start text-gray-500 text-sm font-medium">Valor total</th>
                                    <th class="px-2 py-2 text-start text-gray-500 text-sm font-medium"></th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="(item, key) in productsComputed" :key="key"
                                    class="duration-200 transition-all"
                                    :class="{ 'bg-gray-100': selected.includes(item.product_unique_id) }">
                                    <td class="px-2 py-1 border-b border-black/15 text-gray-700 text-sm font-medium">
                                        <input v-model="selected" @change="print" :value="item.product_unique_id"
                                            class="cursor-pointer accent-black" type="checkbox" name="product_selected">
                                    </td>
                                    <td class="px-2 py-2 border-b border-black/15 text-gray-700 text-sm font-medium">
                                        {{ item.product_name }}
                                    </td>
                                    <td class="px-2 py-2 border-b border-black/15 text-gray-700 text-sm font-medium">
                                        {{ item.product_description }}
                                    </td>
                                    <td class="px-2 py-2 border-b border-black/15 text-gray-700 text-sm font-medium">
                                        {{ parseFloat(item.product_price).toFixed(2) }}
                                    </td>
                                    <td class="px-2 py-2 border-b border-black/15 text-gray-700 text-sm font-medium">
                                        {{ item.product_stock }}
                                    </td>
                                    <td class="px-2 py-2 border-b border-black/15 text-gray-700 text-sm font-medium">
                                        {{ (parseFloat(item.product_price) *
                                            parseFloat(item.product_stock)).toLocaleString() }}
                                    </td>
                                    <td
                                        class="px-2 py-2 border-b border-black/15 text-sm font-medium underline text-blue-500 cursor-pointer">
                                        <router-link
                                            :to="{ name: 'editProduct', params: { id: item.product_unique_id } }">
                                            Editar
                                        </router-link>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>

                <!--                 <table class="border-collapse w-full ">
                    <thead class="">
                        <tr>
                            <th class="px-2 py-2 text-start border-black/15 text-gray-500 text-sm font-medium"></th>
                            <th class="px-2 py-2  text-start border-black/15 text-gray-500 text-sm font-medium">Nombre</th>
                            <th class="px-2 py-2  text-start border-black/15 text-gray-500 text-sm font-medium">Descripción</th>
                            <th class="px-2 py-2  text-start border-black/15 text-gray-500 text-sm font-medium">Precio</th>
                            <th class="px-2 py-2  text-start border-black/15 text-gray-500 text-sm font-medium">Cantidad</th>
                            <th class="px-2 py-2  text-start border-black/15 text-gray-500 text-sm font-medium">Valor total</th>
                            <th class="px-2 py-2  text-start border-black/15 text-gray-500 text-sm font-medium"></th>
                        </tr>
                    </thead>
                    <tbody class="">
                        º
                    </tbody>
                </table> -->
            </div>
        </div>
    </div>
</template>

<style scoped></style>
