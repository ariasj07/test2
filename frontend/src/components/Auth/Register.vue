<template>
    <div class="h-screen flex justify-center items-center relative">
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
        <div class="grid grid-cols-2 w-[98%] h-[98%]">
            <div class="p-10 py-14 relative">
                <div class="absolute top-0 right-0 bg-blue-600 w-full h-full -z-11 rounded-lg">

                </div>
                <h2 class="font-bold text-4xl pb-1 tracking-tight text-white">Empiece a administrar su negocio eficientemente con nosotros</h2>
                <p class="text-lg text-white/90 w-[80%] py-1">Empiece una prueba gratiuta de 7 días desde el momento en el que se registra. No tarjetas requeridas</p>
            </div>
            <div class="p-10">
                <h2 class="font-bold text-4xl text-center my-10">Crea tu cuenta</h2>
                <div class="grid grid-cols-2 gap-2 w-[90%] m-auto">
                    <div class="mb-3 flex flex-col gap-2">
                        <h2 class="font-semibold text-lg">Nombre *</h2>
                        <input v-model="name" type="text" name="" id="" class="p-2 text-sm border border-black/20 rounded-lg focus:outline-2 focus:outline-black/20">
                    </div>
                    <div class="mb-3 flex flex-col gap-2">
                        <h2 class="font-semibold text-lg">Apellidos *</h2>
                        <input v-model="lastName" type="text" name="" id="" class="p-2 text-sm border border-black/20 rounded-lg focus:outline-2 focus:outline-black/20">
                    </div>
                </div>
                <div class="mb-3 flex flex-col gap-2 w-[90%] m-auto">
                    <h2 class="font-semibold text-lg">Correo electrónico *</h2>
                    <input v-model="email" type="text" name="" id="" class="p-2 text-sm border border-black/20 rounded-lg focus:outline-2 focus:outline-black/20">
                </div>
                <div class="mb-3 flex flex-col gap-2 w-[90%] m-auto">
                    <h2 class="font-semibold text-lg">Crear contraseña *</h2>
                    <input v-model="password" @input="passwordInput" type="text" name="" id="" class="p-2 text-sm border border-black/20 rounded-lg focus:outline-2 focus:outline-black/20">
                </div>
                <div class="grid grid-cols-3 gap-x-3 gap-y-1 w-[90%] m-auto py-3">
                    <div class="h-1.5 rounded-full" :class="!touched ? 'bg-gray-200' : (min ? 'bg-green-500' : 'bg-red-500')"></div>
                    <div class="h-1.5 rounded-full" :class="!touched ? 'bg-gray-200' : (mid ? 'bg-green-500' : 'bg-red-500')"></div>
                    <div class="h-1.5 rounded-full" :class="!touched ? 'bg-gray-200' : (max ? 'bg-green-500' : 'bg-red-500')"></div>
                    <p class="text-gray-600 text-sm">Al menos 10 carácteres</p>
                    <p class="text-gray-600 text-sm">Al menos un número</p>
                    <p class="text-gray-600 text-sm">Al menos símbolo</p>
                </div>
                <div class=" w-[90%] m-auto flex flex-col gap-2 py-3">
                    <button @click="send" class="px-4 py-2 w-full text-white bg-blue-600 rounded-lg text-sm">Crear cuenta y empezar prueba</button>
                    <button class="w-full rounded-lg text-sm text-gray-600 underline cursor-pointer py-1">¿Ya tienes cuenta? Iniciar sesión</button>
                </div>


            </div>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue'
import { useAlert } from '../../composables/useAlert'
const { alert, alertIsTrue, message, verify }  = useAlert()

const name = ref('')
const lastName = ref('')
const email = ref('')
const password = ref('')

// Variables de validación
const min = ref(false) // longitud
const mid = ref(false) // número
const max = ref(false) // símbolo
const touched = ref(false) // si el usuario ha empezado a escribir

const passwordInput = () => {
    const val = password.value
    touched.value = val.length > 0

    min.value = val.length >= 10
    mid.value = /\d/.test(val)
    max.value = /[!@#$%^&*(),.?":{}|<>]/.test(val)
}

const send = async function(){
    console.log(0)
    if(min.value && mid.value && max.value && name.value.length >= 1 && email.value.length >= 1 && lastName.value.length >= 1){
        
    }else{
        verify({status: false, alert: "Hay campos por llenar"})
    }
}

</script>
