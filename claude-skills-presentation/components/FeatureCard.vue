<template>
  <div class="p-6 border border-gray-200 rounded-xl hover:shadow-xl transition-all duration-300 bg-white dark:bg-gray-800 dark:border-gray-700 h-full">
    <div class="text-xl font-bold mb-3 flex items-center gap-2" :class="colorClass">
      <slot name="icon"></slot>
      <slot name="title"></slot>
    </div>
    <div class="text-gray-600 dark:text-gray-300 leading-relaxed">
      <slot></slot>
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  colorClass?: string
}>()
</script>
