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

<style scoped>
  .home {
    width: 60%;
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
  }

</style>
