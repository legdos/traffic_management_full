<template>
  <MapView />
</template>

<script setup>
import MapView from './components/MapView.vue'; 
</script>

<style>
html, body, #app {
  margin: 0 ;
  padding: 0 ;
  width: 100vw ;
  height: 100vh ;
  max-width: 100% ; 
  overflow: hidden ;
  box-sizing: border-box ;
}


#app > div {
  width: 100%;
  height: 100%;
}
</style>