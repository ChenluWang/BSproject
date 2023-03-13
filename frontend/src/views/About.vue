<template>
  <div class="about">
    <h1>This is an about page</h1>
    <EventCard/>
  </div>
</template>

<script>
import EventCard from '@/components/EventCard.vue'

export default {
  components: {
    EventCard
  }
}
</script>
