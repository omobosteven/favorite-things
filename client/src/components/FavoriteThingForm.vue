<template>
    <div class="favorite-thing-form">
      <b-form @submit="onSubmit" id="favorite-thing-form">
        <h2 class="mb-4">{{ updateFavoriteThing ? 'Update' : 'Create' }} Favorite thing</h2>
        <span v-for="(value, key, index) in errors"
              :key="index"
              class="error-msg">{{ value }}</span>
        <div class="form-row">
          <div class="col">
            <b-form-group
              id="item-title"
              label="Title:"
              label-for="title">
                <b-form-input
                  id="title"
                  v-model="form.title"
                  type="text"
                  name="title"
                  placeholder="Enter favorite thing title"
                  v-validate="'required'"
                  :class="{ 'is-invalid': vErrors.has('title') || errors[0] }"
                  ></b-form-input>
                <b-form-invalid-feedback v-show="vErrors.has('title')">
                  {{ vErrors.first('title') }}
                </b-form-invalid-feedback>
            </b-form-group>
          </div>

          <div class="col">
            <b-form-group
              id="item-category"
              label="Category:"
              label-for="category">
                <b-form-select v-model="form.category"
                               id="category"
                               name="category"
                               v-validate="'required'"
                               :class="{ 'is-invalid': vErrors.has('category') }">
                  <option value="null" disabled>select category</option>
                  <option v-for="category in categories"
                          :key="category.category_id"
                          :value="category.name"
                          class="text-capitalize">{{ category.name }}</option>
                </b-form-select>

                <b-form-invalid-feedback v-show="vErrors.has('category')">
                  {{ vErrors.first('category') }}
                </b-form-invalid-feedback>

                <b-input-group class="mt-1"
                               size="sm" v-show="createCategoryField">
                  <b-form-input placeholder="Enter category name"
                                v-model="category.name"></b-form-input>
                  <b-input-group-append class="d-flex align-items-center">
                    <b-button @click="createCategory" size="sm" variant="success">Save</b-button>
                    <span class="remove-icon-category ml-2 "
                          @click="createCategoryField = false">x</span>
                  </b-input-group-append>
                </b-input-group>
                <span class="create-category text-left"
                      @click="createCategoryField = true"
                      v-show="!createCategoryField">+ create category</span>
            </b-form-group>
          </div>
        </div>

        <b-form-group
          id="item-description"
          label="Description:"
          label-for="description">
          <b-form-textarea
            id="description"
            v-model="form.description"
            name="description"
            placeholder="Enter description..."
            rows="3"
            max-rows="6"
            v-validate="'min:10'"
            :class="{ 'is-invalid': vErrors.has('description') }"
          ></b-form-textarea>
          <b-form-invalid-feedback v-show="vErrors.has('description')">
            {{ vErrors.first('description') }}
          </b-form-invalid-feedback>
        </b-form-group>

        <b-form-group
            id="item-ranking"
            label="Ranking:"
            label-for="ranking">
              <b-form-input
                id="ranking"
                v-model="form.ranking"
                type="number"
                name="ranking"
                v-validate="'required|numeric|min_value:1'"
                :class="{ 'is-invalid': vErrors.has('ranking') }"
                ></b-form-input>
            <b-form-invalid-feedback v-show="vErrors.has('ranking')">
              {{ vErrors.first('ranking') }}
            </b-form-invalid-feedback>
          </b-form-group>

        <div class="mt-4" id="metadataField">
          <span>Metadata:</span>
          <div class="input-group mt-3 d-flex align-items-center">
            <div class="input-group-prepend">
              <span class="input-group-text">Metadata</span>
            </div>
            <b-form-input
              name="mkey"
              type="text"
              placeholder="key"
              maxlength="20"
              :class="{ 'is-invalid': errors.metadata }"
              ></b-form-input>
            <b-form-input
              name="mvalue"
              type="text"
              placeholder="value"
              maxlength="50"
              :class="{ 'is-invalid': errors.metadata }"
              ></b-form-input>
              <span class="add-icon" @click="addMetadataField">+</span>
          </div>
            <p class="metadata-error" v-if="errors.metadata">
              {{ errors.metadata[0] }}
            </p>
        </div>
        <div class="text-left mt-2">
          <p v-for="(value, key, index) in form.metadata"
             :key="index"
             class="d-flex align-items-center mb-1">
            <span class="meta-key">{{ key }}</span>
            <span class="meta-value">{{ value }}</span>
            <span class="remove-icon ml-2" @click="removeMetadataField(key)">x</span>
          </p>
        </div>

        <div v-show="!updateFavoriteThing" class="mt-4">
          <b-button type="submit" class="submit-btn">Save</b-button>
        </div>
        <div v-show="updateFavoriteThing" class="mt-4">
          <b-button type="submit" class="submit-btn mr-5">Update</b-button>
          <b-button @click="goBack" variant="danger">Cancel</b-button>
        </div>
      </b-form>
    </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'FavoriteThingForm',
  data() {
    return {
      errors: {},
      updateFavoriteThing: false,
      createCategoryField: false,
      categories: [],
      category: {
        name: '',
      },
      form: {
        title: '',
        category: null,
        description: null,
        ranking: 1,
        metadata: {},
      },
    };
  },
  methods: {
    createUpdateFavoriteThing() {
      if (this.updateFavoriteThing) {
        const favoriteThingId = this.$route.params.id;
        axios.put(`things/${favoriteThingId}`, this.form)
          .then(() => {
            this.$router.push({
              name: 'favorite-thing-detail',
              params: { id: favoriteThingId },
            });
          })
          .catch((error) => {
            this.errors = error.response.data;
          });
      } else {
        axios.post('things/', this.form)
          .then(() => {
            this.$router.push({ name: 'favorite-things' });
          })
          .catch((error) => {
            this.errors = error.response.data;
          });
      }
    },
    onSubmit(evt) {
      evt.preventDefault();
      this.$validator.validateAll().then((result) => {
        if (result) {
          this.createUpdateFavoriteThing();
        }
      });
    },
    addMetadataField() {
      const field = document.getElementById('favorite-thing-form');
      const { mkey, mvalue } = field;
      const mkeyValue = mkey.value.trim();
      const mvalueValue = mvalue.value.trim();

      if (mkeyValue === '' || mvalueValue === '') {
        this.errors = {
          ...this.errors,
          metadata: ['This field(key/value) may not be blank'],
        };
        return;
      }

      this.form.metadata = {
        ...this.form.metadata,
        [mkeyValue]: mvalueValue,
      };
      mkey.value = '';
      mvalue.value = '';
    },
    removeMetadataField(key) {
      delete this.form.metadata[key];
      this.form.metadata = {
        ...this.form.metadata,
      };
    },
    createCategory() {
      axios.post('categories/', this.category)
        .then((response) => {
          this.categories.push(response.data);
          this.category.name = '';
          this.createCategoryField = false;
        })
        .catch((error) => {
          this.errors = error.response.data;
        });
    },
    goBack() {
      const goBack = window.history.length > 1
        ? this.$router.go(-1)
        : this.$router.push('/');
      goBack();
    },
  },
  watch: {
    'form.title': function () {
      if (this.errors[0]) {
        delete this.errors[0];
      }
    },

    'category.name': function () {
      if (this.errors.message) {
        delete this.errors.message;
      }
    },

    'form.metadata': function () {
      if (this.errors.metadata) {
        delete this.errors.metadata;
      }
    },
  },
  mounted() {
    const favoriteThingId = this.$route.params.id;
    axios.get('categories')
      .then((response) => {
        this.categories = response.data;
      })
      .catch((error) => {
        console.log(error);
      });

    if (favoriteThingId) {
      const url = `things\\${this.$route.params.id}`;
      axios.get(url)
        .then((response) => {
          const favoriteThing = response.data;

          this.form.title = favoriteThing.title;
          this.form.category = favoriteThing.category;
          this.form.description = favoriteThing.description;
          this.form.ranking = favoriteThing.ranking;
          this.form.metadata = favoriteThing.metadata;

          this.updateFavoriteThing = true;
        })
        .catch((error) => {
          console.log(error);
        });
    }
  },
};
</script>

