<script setup>
import Map from '@/components/Map.vue'
</script>

<template>
  <main class="container mx-auto py-10">
    <div class="mb-10">
      <span>XXXXXX</span>
      <h1 class="text-3xl">REGION NAME</h1>
    </div>

    <div class="grid grid-cols-2 gap-10">
      <div class="border rounded">
        <Map />
      </div>

      <div class="border rounded p-5">Infos</div>
    </div>
  </main>
</template>

<style scoped></style>
