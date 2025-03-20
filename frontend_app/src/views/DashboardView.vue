<script setup>
import Map from '@/components/Map.vue'
import { ref } from 'vue'

const pos = ref(null)
</script>

<template>
  <div class="container mx-auto py-10">
    <div class="mb-10">
      <span>Sahel Navigator</span>

      <h1 class="mt-1 text-3xl">
        <span class="relative w-64">
          <span class="flex items-center border bg-white rounded px-3 py-2">
            <svg
              class="w-5 h-5 text-gray-500 mr-2"
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M19 9l-7 7-7-7"
              ></path>
            </svg>

            <select class="w-full bg-transparent appearance-none focus:outline-none">
              <option selected>Assaba</option>
              <option disabled>more regions will be added soon</option>
            </select>
          </span>
        </span>
      </h1>
    </div>

    <div class="grid grid-cols-5 gap-10">
      <div class="col-span-3">
        <div class="border rounded">
          <Map @pos="(c) => (pos = c)" />
        </div>
      </div>

      <div class="col-span-2 flex flex-col gap-5">
        <div class="border rounded p-5">
          <h3 class="text-2xl mb-3">{{ pos?.title }}</h3>

          <p>
            {{ pos?.content }}
          </p>
        </div>

        <div class="border rounded p-5">
          <h3 class="text-2xl mb-3">Policies for {{ pos?.title }}</h3>

          <ul class="flex flex-col gap-2">
            <li v-for="p in pos?.policies" :key="p.title">
              <strong>{{ p.title }}</strong
              >: {{ p.content }}
            </li>
          </ul>
        </div>

        <div class="border rounded p-5">
          <h3 class="text-2xl mb-3">Help {{ pos?.title }}</h3>

          <p>Support helping organizations :-)</p>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped></style>
