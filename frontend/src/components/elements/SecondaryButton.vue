<script setup>
import { defineProps } from 'vue';
const props = defineProps({
    text: String
})
</script>

<template>
    <button class="px-4 py-2 text-sm rounded-md bg-white border border-black/30 cursor-pointer hover:bg-gray-100">{{ text }}</button>
</template>