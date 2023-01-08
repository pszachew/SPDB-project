<template>
    <div class="spinner-blackout">
    </div>
    <font-awesome-icon class="spinner blurred" icon="fa-solid fa-map-location" size="6x"/>
    <font-awesome-icon class="spinner" icon="fa-solid fa-map-location" size="6x"/>
</template>
<script>
import { library } from '@fortawesome/fontawesome-svg-core'
import { faMapLocation } from '@fortawesome/free-solid-svg-icons'
library.add(faMapLocation)
export default {
    name: "LoadingSpinner",
}
</script>
<style scoped>
    .spinner-blackout {
        opacity:    0.5; 
        background: #000; 
        width:      100%;
        height:     100%; 
        top:        0; 
        left:       0; 
        position:   fixed; 
        z-index:9990;
    }
    .spinner{
        position: fixed; 
        left: 50%; 
        top: 25%;
        z-index:9999;
        animation: spin 2s ease infinite;
    }
    .blurred{
        filter: blur(8px);
    }
    @keyframes spin {
        0% { 
            transform: translate(-50%, -25%) rotate(0deg) scale(0.95); 
            color: rgb(2, 117, 216); 
        }
        50% { 
            transform: translate(-50%, -25%) rotate(720deg) scale(1.2); 
            color: rgb(255, 255, 255); 
        }
        100% { 
            transform: translate(-50%, -25%) rotate(1440deg) scale(0.95); 
            color: rgb(2, 117, 216); 
        }
    }
</style>