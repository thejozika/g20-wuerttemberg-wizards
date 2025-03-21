<script setup>
import Map from '@/components/Map.vue'
import { ref } from 'vue'

const pos = ref(null)
// This will track the currently open accordion panel (either 'box1' or 'box2')
const activeAccordion = ref('box1')

function toggleAccordion(panel) {
  activeAccordion.value = activeAccordion.value === panel ? null : panel
}

// Transition hooks for smooth dynamic height transitions
function beforeEnter(el) {
  el.style.height = '0'
  el.style.opacity = 0
  el.style.transition = 'height 0.3s ease, opacity 0.3s ease'
}
function enter(el) {
  // Set to the scrollHeight to animate to the full height of the content
  el.style.height = el.scrollHeight + 'px'
  el.style.opacity = 1
}
function afterEnter(el) {
  // Reset height so that if content changes later, it won’t be restricted
  el.style.height = 'auto'
}
function beforeLeave(el) {
  // Set the current height before collapsing
  el.style.height = el.scrollHeight + 'px'
  el.style.opacity = 1
  el.style.transition = 'height 0.3s ease, opacity 0.3s ease'
}
function leave(el) {
  // Animate to zero height and opacity
  el.style.height = '0'
  el.style.opacity = 0
}
function afterLeave(el) {
  el.style.height = '0'
}
</script>
-
<template>
  <div
    class="bg-cover bg-bottom min-h-screen"
    style="background-image: url('/desert-8460850_1920.jpg')"
  >
    <div class="bg-black/60 min-h-screen">
      <div class="container mx-auto py-10">
        <div class="mb-10 text-white">
          <span class="font-bold text-gold-dark">Sahel Navigator</span>
          <h2 class="mt-1 text-2xl">
            <span class="relative w-64">
              <span class="flex items-center border border-gold-dark bg-black rounded-lg px-3 py-2">
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
                  <option selected>Assaba - Discover what lays hidden</option>
                  <option disabled>more storys will be added soon</option>
                </select>
              </span>
            </span>
          </h2>
        </div>

        <div class="grid grid-cols-5 gap-10 text-white">
          <div class="col-span-3">
            <div class="border border-gold-dark rounded-lg overflow-hidden">
              <Map @pos="(c) => (pos = c)" />
            </div>
          </div>

          <div class="col-span-2 flex flex-col gap-5 row-span-2">
            <!-- Accordion Box 1 -->
            <div
              id="box_1"
              @click="toggleAccordion('box1')"
              class="transition-all duration-300 bg-black border border-gold-dark rounded-lg p-5 hover:shadow-[inset_0px_0px_80px_-20px_rgba(255,209,0,0.5)]"
            >
              <h3 class="text-2xl mb-3">{{ pos?.title }}</h3>
              <p v-if="activeAccordion !== 'box1'" class="text-white/80">{{ pos?.short }}</p>
              <transition
                name="dynamic-height"
                @before-enter="beforeEnter"
                @enter="enter"
                @after-enter="afterEnter"
                @before-leave="beforeLeave"
                @leave="leave"
                @after-leave="afterLeave"
              >
                <p v-if="activeAccordion === 'box1'">
                  {{ pos?.content }}
                </p>
              </transition>
            </div>

            <!-- Accordion Box 2 -->
            <div
              id="box_2"
              @click="toggleAccordion('box2')"
              class="transition-all duration-300 bg-black border hover:shadow-[inset_0px_0px_80px_-20px_rgba(255,209,0,0.5)] border-gold-dark rounded-lg p-5"
            >
              <h3 class="text-2xl mb-3">Policies for {{ pos?.title }}</h3>
              <p v-if="activeAccordion !== 'box2'" class="text-white/80">learn more...</p>
              <transition
                name="dynamic-height"
                @before-enter="beforeEnter"
                @enter="enter"
                @after-enter="afterEnter"
                @before-leave="beforeLeave"
                @leave="leave"
                @after-leave="afterLeave"
              >
                <ul v-if="activeAccordion === 'box2'" class="flex flex-col gap-2">
                  <li v-for="p in pos?.policies" :key="p.title">
                    <strong>{{ p.title }}</strong
                    >: {{ p.content }}
                  </li>
                </ul>
              </transition>
            </div>

            <!-- Help Section (Static) -->
            <div
              class="transition-all duration-300 bg-black border hover:shadow-[inset_-32px_-32px_40px_-40px_rgba(255,209,0,0.5)] border-gold-dark rounded-lg p-5"
            >
              <h3 class="text-2xl mb-3">Help {{ pos?.title }}</h3>
              <p>There are 4 Projects operating in this region!</p>
              <div class="pt-4 flex flex-row gap-8">
                <button
                  class="px-4 py-2 bg-gold-dark text-black font-bold border-gold-dark border hover:bg-gold-shiny"
                >
                  Help them!
                </button>
                <button
                  class="px-4 py-2 bg-black text-gold-shiny font-bold border-gold-dark border hover:bg-gold-dark hover:text-black"
                >
                  Donate
                </button>
              </div>
            </div>
          </div>
          <div
            class="col-span-3 flex flex-col gap-2 transition-all duration-300 bg-black border border-gold-dark rounded-lg p-5 hover:shadow-[inset_0px_0px_80px_-20px_rgba(255,209,0,0.5)]"
          >
          <div class="flex flex-row justify-between">
              <span>Land Type</span><span class="text-white/70">Green grasslands / Off-white barren land</span>
            </div>
            <div class="bg-white h-[1px] w-full" />
            <div class="flex flex-row justify-between">
              <span>Biomass</span><span class="text-white/70">kg_C/m^2/year</span>
            </div>
            <div class="bg-white h-[1px] w-full" />
            <div class="flex flex-row justify-between">
              <span>Goat</span><span class="text-white/70">count/km^2</span>
            </div>
            <div class="bg-white h-[1px] w-full" />
            <div class="flex flex-row justify-between">
              <span>Cattle</span><span class="text-white/70">count/km^2</span>
            </div>
            <div class="bg-white h-[1px] w-full" />
            <div class="flex flex-row justify-between">
              <span>Sheeps</span><span class="text-white/70">count/km^2</span>
            </div>
            <div class="bg-white h-[1px] w-full" />
            <div class="flex flex-row justify-between">
              <span>Population</span><span class="text-white/70">count/km^2</span>
            </div>
            <div class="bg-white h-[1px] w-full" />
            <div class="flex flex-row justify-between">
              <span>Precipitation</span><span class="text-white/70">mm/year</span>
            </div>
            <div class="bg-white h-[1px] w-full" />
            <div class="flex flex-row justify-between">
              <span>vegetation change</span
              ><span class="text-white/70"
                >land_cover_degradion_count 2010-2023, red => decrease, green => increase
              </span>
            </div>
            <div class="bg-white h-[1px] w-full" />
            <div class="flex flex-row justify-between">
              <span class="w-110">animal GPP</span
              ><span class="text-white/70"
                >negative values of normalized differenz product of total_livestock_count x Biomass
                degredation (2010-2020) (convoluted for smoothing)</span
              >
            </div>
            <div class="bg-white h-[1px] w-full" />
            <div class="flex flex-row justify-between">
              <span class="w-110">animal desertification </span
              ><span class="text-white/70"
                >positive values of normalized pointwise difference product of total_livestock_count
                x terrain_degredation (2010-2020) (convoluted for somoothing)
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* You can remove or adjust these styles since the dynamic height is now handled via the transition hooks */
</style>
