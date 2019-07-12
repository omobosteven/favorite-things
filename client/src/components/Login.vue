<template>
  <div class="login-form">
    <b-form @submit="onSubmit">
      <h2 class="mb-4">Login</h2>
      <p class="error-msg" v-if="errors.message">
        {{ errors.message }}
      </p>
      <b-form-group
        id="email-group"
        label="Email address:"
        label-for="email-login"
      >
        <b-form-input
          id="email-login"
          v-model="form.email"
          type="text"
          name="email"
          placeholder="Enter email"
          v-validate="'required'"
          :class="{ 'is-invalid': vErrors.has('email') }"
        ></b-form-input>
        <b-form-invalid-feedback v-show="vErrors.has('email')">
          {{ vErrors.first('email') }}
        </b-form-invalid-feedback>
      </b-form-group>

      <b-form-group
        id="password-group"
        label="Your Password:"
        label-for="password-login">
        <b-form-input
          id="password-login"
          v-model="form.password"
          type="password"
          name="password"
          placeholder="Enter password"
          v-validate="'required'"
          :class="{ 'is-invalid': vErrors.has('password') }"
        ></b-form-input>
         <b-form-invalid-feedback v-show="vErrors.has('password')">
           {{ vErrors.first('password') }}
         </b-form-invalid-feedback>
      </b-form-group>

      <b-button type="submit" class="submit-btn">Login</b-button>
    </b-form>
  </div>
</template>

<script>
import axios from 'axios';
import Cookie from 'js-cookie';

export default {
  name: 'Login',
  data() {
    return {
      errors: {},
      form: {
        email: '',
        password: '',
      },
    };
  },
  methods: {
    loginUser() {
      axios.post('users/login', this.form)
        .then(() => {
          const token = Cookie.get('jwt_token');
          if (token) {
            this.$store.dispatch('authenticateUser');
            this.$router.push({ name: 'favorite-things' });
          } else {
            this.$router.push({ name: 'home' });
          }
        })
        .catch((error) => {
          this.errors = error.response.data;
        });
    },

    onSubmit(evt) {
      evt.preventDefault();
      this.$validator.validateAll().then((result) => {
        if (result) {
          this.loginUser();
        }
      });
    },
  },
};
</script>

<style scoped>
  .login-form {
    color: #f0f8ff;
    width: 50%;
    padding: .8rem 1rem;
  }

  .login-form {
    padding-right: 2rem;
  }

  .submit-btn {
    background-color: #f0f8ff;
    color: #42b983;
    border-color: #42b983;
    font-weight: 500;
  }

  .submit-btn:hover {
    background-color: #42b983;
    color: #f0f8ff;
    border-color: #f0f8ff;
  }
</style>
