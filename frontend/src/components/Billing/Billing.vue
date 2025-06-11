<template>
    <div class="grid grid-cols-[0.2fr_0.8fr] h-screen relative">
        <Sidebar active="facturacion_vista_general"></Sidebar>
        <!-- new content -->
        <div class="p-6 h-screen overflow-auto bg-gray-50">
            <div class="flex justify-between items-center">
                <h1 class="font-bold text-3xl">Movimientos - Vista general</h1>
                <div class="flex gap-2 items-center">
                    <router-link to="/clients/"
                        class="px-4 py-2 text-sm rounded-md bg-white border border-black/15 cursor-pointer hover:bg-gray-100">Descargar
                        en Excel</router-link>
                    <router-link to="/billing/create"
                        class="px-4 py-2 text-sm rounded-md bg-blue-500 text-white cursor-pointer hover:bg-blue-600">Crear
                        nuevo movimiento</router-link>
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
                        <input type="text" placeholder="Buscar facturas..."
                            class="pl-10 pr-3 py-2 text-sm border border-black/15 bg-white rounded-md outline-none focus:border-2 focus:border-black focus:outline focus:outline-black w-full" />
                    </div>
                    <div class="flex gap-2 items-center">
                        <select name="" id="" class="text-sm p-2 border border-black/15 rounded-md bg-white">
                            <option value=""></option>
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
                                    <th class="px-2 py-2 text-start text-gray-500 text-sm font-medium">ID</th>
                                    <th class="px-2 py-2 text-start border-black/15 text-gray-500 text-sm font-medium">
                                        Fecha de emisión</th>
                                    <th class="px-2 py-2 text-start text-gray-500 text-sm font-medium">Nombre del comprador</th>
                                    <th class="px-2 py-2 text-start text-gray-500 text-sm font-medium">Valor de la
                                        compra</th>
                                    <th class="px-2 py-2 text-start border-black/15 text-gray-500 text-sm font-medium">
                                        Estado</th>
                                    <th class="px-2 py-2 text-start border-black/15 text-gray-500 text-sm font-medium">
                                        Items vendidos
                                    </th>
                                    <th class="px-2 py-2 text-start border-black/15 text-gray-500 text-sm font-medium">

                                    </th>


                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="(item, key) in billsComputed" :key="key">
                                    <td class="px-2 py-2 text-start border-black/15 text-sm border-b">
                                        <input type="checkbox" name="" id="">
                                    </td>
                                    <td class="px-2 py-2 text-start border-black/15 text-sm border-b">{{
                                        item.bill_unique_id }}</td>
                                    <td class="px-2 py-2 text-start border-black/15 text-sm border-b">{{
                                        item.bill_created_date }}</td>
                                    <td class="px-2 py-2 text-start border-black/15 text-sm border-b">{{ 'Josue' }}</td>
                                    <td class="px-2 py-2 text-start border-black/15 text-sm border-b">{{
                                        JSON.parse(item.bill_products).reduce(function (sum, curr){ return sum +
                                        curr.total },0) }}</td>
                                    <td class="px-2 py-2 text-start border-black/15 text-sm cursor-pointer border-b relative"
                                        @click="openModal(item.bill_unique_id)" ref="modalParent">
                                        <div class="w-fit text-sm px-3 py-1 rounded-lg cursor-pointer" :class="{ 'bg-green-500/10 text-green-600': item.bill_status == 'Pagada', 'bg-red-600/10 text-red-600': item.bill_status == 'Anulada', 'bg-black/10 text-black': item.bill_status == 'Pendiente' }">
                                            {{ item.bill_status }}
                                        </div>
                                        <div @click="closeModal" v-if="selected == item.bill_unique_id" ref="modal" class="gap-3 p-3 bg-white rounded-lg border border-black/15 flex flex-col z-10 absolute top-10 right-25  cursor-pointer">
                                            <div @click="changeStatus(badge.text, item.bill_unique_id)" v-for="(badge, key) in badgets" :key="key" class="hover:opacity-50 w-full">
                                                <button :class="badge.classes" class="w-full">{{ badge.text }}</button>
                                            </div>
                                        </div>
                                    </td>

                                    <td class="px-2 py-2 text-start border-black/15 text-sm border-b">
                                        <ul class="">
                                            <li v-for="(product, key) in JSON.parse(item.bill_products)">- {{ product.name }} ({{ product.quantity }})</li>
                                        </ul>
                                    </td>
                                    <td class="px-2 py-2 text-start border-black/15 text-sm border-b">
                                        <div class="flex items-center underline gap-1 cursor-pointer hover:opacity-50">
                                            Detalles
                                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-4 h-4">
                                                <path stroke-linecap="round" stroke-linejoin="round" d="M2.036 12.322a1.012 1.012 0 0 1 0-.639C3.423 7.51 7.36 4.5 12 4.5c4.638 0 8.573 3.007 9.963 7.178.07.207.07.431 0 .639C20.577 16.49 16.64 19.5 12 19.5c-4.638 0-8.573-3.007-9.963-7.178Z" />
                                                <path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z" />
                                            </svg>
                                        </div>
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

<script setup>
import Sidebar from '../Sidebar.vue';
import { computed, onMounted, ref } from 'vue';
const bills = ref([]) /* THE ARRAY DATA */
const selected = ref('')
const modal = ref(false)
const modalParent = ref(false)
const badgets = [
    {
        text: "Pendiente",
        classes: "bg-black/10 text-black text-sm px-3 py-1 rounded-lg cursor-pointer"
    },
    {
        text: "Pagada",
        classes: "text-sm px-3 py-1 rounded-lg cursor-pointer bg-green-500/10 text-green-600"
    },
    {
        text: "Anulada",
        classes: "text-sm px-3 py-1 rounded-lg cursor-pointer bg-red-600/10 text-red-600"
    }
]

onMounted(async function () {
    const data = await fetch("http://127.0.0.1:8000/get/bills", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            user_id: "josueadmin" /* CHANGE IN PRODUCTION */
        })
    })
    const res = await data.json()
    bills.value = res.data
    console.log(res)
})

const openModal = function (item) {
    selected.value = item
}

const closeModal = function () {
    console.log("modal")
    if (modal.value) {
        console.log(modal.value[0])
    }
}
window.addEventListener("click", function (e) {
    console.log("window")
    if (modal.value) {
        if (modalParent.value.includes(e.target.parentElement) || e.target == modal.value[0] || e.target.parentElement == modal.value[0]) {
            console.log("Clicked outside modal. IGNORE")
        } else {
            selected.value = ''
        }
    }
})

const changeStatus = async function(toStatus, forId){
    console.log(toStatus)
    console.log(forId)
    console.log(bills.value.filter(obj => obj.bill_unique_id == forId))
    bills.value = bills.value.map(obj => {
        return obj.bill_unique_id == forId ? {...obj, bill_status: toStatus} : {...obj}
    })
    const data = await fetch("http://localhost:8000/update/bill/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            bill_unique_id: forId,
            to_status: toStatus
        })
    })
    const res = await data.json()
    console.log(res)
}

const billsComputed = computed(function(){
    return bills.value
})

</script>
