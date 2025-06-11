<script setup>
import { computed, ref } from 'vue';
import { onMounted } from 'vue';
const clients = ref([])
const inventory = ref('')
const selected = ref([])
const filters = ["Todos", "Ocultos", "Últimos 7 días", "Últimos 3 meses", "Este año", "Mayor compras", "Menor compras"]
import Sidebar from '../Sidebar.vue';
import { useAlert } from '../../composables/useAlert';
const { alert, alertIsTrue, message, verify } = useAlert() 
onMounted(async function(){
    const data = await fetch("http://127.0.0.1:8000/get/clients", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            user_id: "josueadmin"
        })
    })
    const res = await data.json()
    clients.value = res
    filterSelected.value = "Todos"
    const data2 = await fetch("http://127.0.0.1:8000/get/inventory", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            id: "josueadmin"
        })
    })
    const res2 = await data2.json()
    inventory.value = res2
})

const clientsList = computed(function(){

})

const print = function(){
    console.log(selected.value)
}

const filterSelected = ref(filters[0])
const applyFilter = function(item){
    filterSelected.value = item
    console.log(filterSelected.value)
}

const clientsComputed = computed(function(){
    console.log("si")
    console.log(filterSelected.value)
    const index = filters.indexOf(filterSelected.value)
    console.log(clients.value)
    if(index == 0 && clients.value.data){
        return clients.value.data.filter(client => client.client_is_hidden == 0)
    }else if(index == 1 && clients.value.data){
        return clients.value.data.filter(client => client.client_is_hidden == 1)
    }
})

const hideItems = async function(){
    const data = await fetch("http://localhost:8000/hide/client", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            user_id: "josueadmin", /* CHANGE IN PRODUCTION BITCH */
            to_hide: selected.value
        })
    })
    const res = await data.json()
    verify(res)
    console.log(res)
    clients.value = res.data
    
}


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
        <Sidebar active="clientes_vista_general"></Sidebar>
        <div class="p-6 h-screen overflow-auto bg-gray-50">
            <div class="flex justify-between items-center">
                <h1 class="font-bold text-3xl">Clientes - Vista general</h1>
                <div class="flex gap-2 items-center" v-if="selected.length < 1">
                    <router-link to="/clients/" class="px-4 py-2 text-sm rounded-md bg-white border border-black/15 cursor-pointer hover:bg-gray-100">Descargar en Excel</router-link>
                    <router-link to="/clients/create" class="px-4 py-2 text-sm rounded-md bg-blue-500 text-white cursor-pointer hover:bg-blue-600">Añadir nuevo</router-link>
                </div>
                <div class="flex gap-2 items-center" v-else>
                    <button  to="/clients/" class="px-4 py-2 text-sm rounded-md bg-white border border-black/15 cursor-pointer hover:bg-gray-100">Descargar selección en Excel</button>
                    <button @click="hideItems" to="/clients/create" class="px-4 py-2 text-sm rounded-md bg-blue-500 text-white cursor-pointer hover:bg-blue-600">Ocultar seleccionados</button>
                </div>
            </div>
            <div class="overflow-scroll relative w-full p-5 mt-5 bg-white rounded-md  border border-black/15">
                <div class="flex justify-between items-center">
                    <div class="relative flex items-center">
                        <svg class="w-5 h-5 absolute ms-3 text-black" xmlns="http://www.w3.org/2000/svg" fill="none"
                            viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round"
                                d="m21 21-5.197-5.197m0 0A7.5 7.5 0 1 0 5.196 5.196a7.5 7.5 0 0 0 10.607 10.607Z" />
                        </svg>
                        <input type="text" placeholder="Buscar productos..." class="pl-10 pr-3 py-2 text-sm border border-black/15 bg-white rounded-md outline-none focus:border-2 focus:border-black focus:outline focus:outline-black w-full" />
                    </div>
                    <div class="flex gap-2 items-center">
                        <select name=""  id="" class="text-sm p-2 border border-black/15 rounded-md bg-white">
                            <option  v-for="(item, key) in filters" @click="applyFilter(item)" :key="key" :value="item">{{ item }}</option>
                        </select>
                    </div>
                </div>
                <div class="my-5">
                    <div class="h-[400px] overflow-scroll">
                        <table class="w-full border-collapse relative">
                            <thead class="sticky top-0 bg-white z-10">
                                <tr class="border-b border-black/15">
                                    <th class="px-2 py-2 text-start border-black/15 text-gray-500 text-sm font-medium"></th>
                                    <th class="px-2 py-2 text-start text-gray-500 text-sm font-medium">ID</th>
                                    <th class="px-2 py-2 text-start border-black/15 text-gray-500 text-sm font-medium">Nombre</th>
                                    <th class="px-2 py-2 text-start text-gray-500 text-sm font-medium">Email</th>
                                    <th class="px-2 py-2 text-start text-gray-500 text-sm font-medium">Telefono</th>
                                    <th class="px-2 py-2 text-start border-black/15 text-gray-500 text-sm font-medium">Notas del cliente</th>
                                    <th class="px-2 py-2 text-start border-black/15 text-gray-500 text-sm font-medium">Fecha de ingreso</th>
                                    <th class="px-2 py-2 text-start border-black/15 text-gray-500 text-sm font-medium">Dirección del cliente</th>
                                    <th class="px-2 py-2 text-start border-black/15 text-gray-500 text-sm font-medium">Compras realizadas</th>
                                    <th class="px-2 py-2 text-start border-black/15 text-gray-500 text-sm font-medium"></th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="(item, key) in clientsComputed" :key="key" class="duration-200 transition-all" :class="{'bg-gray-100': selected.includes(item.client_unique_id)}">
                                    <td class="px-2 py-1 border-b border-black/15 text-gray-700 text-sm font-medium">
                                        <input class="cursor-pointer accent-black" @change="print"  :value="item.client_unique_id" v-model="selected" type="checkbox" name="product_selected">
                                    </td>
                                    <td class="px-2 py-1 border-b border-black/15 text-gray-700 text-sm font-medium">
                                        {{ item.client_id ? item.client_id : '-'}}
                                    </td>
                                    <td class="px-2 py-1 border-b border-black/15 text-gray-700 text-sm font-medium">
                                        {{ item.client_name }}
                                    </td>
                                    <td class="px-2 py-1 border-b border-black/15 text-gray-700 text-sm font-medium">
                                        {{ item.client_email ? item.client_email : '-' }}
                                    </td>
                                    <td class="px-2 py-1 border-b border-black/15 text-gray-700 text-sm font-medium">
                                        {{ item.client_phone ? item.client_phone : '-' }}
                                    </td>
                                    <td class="px-2 py-1 border-b border-black/15 text-gray-700 text-sm font-medium">
                                        {{ item.client_notes ? item.client_notes : '-' }}
                                    </td>
                                    <td class="px-2 py-1 border-b border-black/15 text-gray-700 text-sm font-medium">
                                        {{ item.client_register_date ? item.client_register_date : '-' }}
                                    </td>
                                    <td class="px-2 py-1 border-b border-black/15 text-gray-700 text-sm font-medium">
                                        {{ item.client_adress ? item.client_adress : '-' }}
                                    </td>
                                    <td class="px-2 py-1 border-b border-black/15 text-gray-700 text-sm font-medium">
                                        0
                                    </td>
                                    <td class="px-2 py-1 border-b border-black/15 text-blue-500 underline text-sm font-medium">
                                        <router-link :to="{ name: 'clientsEdit', params: { id: item.client_unique_id } }">
                                            Editar
                                        </router-link>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped></style>
