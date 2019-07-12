<template>
  <div class="things">
    <div class="d-flex justify-content-between align-items-center">
      <div class="d-flex align-items-center">
        <span class="text-muted">Add favorite a thing</span>
        <span class="add-icon" @click="createFavoriteThing">+</span>
      </div>
      <b-form-select v-model="selected"
                     @change="itemsInCategory($event)"
                     class="mb-3">
        <option value="null" disabled>select category</option>
        <option value="all" class="text-capitalize">all</option>
        <option v-for="category in categories"
                :key="category.category_id"
                :value="category.category_id"
                class="text-capitalize">{{ category.name }}</option>
      </b-form-select>
    </div>
    <b-list-group>
      <b-list-group-item class="d-flex justify-content-between align-items-center mb-1 fav-heading">
        <span class="fav-title font-italic title-category">category</span>
        <span class="fav-title font-italic">title</span>
        <span class="fav-title font-italic">date created</span>
        <span class="fav-title font-italic title-ranking">ranking</span>
      </b-list-group-item>
      <b-list-group-item v-for="thing in favThings"
                         :key="thing.favorite_thing_id"
                         class="d-flex justify-content-between align-items-center mb-3 items"
                         @click="itemDetail($event, thing.favorite_thing_id)">
        <span class="fav-item text-capitalize fav-category">{{ thing.category }}</span>
        <span class="fav-item text-capitalize">{{ thing.title }}</span>
        <span class="fav-item">{{ dateFormat(thing.created_at) }}</span>
        <span class="fav-item fav-ranking">
          <font-awesome-layers full-width class="fa-2x">
            <font-awesome-icon icon="circle"/>
            <font-awesome-layers-text transform="down-1 shrink-7"
                                      :value="thing.ranking"
                                      class="ranking" />
          </font-awesome-layers>
        </span>
      </b-list-group-item>
    </b-list-group>
  </div>
</template>

<script>
import axios from 'axios';
import { format } from 'date-fns';

export default {
  name: 'FavoriteThings',
  data() {
    return {
      favThings: [],
      selected: null,
      categories: [],
    };
  },
  methods: {
    dateFormat(date) {
      return format(new Date(date), 'ddd Do, MMM YYYY hh:mmA');
    },
    itemDetail(event, id) {
      this.$router.push({ name: 'favorite-thing-detail', params: { id } });
    },
    itemsInCategory(event) {
      let url = `things/categories/${event}`;
      if (event === 'all') {
        url = 'things';
      }

      axios.get(url)
        .then((response) => {
          this.favThings = response.data;
        })
        .catch((error) => {
          console.log(error);
        });
    },
    createFavoriteThing() {
      this.$router.push({ name: 'favorite-thing-form' });
    },
  },
  mounted() {
    if (!this.$store.state.isAuthenticated) {
      this.$router.push({ name: 'home' });
      return;
    }

    const getUserCategories = () => axios.get('categories');
    const getUserFavoriteThings = () => axios.get('things');

    axios.all([getUserCategories(), getUserFavoriteThings()])
      .then(axios.spread((categories, things) => {
        this.categories = categories.data;
        this.favThings = things.data;
      }))
      .catch(error => error.response);
  },
};
</script>

<style scoped>
  .things {
    display: flex;
    flex-direction: column;
    width: 70%;
    margin: 0 auto;
  }

  div .fav-heading {
    background-color: #42b983;
    color: #f0f8ff;
    font-weight: 600;
  }

  div.items-title {
    padding: 0.75rem 1.25rem;
  }

  div.items:hover {
    background-color: #4e687a;
    color: #f0f8ff;
    cursor: pointer;
  }

  div .custom-select {
    width: 25%;
  }

  span.fav-item,
  span.fav-title {
    user-select: none;
    flex-basis: 30%;
  }

  span.fav-category,
  span.fav-ranking,
  span.title-category,
  span.title-ranking {
    flex-basis: 10%;
  }

  .ranking {
    color: #42b983;
  }

  .add-icon {
    cursor: pointer;
    line-height: 0.95;
    color: #42b983;
    display: inline-block;
    font-size: 2rem;
    border: 1px solid #42b983;
    border-radius: 100%;
    margin-left: 5px;
    height: 32px;
    width: 32px;
  }

  .add-icon:hover {
    color: #f0f8ff;
    background-color: #4e687a;
  }

</style>
