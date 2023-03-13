<template>
<section>
  <div class="container">
    <nav class="navbar navbar-expand-lg navbar-light bg-light" style="margin-bottom: 20px;">
      <router-link to="/" class="navbar-brand">
        <img src="../assets/logo.png" width="30" height="30" class="d-inline-block align-top" alt="">
          Lulabel
      </router-link>
      <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>

      <div class="collapse navbar-collapse" id="navbarSupportedContent">
        <ul class="navbar-nav mr-auto mt-2 mt-lg-0">
          <li class="nav-item active">
            <router-link v-bind:to="{ name: 'Home', params: { id: sharedState.user_id }}" class="nav-link" >Home</router-link>
          </li>
          <!-- <li class="nav-item">
            <router-link to="/createtask" class="nav-link">Post Image Task</router-link>
          </li> -->
          <li class="nav-item">
            <router-link to="/createvediotask" class="nav-link">PostTask</router-link>
          </li>
        </ul>

        <ul v-if="sharedState.is_authenticated" class="nav navbar-nav navbar-right">          
          <!-- <li class="nav-item active">
            <router-link v-bind:to="{ name: 'MyTask', params: { id: sharedState.user_id }}" class="nav-link" >MyTask</router-link>
          </li> -->
          <li class="nav-item">
            <router-link v-bind:to="{ name: 'Profile', params: { id: sharedState.user_id }}" class="nav-link">Profile</router-link>
          </li>
          <li class="nav-item">
            <a v-on:click="handlerLogout" class="nav-link" href="#">Logout</a>
          </li>
        </ul>
        <ul v-else class="nav navbar-nav navbar-right">          
          <li class="nav-item">
            <router-link to="/login" class="nav-link">Login</router-link>
          </li>
        </ul>
      </div>
    </nav>
  </div>
</section>
</template>

<script>
import store from '../store/index.js'
export default {
  name: 'Navbar',  //this is the name of the component
  data () {
    return {
      sharedState: store.state
    }
  },
  methods: {
    handlerLogout () {
      store.logoutAction()
      this.$toasted.show('You have been logged out.')
      this.$router.push('/login')
    }
  }
}
</script>