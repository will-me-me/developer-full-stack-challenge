<template>
    <div>
        <b-navbar toggleable="lg" type="dark" variant="" fixed="top" class="mb-3" style="background-color: #3f51b5">
            <b-navbar-brand href="#" to="/">Manage Books</b-navbar-brand>

            <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

            <b-collapse id="nav-collapse" is-nav>
                <!-- Right aligned nav items -->
                <b-navbar-nav class="ml-auto">
                    <b-button to="books" pill variant="outline-primary" class="mb-2 mr-2" size="sm">
                        <b-icon icon="file-earmark" aria-hidden="true"></b-icon>
                        Books
                    </b-button>

                    <b-button to="/authors" pill variant="outline-primary" class="mb-2 mr-2" size="sm">
                        <b-icon icon=" person-fill "></b-icon>
                        Authors
                    </b-button>
                    <b-button
                        v-if="isAuthenticated"
                        pill
                        @click="logout"
                        variant="outline-primary"
                        class="mb-2 mr-2"
                        size="sm"
                    >
                        <b-icon icon="box-arrow-right"></b-icon>
                        Logout
                    </b-button>
                </b-navbar-nav>
            </b-collapse>
        </b-navbar>

        <nuxt />
    </div>
</template>

<script>
export default {
    data() {
        return {
            isLoggedIn: false,
        };
    },

    computed: {
        isAuthenticated() {
            const token = localStorage.getItem('token');
            return token !== null; // Returns true if token is present, false otherwise
        },
    },

    methods: {
        logout() {
            localStorage.removeItem('token');
            localStorage.removeItem('user');
            this.$router.push('/');
        },
    },

    mounted() {
        this.isAuthenticated;
    },
};
</script>

<style></style>
