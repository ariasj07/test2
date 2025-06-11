<template>
    <div class="grid grid-cols-[0.2fr_0.7fr_0.1fr] h-screen relative">
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
        <Sidebar active="facturacion_crear"></Sidebar>
        <div class="p-6 h-screen overflow-auto bg-gray-50">
            <div class="flex justify-between items-center">
                <h1 class="font-bold text-3xl">Movimientos - Registrar movimiento</h1>
                <div class="flex gap-2 items-center">
                    <router-link to="/clients/"
                        class="px-4 py-2 text-sm rounded-md bg-white border border-black/15 cursor-pointer hover:bg-gray-100">Cancelar</router-link>
                    <button v-if="!isSendedOk" class="px-4 py-2 text-sm rounded-md bg-zinc-800 text-white cursor-pointer hover:bg-zinc-600"
                        @click="sendBill">
                        Generar factura
                    </button>
                    <button v-else class="px-4 py-2 text-sm rounded-md bg-zinc-800/80 text-white cursor-pointer hover:bg-zinc-600">
                        Cargando...
                    </button>
                </div>
            </div>
            <div class="mt-5 bg-white p-5 rounded-md border border-black/15">
                <div class="grid grid-cols-2 gap-4 ">
                    <div class="flex flex-col gap-2">
                        <h2 class="font-medium text-xl">ID</h2>
                        <input readonly type="text" class="text-sm p-2 border border-black/15 rounded-md bg-gray-100 outline-0 pointer-events-none" placeholder="" :value="newBill" />
                    </div>
                    <div class="flex flex-col gap-2">
                        <h2 class="font-medium text-xl">Fecha del movimiento *</h2>
                        <input type="date" v-model="dateInput" class="text-sm p-2 border border-black/15 rounded-md" placeholder="" />
                    </div>
                    <div class="flex flex-col gap-2">
                        <h2 class="font-medium text-xl">Cliente a registrar *</h2>
                        <select v-model="selectedClient" name="" id="" class="text-sm p-2.5 border border-black/15 rounded-md">
                            <option v-for="(client, key) in clients.data" :key="key" :value="client.client_unique_id">{{ client.client_name }} - {{ client.client_email ? client.client_email : 'Ningún correo asociado' }}</option>
                        </select>
                    </div>
                    <div class="flex flex-col gap-2">
                        <h2 class="font-medium text-xl">Impuestos aplicados (%)</h2>
                        <input v-model="tax" type="text" class="text-sm p-2 border border-black/15 rounded-md"
                            placeholder="Ejemplo: 13" />
                    </div>
                    <div class="flex flex-col gap-2">
                        <h2 class="font-medium text-xl">Estado del movimiento:</h2>
                        <div class="flex items-center gap-2 py-1">
                            <div v-for="(item, key) in status" :key="key" @click="changeStatus(item.text)" :class="[
                                item.classes,
                                statusSelected === item.text ? item.specialClasses : item.normalClasses
                            ]">
                                {{ item.text }}
                            </div>
                        </div>
                        <p class="text-sm text-gray-600">Pendiente: Se registra el movimiento, pero no se descuenta nada del inventario, hasta que haya un cambio en el estado</p>
                        <p class="text-sm text-gray-600">Pagada: Se registra el movimiento, y se descuenta lo registrado del inventario</p>
                        <p class="text-sm text-gray-600">Anulada: Se registra el movimiento como nulo, y no se descuenta nada del inventario</p>
                    </div>
                </div>
            </div>
            <div class="mt-5 bg-white p-5 rounded-md border border-black/15">
                <div class="flex justify-between items-center">
                    <h2 class="font-medium text-xl">Productos adquiridos:</h2>
                    <button
                        class="px-4 py-2 text-sm bg-white border border-black/20 cursor-pointer hover:bg-gray-100 rounded-lg"
                        @click="addProduct">Agregar producto</button>
                </div>
                <div class="grid grid-cols-5 gap-y-2 gap-x-4 py-3">
                    <p class="text-sm text-gray-600">Producto</p>
                    <p class="text-sm text-gray-600">Cantidad</p>
                    <p class="text-sm text-gray-600">Descuento</p>
                    <p class="text-sm text-gray-600">Subtotal</p>
                    <p class="text-sm text-gray-600">Total</p>
                    <select v-model="selected" class="text-sm p-2 border border-black/15 rounded-md " name="" id="">
                        <option v-for="(item, key) in products" :key="key"
                            @click="selectedName(item.product_name, item.product_price, item.product_unique_id)"
                            :value="item.product_unique_id">{{ item.product_name }} - {{ item.product_price }}</option>
                    </select>
                    <input type="text" v-model="quantity" @input="validate"
                        class="text-sm p-2 border border-black/15 rounded-md" placeholder="Ejemplo: 1" />
                    <input type="text" v-model="discount" @input="validate"
                        class="text-sm p-2 border border-black/15 rounded-md" placeholder="Ejemplo: 50" />
                    <input readonly v-model="subtotal" type="text"
                        class="text-sm p-2 border border-black/15 rounded-md bg-gray-100 outline-0" placeholder="" />
                    <input readonly v-model="total" type="text"
                        class="text-sm p-2 border border-black/15 rounded-md bg-gray-100 outline-0" placeholder="" />
                </div>
            </div>
            <div class="mt-5 bg-white p-5 rounded-md border border-black/15">
                <div class="flex justify-between items-center">
                    <h2 class="font-medium text-xl">Resumen del movimiento</h2>
                </div>
                <div class="py-3">
                    <table class="w-full border-collapse">
                        <thead>
                            <tr>
                                <th class="text-sm text-start font-medium py-1">Nombre</th>
                                <th class="text-sm text-start font-medium py-1">Precio</th>
                                <th class="text-sm text-start font-medium py-1">Cantidad</th>
                                <th class="text-sm text-start font-medium py-1">Subtotal</th>
                                <th class="text-sm text-start font-medium py-1 w-fit">Descuento</th>
                                <th class="text-sm text-start font-medium py-1">Impuesto</th>
                                <th class="text-sm text-start font-medium py-1">Total</th>
                                <th class="text-sm text-start font-medium py-1"></th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="(item, key) in productsAdded">
                                <td class="text-sm text-start text-gray-600 py-3">{{ item.name }}</td>
                                <td class="text-sm text-start text-gray-600 py-3">{{ item.price }}</td>
                                <td class="text-sm text-start text-gray-600 py-3">{{ item.quantity }}</td>
                                <td class="text-sm text-start text-gray-600 py-3">{{ item.subtotal }}</td>
                                <td class="text-sm text-start text-gray-600 py-3 w-fit">{{ item.discount ? item.discount : 0  }}%</td>
                                <td class="text-sm text-start text-gray-600 py-3">{{ item.appliedTax ? item.appliedTax : 0  }}%</td>
                                <td class="text-sm text-start text-gray-600 py-3">{{ item.total }}</td>
                                <td class="hover:opacity-60 cursor-pointer" :id="item.id" @click="deleteRow(item.id)">
                                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"
                                        stroke-width="1.5" stroke="currentColor"
                                        class="w-7 h-7 text-red-600 p-1 bg-red-500/10 rounded-full">
                                        <path stroke-linecap="round" stroke-linejoin="round"
                                            d="m14.74 9-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 0 1-2.244 2.077H8.084a2.25 2.25 0 0 1-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 0 0-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 0 1 3.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 0 0-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 0 0-7.5 0" />
                                    </svg>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
                <div class="py-4 border-t border-black/20 mt-4">
                    <p class="font-medium">Subtotal: {{ subtotalResume }}</p>
                    <p class="font-medium">Total con impuestos: {{ totalResume }}</p>
                </div>
            </div>
        </div>
        <div class="p-6 h-screen overflow-auto bg-gray-50">
            <p class="text-sm text-gray-600 underline pt-4 cursor-pointer">Mira un tutorial sobre como crear tu primer movimiento</p>
            <p class="text-sm text-gray-600 underline pt-4 cursor-pointer">Añade tu primer cliente</p>
            <p class="text-sm text-gray-600 underline pt-4 cursor-pointer">¿Qué son los estados de los movimientos?</p>
            <p class="text-sm text-gray-600 underline pt-4 cursor-pointer">Mira las novedades de la última actualización</p>
        </div>
    </div>
