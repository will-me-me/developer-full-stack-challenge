<template>
    <div class="" style="display: flex; justify-content: center; align-items: center; height: 100vh">
        <UserLogin />
    </div>
</template>
<script>
import UserLogin from '~/components/UserLogin.vue';
export default {
    layout: ' default  ',

    components: {
        UserLogin,
    },
    data() {
        return {
            //
        };
    },
};
</script>
