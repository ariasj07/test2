import { createRouter, createWebHistory } from "vue-router";
import Home from "./components/Home.vue";
import Crud from "./components/inventory/Crud.vue";
import Edit from "./components/inventory/Edit.vue";
import Stats from "./components/inventory/Stats.vue";
import Clients from "./components/Clients/Clients.vue";
import ClientCrud from "./components/Clients/Crud.vue";
import ClientEdit from "./components/Clients/Edit.vue";
import Register from "./components/Auth/Register.vue";
import Billing from "./components/Billing/Billing.vue";
import CrudBilling from "./components/Billing/CrudBilling.vue";
import Document from "./components/Document.vue";

const routes = [
    {path: "/" ,component: Home},
    {path: "/inventory/create", component: Crud},
    {path: "/edit/:id", name: 'editProduct', component: Edit},
    {path: "/stats/", name: 'inventoryStats', component: Stats},
    {path: "/clients/", name: 'clients', component: Clients},
    {path: "/clients/create", name: 'clientsCreate', component: ClientCrud},
    {path: "/clients/edit/:id", name: 'clientsEdit', component: ClientEdit},
    {path: "/register", name: 'register', component: Register},
    {path: "/billing", name: 'billing', component: Billing},
    {path: "/billing/create", name: 'billingCreate', component: CrudBilling},
    {path: "/bill/:id", name: 'generatedBill', component: Document},
]

const router = createRouter({
    history: createWebHistory(),
    routes
});

export default router