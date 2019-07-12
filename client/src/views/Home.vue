<template>
  <div class="home">
    <LandingPage msg="Welcome to Favorite Things App"/>
  </div>
</template>

<script>
// @ is an alias to /src
import LandingPage from '@/components/LandingPage.vue';

export default {
  name: 'home',
  components: {
    LandingPage,
  },
};
</script>
