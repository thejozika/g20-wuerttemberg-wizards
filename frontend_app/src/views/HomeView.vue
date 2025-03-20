<script setup></script>

<template>
  <div
    class="flex h-screen bg-cover bg-bottom relative"
    style="background-image: url('/desert-8460850_1920.jpg')"
  >
    <div class="mt-auto w-full py-10 px-20 mb-44 text-white bg-black/50 relative left-0 right-0">
      <h1 class="text-4xl text-gold-shiny">Sahel Navigator</h1>
      <h2 class="text-7xl">Welcome to the desert</h2>

      <RouterLink to="/dashboard">
        <button
          class="mt-5 px-8 py-3 bg-black text-gold-shiny font-bold border-gold-dark border hover:bg-gold-dark hover:text-black"
        >
          Access the Dashboard
        </button>
      </RouterLink>
    </div>
  </div>
</template>

<style scoped></style>
