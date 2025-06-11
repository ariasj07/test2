<script setup>
import { defineProps } from 'vue';
const props = defineProps({
    text: String
})
</script>

<template>
    <button class="px-4 py-2 text-sm rounded-md bg-blue-500 text-white cursor-pointer0 hover:bg-blue-600">{{ text }}</button>
</template>