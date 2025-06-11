<script setup>
import { onMounted, ref } from 'vue';
import { useRoute } from 'vue-router'

const route = useRoute()
const param_product_unique_id = route.params.id
import Sidebar from '../Sidebar.vue';
const productName = ref('')
const productDescription = ref('')
const productPrice = ref('')
const productStock = ref('')
const productId = ref('')
const alert = ref(false)
const alertIsTrue = ref(true)
const message = ref('')

const send = async function() {
    const res = await fetch("http://127.0.0.1:8000/update", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            product_name: productName.value.toString(),
            product_description: productDescription.value.toString(),
            product_price: productPrice.value,
            product_stock: productStock.value,
            product_id: productId.value,
            product_unique_id: param_product_unique_id
        })
    })
    const data = await res.json()
    if(data.status){
        alert.value = true /* fires the alert */
        alertIsTrue.value = true
        message.value = data.alert
        console.log("si")
        setTimeout(()=>{
            alert.value = false
        }, 6000)
        productName.value = ''
        productDescription.value = ''
        productPrice.value = ''
        productId.value = ''
        productStock.value = ''
    }else{
        alert.value = true /* fires the alert */
        alertIsTrue.value = false
        message.value = data.alert
        setTimeout(()=>{
            alert.value = false
        }, 6000)
    }
    console.log(data)

}
const validate = function(e){
    productPrice.value = productPrice.value.replace(/[^0-9.]/g, "");
    productStock.value = productStock.value.replace(/[^0-9]/g, "");
}
onMounted(async function() {
    const data = await fetch("http://127.0.0.1:8000/get/inventory", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            product_unique_id: param_product_unique_id
        })
    })
    const res = await data.json()
    console.log(res)
    productName.value = res.data[0].product_name
    productDescription.value = res.data[0].product_description
    productPrice.value = res.data[0].product_price
    productStock.value = res.data[0].product_stock
    productId.value = res.data[0].product_id
})
</script>

<template>
    <div class="grid grid-cols-[0.2fr_0.8fr] h-screen relative">
        <div class="absolute w-full flex justify-center py-5 top-0 duration-200 transition-all pointer-events-none" :class="{'opacity-100': alert == true, 'opacity-0': alert == false}">
            <div class="flex items-center gap-2 border border-black/30 p-2 rounded-lg ">
                <svg v-if="alertIsTrue" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6 text-green-500">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M9 12.75 11.25 15 15 9.75M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />
                </svg>
                <svg v-else xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6 text-red-500">
                    <path stroke-linecap="round" stroke-linejoin="round" d="m9.75 9.75 4.5 4.5m0-4.5-4.5 4.5M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />
                </svg>
                <p class="text-sm">{{ message }}</p>
            </div>
        </div>
        <Sidebar active="productos_crear"></Sidebar>
        <div class="p-6 h-screen overflow-auto">
            <div class="flex justify-between items-center">
                <h1 class="font-bold text-3xl">Editar producto</h1>
                <div class="flex gap-2 items-center">
                    <router-link to="/" class="px-4 py-2 text-sm rounded-md bg-white border border-black/30 cursor-pointer hover:bg-gray-100">Cancelar</router-link>
                    <button @click="send" class="px-4 py-2 text-sm rounded-md bg-blue-500 text-white cursor-pointer hover:bg-blue-600">Actualizar valores</button>
                </div>
            </div>
            <div class="mt-5">
                <div class="grid grid-cols-2 gap-4">
                    <div class="flex flex-col gap-2">
                        <h2 class="font-medium text-xl">Nombre del producto * </h2>
                        <input v-model="productName" type="text" class="text-sm p-2 border border-black/30 rounded-md" placeholder="Laptop 144hz...">
                    </div>
                    <div class="flex flex-col gap-2">
                        <h2 class="font-medium text-xl">Descripción del producto * </h2>
                        <input v-model="productDescription" type="text" class="text-sm p-2 border border-black/30 rounded-md" placeholder="Laptop con x caracteresiticas...">
                    </div>
                    <div class="flex flex-col gap-2">
                        <h2 class="font-medium text-xl">Precio del producto * </h2>
                        <input v-model="productPrice" @input="validate" type="text" class="text-sm p-2 border border-black/30 rounded-md" placeholder="500000">
                    </div>
                    <div class="flex flex-col gap-2">
                        <h2 class="font-medium text-xl">Cantidad del producto * </h2>
                        <input v-model="productStock" @input="validate" type="text" class="text-sm p-2 border border-black/30 rounded-md" placeholder="200">
                    </div>
                    <div class="flex flex-col gap-2">
                        <h2 class="font-medium text-xl">ID del producto (opcional)</h2>
                        <input v-model="productId" type="text" class="text-sm p-2 border border-black/30 rounded-md" placeholder="200">
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>

</style>
