<template>
  <div class="fav-detail">
    <div class="d-flex fav-heading">
      <font-awesome-layers class="fa-5x">
        <font-awesome-icon icon="square"
                          :style="{ color: '#42b983' }" />
        <font-awesome-layers-text transform="down-0.5 shrink-5"
                                  :value="favoriteThing.ranking"
                                  class="fav-ranking" />
      </font-awesome-layers>
      <div class="d-flex flex-column align-items-baseline align-self-center fav-title ml-3">
        <span class="text-uppercase">
          <span class="text-muted text-capitalize font-italic">title:</span>
            {{ favoriteThing.title }}
        </span>
        <span class="text-capitalize">
          <span class="text-muted font-italic">category:</span>
            {{ favoriteThing.category }}
          </span>
      </div>
    </div>
    <b-card title="Description:" class="text-left mt-4">
      <b-card-text>
        {{ favoriteThing.description }}
      </b-card-text>
    </b-card>
    <b-card-group class="text-left mt-4">
      <b-card title="Created:" class="text-left">
        <b-card-text>
          {{ dateFormat(favoriteThing.created_at) }}.
        </b-card-text>
      </b-card>
      <b-card title="Modified:" class="text-left">
        <b-card-text>
          {{ dateFormat(favoriteThing.modified_at) }}.
        </b-card-text>
      </b-card>
    </b-card-group>
    <b-card title="Metadata:" class="text-left mt-4">
      <b-card-text v-for="(value, name, index) in favoriteThing.metadata"
                   :key="index" class="d-flex align-items-center">
        <span class="meta-key">{{ name }}</span>
        <span class="meta-value">{{ value }}</span>
      </b-card-text>
    </b-card>
    <div class="action-btn mt-5">
      <b-button variant="success" class="mr-5" @click="editFavoriteThing">Update</b-button>
      <b-button variant="danger" @click="$bvToast.show('warning')">Delete</b-button>

      <b-toast id="warning" variant="danger" solid no-auto-hide>
        <div slot="toast-title" class="d-flex flex-grow-1 align-items-baseline">
          <strong class="mr-auto">Are you sure?</strong>
        </div>
        <b-button variant="danger" size="sm" @click="deleteFavoriteThing">OK</b-button>
      </b-toast>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { format } from 'date-fns';

export default {
  name: 'FavoriteThingDetails',
  data() {
    return {
      favoriteThing: {},
    };
  },
  methods: {
    dateFormat(date) {
      return format(new Date(date), 'ddd Do, MMM YYYY hh:mmA');
    },
    editFavoriteThing() {
      const favoriteThingId = this.favoriteThing.favorite_thing_id;
      this.$router.push({ name: 'favorite-thing-edit', params: { favoriteThingId } });
    },
    deleteFavoriteThing() {
      const favoriteThingId = this.favoriteThing.favorite_thing_id;
      axios.delete(`things\\${favoriteThingId}`)
        .then(() => {
          this.$router.push({ name: 'favorite-things' });
        })
        .catch((error) => {
          console.log(error.response.data);
        });
    },
  },
  mounted() {
    const url = `things\\${this.$route.params.id}`;
    axios.get(url)
      .then((response) => {
        this.favoriteThing = response.data;
      })
      .catch((error) => {
        console.log(error);
      });
  },
};
</script>

<style scoped>
  div.fav-detail {
    width: 70%;
    margin: 0 auto;
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
  }

  div .fav-ranking {
    color: #f0f8ff;
    font-weight: bolder;
  }

  div.fav-title {
    font-size: 1.2rem;
  }

.meta-value,
.meta-key {
  display: inline-block;
  padding: 2px 10px;
  color: #f0f8ff;
  font-size: 1.2rem;
  font-weight: 500;
}

.meta-key {
  background-color: #666c72;
  width: 200px;
}

.meta-value {
  background-color: #80868C;
  width: 450px;
}

</style>
