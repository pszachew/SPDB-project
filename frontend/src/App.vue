<template>
	<div class="p-4">
		<h1>Journey App</h1>
		<JourneyMain />
		<LoadingSpinner v-if="this.$store.state.isLoading"></LoadingSpinner>
	</div>
</template>

<script>
import JourneyMain from './components/journey/JourneyMain.vue'
import LoadingSpinner from './components/LoadingSpinner.vue'

export default {
	name: 'App',
	components: {
		JourneyMain,
		LoadingSpinner,
	}
}
</script>

<style>
</style>
