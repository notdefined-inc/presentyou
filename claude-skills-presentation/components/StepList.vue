<template>
  <div class="space-y-4">
    <div v-for="(step, idx) in steps" :key="idx" class="flex gap-4 items-start group">
      <div class="flex-none w-8 h-8 rounded-full bg-blue-100 dark:bg-blue-900/50 text-blue-600 dark:text-blue-400 flex items-center justify-center font-bold text-sm border-2 border-white dark:border-gray-900 shadow-sm ring-1 ring-blue-500/20 group-hover:scale-110 transition-transform">
        {{ idx + 1 }}
      </div>
      <div class="pt-1">
        <h3 class="font-bold text-lg mb-1">{{ step.title }}</h3>
        <p class="text-sm opacity-80 leading-relaxed">{{ step.desc }}</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  steps: { title: string, desc: string }[]
}>()
</script>
