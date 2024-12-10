<template>

  <Header />

  <div class="event-card-menu">

    <div class="event-cards-container">
      <EventCard v-for="event in events" :key="event.id" :event="event" />
    </div>

  </div>

  <Footer />

</template>

<script>
import Header from '@/components/Header.vue'
import EventCard from '@/components/EventCard.vue'
import Footer from '@/components/Footer.vue'

export default {
  components: {
    Header,
    EventCard,
    Footer
  },
  data() {
    return {
      events: []
    }
  },
  mounted() {
    this.getEvents()
  },
  methods: {
    async getEvents() {
      try {
        const response = await fetch('http://localhost:8000/api/v1/events/')
        this.events = await response.json()
      } catch (error) {
        console.error('Error while retrieving event data:', error)
      }
    }
  }
}
</script>

<style scoped>
.event-card-menu {
  padding: 24px;
}

.event-cards-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  grid-gap: 24px;
}
</style>