</template>

<script setup>
import { onMounted, ref, computed, watch } from "vue";
import Sidebar from "../Sidebar.vue";
import { useAlert } from '../../composables/useAlert';
const { alert, alertIsTrue, message, verify } = useAlert() 

function generarCadenaAleatoria(longitud) {
    const caracteres = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    let resultado = '';

    for (let i = 0; i < longitud; i++) {
        const indiceAleatorio = Math.floor(Math.random() * caracteres.length);
        resultado += caracteres.charAt(indiceAleatorio);
    }

    return resultado;
}

const status = [
    {
        text: "Pendiente",
        classes: "text-sm cursor-pointer hover:opacity-70 px-4 py-1 rounded-lg text-center",
        normalClasses: 'bg-gray-500/15 text-black',
        specialClasses: 'bg-black text-white',
    },
    {
        text: "Pagada",
        classes: "text-sm cursor-pointer hover:opacity-70 px-4 py-1 rounded-lg text-center",
        normalClasses: 'bg-green-500/15 text-green-600',
        specialClasses: 'bg-green-500 text-white',
    },
    {
        text: "Anulada",
        classes: "text-sm cursor-pointer hover:opacity-70 px-4 py-1 rounded-lg text-center",
        normalClasses: 'bg-red-500/15 text-red-600',
        specialClasses: 'bg-red-600 text-white'
    },
];

