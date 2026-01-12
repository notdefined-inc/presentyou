<template>
  <div class="text-center p-6 rounded-lg bg-gray-50 dark:bg-white/5 border border-gray-100 dark:border-gray-800">
    <div class="text-5xl font-black mb-2 bg-clip-text text-transparent bg-gradient-to-r from-teal-500 to-blue-600">
      {{ value }}
    </div>
    <div class="text-sm font-bold uppercase tracking-widest opacity-60">{{ label }}</div>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  value: string | number
  label: string
}>()
</script>
