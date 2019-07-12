<template>
  <div class="signup-form">
    <b-form @submit="onSubmit">
      <h2 class="mb-4">Register</h2>
      <b-form-group
        id="email-group"
        label="Email address:"
        label-for="email">
        <b-form-input
          id="email"
          v-model="form.email"
          type="email"
          name="email"
          placeholder="Enter email"
          v-validate="'required|email'"
          :class="{ 'is-invalid': vErrors.has('email') }"
        ></b-form-input>
        <b-form-invalid-feedback v-show="vErrors.has('email')">
          {{ vErrors.first('email') }}
        </b-form-invalid-feedback>
      </b-form-group>

      <b-form-group
        id="password-group"
        label="Your Password:"
        label-for="password">
        <b-form-input
          id="password"
          v-model="form.password"
          type="password"
          name="password"
          placeholder="Enter password"
          v-validate="'required|min:6'"
          :class="{ 'is-invalid': vErrors.has('password') }"
        ></b-form-input>
        <b-form-invalid-feedback v-show="vErrors.has('password')">
          {{ vErrors.first('password') }}
        </b-form-invalid-feedback>
      </b-form-group>

      <b-form-group
        id="firstname-group"
        label="Firstname:"
        label-for="firstname">
        <b-form-input
          id="firstname"
          v-model="form.firstname"
          type="text"
          name="firstname"
          placeholder="Enter firstname"
          v-validate="'required|alpha'"
          :class="{ 'is-invalid': vErrors.has('firstname') }"
        ></b-form-input>
        <b-form-invalid-feedback v-show="vErrors.has('firstname')">
          {{ vErrors.first('firstname') }}
        </b-form-invalid-feedback>
      </b-form-group>

      <b-form-group
        id="lastname-group"
        label="Lastname:"
        label-for="lastname"
      >
        <b-form-input
          id="lastname"
          v-model="form.lastname"
          type="text"
          name="lastname"
          placeholder="Enter lastname"
          v-validate="'required|alpha'"
          :class="{ 'is-invalid': vErrors.has('lastname') }"
        ></b-form-input>
        <b-form-invalid-feedback v-show="vErrors.has('lastname')">
          {{ vErrors.first('lastname') }}
        </b-form-invalid-feedback>
      </b-form-group>

      <b-button type="submit" class="submit-btn">Register</b-button>
    </b-form>
  </div>
</template>

<script>
import axios from 'axios';
import Cookie from 'js-cookie';

export default {
  name: 'Signup',
  data() {
    return {
      errors: {},
      form: {
        email: '',
        password: '',
        firstname: '',
        lastname: '',
      },
    };
  },
  methods: {
    registerUser() {
      axios.post('users/register', this.form)
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
          this.registerUser();
        }
      });
    },
  },
  watch: {
    'form.email': function () {
      if (this.errors.email) {
        delete this.errors.email;
      }
    },
  },
};
</script>

<style scoped>
  .signup-form {
    color: #f0f8ff;
    width: 50%;
    padding: .8rem 1rem;
  }

  .signup-form {
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
