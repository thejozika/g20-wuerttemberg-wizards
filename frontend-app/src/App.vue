<script setup></script>

<template>
  <div class="flex flex-col min-h-screen">
    <main>
      <RouterView />
    </main>

    <footer class="mt-auto bg-black text-white text-sm">
      <div class="container mx-auto py-5 flex flex-row justify-between items-center">
        <div>
          <p>
            This website was created during
            <a href="https://www.startglobal.org/start-hack/home/" target="_blank"
              >START Hack 2025</a
            >.
          </p>
          <p>&copy; 2025</p>
        </div>

        <p class="flex flex-wrap gap-2">
          <img src="./assets/github.svg" alt="GitHub" class="w-5 invert" />
          <a href="https://github.com/thejozika/g20-wuerttemberg-wizards" target="_blank"
            >Source Code on GitHub</a
          >
        </p>
      </div>
    </footer>
  </div>
</template>

<style scoped></style>
