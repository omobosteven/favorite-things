<template>
  <div class="logs">
    <b-list-group>
      <b-list-group-item class="d-flex justify-content-between align-items-center mb-1 log-heading">
        <span class="log-title font-italic">date</span>
        <span class="log-title font-italic title-category">logs</span>
      </b-list-group-item>
      <b-list-group-item v-for="log in logs"
                         :key="log.audit_log_id"
                         class="d-flex justify-content-between align-items-center mb-2 logs w-100">
        <span class="log">{{ dateFormat(log.created_at) }}</span>
        <span class="log text-capitalize">{{ log.log }}</span>
      </b-list-group-item>
    </b-list-group>
  </div>
</template>


<script>
import axios from 'axios';
import { format } from 'date-fns';

export default {
  name: 'Log',
  data() {
    return {
      logs: [],
    };
  },
  methods: {
    dateFormat(date) {
      return format(new Date(date), 'ddd Do, MMM YYYY hh:mmA');
    },
  },
  mounted() {
    if (!this.$store.state.isAuthenticated) {
      this.$router.push({ name: 'home' });
      return;
    }

    axios.get('logs')
      .then((response) => {
        this.logs = response.data;
      })
      .catch(error => error.response);
  },
};
</script>

<style scoped>
.logs {
  width: 70%;
  margin: 0 auto;
}

div .log-heading {
  background-color: #e84118;
  color: #f0f8ff;
  font-weight: 600;
}

span.log,
span.log-title {
  user-select: none;
}
</style>
