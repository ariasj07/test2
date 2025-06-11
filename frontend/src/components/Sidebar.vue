<script setup>
import { ref } from 'vue';

const props = defineProps({
    active: ref('')
})

// Opciones de menú
const menu = [
    {
        titulo: "Inventario",
        icono: "home",
        sub: [
            { label: "Vista general", key: "productos_vista_general", to:"/"},
            { label: "Crear productos", key: "productos_crear", to:"/inventory/create" },
            { label: "Estadisticas", key: "productos_estadisticas", to: "/stats/"}
        ]
    },
    {
        titulo: "Clientes",
        icono: "users",
        sub: [
            { label: "Vista general", key: "clientes_vista_general", to:"/clients/" },
            { label: "Añadir cliente", key: "clientes_añadir", to:"/clients/create" },
            { label: "Estadísticas", key: "clientes_estadisticas" }
        ]
    },
    {
        titulo: "Movimientos",
        icono: "document",
        sub: [
            { label: "Vista general", key: "facturacion_vista_general", to:"/billing" },
            { label: "Registrar movimiento", key: "facturacion_crear", to: "/billing/create/" }
        ]
    }
]
</script>

<template>
    <div class="w-full p-4 h-screen">
        <div class="flex flex-col pt-2 pb-4">
            <h2 class="font-medium text-xl">Josué Arias</h2>
            <p class="text-gray-600 text-sm">josue@gmail.com</p>
        </div>

        <ul class="flex flex-col gap-2">
            <template v-for="(seccion, i) in menu" :key="i">
                <li class="text-base hover:bg-gray-200 font-medium p-2 rounded-md flex gap-2 items-center">

                    <svg v-if="seccion.icono === 'home'" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M6.429 9.75 2.25 12l4.179 2.25m0-4.5 5.571 3 5.571-3m-11.142 0L2.25 7.5 12 2.25l9.75 5.25-4.179 2.25m0 0L21.75 12l-4.179 2.25m0 0 4.179 2.25L12 21.75 2.25 16.5l4.179-2.25m11.142 0-5.571 3-5.571-3" />
                    </svg>
                    <svg v-else-if="seccion.icono === 'users'" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M15 19.128a9.38 9.38 0 0 0 2.625.372 9.337 9.337 0 0 0 4.121-.952 4.125 4.125 0 0 0-7.533-2.493M15 19.128v-.003c0-1.113-.285-2.16-.786-3.07M15 19.128v.106A12.318 12.318 0 0 1 8.624 21c-2.331 0-4.512-.645-6.374-1.766l-.001-.109a6.375 6.375 0 0 1 11.964-3.07M12 6.375a3.375 3.375 0 1 1-6.75 0 3.375 3.375 0 0 1 6.75 0Zm8.25 2.25a2.625 2.625 0 1 1-5.25 0 2.625 2.625 0 0 1 5.25 0Z" />
                    </svg>
                    <svg v-else xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M19.5 14.25v-2.625a3.375 3.375 0 0 0-3.375-3.375h-1.5A1.125 1.125 0 0 1 13.5 7.125v-1.5a3.375 3.375 0 0 0-3.375-3.375H8.25m2.25 0H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 0 0-9-9Z" />
                    </svg>

                    {{ seccion.titulo }}
                </li>
                <div class="w-full pl-2 border-l border-black/20">
                    <router-link v-for="(item, j) in seccion.sub" :to="item.to" :key="j"
                        class="text-sm p-2 rounded-md my-1 block"
                        :class="active === item.key ? 'bg-black text-white' : 'hover:bg-gray-200'">
                        {{ item.label }}
                    </router-link>
                </div>
            </template>
        </ul>
    </div>
</template>
