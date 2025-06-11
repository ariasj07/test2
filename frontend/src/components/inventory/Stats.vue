<script setup>
import { ref, onMounted } from 'vue';
import Sidebar from '../Sidebar.vue';

const arr = ref([])
const products = ref([])
const clients = ref([])
const total = ref(0)
onMounted(async function() {
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
    arr.value = await res
    console.log(res)
    products.value = res.data
    total.value = products.value.reduce(function(acc, curr) {
        return acc + (parseFloat(curr.product_price) * parseFloat(curr.product_stock));
    }, 0);
    console.log(total.value)
    console.log(res.data)
    const data2 = await fetch("http://127.0.0.1:8000/get/clients", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            user_id: "josueadmin"
        })
    })
    const res2 = await data2.json()
    clients.value = res2
    console.log()
})

</script>

<template>
    <div class="grid grid-cols-[0.2fr_0.8fr] h-screen relative">
        <Sidebar active="productos_estadisticas"></Sidebar>
        <div class="p-6 h-screen overflow-auto bg-gray-50">
            <h1 class="font-bold text-3xl">Estadísticas</h1>
            <div class="grid grid-cols-3 bg-white my-5 border border-black/20 rounded-tl-md rounded-bl-md rounded-tr-md rounded-br-md">
                <div class="p-3 border-r border-black/20 flex flex-col gap-1">
                    <h2 class="font-medium text-base">Productos creados</h2>
                    <h2 class="font-bold text-2xl">{{ arr.data ? arr.data.length : 0 }}</h2>
                    <p class="text-sm text-gray-600">Todos los productos que has creado</p>
                </div>
                <div class="p-3 border-r border-black/20 flex flex-col gap-1">
                    <h2 class="font-medium text-base">Valor total en inventario</h2>
                    <h2 class="font-bold text-2xl">{{ total.toLocaleString() }}</h2>
                    <p class="text-sm text-gray-600">Cantidad de cada producto * su precio</p>
                </div>
                <div class="p-3 border-r border-black/20 flex flex-col gap-1">
                    <h2 class="font-medium text-base">Clientes registrados</h2>
                    <h2 class="font-bold text-2xl">{{ clients.data ? clients.data.length : 0 }}</h2>
                    <p class="text-sm text-gray-600">Todos los clientes que has registrado</p>
                </div>

            </div>
        </div>        
    </div>
</template>

<style scoped>

</style>
