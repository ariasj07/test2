<script setup>
import { ref } from 'vue';
import Sidebar from '../Sidebar.vue';
import { useRoute } from 'vue-router'

const route = useRoute()
const param_client_unique_id = route.params.id
import { onMounted } from 'vue';
const today = ref("")
const clientName = ref("")
const clientNotes = ref("")
const clientEmail = ref("")
const clientAdress = ref("")
const clientPhone = ref("")
const clientID = ref("")
import { useAlert } from '../../composables/useAlert';
const { alert, alertIsTrue, message, verify } = useAlert()
onMounted(async function(){
    console.log(param_client_unique_id)
    const clients = await fetch("http://localhost:8000/get/client", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            client_id: param_client_unique_id /* CHANGE IN PRODUCTION */
        })
    })
    const clients_data = await clients.json()
    console.log(clients_data)
    clientName.value = clients_data.data[0].client_name
    clientNotes.value = clients_data.data[0].client_notes
    clientEmail.value = clients_data.data[0].client_email
    clientPhone.value = clients_data.data[0].client_phone
    clientID.value = clients_data.data[0].client_id
    clientAdress.value = clients_data.data[0].client_adress
    today.value = clients_data.data[0].client_register_date
})

const sendClient = async function(){
    const data = await fetch("http://localhost:8000/update/client", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            user_id: "josueadmin",
            client_unique_id: param_client_unique_id /* CHANGE IN PRODUCTION FOR A REAL ONE */,
            client_name: clientName.value,
            client_email: clientEmail.value,
            client_adress: clientAdress.value,
            client_phone: clientPhone.value,
            client_notes: clientNotes.value,
            client_register_date: today.value
        })
    })
    const res = await data.json()
    if(res.status){
        clientName.value = ""
        clientEmail.value = ""
        clientAdress.value = ""
        clientPhone.value = ''
        clientNotes.value = ''
    }
    verify(res)
    console.log(res)
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
        <Sidebar active="clientes_añadir"></Sidebar>
        <div class="p-6 h-screen overflow-auto bg-gray-50">
            <div class="flex justify-between items-center">
                <h1 class="font-bold text-3xl">Clientes - Editar cliente</h1>
                <div class="flex gap-2 items-center">
                    <router-link to="/clients/" class="px-4 py-2 text-sm rounded-md bg-white border border-black/15 cursor-pointer hover:bg-gray-100">Cancelar</router-link>        
                    <button class="px-4 py-2 text-sm rounded-md bg-zinc-800 text-white cursor-pointer hover:bg-zinc-600" @click="sendClient">Actualizar datos</button>
                </div>
            </div>
            <div class="mt-5 bg-white p-5 rounded-md border border-black/15">
                <div class="grid grid-cols-2 gap-4 ">
                    <div class="flex flex-col gap-2">
                        <h2 class="font-medium text-xl">Nombre del cliente * </h2>
                        <input v-model="clientName" type="text" class="text-sm p-2 border border-black/15 rounded-md" placeholder="Ejemplo: John Doe">
                    </div>
                    <div class="flex flex-col gap-2">
                        <h2 class="font-medium text-xl">Notas del cliente</h2>
                        <input v-model="clientNotes" type="text" class="text-sm p-2 border border-black/15 rounded-md" placeholder="Ejemplo: Cliente nuevo">
                    </div>
                    <div class="flex flex-col gap-2">
                        <h2 class="font-medium text-xl">Email del cliente</h2>
                        <input v-model="clientEmail" type="text" class="text-sm p-2 border border-black/15 rounded-md" placeholder="Ejemplo: john@gmail.com">
                    </div>
                    <div class="flex flex-col gap-2">
                        <h2 class="font-medium text-xl">Teléfono del cliente</h2>
                        <input v-model="clientPhone" type="text" class="text-sm p-2 border border-black/15 rounded-md" placeholder="0000">
                    </div>
                    <div class="flex flex-col gap-2">
                        <h2 class="font-medium text-xl">ID de cliente</h2>
                        <input v-model="clientID" type="text" class="text-sm p-2 border border-black/15 rounded-md" placeholder="">
                    </div>
                    <div class="flex flex-col gap-2">
                        <h2 class="font-medium text-xl">Dirección del cliente</h2>
                        <input v-model="clientAdress" type="text" class="text-sm p-2 border border-black/15 rounded-md" placeholder="">
                    </div>
                    <div class="flex flex-col gap-2">
                        <h2 class="font-medium text-xl">Fecha de ingreso al sistema</h2>
                        <input v-model="today" readonly type="text" class="text-sm p-2 border border-black/15 rounded-md bg-gray-100 outline-0" placeholder="">
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped></style>
