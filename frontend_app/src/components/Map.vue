<script setup>
import 'leaflet'
import 'leaflet/dist/leaflet.css'
import { computed, onMounted, ref, watch } from 'vue'

const emit = defineEmits(['pos'])

import pos from '../assets/content_texts.json'

let overlayMaps = {}

let map = null

let cutout = {
  land: null,
  gpp: null,
  population: null,
  precipitation: null,
  goat: null,
  cattle: null,
  sheep: null,
  analytics: null,

  Assaba_Districts_layer: null,
  Assaba_Region_layer: null,
  Main_Road: null,
  Streamwater: null,
}

const blockedCutouts = ['Assaba_Districts_layer', 'Assaba_Region_layer', 'Main_Road', 'Streamwater']

const currentPosition = ref(0)

const positionCount = computed(() => {
  return pos.length
})

const position = computed(() => {
  return pos[currentPosition.value]
})

const year = ref(2023)

const getCutoutUrl = (map, type) => {
  let base = '/backend'

  if (import.meta.env.DEV) {
    base = 'http://localhost:8080/backend'
  }

  const lon1 = map.getBounds().getNorthWest().lng
  const lat1 = map.getBounds().getNorthWest().lat
  const lon2 = map.getBounds().getSouthEast().lng
  const lat2 = map.getBounds().getSouthEast().lat

  return `${base}/cutout/${type}?lon1=${lon1}&lat1=${lat1}&lon2=${lon2}&lat2=${lat2}&year=${year.value}`
}

let zoom = null

onMounted(() => {
  const baseMaps = {
    OpenStreetMap: L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
      maxZoom: 19,
      attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>',
    }),
    Satellite: L.tileLayer(
      'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
      {
        maxZoom: 19,
        attribution: '&copy; <a href="https://www.esri.com/">Esri</a> contributors',
      },
    ),
    OpenTopoMap: L.tileLayer('https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png', {
      maxZoom: 19,
      attribution: '&copy; OpenTopoMap & OpenStreetMap contributors',
    }),
  }

  map = L.map('map', {
    //dragging: false,
    layers: [baseMaps.Satellite],
  }).setView(
    {
      lat: position.value.lat,
      lng: position.value.lng,
    },
    position.value.zoom,
  )

  map.setMaxBounds(L.latLngBounds(L.latLng(14, -15), L.latLng(19, -9)))
  map.setMaxZoom(15)
  map.setMinZoom(8)

  nextPosition('n', 0)

  L.control.layers(baseMaps).addTo(map)

  cutout.Assaba_Districts_layer = L.geoJson(null, {
    style: { color: 'gray', weight: 2 },
  })

  cutout.Assaba_Region_layer = L.geoJson(null, {
    style: { color: 'darkgray', weight: 2 },
  })

  cutout.Main_Road = L.geoJson(null, {
    style: { color: 'black', weight: 2 },
  })

  cutout.Streamwater = L.geoJson(null, {
    style: { color: 'blue', weight: 1 },
  })

  Object.keys(cutout).forEach((t) => {
    if (!blockedCutouts.includes(t)) {
      cutout[t] = L.imageOverlay(getCutoutUrl(map, t), map.getBounds(), {
        opacity: 0.5,
      })
    }
  })

  fetch('/Assaba_Districts_layer.geojson')
    .then((response) => response.json())
    .then((data) => {
      cutout.Assaba_Districts_layer.addData(data)
    })

  fetch('/Assaba_Region_layer.geojson')
    .then((response) => response.json())
    .then((data) => {
      cutout.Assaba_Region_layer.addData(data)
    })

  fetch('/Main_Road.geojson')
    .then((response) => response.json())
    .then((data) => {
      cutout.Main_Road.addData(data)
    })

  fetch('/Streamwater.geojson')
    .then((response) => response.json())
    .then((data) => {
      cutout.Streamwater.addData(data)
    })

  overlayMaps = {
    'Land Type': cutout.land,
    Biomass: cutout.gpp,
    Goat: cutout.goat,
    Cattle: cutout.cattle,
    Sheep: cutout.sheep,
    Population: cutout.population,
    Precipitation: cutout.precipitation,
    Analytics: cutout.analytics,
    'Assaba Districts': cutout.Assaba_Districts_layer,
    'Assaba Region': cutout.Assaba_Region_layer,
    'Main Road': cutout.Main_Road,
    Streamwater: cutout.Streamwater,
  }

  L.control.layers(null, overlayMaps, { collapsed: false }).addTo(map)

  map.on('moveend', (e) => {
    console.log(map.getBounds().getNorthEast(), map.getCenter(), map.getZoom())

    Object.keys(cutout).forEach((t) => {
      if (!blockedCutouts.includes(t)) {
        cutout[t].setUrl(getCutoutUrl(map, t))
        cutout[t].setBounds(map.getBounds())
      }
    })
  })
})

watch(year, () => {
  Object.keys(cutout).forEach((t) => {
    if (!blockedCutouts.includes(t)) {
      cutout[t].setUrl(getCutoutUrl(map, t))
      cutout[t].setBounds(map.getBounds())
    }
  })
})

const nextPosition = (direction = 'next', set = undefined) => {
  if (set !== undefined) {
    currentPosition.value = set
  } else {
    if (direction === 'next') {
      if (currentPosition.value < positionCount.value - 1) {
        currentPosition.value++
      } else {
        currentPosition.value = 0
      }
    } else {
      if (currentPosition.value > 0) {
        currentPosition.value--
      } else {
        currentPosition.value = positionCount.value - 1
      }
    }
  }

  emit('pos', position.value)

  Object.values(overlayMaps).forEach((layer) => {
    if (map.hasLayer(layer)) {
      map.removeLayer(layer)
    }
  })

  map.flyTo(
    {
      lat: position.value.lat,
      lng: position.value.lng,
    },
    position.value.zoom,
    {
      duration: 0.75,
    },
  )

  setTimeout(() => {
    position.value.layers.forEach((l) => {
      if (Object.keys(cutout).filter((e) => e === l).length === 1) {
        map.addLayer(cutout[l])
      }
    })
  }, 750)
}

const play = async () => {
  const currentYear = year.value

  for (let i = 0; i < years.length; i++) {
    year.value = years[i]
    await new Promise((p) => setTimeout(p, 2000))
  }

  year.value = currentYear
}

const years = [2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023]
</script>

<template>
  <div>
    <div class="relative">
      <div class="absolute top-[50%] left-[50%] z-[1000] opacity-25">
        <div class="h-[20px] w-[2px] bg-black absolute top-[-10px] left-[-1px]" />
        <div class="h-[2px] w-[20px] bg-black absolute top-[-1px] left-[-10px]" />
      </div>

      <div id="map" class="aspect-video rounded-t" />
    </div>
  </div>

  <div class="p-5">
    <div class="flex flex-row justify-between">
      <button @click="nextPosition('previous')">Previous</button>
      <button @click="play()">Play</button>
      <button @click="nextPosition('next')">Next</button>
    </div>

    <div>
      <div class="relative mb-6">
        <label for="labels-range-input" class="sr-only">Labels range</label>
        <input
          id="labels-range-input"
          v-model="year"
          type="range"
          value="2023"
          min="2010"
          max="2023"
          class="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer dark:bg-gray-700"
        />

        <div class="flex flex-row justify-between">
          <span
            class="text-sm text-gray-500 dark:text-gray-400"
            v-for="year in years"
            :key="year"
            >{{ year }}</span
          >
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped></style>
