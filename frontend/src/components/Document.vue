<template>
    <div class="bg-white p-8 rounded shadow max-w-3xl mx-auto">
        <!-- Header -->
        <div class="flex justify-between mb-6 border-b pb-4">
            <div>
                <h1 class="text-2xl font-bold">{{ empresa.nombre }}</h1>
                <p class="text-sm">{{ empresa.direccion }}</p>
                <p class="text-sm">Tel: {{ empresa.telefono }}</p>
                <p class="text-sm">Identificación: {{ empresa.nit }}</p>
            </div>
            <div class="text-right">
                <h2 class="text-xl font-semibold">Factura Electrónica</h2>
                <p>Factura #: <span class="font-medium">{{ factura.numero }}</span></p>
                <p>Fecha emisión: {{ factura.fecha }}</p>
            </div>
        </div>

        <!-- Cliente -->
        <div class="mb-6">
            <h3 class="font-semibold">Datos del Cliente</h3>
            <p class="text-sm">{{ cliente.nombre }}</p>
            <p class="text-sm">{{ cliente.direccion }}</p>
            <p class="text-sm">ID: {{ cliente.nit }}</p>
        </div>

        <!-- Detalle -->
        <table class="w-full text-sm mb-6 border border-gray-300">
            <thead class="bg-gray-100">
                <tr>
                    <th class="p-2 border">Cant.</th>
                    <th class="p-2 border">Descripción</th>
                    <th class="p-2 border">CAByS</th>
                    <th class="p-2 border">Unit.</th>
                    <th class="p-2 border">Impuesto</th>
                    <th class="p-2 border">Total</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="(item, i) in factura.items" :key="i">
                    <td class="p-2 border text-center">{{ item.cantidad }}</td>
                    <td class="p-2 border">{{ item.descripcion }}</td>
                    <td class="p-2 border text-center">{{ item.codigoCABYS }}</td>
                    <td class="p-2 border text-right">{{ format(item.unitario) }}</td>
                    <td class="p-2 border text-right">{{ format(item.impuesto) }}</td>
                    <td class="p-2 border text-right">{{ format(item.total) }}</td>
                </tr>
            </tbody>
        </table>

        <!-- Totales -->
        <div class="flex justify-end mb-4">
            <div class="w-1/2">
                <div class="flex justify-between"><span>Subtotal</span><span>{{ format(subtotal) }}</span></div>
                <div class="flex justify-between"><span>Total Impuesto</span><span>{{ format(totalImpuesto) }}</span>
                </div>
                <div class="flex justify-between font-semibold text-lg"><span>Total ₡</span><span>{{ format(total)
                        }}</span></div>
            </div>
        </div>

        <p class="text-xs text-gray-500">Representación impresa de la factura electrónica validada por Hacienda.</p>
    </div>
</template>

<script setup>
import { computed } from 'vue'

// Datos de ejemplo (reemplaza por props o data)
const empresa = {
    nombre: 'Mi SaaS Facturación CR',
    direccion: 'Av. Central 1000, San José, CR',
    telefono: '+506 2222-2222',
    nit: '3-101-123456'
}

const cliente = {
    nombre: 'Cliente Ejemplar S.A.',
    direccion: 'Calle Secundaria 500',
    nit: '3-702-765432'
}

const factura = {
    numero: 'FE-2025-000456',
    fecha: '2025-06-10',
    items: [
        { cantidad: 1, descripcion: 'Servicio SaaS mensual', codigoCABYS: '432100', unitario: 50000, impuesto: 9200, total: 59200 },
        { cantidad: 2, descripcion: 'Soporte adicional', codigoCABYS: '432200', unitario: 15000, impuesto: 2760, total: 17760 }
    ]
}

const subtotal = computed(() => factura.items.reduce((s, x) => s + x.unitario * x.cantidad, 0))
const totalImpuesto = computed(() => factura.items.reduce((s, x) => s + x.impuesto, 0))
const total = computed(() => subtotal.value + totalImpuesto.value)

function format(value) {
    return new Intl.NumberFormat('es-CR', { style: 'currency', currency: 'CRC' }).format(value)
}
</script>

<style scoped>
table {
    border-collapse: collapse;
}
</style>