const statusSelected = ref('')
const changeStatus = function (item) {
    statusSelected.value = item
}

const productsAdded = ref([

])




const products = ref([])
const clients = ref([])

onMounted(async function () {
    const data = await fetch("http://127.0.0.1:8000/get/inventory", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            id: "josueadmin" /* CHANGE IN PRODUCTION */
        })
    })
    const res = await data.json()
    console.log(res)
    products.value = res.data
    const clientsData = await fetch("http://127.0.0.1:8000/get/clients", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            user_id: "josueadmin" /* CHANGE IN PRODUCTION!!!! */
        })
    })
    clients.value = await clientsData.json()
    console.log(clients.value)

    newBill.value = generarDatos()

})

const selected = ref('')
const dateInput = ref(undefined)
const newBill = ref('')
const selectedClient = ref('')
const selectedByName = ref('')
const selectedByPrice = ref('')
const selectedById = ref('')


const generarDatos = function() {
    const añoActual = new Date().getFullYear();
    const caracteres = 'abcdefghijklmnopqrstuvwxyz123456789';
    let seleccion = '';
    for (let i = 0; i < 20; i++) {
    const indice = Math.floor(Math.random() * caracteres.length);
    seleccion += caracteres[indice];
    }

    return `${añoActual}_${seleccion}`;
}


const selectedName = function (name, price, id) {
    selectedByName.value = name
    selectedByPrice.value = price
    selectedById.value = id
}
const quantity = ref('')
const discount = ref('')
const subtotal = ref('')
const total = ref('')
const tax = ref('')


const validate = function (e) {
    quantity.value = quantity.value.replace(/[^0-9.]/g, "");
    discount.value = discount.value.replace(/[^0-9]/g, "");
}

watch([quantity, discount, selected], function ([newQuantity, newDiscount, newSelected], [oldQuantity, oldDiscount, oldSelected]) {
    if (selected.value.length >= 1) {
        const focused = products.value.filter(product => product.product_unique_id == selected.value)
        const price = parseInt(focused[0].product_price)
        console.log(price)
        subtotal.value = price * newQuantity
        total.value = subtotal.value - ((subtotal.value * newDiscount) / 100)
    }
})

const addProduct = function () {
    if(statusSelected.value.length >= 1){
    productsAdded.value.push(
        {
            id: selectedById.value,
            name: selectedByName.value,
            price: selectedByPrice.value,
            quantity: quantity.value,
            discount: discount.value,
            subtotal: subtotal.value,
            total: total.value + (total.value * (tax.value / 100)),
            appliedTax: tax.value,

        },
    )}else{
        verify({status: false, alert: "Selecciona el estado de la factura primero"})
    }
    console.log(productsAdded.value)
}

const deleteRow = function (itemId) {
    console.log(itemId)
    productsAdded.value = productsAdded.value.filter(obj => obj.id !== itemId)
}

const subtotalResume = computed(() => {
    return productsAdded.value.reduce((sum, product) => {
        return sum + product.subtotal; // Suma la propiedad "subtotal" de cada producto
    }, 0);
});

const totalResume = computed(() => {
    return productsAdded.value.reduce((sum, product) => {
        return sum + product.total; // Suma la propiedad "subtotal" de cada producto
    }, 0);
});

const isSendedOk = ref(false)

const sendBill = async function(){
    if(selectedClient.value.length >= 1 && dateInput.value  && productsAdded.value.length >= 1){
        isSendedOk.value = true
        const response = await fetch("http://127.0.0.1:8000/send/bill", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                user_id: "josueadmin" /* CHANGE IN PRODUCTION!!!!!!! */,
                products: productsAdded.value,
                client: selectedClient.value,
                bill_id: newBill.value,
                bill_date: dateInput.value,
                status: statusSelected.value
            })
        })
        const data = await response.json()
        console.log(data)
        isSendedOk.value = false
        productsAdded.value = []
        dateInput.value = undefined
        selectedClient.value = ''
        tax.value = ''
        newBill.value = generarDatos()
        verify(data)
    }else{
        verify({"status": false, "alert": "Hay campos vacíos"})
    }
    console.log(dateInput.value)
}

</script>