<style scoped>
  div.favorite-thing-form {
    width: 70%;
    margin: 0 auto;
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
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

.remove-icon,
.remove-icon-category {
  display: inline-block;
  cursor: pointer;
  color: #f53031;
  border: 1px solid #f53031;
  border-radius: 100%;
  height: 25px;
  width: 25px;
  font-size: 1.6rem;
  line-height: 0.74;
  padding-left: 5.2px;
}

.remove-icon-category {
  line-height: 0.9;
  padding-left: 0;
  font-size: 1.2rem;
  height: 20px;
  width: 20px;
}

.remove-icon:hover,
.remove-icon-category:hover{
  color: #f0f8ff;
  background-color: #f53031;
}

.input-group-text {
  background-color: #80868C;
  color: #f0f8ff;
  font-weight: 600;
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

.create-category {
  color: #42b983;
  cursor: pointer;
}

.create-category:hover {
  color: #3b7a4b;
}

.submit-btn {
  background-color: #42b983;
  color: #f0f8ff;
  border-color: #f0f8ff;
  font-weight: 500;
}

.submit-btn:hover {
  background-color: #f2f2f2;
  color: #42b983;
  border-color: #42b983;
}

.metadata-error {
  color: #dc3545;
  font-size: 80%;
  margin-top: 0.25rem;
}

.error-msg {
  color: #dc3545;
}
</style>
