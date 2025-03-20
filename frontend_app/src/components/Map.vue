<script setup>
import 'leaflet'
import 'leaflet/dist/leaflet.css'
import { onMounted } from 'vue'

let map = null

let currentPosition = 0

const positions = [
  {
    latLng: {
      lat: 16.619579678236377,
      lng: -11.406211853027344,
    },
    zoom: 13,
  },
  {
    latLng: {
      lat: 48,
      lng: 9,
    },
    zoom: 10,
  },
]

const getCutoutUrl = (map) => {
  let base = '/backend'

  if (import.meta.env.DEV) {
    base = 'http://localhost:8080/backend'
  }

  const lon1 = map.getBounds().getNorthWest().lng
  const lat1 = map.getBounds().getNorthWest().lat
  const lon2 = map.getBounds().getSouthEast().lng
  const lat2 = map.getBounds().getSouthEast().lat

  return `${base}/cutout?lon1=${lon1}&lat1=${lat1}&lon2=${lon2}&lat2=${lat2}`
}

onMounted(() => {
  map = L.map('map', {
    //dragging: false,
  }).setView(positions[0].latLng, positions[0].zoom)

  L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>',
  }).addTo(map)

  const Assaba_Districts_layer = L.geoJson(null, {
    style: { color: 'gray', weight: 2 },
  })

  const Assaba_Region_layer = L.geoJson(null, {
    style: { color: 'darkgray', weight: 2 },
  })

  const Main_Road = L.geoJson(null, {
    style: { color: 'black', weight: 2 },
  })

  const Streamwater = L.geoJson(null, {
    style: { color: 'blue', weight: 1 },
  })

  const Cutout = L.imageOverlay(getCutoutUrl(map), map.getBounds(), {
    opacity: 0.5,
  })

  fetch('/Assaba_Districts_layer.geojson')
    .then((response) => response.json())
    .then((data) => {
      Assaba_Districts_layer.addData(data)
    })

  fetch('/Assaba_Region_layer.geojson')
    .then((response) => response.json())
    .then((data) => {
      Assaba_Region_layer.addData(data)
    })

  fetch('/Main_Road.geojson')
    .then((response) => response.json())
    .then((data) => {
      Main_Road.addData(data)
    })

  fetch('/Streamwater.geojson')
    .then((response) => response.json())
    .then((data) => {
      Streamwater.addData(data)
    })

  const overlayMaps = {
    'Land Type': Cutout,
    'Assaba Districts': Assaba_Districts_layer,
    'Assaba Region': Assaba_Region_layer,
    'Main Road': Main_Road,
    Streamwater: Streamwater,
  }

  L.control.layers(null, overlayMaps, { collapsed: false }).addTo(map)

  map.on('moveend', (e) => {
    console.log(map.getBounds(), map.getCenter(), map.getZoom())

    Cutout.setUrl(getCutoutUrl(map))
    Cutout.setBounds(map.getBounds())
  })
})

const nextPosition = (direction = 'next') => {
  if (direction === 'next') {
    if (currentPosition < positions.length - 1) {
      currentPosition++
    } else {
      currentPosition = 0
    }
  } else {
    if (currentPosition > 0) {
      currentPosition--
    } else {
      currentPosition = positions.length - 1
    }
  }

  map.flyTo(positions[currentPosition].latLng, positions[currentPosition].zoom, {
    duration: 0.75,
  })
}

const years = [2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023]
</script>

<template>
  <div>
    <div class="relative">
      <div class="absolute top-[50%] left-[50%] z-[1000]">
        <div class="h-[40px] w-[2px] bg-black absolute top-[-20px] left-[-1px]" />
        <div class="h-[2px] w-[40px] bg-black absolute top-[-1px] left-[-20px]" />
      </div>

      <div id="map" class="aspect-video rounded-t" />
    </div>
  </div>

  <div class="p-5">
    <div class="flex flex-row justify-between">
      <button @click="nextPosition('previous')">Previous</button>
      <button @click="nextPosition('next')">Next</button>
    </div>

    <div>
      <div class="relative mb-6">
        <label for="labels-range-input" class="sr-only">Labels range</label>
        <input
          id="labels-range-input"
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
