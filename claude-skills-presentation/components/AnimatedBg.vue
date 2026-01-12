<template>
  <div class="fixed inset-0 -z-10 overflow-hidden pointer-events-none">
    <div class="absolute -top-[50%] -left-[50%] w-[200%] h-[200%] anime-bg opacity-60"></div>
  </div>
</template>

<style scoped>
.anime-bg {
  background: radial-gradient(circle at 50% 50%, rgba(244, 114, 182, 0.5), rgba(56, 189, 248, 0.5), rgba(251, 191, 36, 0.5));
  filter: blur(100px);
  animation: bg-spin 25s linear infinite;
  
  /* Ensure it prints! */
  -webkit-print-color-adjust: exact !important;
  print-color-adjust: exact !important;
}

@media print {
  .anime-bg {
    opacity: 0.6 !important; /* Force opacity on print */
  }
}

@keyframes bg-spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
</style>
