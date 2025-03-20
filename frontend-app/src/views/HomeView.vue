<script setup></script>

<template>
  <div
    class="flex h-screen bg-cover bg-bottom"
    style="background-image: url('/desert-8460850_1920.jpg')"
  >
    <div class="container mx-auto mt-auto mb-44 text-white">
      <h1 class="text-4xl">Sahel Navigator</h1>
      <h2 class="text-7xl">Welcome to the desert</h2>

      <RouterLink to="/dashboard">
        <button class="mt-5 px-8 py-3 bg-white text-black hover:bg-gray-200">
          Access the Dashboard
        </button>
      </RouterLink>
    </div>
  </div>

  <div class="container mx-auto py-10 flex flex-col gap-3">
    <h2 class="text-4xl">The desert is burning!</h2>

    <p>
      Lorem ipsum dolor sit amet, consectetur adipisicing elit. Alias aliquam atque delectus
      deleniti, dicta doloribus hic illo iure libero officiis, perspiciatis provident qui quidem
      quod sapiente ullam vero vitae voluptate?
    </p>

    <p>
      <RouterLink to="/dashboard">
        <button>Access the Dashboard</button>
      </RouterLink>
    </p>
  </div>
</template>

<style scoped></style>
