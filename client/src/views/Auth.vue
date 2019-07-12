<template>
  <div class="form">
    <div class="form-container">
      <div class="form-text">
        <div class="form-border">
          <p>{{ show ? signupMessage : loginMessage }}</p>
          <b-button class="form-sec-btn" @click="toggleForm">
            {{ show ? 'Register' : 'Login' }}
          </b-button>
        </div>
      </div>
      <Login v-show="show"></Login>
      <Signup v-show="!show"></Signup>
    </div>
  </div>
</template>

<script>
import Login from '@/components/Login.vue';
import Signup from '@/components/Signup.vue';

export default {
  name: 'Auth',
  data() {
    return {
      show: true,
      loginMessage: 'Already have an account?',
      signupMessage: 'Don\'t have an account?',
    };
  },
  methods: {
    toggleForm() {
      this.show = !this.show;
    },
  },
  components: {
    Login,
    Signup,
  },
};
</script>

<style scoped>
  .form {
    background-color: #42b983;
    width: 60%;
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    display: flex;
    align-items: center;
    padding: 20px 0;
  }

  .form-container {
    display: flex;
    justify-content: space-between;
    align-items: center;
    width: 100%;
  }

  .form-text {
    font-size: 1.3rem;
    padding-right: 5rem;
    padding-left: 5rem;
    color: #f0f8ff;
    width: 50%;
  }

  .form-border {
    border: medium ridge aliceblue;
    border-radius: 10px;
    padding-top: 2rem;
    padding-bottom: 2rem;
  }

  .form-sec-btn {
    background-color: #f0f8ff;
    color: #42b983;
    border-color: #42b983;
  }

</style>
